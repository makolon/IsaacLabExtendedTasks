from dataclasses import MISSING

import isaaclab.sim as sim_utils
from isaaclab.assets import (
    ArticulationCfg,
    AssetBaseCfg,
    RigidObjectCfg,
)
from isaaclab.envs import ManagerBasedRLEnvCfg, mdp
from isaaclab.envs.common import ViewerCfg
from isaaclab.managers import CurriculumTermCfg as CurrTerm
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import ObservationGroupCfg as ObsGroup
from isaaclab.managers import ObservationTermCfg as ObsTerm
from isaaclab.managers import RewardTermCfg as RewTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.managers import TerminationTermCfg as DoneTerm
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.sensors import CameraCfg, TiledCameraCfg
from isaaclab.sensors.frame_transformer.frame_transformer_cfg import (
    FrameTransformerCfg,
)
from isaaclab.sim.spawners.from_files.from_files_cfg import (
    GroundPlaneCfg,
    UsdFileCfg,
)
from isaaclab.utils import configclass
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR

from . import mdp as extended_mdp


@configclass
class SortSceneCfg(InteractiveSceneCfg):
    """Configuration for the sorting scene with a robot and multiple blocks.
    This is the abstract base implementation, the exact scene is defined in the derived classes
    which need to set the target object, robot and end-effector frames
    """

    # robots: will be populated by agent env cfg
    robot: ArticulationCfg = MISSING
    # end-effector sensor: will be populated by agent env cfg
    ee_frame: FrameTransformerCfg = MISSING
    # base: will be populated by agent env cfg
    base: RigidObjectCfg = MISSING

    # table
    table = AssetBaseCfg(
        prim_path="{ENV_REGEX_NS}/Table",
        init_state=AssetBaseCfg.InitialStateCfg(
            pos=[0.5, 0, 0], rot=[0.707, 0, 0, 0.707]
        ),
        spawn=UsdFileCfg(
            usd_path=f"{ISAAC_NUCLEUS_DIR}/Props/Mounts/SeattleLabTable/table_instanceable.usd"
        ),
    )

    # lights
    light = AssetBaseCfg(
        prim_path="/World/light",
        spawn=sim_utils.DomeLightCfg(
            intensity=750.0,
            texture_format="latlong",
            texture_file="https://omniverse-content-staging.s3.us-west-2.amazonaws.com/DoNotDelete/PhysicsDemoAssets/106.5/FrankaNutBolt/ZetoCG.com_WarehouseInterior2b_4x8k.hdr",
        ),  # TODO: Fix texture file path
    )

    # rgb camera
    rgb_camera = TiledCameraCfg(
        prim_path="{ENV_REGEX_NS}/rgb_camera",
        update_period=0.0,
        width=640,
        height=480,
        data_types=["rgb"],
        spawn=sim_utils.PinholeCameraCfg(
            focal_length=19.3,
            focus_distance=5.0,
            horizontal_aperture=38.96,
            vertical_aperture=24.53,
            clipping_range=(0.01, 1000000.0),
        ),
        offset=TiledCameraCfg.OffsetCfg(
            pos=(1.2, 0.0, 0.75),
            rot=(0.61237, 0.35355, 0.35355, 0.61237),  # (0.0, 60.0, 90.0)
            convention="opengl"
        ),
    )

    # depth camera
    depth_camera = TiledCameraCfg(
        prim_path="{ENV_REGEX_NS}/depth_camera",
        update_period=0.0,
        width=640,
        height=480,
        data_types=["distance_to_image_plane"],
        spawn=sim_utils.PinholeCameraCfg(
            focal_length=19.3,
            focus_distance=5.0,
            horizontal_aperture=38.96,
            vertical_aperture=24.53,
            clipping_range=(0.01, 1000000.0),
        ),
        offset=TiledCameraCfg.OffsetCfg(
            pos=(1.2, 0.0, 0.75),
            rot=(0.61237, 0.35355, 0.35355, 0.61237),  # (0.0, 60.0, 90.0)
            convention="opengl"
        ),
    )

    # semantic camera
    semantic_camera = TiledCameraCfg(
        prim_path="{ENV_REGEX_NS}/semantic_camera",
        update_period=0.0,
        width=640,
        height=480,
        data_types=["semantic_segmentation"],
        spawn=sim_utils.PinholeCameraCfg(
            focal_length=19.3,
            focus_distance=5.0,
            horizontal_aperture=38.96,
            vertical_aperture=24.53,
            clipping_range=(0.01, 1000000.0),
        ),
        offset=TiledCameraCfg.OffsetCfg(
            pos=(1.2, 0.0, 0.75),
            rot=(0.61237, 0.35355, 0.35355, 0.61237),  # (0.0, 60.0, 90.0)
            convention="opengl"
        ),
    )


@configclass
class CommandsCfg:
    """Command terms for the MDP."""

    object_pose = mdp.UniformPoseCommandCfg(
        asset_name="robot",
        body_name=MISSING,  # will be set by agent env cfg
        resampling_time_range=(5.0, 5.0),
        debug_vis=False,
        ranges=mdp.UniformPoseCommandCfg.Ranges(
            pos_x=(0.4, 0.6),
            pos_y=(-0.25, 0.25),
            pos_z=(0.25, 0.5),
            roll=(0.0, 0.0),
            pitch=(0.0, 0.0),
            yaw=(0.0, 0.0),
        ),
    )


@configclass
class ActionsCfg:
    """Action specifications for the MDP."""

    # will be set by agent env cfg
    arm_action: (
        mdp.JointPositionActionCfg | mdp.DifferentialInverseKinematicsActionCfg
    ) = MISSING
    gripper_action: mdp.JointPositionActionCfg = MISSING


@configclass
class ObservationsCfg:
    """Observation specifications for the MDP."""

    @configclass
    class PolicyCfg(ObsGroup):
        """Observations for policy group."""

        joint_pos = ObsTerm(func=mdp.joint_pos)
        joint_vel = ObsTerm(func=mdp.joint_vel)
        actions = ObsTerm(func=mdp.last_action)

        def __post_init__(self):
            self.enable_corruption = True
            self.concatenate_terms = True

    @configclass
    class CameraImageCfg(ObsGroup):
        """Observations for image group."""

        rgb_image = ObsTerm(
            func=mdp.image,
            params={"sensor_cfg": SceneEntityCfg("rgb_camera"), "data_type": "rgb"},
        )
        depth_image = ObsTerm(
            func=mdp.image,
            params={
                "sensor_cfg": SceneEntityCfg("depth_camera"),
                "data_type": "distance_to_image_plane",
            },
        )
        semantic_image = ObsTerm(
            func=mdp.image,
            params={
                "sensor_cfg": SceneEntityCfg("semantic_camera"),
                "data_type": "semantic_segmentation",
            },
        )

        def __post_init__(self):
            self.enable_corruption = False
            self.concatenate_terms = False

    @configclass
    class CameraTransformCfg(ObsGroup):
        camera_position = ObsTerm(
            func=extended_mdp.cam_position,
            params={"sensor_cfg": SceneEntityCfg("rgb_camera")},
        )
        camera_orientation = ObsTerm(
            func=extended_mdp.cam_orientation,
            params={"sensor_cfg": SceneEntityCfg("rgb_camera")},
        )

        def __post_init__(self):
            self.enable_corruption = False
            self.concatenate_terms = False

    # observation groups
    policy: PolicyCfg = PolicyCfg()
    camera_image: CameraImageCfg = CameraImageCfg()
    camera_transform: CameraTransformCfg = CameraTransformCfg()


@configclass
class EventCfg:
    """Configuration for events."""

    reset_all = EventTerm(func=mdp.reset_scene_to_default, mode="reset")


@configclass
class RewardsCfg:
    """Reward terms for the MDP."""

    # action penalty
    action_rate = RewTerm(func=mdp.action_rate_l2, weight=-1e-4)

    joint_vel = RewTerm(
        func=mdp.joint_vel_l2,
        weight=-1e-4,
        params={"asset_cfg": SceneEntityCfg("robot")},
    )


@configclass
class TerminationsCfg:
    """Termination terms for the MDP."""

    time_out = DoneTerm(func=mdp.time_out, time_out=True)


@configclass
class CurriculumCfg:
    """Curriculum terms for the MDP."""

    action_rate = CurrTerm(
        func=mdp.modify_reward_weight,
        params={"term_name": "action_rate", "weight": -1e-1, "num_steps": 10000},
    )

    joint_vel = CurrTerm(
        func=mdp.modify_reward_weight,
        params={"term_name": "joint_vel", "weight": -1e-1, "num_steps": 10000},
    )


@configclass
class SortEnvCfg(ManagerBasedRLEnvCfg):
    """Configuration for the sorting environment."""

    # scene settings
    scene: SortSceneCfg = SortSceneCfg(num_envs=4096, env_spacing=2.5)
    # viewer settings
    viewer: ViewerCfg = ViewerCfg(eye=(1.5, 1.5, 1.5), lookat=(0.0, 0.0, 0.0))
    # basic settings
    observations: ObservationsCfg = ObservationsCfg()
    actions: ActionsCfg = ActionsCfg()
    commands: CommandsCfg = CommandsCfg()
    # MDP settings
    rewards: RewardsCfg = RewardsCfg()
    terminations: TerminationsCfg = TerminationsCfg()
    events: EventCfg = EventCfg()
    curriculum: CurriculumCfg = CurriculumCfg()

    def __post_init__(self):
        """Post initialization."""
        # general settings
        self.decimation = 2
        self.episode_length_s = 2000.0
        # simulation settings
        self.sim.dt = 1 / 60
        self.sim.render_interval = self.decimation
        self.sim.physx.enable_ccd = True
        self.sim.physx.enable_stabilization = True
        self.sim.physx.bounce_threshold_velocity = 0.2
        self.sim.physx.friction_offset_threshold = 0.1
        self.sim.physx.friction_correlation_distance = 0.00625
        self.sim.physx.gpu_max_rigid_contact_count = 1024 * 1024 * 64
        self.sim.physx.gpu_found_lost_aggregate_pairs_capacity = 1024 * 1024 * 64
        self.sim.physx.gpu_total_aggregate_pairs_capacity = 64 * 1024
        self.sim.physx.solver_type = 0
        # physics material settings
        self.sim.physics_material.static_friction = 1.0
        self.sim.physics_material.dynamic_friction = 1.0