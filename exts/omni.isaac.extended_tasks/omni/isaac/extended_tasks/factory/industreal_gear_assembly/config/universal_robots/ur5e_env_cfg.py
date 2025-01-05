from omni.isaac.extended_tasks.factory.industreal_gear_assembly import mdp
from omni.isaac.extended_tasks.factory.industreal_gear_assembly.industreal_gear_assembly_env_cfg import IndustrealGearAssemblyEnvCfg
from omni.isaac.lab.assets import RigidObjectCfg
from omni.isaac.lab.sensors import FrameTransformerCfg
from omni.isaac.lab.sensors.frame_transformer.frame_transformer_cfg import OffsetCfg
from omni.isaac.lab.sim.schemas.schemas_cfg import RigidBodyPropertiesCfg
from omni.isaac.lab.sim.spawners.from_files.from_files_cfg import UsdFileCfg
from omni.isaac.lab.utils import configclass

from omni.isaac.lab.markers.config import FRAME_MARKER_CFG  # isort: skip
from omni.isaac.extended_assets.universal_robots import UR5E_ROBOTIQ_2F_85_CFG  # isort: skip
from omni.isaac.extended_tasks.factory.industreal_gear_assembly import INDUSTREAL_ASSEMBLY_DIR  # isort: skip


@configclass
class UR5eAssemblyEnvCfg(IndustrealGearAssemblyEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # Set UR5e as robot
        self.scene.robot = UR5E_ROBOTIQ_2F_85_CFG.replace(
            prim_path="{ENV_REGEX_NS}/Robot"
        )

        # Set actions for the specific robot type (ur5e)
        self.actions.arm_action = mdp.JointPositionActionCfg(
            asset_name="robot",
            joint_names=[
                "shoulder_pan_joint",
                "shoulder_lift_joint",
                "elbow_joint",
                "wrist_1_joint",
                "wrist_2_joint",
                "wrist_3_joint",
            ],
            scale=1.0,
            use_default_offset=False,
            preserve_order=True,
        )
        self.actions.gripper_action = mdp.JointPositionActionCfg(
            asset_name="robot",
            joint_names=["finger_joint"],
            scale=1.0,
            use_default_offset=False,
            preserve_order=True,
        )
        # Set the body name for the end effector
        self.commands.object_pose.body_name = "grasp_frame"

        # Set gear small
        self.scene.gear_small = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/GearSmall",
            init_state=RigidObjectCfg.InitialStateCfg(
                pos=[0.5, 0, 0.055], rot=[1, 0, 0, 0]
            ),
            spawn=UsdFileCfg(
                usd_path=f"{INDUSTREAL_ASSEMBLY_DIR}/industreal_gear_small/industreal_gear_small.usd",
                scale=(1.0, 1.0, 1.0),
                rigid_props=RigidBodyPropertiesCfg(
                    solver_position_iteration_count=192,
                    solver_velocity_iteration_count=1,
                    max_angular_velocity=3666.0,
                    max_linear_velocity=1000.0,
                    max_contact_impulse=1e32,
                    max_depenetration_velocity=5.0,
                    linear_damping=0.0,
                    angular_damping=0.0,
                    enable_gyroscopic_forces=True,
                    rigid_body_enabled=True,
                    disable_gravity=False,
                ),
            ),
        )

        # Set gear medium
        self.scene.gear_medium = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/GearMedium",
            init_state=RigidObjectCfg.InitialStateCfg(
                pos=[0.5, 0, 0.055], rot=[1, 0, 0, 0]
            ),
            spawn=UsdFileCfg(
                usd_path=f"{INDUSTREAL_ASSEMBLY_DIR}/industreal_gear_medium/industreal_gear_medium.usd",
                scale=(1.0, 1.0, 1.0),
                rigid_props=RigidBodyPropertiesCfg(
                    solver_position_iteration_count=192,
                    solver_velocity_iteration_count=1,
                    max_angular_velocity=3666.0,
                    max_linear_velocity=1000.0,
                    max_contact_impulse=1e32,
                    max_depenetration_velocity=5.0,
                    linear_damping=0.0,
                    angular_damping=0.0,
                    enable_gyroscopic_forces=True,
                    rigid_body_enabled=True,
                    disable_gravity=False,
                ),
            ),
        )

        # Set gear large
        self.scene.gear_large = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/GearLarge",
            init_state=RigidObjectCfg.InitialStateCfg(
                pos=[0.5, 0, 0.055], rot=[1, 0, 0, 0]
            ),
            spawn=UsdFileCfg(
                usd_path=f"{INDUSTREAL_ASSEMBLY_DIR}/industreal_gear_large/industreal_gear_large.usd",
                scale=(1.0, 1.0, 1.0),
                rigid_props=RigidBodyPropertiesCfg(
                    solver_position_iteration_count=192,
                    solver_velocity_iteration_count=1,
                    max_angular_velocity=3666.0,
                    max_linear_velocity=1000.0,
                    max_contact_impulse=1e32,
                    max_depenetration_velocity=5.0,
                    linear_damping=0.0,
                    angular_damping=0.0,
                    enable_gyroscopic_forces=True,
                    rigid_body_enabled=True,
                    disable_gravity=False,
                ),
            ),
        )

        # Set gear base
        self.scene.gear_base = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/GearBase",
            init_state=RigidObjectCfg.InitialStateCfg(
                pos=[0.5, 0.1, 0.01], rot=[1, 0, 0, 0]
            ),
            spawn=UsdFileCfg(
                usd_path=f"{INDUSTREAL_ASSEMBLY_DIR}/industreal_gear_base/industreal_gear_base.usd",
                scale=(1.0, 1.0, 1.0),
                rigid_props=RigidBodyPropertiesCfg(
                    solver_position_iteration_count=192,
                    solver_velocity_iteration_count=1,
                    max_angular_velocity=3666.0,
                    max_linear_velocity=1000.0,
                    max_contact_impulse=1e32,
                    max_depenetration_velocity=5.0,
                    linear_damping=0.0,
                    angular_damping=0.0,
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
            prim_path="{ENV_REGEX_NS}/Robot/base_link",
            debug_vis=False,
            visualizer_cfg=marker_cfg,
            target_frames=[
                FrameTransformerCfg.FrameCfg(
                    prim_path="{ENV_REGEX_NS}/Robot/grasp_frame",
                    name="end_effector",
                    offset=OffsetCfg(
                        pos=[0.0, 0.0, 0.1034],
                    ),
                ),
            ],
        )


@configclass
class UR5eAssemblyEnvCfg_PLAY(UR5eAssemblyEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False
