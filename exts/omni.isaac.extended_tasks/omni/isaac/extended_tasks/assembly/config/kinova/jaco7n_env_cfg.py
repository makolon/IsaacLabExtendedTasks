from omni.isaac.extended_tasks.assembly import mdp
from omni.isaac.extended_tasks.assembly.assembly_env_cfg import AssemblyEnvCfg
from omni.isaac.lab.assets import RigidObjectCfg
from omni.isaac.lab.sensors import FrameTransformerCfg
from omni.isaac.lab.sensors.frame_transformer.frame_transformer_cfg import OffsetCfg
from omni.isaac.lab.sim.schemas.schemas_cfg import RigidBodyPropertiesCfg
from omni.isaac.lab.sim.spawners.from_files.from_files_cfg import UsdFileCfg
from omni.isaac.lab.utils import configclass

from omni.isaac.lab.markers.config import FRAME_MARKER_CFG  # isort: skip
from omni.isaac.extended_assets.kinova import KINOVA_JACO_7N_CFG  # isort: skip
from omni.isaac.extended_assets import ISAACLAB_EXTENDED_ASSETS_DATA_DIR


@configclass
class Jaco7NAssemblyEnvCfg(AssemblyEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # Set Franka as robot
        self.scene.robot = KINOVA_JACO_7N_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")

        # Set actions for the specific robot type (franka)
        self.actions.arm_action = mdp.JointPositionActionCfg(
            asset_name="robot",
            joint_names=["j2s7n300_joint.*"],
            scale=0.5,
            use_default_offset=True,
        )
        self.actions.gripper_action = mdp.BinaryJointPositionActionCfg(
            asset_name="robot",
            joint_names=["j2n7n300_joint_finger.*"],
            open_command_expr={"j2n7n300_joint_finger.*": 0.04},
            close_command_expr={"j2n7n300_joint_finger.*": 0.0},
        )
        # Set the body name for the end effector
        self.commands.object_pose.body_name = "j2n7n300_end_effector"

        # Set target object
        self.scene.object = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/Object",
            init_state=RigidObjectCfg.InitialStateCfg(
                pos=[0.5, 0, 0.055], rot=[1, 0, 0, 0]
            ),
            spawn=UsdFileCfg(
                usd_path=f"{ISAACLAB_EXTENDED_ASSETS_DATA_DIR}/Props/USD/fusion360/00004/model_0/model_0.usd",
                scale=(1.0, 1.0, 1.0),
                rigid_props=RigidBodyPropertiesCfg(
                    solver_position_iteration_count=32,
                    solver_velocity_iteration_count=32,
                    max_angular_velocity=10.0,
                    max_linear_velocity=10.0,
                    max_depenetration_velocity=3.0,
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
                usd_path=f"{ISAACLAB_EXTENDED_ASSETS_DATA_DIR}/Props/USD/fusion360/00004/model_1/model_1.usd",
                scale=(1.0, 1.0, 1.0),
                rigid_props=RigidBodyPropertiesCfg(
                    solver_position_iteration_count=32,
                    solver_velocity_iteration_count=32,
                    max_angular_velocity=10.0,
                    max_linear_velocity=10.0,
                    max_depenetration_velocity=3.0,
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
            prim_path="{ENV_REGEX_NS}/Robot/j2n7n300_link_base",
            debug_vis=False,
            visualizer_cfg=marker_cfg,
            target_frames=[
                FrameTransformerCfg.FrameCfg(
                    prim_path="{ENV_REGEX_NS}/Robot/j2n7n300_end_effector",
                    name="end_effector",
                    offset=OffsetCfg(
                        pos=[0.0, 0.0, 0.1034],
                    ),
                ),
            ],
        )


@configclass
class Jaco7NAssemblyEnvCfg_PLAY(Jaco7NAssemblyEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False
