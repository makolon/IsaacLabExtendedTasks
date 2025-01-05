from omni.isaac.extended_tasks.factory.siemens_gearbox_assembly import mdp
from omni.isaac.extended_tasks.factory.siemens_gearbox_assembly.siemens_gearbox_assembly_env_cfg import SiemensGearboxAssemblyEnvCfg
from omni.isaac.lab.assets import RigidObjectCfg
from omni.isaac.lab.sensors import FrameTransformerCfg
from omni.isaac.lab.sensors.frame_transformer.frame_transformer_cfg import OffsetCfg
from omni.isaac.lab.sim.schemas.schemas_cfg import RigidBodyPropertiesCfg
from omni.isaac.lab.sim.spawners.from_files.from_files_cfg import UsdFileCfg
from omni.isaac.lab.utils import configclass

from omni.isaac.lab.markers.config import FRAME_MARKER_CFG  # isort: skip
from omni.isaac.extended_assets.ufactory import FACTORY_XARM7_CFG  # isort: skip
from omni.isaac.extended_tasks.factory.siemens_gearbox_assembly import SIEMENS_ASSEMBLY_DIR  # isort: skip


@configclass
class XArm7AssemblyEnvCfg(SiemensGearboxAssemblyEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # Set xArm7 as robot
        self.scene.robot = FACTORY_XARM7_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")

        # Set actions for the specific robot type (xarm7)
        self.actions.arm_action = mdp.JointPositionActionCfg(
            asset_name="robot",
            joint_names=["joint.*"],
            scale=1.0,
            use_default_offset=False,
            preserve_order=True,
        )
        self.actions.gripper_action = mdp.JointPositionActionCfg(
            asset_name="robot",
            joint_names=["drive_joint"],
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
                # NOTE: When scale is 1.0, the position should be pos=[0.5, 0, 0.0135]
                pos=[0.5, 0, 0.0675], rot=[1, 0, 0, 0]
            ),
            spawn=UsdFileCfg(
                usd_path=f"{SIEMENS_ASSEMBLY_DIR}/gear_small/gear_small.usd",
                scale=(0.5, 0.5, 0.5),
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
                # NOTE: When scale is 1.0, the position should be pos=[0.5, 0, 0.0135]
                pos=[0.5, 0, 0.0675], rot=[1, 0, 0, 0]
            ),
            spawn=UsdFileCfg(
                usd_path=f"{SIEMENS_ASSEMBLY_DIR}/gear_medium/gear_medium.usd",
                scale=(0.5, 0.5, 0.5),
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
                # NOTE: When scale is 1.0, the position should be pos=[0.5, 0, 0.0285]
                pos=[0.5, 0, 0.01425], rot=[1, 0, 0, 0]
            ),
            spawn=UsdFileCfg(
                usd_path=f"{SIEMENS_ASSEMBLY_DIR}/gear_large/gear_large.usd",
                scale=(0.5, 0.5, 0.5),
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

        # Set shaft left
        self.scene.shaft_left = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/ShaftLeft",
            init_state=RigidObjectCfg.InitialStateCfg(
                # NOTE: When scale is 1.0, the position should be pos=[0.5, 0, 0.096]
                pos=[0.5, 0, 0.048], rot=[1, 0, 0, 0]
            ),
            spawn=UsdFileCfg(
                usd_path=f"{SIEMENS_ASSEMBLY_DIR}/shaft_left/shaft_left.usd",
                scale=(0.5, 0.5, 0.5),
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

        # Set shaft right
        self.scene.shaft_right = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/ShaftRight",
            init_state=RigidObjectCfg.InitialStateCfg(
                # NOTE: When scale is 1.0, the position should be pos=[0.5, 0, 0.096]
                pos=[0.5, 0, 0.048], rot=[1, 0, 0, 0]
            ),
            spawn=UsdFileCfg(
                usd_path=f"{SIEMENS_ASSEMBLY_DIR}/shaft_right/shaft_right.usd",
                scale=(0.5, 0.5, 0.5),
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
        self.scene.gearbox_base = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/GearBase",
            init_state=RigidObjectCfg.InitialStateCfg(
                # NOTE: When scale is 1.0, the position should be pos=[0.5, 0.1, 0.1025]
                pos=[0.5, 0.1, 0.05125], rot=[1, 0, 0, 0]
            ),
            spawn=UsdFileCfg(
                usd_path=f"{SIEMENS_ASSEMBLY_DIR}/gearbox_base/gearbox_base.usd",
                scale=(0.5, 0.5, 0.5),
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
            prim_path="{ENV_REGEX_NS}/Robot/link_base",
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
class XArm7AssemblyEnvCfg_PLAY(XArm7AssemblyEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False
