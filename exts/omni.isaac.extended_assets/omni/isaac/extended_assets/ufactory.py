import omni.isaac.lab.sim as sim_utils
from omni.isaac.lab.actuators import ImplicitActuatorCfg
from omni.isaac.lab.assets.articulation import ArticulationCfg

from . import ISAACLAB_EXTENDED_ASSETS_DATA_DIR

##
# Configuration
##

XARM7_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ISAACLAB_EXTENDED_ASSETS_DATA_DIR}/Robots/USD/UFactory/xarm7/xarm7.usd",
        activate_contact_sensors=False,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=True,
            max_depenetration_velocity=5.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=False,
            solver_position_iteration_count=8,
            solver_velocity_iteration_count=0,
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        joint_pos={
            "joint1": 0.0,
            "joint2": -0.698,
            "joint3": 0.0,
            "joint4": 0.349,
            "joint5": 0.0,
            "joint6": 1.047,
            "joint7": 0.0,
            "drive_joint": 0.0,
        },
    ),
    actuators={
        "arm": ImplicitActuatorCfg(
            joint_names_expr=[
                "joint1",
                "joint2",
                "joint3",
                "joint4",
                "joint5",
                "joint6",
                "joint7",
            ],
            velocity_limit=3.14,
            effort_limit={
                "joint1": 390.0,
                "joint2": 390.0,
                "joint3": 390.0,
                "joint4": 390.0,
                "joint5": 90.0,
                "joint6": 90.0,
                "joint7": 90.0,
            },
            stiffness={
                "joint1": 400.0,
                "joint2": 400.0,
                "joint3": 400.0,
                "joint4": 400.0,
                "joint5": 150.0,
                "joint6": 150.0,
                "joint7": 15.0,
            },
            damping={
                "joint1": 10.0,
                "joint2": 10.0,
                "joint3": 10.0,
                "joint4": 10.0,
                "joint5": 5.0,
                "joint6": 5.0,
                "joint7": 5.0,
            },
        ),
        "gripper": ImplicitActuatorCfg(
            joint_names_expr=["drive_joint"],
            effort_limit=5.0,
            velocity_limit=0.2,
            stiffness=20.0,
            damping=5.0,
        ),
    },
    soft_joint_pos_limit_factor=1.0,
)
"""Configuration of UFactory XArm7 robot with gripper."""


FACTORY_XARM7_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ISAACLAB_EXTENDED_ASSETS_DATA_DIR}/Robots/USD/UFactory/xarm7/xarm7.usd",
        activate_contact_sensors=True,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=True,
            max_depenetration_velocity=5.0,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=1000.0,
            max_angular_velocity=3666.0,
            enable_gyroscopic_forces=True,
            solver_position_iteration_count=192,
            solver_velocity_iteration_count=1,
            max_contact_impulse=1e32,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=False,
            solver_position_iteration_count=192,
            solver_velocity_iteration_count=1,
        ),
        collision_props=sim_utils.CollisionPropertiesCfg(contact_offset=0.005, rest_offset=0.0),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        joint_pos={
            "joint1": 0.0,
            "joint2": -0.698,
            "joint3": 0.0,
            "joint4": 0.349,
            "joint5": 0.0,
            "joint6": 1.047,
            "joint7": 0.0,
            "drive_joint": 0.0,
        },
    ),
    actuators={
        "arm": ImplicitActuatorCfg(
            joint_names_expr=[
                "joint1",
                "joint2",
                "joint3",
                "joint4",
                "joint5",
                "joint6",
                "joint7",
            ],
            velocity_limit=3.14,
            effort_limit={
                "joint1": 390.0,
                "joint2": 390.0,
                "joint3": 390.0,
                "joint4": 390.0,
                "joint5": 90.0,
                "joint6": 90.0,
                "joint7": 90.0,
            },
            stiffness={
                "joint1": 400.0,
                "joint2": 400.0,
                "joint3": 400.0,
                "joint4": 400.0,
                "joint5": 150.0,
                "joint6": 150.0,
                "joint7": 15.0,
            },
            damping={
                "joint1": 10.0,
                "joint2": 10.0,
                "joint3": 10.0,
                "joint4": 10.0,
                "joint5": 5.0,
                "joint6": 5.0,
                "joint7": 5.0,
            },
        ),
        "gripper": ImplicitActuatorCfg(
            joint_names_expr=["drive_joint"],
            effort_limit=5.0,
            velocity_limit=0.2,
            stiffness=20.0,
            damping=5.0,
        ),
    },
    soft_joint_pos_limit_factor=1.0,
)
"""Configuration of UFactory XArm7 robot with gripper for contact-rich tasks."""