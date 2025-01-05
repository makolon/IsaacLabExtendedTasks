from dataclasses import MISSING

import omni.isaac.lab.sim as sim_utils
from omni.isaac.lab.assets import (
    ArticulationCfg,
    AssetBaseCfg,
    DeformableObjectCfg,
    RigidObjectCfg,
)
from omni.isaac.lab.envs import ManagerBasedRLEnvCfg, mdp
from omni.isaac.lab.managers import CurriculumTermCfg as CurrTerm
from omni.isaac.lab.managers import EventTermCfg as EventTerm
from omni.isaac.lab.managers import ObservationGroupCfg as ObsGroup
from omni.isaac.lab.managers import ObservationTermCfg as ObsTerm
from omni.isaac.lab.managers import RewardTermCfg as RewTerm
from omni.isaac.lab.managers import SceneEntityCfg
from omni.isaac.lab.managers import TerminationTermCfg as DoneTerm
from omni.isaac.lab.scene import InteractiveSceneCfg
from omni.isaac.lab.sensors import CameraCfg
from omni.isaac.lab.sensors.frame_transformer.frame_transformer_cfg import (
    FrameTransformerCfg,
)
from omni.isaac.lab.sim.spawners.from_files.from_files_cfg import (
    GroundPlaneCfg,
    UsdFileCfg,
)
from omni.isaac.lab.utils import configclass
from omni.isaac.lab.utils.assets import ISAAC_NUCLEUS_DIR

from . import mdp as extended_mdp


@configclass
class SiemensGearboxAssemblySceneCfg(InteractiveSceneCfg):
    """Configuration for the assembly scene with a robot and a object.
    This is the abstract base implementation, the exact scene is defined in the derived classes
    which need to set the target object, robot and end-effector frames
    """

    # robots: will be populated by agent env cfg
    robot: ArticulationCfg = MISSING
    # end-effector sensor: will be populated by agent env cfg
    ee_frame: FrameTransformerCfg = MISSING
    # gear: will be populated by agent env cfg
    gear_small: RigidObjectCfg | DeformableObjectCfg = MISSING
    gear_medium: RigidObjectCfg | DeformableObjectCfg = MISSING
    gear_large: RigidObjectCfg | DeformableObjectCfg = MISSING
    # shaft: will be populated by agent env cfg
    shaft_left: RigidObjectCfg | DeformableObjectCfg = MISSING
    shaft_right: RigidObjectCfg | DeformableObjectCfg = MISSING
    # fixture: will be populated by agent env cfg
    gearbox_base: RigidObjectCfg | DeformableObjectCfg = MISSING

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

    # plane
    plane = AssetBaseCfg(
        prim_path="/World/GroundPlane",
        init_state=AssetBaseCfg.InitialStateCfg(pos=[0, 0, -1.05]),
        spawn=GroundPlaneCfg(),
    )

    # lights
    light = AssetBaseCfg(
        prim_path="/World/light",
        spawn=sim_utils.DomeLightCfg(color=(0.75, 0.75, 0.75), intensity=3000.0),
    )

    # rgb camera
    rgb_camera = CameraCfg(
        prim_path="{ENV_REGEX_NS}/rgb_camera",
        update_period=0.0,
        spawn=sim_utils.PinholeCameraCfg(
            focal_length=1.93,
            horizontal_aperture=45.6,
        ),
        width=640,
        height=480,
        data_types=["rgb"],
    )

    # depth camera
    depth_camera = CameraCfg(
        prim_path="{ENV_REGEX_NS}/depth_camera",
        update_period=0.0,
        spawn=sim_utils.PinholeCameraCfg(
            focal_length=1.93,
            horizontal_aperture=45.6,
        ),
        width=640,
        height=480,
        data_types=["distance_to_image_plane"],
    )

    # semantic camera
    semantic_camera = CameraCfg(
        prim_path="{ENV_REGEX_NS}/semantic_camera",
        update_period=0.0,
        spawn=sim_utils.PinholeCameraCfg(
            focal_length=1.93,
            horizontal_aperture=45.6,
        ),
        width=640,
        height=480,
        data_types=["semantic_segmentation"],
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

        joint_pos = ObsTerm(func=mdp.joint_pos_rel)
        joint_vel = ObsTerm(func=mdp.joint_vel_rel)
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

    reset_object_position = EventTerm(
        func=extended_mdp.reset_root_state_uniform,
        mode="reset",
        params={
            "pose_range": {"x": (-0.1, 0.3), "y": (-0.25, 0.25), "z": (0.0, 0.0)},
            "velocity_range": {},
            "asset_names": ["gear_small", "gear_medium", "gear_large", "shaft_left", "shaft_right", "gearbox_base"],
        },
    )


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
class SiemensGearboxAssemblyEnvCfg(ManagerBasedRLEnvCfg):
    """Configuration for the assembly environment."""

    # scene settings
    scene: SiemensGearboxAssemblySceneCfg = SiemensGearboxAssemblySceneCfg(num_envs=4096, env_spacing=2.5)
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
        self.episode_length_s = 60.0
        # simulation settings
        self.sim.dt = 1 / 120
        self.sim.render_interval = self.decimation
        # PhysX settings
        self.sim.physx.solver_type = 1
        self.sim.physx.max_position_iteration_count = 192  # Important to avoid interpenetration.
        self.sim.physx.max_velocity_iteration_count = 1
        self.sim.physx.enable_ccd = True
        self.sim.physx.enable_stabilization = True
        self.sim.physx.bounce_threshold_velocity = 0.2
        self.sim.physx.friction_offset_threshold = 0.01
        self.sim.physx.friction_correlation_distance = 0.00625
        self.sim.physx.gpu_max_rigid_contact_count = 1024 * 1024 * 64
        self.sim.physx.gpu_found_lost_aggregate_pairs_capacity = 1024 * 1024 * 64
        self.sim.physx.gpu_total_aggregate_pairs_capacity = 64 * 1024
        self.sim.physx.gpu_max_num_partitions = 1  # Important for stable simulation.
        # physics material settings
        self.sim.physics_material.static_friction = 1.0
        self.sim.physics_material.dynamic_friction = 1.0
