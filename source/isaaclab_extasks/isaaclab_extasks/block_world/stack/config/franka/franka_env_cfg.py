import random
from isaaclab.envs import mdp
from isaaclab.assets import RigidObjectCfg
from isaaclab.sensors import FrameTransformerCfg
from isaaclab.sensors.frame_transformer.frame_transformer_cfg import OffsetCfg
from isaaclab.sim.schemas.schemas_cfg import RigidBodyPropertiesCfg
from isaaclab.sim.spawners.from_files.from_files_cfg import UsdFileCfg
from isaaclab.sim.spawners.shapes import CuboidCfg
from isaaclab.utils import configclass
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR
from isaaclab.markers.config import FRAME_MARKER_CFG  # isort: skip
from isaaclab_exassets.franka import FRANKA_PANDA_CFG  # isort: skip
from isaaclab_extasks.block_world.stack.stack_env_cfg import StackEnvCfg


@configclass
class FrankaStackEnvCfg(StackEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # Set Franka as robot
        self.scene.robot = FRANKA_PANDA_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")

        # Set actions for the specific robot type (franka)
        self.actions.arm_action = mdp.JointPositionActionCfg(
            asset_name="robot",
            joint_names=["panda_joint.*"],
            scale=1.0,
            use_default_offset=False,
            preserve_order=True,
        )
        self.actions.gripper_action = mdp.JointPositionActionCfg(
            asset_name="robot",
            joint_names=["panda_finger_joint.*"],
            scale=1.0,
            use_default_offset=False,
            preserve_order=True,
        )
        # Set the body name for the end effector
        self.commands.object_pose.body_name = "grasp_frame"

        # Add base as a rigid object
        self.scene.base = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/Base",
            init_state=RigidObjectCfg.InitialStateCfg(
                pos=[0.45, 0.0, -0.01], rot=[1, 0, 0, 0]
            ),
            spawn=CuboidCfg(
                size=[0.5, 0.7, 0.02],
                visible=False,
                rigid_props=RigidBodyPropertiesCfg(
                    solver_position_iteration_count=32,
                    solver_velocity_iteration_count=4,
                    max_angular_velocity=64.0,
                    max_linear_velocity=1000.0,
                    max_depenetration_velocity=5.0,
                    linear_damping=0.5,
                    angular_damping=0.5,
                    enable_gyroscopic_forces=True,
                    rigid_body_enabled=True,
                    disable_gravity=True,
                    kinematic_enabled=True,
                ),
            ),
        )

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
                        solver_position_iteration_count=32,
                        solver_velocity_iteration_count=4,
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
            prim_path="{ENV_REGEX_NS}/Robot/panda_link0",
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
class FrankaStackEnvCfg_PLAY(FrankaStackEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False
