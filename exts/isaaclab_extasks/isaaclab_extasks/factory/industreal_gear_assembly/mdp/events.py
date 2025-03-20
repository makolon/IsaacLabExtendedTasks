from __future__ import annotations

import torch
from typing import TYPE_CHECKING

import isaaclab.utils.math as math_utils
from isaaclab.assets import Articulation, RigidObject

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedEnv


def reset_root_state_uniform_non_overlapping(
    env: ManagerBasedEnv,
    env_ids: torch.Tensor,
    pose_range: dict[str, tuple[float, float]],
    velocity_range: dict[str, tuple[float, float]],
    target_asset: str,
    asset_names: list[str],
    offset: torch.Tensor = torch.tensor([0.1, 0.1, 0.0]),  # Exclusion zone offset
):
    """
    Reset asset root states with random positions and velocities while ensuring that 
    `asset_names` do not overlap with `target_asset`.

    The `target_asset` is placed first, and an exclusion zone is created around it based on `offset`. 
    Other assets are then sampled within `pose_range`, avoiding the exclusion zone.

    Parameters
    ----------
    env : ManagerBasedEnv
        The simulation environment.
    env_ids : torch.Tensor
        The environment indices to reset.
    pose_range : dict[str, tuple[float, float]]
        Position (`x, y, z`) and rotation (`roll, pitch, yaw`) sampling ranges.
    velocity_range : dict[str, tuple[float, float]]
        Velocity (`x, y, z, roll, pitch, yaw`) sampling ranges.
    target_asset : str
        The asset to be placed first.
    asset_names : list[str]
        List of asset names to reset.
    offset : torch.Tensor, optional
        Exclusion zone margin around `target_asset` where other objects cannot be placed.
    """

    # Sample a random position and orientation for `target_asset`
    target_obj: RigidObject | Articulation = env.scene[target_asset]
    target_root_states = target_obj.data.default_root_state[env_ids].clone()

    pose_values = [pose_range.get(key, (0.0, 0.0)) for key in ["x", "y", "z", "roll", "pitch", "yaw"]]
    pose_ranges = torch.tensor(pose_values, device=target_obj.device)
    rand_pose = math_utils.sample_uniform(pose_ranges[:, 0], pose_ranges[:, 1], (len(env_ids), 6), device=target_obj.device)

    target_positions = target_root_states[:, 0:3] + env.scene.env_origins[env_ids] + rand_pose[:, 0:3]
    target_orientations = math_utils.quat_mul(
        target_root_states[:, 3:7], math_utils.quat_from_euler_xyz(rand_pose[:, 3], rand_pose[:, 4], rand_pose[:, 5])
    )

    # Define the exclusion zone around `target_asset`
    offset = offset.to(env.device)
    min_forbidden = target_positions - offset
    max_forbidden = target_positions + offset

    # Apply the new state to the simulation
    target_obj.write_root_pose_to_sim(torch.cat([target_positions, target_orientations], dim=-1), env_ids=env_ids)

    # Sample positions for other assets while avoiding the exclusion zone
    for name in asset_names:
        if name == target_asset:
            continue

        asset: RigidObject | Articulation = env.scene[name]
        root_states = asset.data.default_root_state[env_ids].clone()

        valid_positions = torch.zeros((len(env_ids), 3), device=asset.device)
        num_valid_samples = 0

        while num_valid_samples < len(env_ids):
            range_list = [pose_range.get(key, (0.0, 0.0)) for key in ["x", "y", "z"]]
            ranges = torch.tensor(range_list, device=asset.device)
            rand_samples = math_utils.sample_uniform(ranges[:, 0], ranges[:, 1], (len(env_ids) - num_valid_samples, 3), device=asset.device)

            candidate_positions = root_states[num_valid_samples:, 0:3] + env.scene.env_origins[env_ids[num_valid_samples:]] + rand_samples

            # Ensure objects are placed outside the exclusion zone
            mask_valid = (
                (candidate_positions[:, 0] < min_forbidden[:, 0]) | (candidate_positions[:, 0] > max_forbidden[:, 0]) |
                (candidate_positions[:, 1] < min_forbidden[:, 1]) | (candidate_positions[:, 1] > max_forbidden[:, 1]) |
                (candidate_positions[:, 2] < min_forbidden[:, 2]) | (candidate_positions[:, 2] > max_forbidden[:, 2])
            )

            valid_samples = candidate_positions[mask_valid]
            valid_count = valid_samples.shape[0]

            valid_positions[num_valid_samples:num_valid_samples + valid_count] = valid_samples
            num_valid_samples += valid_count

        # Apply random orientations
        range_list = [pose_range.get(key, (0.0, 0.0)) for key in ["roll", "pitch", "yaw"]]
        ranges = torch.tensor(range_list, device=asset.device)
        rand_samples = math_utils.sample_uniform(ranges[:, 0], ranges[:, 1], (len(env_ids), 3), device=asset.device)
        orientations_delta = math_utils.quat_from_euler_xyz(rand_samples[:, 0], rand_samples[:, 1], rand_samples[:, 2])
        orientations = math_utils.quat_mul(root_states[:, 3:7], orientations_delta)

        # Sample velocities
        range_list = [velocity_range.get(key, (0.0, 0.0)) for key in ["x", "y", "z", "roll", "pitch", "yaw"]]
        ranges = torch.tensor(range_list, device=asset.device)
        rand_samples = math_utils.sample_uniform(ranges[:, 0], ranges[:, 1], (len(env_ids), 6), device=asset.device)
        velocities = root_states[:, 7:13] + rand_samples

        # Apply new states to the simulation
        asset.write_root_pose_to_sim(torch.cat([valid_positions, orientations], dim=-1), env_ids=env_ids)
        asset.write_root_velocity_to_sim(velocities, env_ids=env_ids)


def reset_target_position(
    env: ManagerBasedEnv,
    env_ids: torch.Tensor,
    target_asset: str,
    offset_dict: dict[str, float],  # Offset is a single float (yaw-based displacement)
):
    """
    Reset the root states of assets based on offsets along the yaw direction from a target asset's position.

    Parameters
    ----------
    env : ManagerBasedEnv
        The simulation environment.
    env_ids : torch.Tensor
        The environment indices to reset.
    target_asset : str
        The name of the target asset.
    offset_dict : dict[str, float]
        Dictionary mapping asset names to their offsets along the yaw direction.
    """

    # Get the target asset's current position and orientation
    target_obj: RigidObject = env.scene[target_asset]
    target_root_states = target_obj.data.root_state_w[env_ids].clone()

    target_position = target_root_states[:, 0:3]  # (batch_size, 3)
    target_rotation = target_root_states[:, 3:7]  # (batch_size, 4)
    _, _, target_yaw = math_utils.euler_xyz_from_quat(target_rotation)  # Extract yaw angle (batch_size,)

    # Convert yaw into rotation matrix (batch_size, 2, 2) for XY plane
    cos_yaw = torch.cos(target_yaw)
    sin_yaw = torch.sin(target_yaw)
    rotation_matrix = torch.stack([
        torch.stack([cos_yaw, -sin_yaw], dim=-1),
        torch.stack([sin_yaw, cos_yaw], dim=-1),
    ], dim=1)  # Shape: (batch_size, 2, 2)

    # Apply offsets to asset positions
    for name, offset in offset_dict.items():
        asset: RigidObject = env.scene[name]
        root_states = asset.data.default_root_state[env_ids].clone()

        # Convert offset to XY displacement (batch_size, 2)
        offset_xy = torch.stack([offset * torch.ones_like(target_yaw), torch.zeros_like(target_yaw)], dim=-1)

        # Rotate the offset in the XY plane
        rotated_offset_xy = torch.bmm(rotation_matrix, offset_xy.unsqueeze(-1)).squeeze(-1)  # (batch_size, 2)

        # Compute the new positions
        new_positions = target_position.clone()
        new_positions[:, :2] += rotated_offset_xy  # Apply XY displacement

        # Sample random orientations
        range_list = [(0., 0.), (0., 0.), (0., 0.)]
        ranges = torch.tensor(range_list, device=asset.device)
        rand_samples = math_utils.sample_uniform(ranges[:, 0], ranges[:, 1], (len(env_ids), 3), device=asset.device)
        orientations_delta = math_utils.quat_from_euler_xyz(rand_samples[:, 0], rand_samples[:, 1], rand_samples[:, 2])
        new_orientations = math_utils.quat_mul(root_states[:, 3:7], orientations_delta)

        # Apply new states to the simulation
        asset.write_root_pose_to_sim(torch.cat([new_positions, new_orientations], dim=-1), env_ids=env_ids)
