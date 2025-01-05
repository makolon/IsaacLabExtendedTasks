import random
from omni.isaac.extended_tasks.block_world.sort import mdp
from omni.isaac.extended_tasks.block_world.sort.sort_env_cfg import SortEnvCfg
from omni.isaac.lab.assets import RigidObjectCfg
from omni.isaac.lab.sensors import FrameTransformerCfg
from omni.isaac.lab.sensors.frame_transformer.frame_transformer_cfg import OffsetCfg
from omni.isaac.lab.sim.schemas.schemas_cfg import RigidBodyPropertiesCfg
from omni.isaac.lab.sim.spawners.shapes import SphereCfg, ConeCfg, CuboidCfg, CapsuleCfg, CylinderCfg
from omni.isaac.lab.utils import configclass

from omni.isaac.lab.markers.config import FRAME_MARKER_CFG  # isort: skip
from omni.isaac.extended_assets.universal_robots import UR5E_ROBOTIQ_2F_85_CFG  # isort: skip


@configclass
class UR5eSortEnvCfg(SortEnvCfg):
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

        # Collect all configs
        rigid_props = RigidBodyPropertiesCfg(
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
        )
        shape_cfg = {
            "sphere": SphereCfg(radius=0.025, rigid_props=rigid_props),
            "cone": ConeCfg(radius=0.025, height=0.05, rigid_props=rigid_props),
            "cuboid": CuboidCfg(size=[0.05, 0.05, 0.05], rigid_props=rigid_props),
            "capsule": CapsuleCfg(radius=0.025, height=0.05, rigid_props=rigid_props),
            "cylinder": CylinderCfg(radius=0.025, height=0.05, rigid_props=rigid_props),
        }
        block_cfgs = {}
        for block_shape in ["sphere", "cone", "cuboid", "capsule", "cylinder"]:
            block_cfgs[block_shape] = RigidObjectCfg(
                prim_path="{ENV_REGEX_NS}/" + "{}Block".format(block_shape.capitalize()),
                init_state=RigidObjectCfg.InitialStateCfg(
                    pos=[0.5, 0, 0.02], rot=[1, 0, 0, 0]
                ),
                spawn=shape_cfg[block_shape],
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
class UR5eSortEnvCfg_PLAY(UR5eSortEnvCfg):
    def __post_init__(self):
        # post init of parent
        super().__post_init__()
        # make a smaller scene for play
        self.scene.num_envs = 50
        self.scene.env_spacing = 2.5
        # disable randomization for play
        self.observations.policy.enable_corruption = False
