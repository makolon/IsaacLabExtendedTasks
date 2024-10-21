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
            disable_gravity=False,
            max_depenetration_velocity=5.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True,
            solver_position_iteration_count=8,
            solver_velocity_iteration_count=0,
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        joint_pos={
            "joint1": 0.0,
            "joint2": -0.569,
            "joint3": 0.0,
            "joint4": 2.810,
            "joint5": 0.0,
            "joint6": 3.037,
            "joint7": 0.741,
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
            velocity_limit=100.0,
            effort_limit={
                "joint1": 39.0,
                "joint2": 39.0,
                "joint3": 39.0,
                "joint4": 39.0,
                "joint5": 9.0,
                "joint6": 9.0,
                "joint7": 9.0,
            },
            stiffness={
                "joint1": 40.0,
                "joint2": 40.0,
                "joint3": 40.0,
                "joint4": 40.0,
                "joint5": 15.0,
                "joint6": 15.0,
                "joint7": 15.0,
            },
            damping={
                "joint1": 1.0,
                "joint2": 1.0,
                "joint3": 1.0,
                "joint4": 1.0,
                "joint5": 0.5,
                "joint6": 0.5,
                "joint7": 0.5,
            },
        ),
        "gripper": ImplicitActuatorCfg(
            joint_names_expr=["drive_joint"],
            effort_limit=10.0,
            velocity_limit=0.05,
            stiffness=2e1,
            damping=1e2,
        ),
    },
    soft_joint_pos_limit_factor=1.0,
)
"""Configuration of UFactory XArm7 robot with gripper."""
