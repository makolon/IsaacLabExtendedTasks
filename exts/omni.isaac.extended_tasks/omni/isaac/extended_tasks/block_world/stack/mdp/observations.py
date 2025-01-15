from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import torch
from PIL import Image, ImageChops, ImageEnhance

import omni.isaac.lab.utils.math as math_utils
from omni.isaac.lab.assets import RigidObject
from omni.isaac.lab.managers import SceneEntityCfg
from omni.isaac.lab.sensors import CameraData
from omni.isaac.lab.sensors import Camera, RayCasterCamera, TiledCamera

from omni.isaac.lab.utils.math import subtract_frame_transforms

if TYPE_CHECKING:
    from omni.isaac.lab.envs import ManagerBasedRLEnv


def target_object_position_in_robot_root_frame(
    env: ManagerBasedRLEnv,
    robot_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
    object_cfg: SceneEntityCfg = SceneEntityCfg("target_object"),
) -> torch.Tensor:
    """The position of the object in the robot's root frame."""
    robot: RigidObject = env.scene[robot_cfg.name]
    object: RigidObject = env.scene[object_cfg.name]
    object_pos_w = object.data.root_pos_w[:, :3]
    object_pos_b, _ = subtract_frame_transforms(
        robot.data.root_state_w[:, :3], robot.data.root_state_w[:, 3:7], object_pos_w
    )
    return object_pos_b


def cam_position(env: ManagerBasedRLEnv, sensor_cfg: SceneEntityCfg) -> torch.Tensor:
    """Position of the camera."""
    # extract the used quantities (to enable type-hinting)
    sensor: Camera = env.scene.sensors[sensor_cfg.name]

    return sensor.data.pos_w.clone()


def cam_orientation(env: ManagerBasedRLEnv, sensor_cfg: SceneEntityCfg) -> torch.Tensor:
    """Orientation of the camera."""
    # extract the used quantities (to enable type-hinting)
    sensor: Camera = env.scene.sensors[sensor_cfg.name]

    return sensor.data.quat_w_world.clone()


def gelsight_image(
    env: ManagerBasedRLEnv,
    sensor_cfg: SceneEntityCfg,
    data_type: str = "rgb",
    convert_perspective_to_orthogonal: bool = False,
    normalize: bool = True,
) -> torch.Tensor:
    """Gelsight image."""
    # extract the used quantities (to enable type-hinting)
    sensor: TiledCamera | Camera | RayCasterCamera = env.scene.sensors[sensor_cfg.name]

    # obtain the input image
    images = sensor.data.output[data_type]

    # depth image conversion
    if (data_type == "distance_to_camera") and convert_perspective_to_orthogonal:
        images = math_utils.orthogonalize_perspective_depth(images, sensor.data.intrinsic_matrices)

    # rgb/depth image normalization
    if normalize:
        if data_type == "rgb":
            images = images.float() / 255.0
            mean_tensor = torch.mean(images, dim=(1, 2), keepdim=True)
            images -= mean_tensor
        elif "distance_to" in data_type or "depth" in data_type:
            images[images == float("inf")] = 0


    return _process_and_convert_image(images.clone())


def _process_and_convert_image(
    input_tensor: torch.Tensor,
    static_img_path: str,
    default_img_path: str,
    border_indices: torch.Tensor,
) -> torch.Tensor:
    """
    Process the RGB image from a torch.Tensor, subtract the static image, 
    add the default image, and return the result as a torch.Tensor.

    Args:
        input_tensor (torch.Tensor): The input tensor of shape (H, W, 4) or (H, W, 3).
        static_img_path (str): Path to the static image.
        default_img_path (str): Path to the default image.
        border_indices (torch.Tensor): Indices to modify for the border pixels, shape (N, 2).

    Returns:
        torch.Tensor: Processed image tensor of shape (H, W, 3).
    """
    # Convert input tensor to numpy array and drop alpha channel if present
    input_array = input_tensor.detach().cpu().numpy()
    if input_array.shape[2] == 4:
        input_array = input_array[:, :, :3]

    # Apply border modifications
    input_array[border_indices[:, 0], border_indices[:, 1]] = [255, 255, 255]

    # Convert to PIL image
    input_img = Image.fromarray(input_array.astype(np.uint8), 'RGB')

    # Load the static and default images
    static_img = Image.open(static_img_path).convert('RGB')
    default_img = Image.open(default_img_path).convert('RGB')

    # Subtract the static image
    subtracted_img = ImageChops.subtract(input_img, static_img)
    enhancer = ImageEnhance.Brightness(subtracted_img)
    subtracted_img = enhancer.enhance(1)

    # Add the default image
    result_img = ImageChops.add(subtracted_img, default_img)

    # Add Gaussian noise
    result_array = np.array(result_img)
    gauss = np.random.normal(0, 7, result_array.shape)
    result_array = np.clip(result_array + gauss, 0, 255).astype(np.uint8)

    # Convert back to torch.Tensor
    result_tensor = torch.from_numpy(result_array).float() / 255.0  # Normalize to [0, 1]

    return result_tensor