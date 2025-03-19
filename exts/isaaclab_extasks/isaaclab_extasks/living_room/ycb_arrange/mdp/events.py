from __future__ import annotations

import random
import torch
from typing import TYPE_CHECKING

import isaaclab.utils.math as math_utils
from isaaclab.assets import Articulation, RigidObject

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedEnv


def reset_root_state_uniform(
    env: ManagerBasedEnv,
    env_ids: torch.Tensor,
    pose_range: dict[str, tuple[float, float]],
    velocity_range: dict[str, tuple[float, float]],
    asset_names: list[str],
):
    """Reset the asset root state to a random position and velocity uniformly within the given ranges.

    This function randomizes the root position and velocity of the asset.

    * It samples the root position from the given ranges and adds them to the default root position, before setting
      them into the physics simulation.
    * It samples the root orientation from the given ranges and sets them into the physics simulation.
    * It samples the root velocity from the given ranges and sets them into the physics simulation.

    The function takes a dictionary of pose and velocity ranges for each axis and rotation. The keys of the
    dictionary are ``x``, ``y``, ``z``, ``roll``, ``pitch``, and ``yaw``. The values are tuples of the form
    ``(min, max)``. If the dictionary does not contain a key, the position or velocity is set to zero for that axis.
    """
    # extract the used quantities (to enable type-hinting)
    for name in asset_names:
        asset: RigidObject | Articulation = env.scene[name]
        # get default root state
        root_states = asset.data.default_root_state[env_ids].clone()

        # poses
        range_list = [pose_range.get(key, (0.0, 0.0)) for key in ["x", "y", "z", "roll", "pitch", "yaw"]]
        ranges = torch.tensor(range_list, device=asset.device)
        rand_samples = math_utils.sample_uniform(ranges[:, 0], ranges[:, 1], (len(env_ids), 6), device=asset.device)

        positions = root_states[:, 0:3] + env.scene.env_origins[env_ids] + rand_samples[:, 0:3]
        orientations_delta = math_utils.quat_from_euler_xyz(rand_samples[:, 3], rand_samples[:, 4], rand_samples[:, 5])
        orientations = math_utils.quat_mul(root_states[:, 3:7], orientations_delta)
        # velocities
        range_list = [velocity_range.get(key, (0.0, 0.0)) for key in ["x", "y", "z", "roll", "pitch", "yaw"]]
        ranges = torch.tensor(range_list, device=asset.device)
        rand_samples = math_utils.sample_uniform(ranges[:, 0], ranges[:, 1], (len(env_ids), 6), device=asset.device)

        velocities = root_states[:, 7:13] + rand_samples

        # set into the physics simulation
        asset.write_root_pose_to_sim(torch.cat([positions, orientations], dim=-1), env_ids=env_ids)
        asset.write_root_velocity_to_sim(velocities, env_ids=env_ids)


def reset_root_state_uniform_outside(
    env: ManagerBasedEnv,
    env_ids: torch.Tensor,
    pose_range: dict[str, tuple[float, float]],
    velocity_range: dict[str, tuple[float, float]],
    region_name: str,
    asset_names: list[str],
):
    """Reset the asset root state to a random position and velocity uniformly within the given ranges,
    ensuring the asset is placed **outside** the specified region.

    The sampling ensures that objects are placed in a region that is within `pose_range`
    but **outside** the forbidden `region_name`.

    Parameters
    ----------
    env : ManagerBasedEnv
        The simulation environment.
    env_ids : torch.Tensor
        The environment indices to reset.
    pose_range : dict[str, tuple[float, float]]
        Ranges for position (`x, y, z`) and rotation (`roll, pitch, yaw`).
    velocity_range : dict[str, tuple[float, float]]
        Ranges for velocity (`x, y, z, roll, pitch, yaw`).
    region_name : str
        The name of the region that assets must be placed **outside**.
    asset_names : list[str]
        The names of the assets to reset.
    """

    # Get the bounding box of the forbidden region
    region = env.scene[region_name]
    pos = torch.tensor(region.cfg.init_state.pos, device=env.device)
    size = torch.tensor(region.cfg.spawn.size, device=env.device)

    min_forbidden = pos - (size / 2)
    max_forbidden = pos + (size / 2)

    # Get the overall sampling bounds from `pose_range`
    min_bounds = torch.tensor([pose_range["x"][0], pose_range["y"][0], pose_range["z"][0]], device=env.device)
    max_bounds = torch.tensor([pose_range["x"][1], pose_range["y"][1], pose_range["z"][1]], device=env.device)

    # Define the four valid regions around the forbidden region (X-Y plane)
    valid_regions = [
        (min_bounds, torch.tensor([min_forbidden[0], max_bounds[1], max_bounds[2]], device=env.device)),  # Left region
        (torch.tensor([max_forbidden[0], min_bounds[1], min_bounds[2]], device=env.device), max_bounds),  # Right region
        (torch.tensor([min_forbidden[0], max_bounds[1], min_bounds[2]], device=env.device), max_bounds),  # Top region
        (min_bounds, torch.tensor([max_bounds[0], min_forbidden[1], max_bounds[2]], device=env.device)),  # Bottom region
    ]

    for name in asset_names:
        asset: RigidObject | Articulation = env.scene[name]
        root_states = asset.data.default_root_state[env_ids].clone()

        # Sample positions ensuring they are OUTSIDE the forbidden region
        positions = torch.zeros((len(env_ids), 3), device=asset.device)

        for i in range(len(env_ids)):
            # Randomly select one of the valid regions
            min_valid, max_valid = random.choice(valid_regions)

            # Sample uniformly within the selected region
            positions[i] = torch.tensor([
                torch.rand((), device=asset.device) * (max_valid[0] - min_valid[0]) + min_valid[0],
                torch.rand((), device=asset.device) * (max_valid[1] - min_valid[1]) + min_valid[1],
                torch.rand((), device=asset.device) * (max_valid[2] - min_valid[2]) + min_valid[2],
            ])

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

        # Set new state into the simulation
        asset.write_root_pose_to_sim(torch.cat([positions, orientations], dim=-1), env_ids=env_ids)
        asset.write_root_velocity_to_sim(velocities, env_ids=env_ids)
