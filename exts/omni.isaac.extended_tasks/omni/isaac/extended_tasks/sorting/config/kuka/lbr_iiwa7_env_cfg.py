import os
import random
from omni.isaac.extended_tasks.assembly import mdp
from omni.isaac.extended_tasks.assembly.assembly_env_cfg import AssemblyEnvCfg
from omni.isaac.lab.assets import RigidObjectCfg
from omni.isaac.lab.sensors import FrameTransformerCfg
from omni.isaac.lab.sensors.frame_transformer.frame_transformer_cfg import OffsetCfg
from omni.isaac.lab.sim.schemas.schemas_cfg import RigidBodyPropertiesCfg
from omni.isaac.lab.sim.spawners.from_files.from_files_cfg import UsdFileCfg
from omni.isaac.lab.utils import configclass

from omni.isaac.lab.markers.config import FRAME_MARKER_CFG  # isort: skip
from omni.isaac.extended_assets.kuka import LBR_IIWA7_SCHUNK_WSG_50_CFG  # isort: skip
from omni.isaac.extended_tasks.assembly import FUSION360_FIXTURE_PATH, FUSION360_OBJECT_PATH  # isort: skip


@configclass
class LBRIIWA7AssemblyEnvCfg(AssemblyEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # Set Franka as robot
        self.scene.robot = LBR_IIWA7_SCHUNK_WSG_50_CFG.replace(
            prim_path="{ENV_REGEX_NS}/Robot"
        )

        # Set actions for the specific robot type (franka)
        self.actions.arm_action = mdp.JointPositionActionCfg(
            asset_name="robot",
            joint_names=["iiwa7_joint_.*"],
            scale=1.0,
            use_default_offset=False,
            preserve_order=True,
        )
        self.actions.gripper_action = mdp.BinaryJointPositionActionCfg(
            asset_name="robot",
            joint_names=["wsg_50_base_joint_gripper_.*"],
            open_command_expr={"wsg_50_base_joint_gripper_.*": 0.0},
            close_command_expr={"wsg_50_base_joint_gripper_.*": 0.04},
        )
        # Set the body name for the end effector
        self.commands.object_pose.body_name = "wsg_50_base_link"

        # Create dictionaries with IDs as keys and paths as values
        fixture_dict = {os.path.basename(os.path.dirname(os.path.dirname(fixture))): fixture for fixture in FUSION360_FIXTURE_PATH}
        object_dict = {os.path.basename(os.path.dirname(os.path.dirname(obj))): obj for obj in FUSION360_OBJECT_PATH}

        # Find common IDs and corresponding paths
        common_ids = set(fixture_dict.keys()) & set(object_dict.keys())
        common_paths = [(fixture_dict[id], object_dict[id]) for id in common_ids]

        # Select parts path randomly
        fixture_path, object_path = random.choice(common_paths)

        # Set target object
        self.scene.object = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/Object",
            init_state=RigidObjectCfg.InitialStateCfg(
                pos=[0.5, 0, 0.055], rot=[1, 0, 0, 0]
            ),
            spawn=UsdFileCfg(
                usd_path=object_path,
                scale=(1.0, 1.0, 1.0),
                rigid_props=RigidBodyPropertiesCfg(
                    solver_position_iteration_count=16,
                    solver_velocity_iteration_count=0,
                    max_angular_velocity=64.0,
                    max_linear_velocity=1000.0,
                    max_depenetration_velocity=5.0,
                    linear_damping=0.5,
                    angular_damping=0.5,
                    enable_gyroscopic_forces=True,
                    rigid_body_enabled=True,
                    disable_gravity=False,
                ),
            ),
        )

        # Set fixture
        self.scene.fixture = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/Fixture",
            init_state=RigidObjectCfg.InitialStateCfg(
                pos=[0.5, 0.1, 0.055], rot=[1, 0, 0, 0]
            ),
            spawn=UsdFileCfg(
                usd_path=fixture_path,
                scale=(1.0, 1.0, 1.0),
                rigid_props=RigidBodyPropertiesCfg(
                    solver_position_iteration_count=16,
                    solver_velocity_iteration_count=0,
                    max_angular_velocity=64.0,
                    max_linear_velocity=1000.0,
                    max_depenetration_velocity=5.0,
                    linear_damping=0.5,
                    angular_damping=0.5,
                    enable_gyroscopic_forces=True,
                    rigid_body_enabled=True,
                    disable_gravity=False,
                    kinematic_enabled=True,
                ),
            ),
        )

        # Listens to the required transforms
        marker_cfg = FRAME_MARKER_CFG.copy()
        marker_cfg.markers["frame"].scale = (0.1, 0.1, 0.1)
        marker_cfg.prim_path = "/Visuals/FrameTransformer"
        self.scene.ee_frame = FrameTransformerCfg(
            prim_path="{ENV_REGEX_NS}/Robot/iiwa7_link_0",
            debug_vis=False,
            visualizer_cfg=marker_cfg,
            target_frames=[
                FrameTransformerCfg.FrameCfg(
                    prim_path="{ENV_REGEX_NS}/Robot/wsg_50_base_link",
                    name="end_effector",
                    offset=OffsetCfg(
                        pos=[0.0, 0.0, 0.1034],
                    ),
                ),
            ],
        )


@configclass
class LBRIIWA7AssemblyEnvCfg_PLAY(LBRIIWA7AssemblyEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False
