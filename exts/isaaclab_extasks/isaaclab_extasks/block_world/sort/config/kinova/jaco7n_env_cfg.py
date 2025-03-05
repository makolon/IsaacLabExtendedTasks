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
from isaaclab_exassets.kinova import KINOVA_JACO_7N_CFG  # isort: skip
from isaaclab_extasks.block_world.sort.sort_env_cfg import SortEnvCfg


@configclass
class Jaco7NSortEnvCfg(SortEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        # Set Jaco7N as robot
        self.scene.robot = KINOVA_JACO_7N_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")

        # Set actions for the specific robot type (jaco7n)
        self.actions.arm_action = mdp.JointPositionActionCfg(
            asset_name="robot",
            joint_names=["j2s7n300_joint.*"],
            scale=1.0,
            use_default_offset=False,
            preserve_order=True,
        )
        self.actions.gripper_action = mdp.JointPositionActionCfg(
            asset_name="robot",
            joint_names=["j2n7n300_joint_finger.*"],
            scale=1.0,
            use_default_offset=False,
            preserve_order=True,
        )
        # Set the body name for the end effector
        self.commands.object_pose.body_name = "j2n7n300_end_effector"

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

        # Add base as a rigid object
        base_cfgs = {}
        for i, base_number in enumerate(["1", "2", "3", "4"]):
            base_cfgs[base_number] = RigidObjectCfg(
                prim_path="{ENV_REGEX_NS}/Base" + base_number,
                init_state=RigidObjectCfg.InitialStateCfg(
                    pos=[0.5, -0.3+i*0.2, 0.0], rot=[1, 0, 0, 0]
                ),
                spawn=CuboidCfg(
                    size=[0.05, 0.05, 0.01],
                    visible=True,
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
                        kinematic_enabled=True,
                    ),
                ),
            )

        # Set the configs as member of the class
        for k, v in base_cfgs.items():
            attr_name = "base{}".format(k)
            self.scene.__setattr__(attr_name, v)

        # Collect all configs
        block_cfgs = {}
        for i, block_color in enumerate(["blue", "green", "red", "yellow"]):
            block_cfgs[block_color] = RigidObjectCfg(
                prim_path="{ENV_REGEX_NS}/" + "{}Block".format(block_color.capitalize()),
                init_state=RigidObjectCfg.InitialStateCfg(
                    pos=[0.5, -0.3+i*0.2, 0.05], rot=[1, 0, 0, 0]
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
class Jaco7NSortEnvCfg_PLAY(Jaco7NSortEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False
