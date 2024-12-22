import random
from omni.isaac.extended_tasks.block_world.stack import mdp
from omni.isaac.extended_tasks.block_world.stack.stack_env_cfg import StackEnvCfg
from omni.isaac.lab.assets import RigidObjectCfg
from omni.isaac.lab.sensors import FrameTransformerCfg
from omni.isaac.lab.sensors.frame_transformer.frame_transformer_cfg import OffsetCfg
from omni.isaac.lab.sim.schemas.schemas_cfg import RigidBodyPropertiesCfg
from omni.isaac.lab.sim.spawners.from_files.from_files_cfg import UsdFileCfg
from omni.isaac.lab.utils import configclass
from omni.isaac.lab.utils.assets import ISAAC_NUCLEUS_DIR

from omni.isaac.lab.markers.config import FRAME_MARKER_CFG  # isort: skip
from omni.isaac.extended_assets.kinova import KINOVA_JACO_7N_CFG  # isort: skip


@configclass
class Jaco7NStackEnvCfg(StackEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # Set Franka as robot
        self.scene.robot = KINOVA_JACO_7N_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")

        # Set actions for the specific robot type (franka)
        self.actions.arm_action = mdp.JointPositionActionCfg(
            asset_name="robot",
            joint_names=["j2s7n300_joint.*"],
            scale=1.0,
            use_default_offset=False,
            preserve_order=True,
        )
        self.actions.gripper_action = mdp.BinaryJointPositionActionCfg(
            asset_name="robot",
            joint_names=["j2n7n300_joint_finger.*"],
            open_command_expr={"j2n7n300_joint_finger.*": 0.04},
            close_command_expr={"j2n7n300_joint_finger.*": 0.0},
        )
        # Set the body name for the end effector
        self.commands.object_pose.body_name = "j2n7n300_end_effector"

        # Collect all configs
        block_cfgs = {}
        for block_color in ["blue", "green", "red", "yellow"]:
            block_cfgs[block_color] = RigidObjectCfg(
                prim_path="{ENV_REGEX_NS}/" + "{}Block".format(block_color.capitalize()),
                init_state=RigidObjectCfg.InitialStateCfg(
                    pos=[0.5, 0, 0.02], rot=[1, 0, 0, 0]
                ),
                spawn=UsdFileCfg(
                    usd_path=f"{ISAAC_NUCLEUS_DIR}/Props/Blocks/{block_color}_block.usd",
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

        # Set the configs as member of the class
        for k, v in block_cfgs.items():
            attr_name = "{}_block".format(k)
            self.scene.__setattr__(attr_name, v)

        # Set target object (randomly)
        self.scene.target_object = random.choice(list(block_cfgs.values()))

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
class Jaco7NStackEnvCfg_PLAY(Jaco7NStackEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False
