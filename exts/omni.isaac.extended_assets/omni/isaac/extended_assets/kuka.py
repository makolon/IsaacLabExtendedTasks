import omni.isaac.lab.sim as sim_utils
from omni.isaac.lab.actuators import ImplicitActuatorCfg
from omni.isaac.lab.assets.articulation import ArticulationCfg

from . import ISAACLAB_EXTENDED_ASSETS_DATA_DIR

##
# Configuration
##

LBR_IIWA7_SCHUNK_WSG_50_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ISAACLAB_EXTENDED_ASSETS_DATA_DIR}/Robots/USD/KUKA/iiwa7_schunk_wsg50/iiwa_schunk_wsg50.usd",
        activate_contact_sensors=False,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=True,
            max_depenetration_velocity=5.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=False,
            solver_position_iteration_count=32,
            solver_velocity_iteration_count=4,
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        joint_pos={
            "iiwa7_joint_1": 0.0,
            "iiwa7_joint_2": 0.611,
            "iiwa7_joint_3": 0.0,
            "iiwa7_joint_4": -1.31,
            "iiwa7_joint_5": 0.0,
            "iiwa7_joint_6": 1.22,
            "iiwa7_joint_7": 1.57,
            "drive_joint": 0.003,
        },
    ),
    actuators={
        "arm": ImplicitActuatorCfg(
            joint_names_expr=[
                "iiwa7_joint_1",
                "iiwa7_joint_2",
                "iiwa7_joint_3",
                "iiwa7_joint_4",
                "iiwa7_joint_5",
                "iiwa7_joint_6",
                "iiwa7_joint_7",
            ],
            velocity_limit=300.0,
            effort_limit={
                "iiwa7_joint_1": 500.0,
                "iiwa7_joint_2": 500.0,
                "iiwa7_joint_3": 500.0,
                "iiwa7_joint_4": 500.0,
                "iiwa7_joint_5": 300.0,
                "iiwa7_joint_6": 300.0,
                "iiwa7_joint_7": 300.0,
            },
            stiffness={
                "iiwa7_joint_1": 500.0,
                "iiwa7_joint_2": 500.0,
                "iiwa7_joint_3": 500.0,
                "iiwa7_joint_4": 500.0,
                "iiwa7_joint_5": 300.0,
                "iiwa7_joint_6": 300.0,
                "iiwa7_joint_7": 300.0,
            },
            damping={
                "iiwa7_joint_1": 10.0,
                "iiwa7_joint_2": 10.0,
                "iiwa7_joint_3": 10.0,
                "iiwa7_joint_4": 10.0,
                "iiwa7_joint_5": 5.0,
                "iiwa7_joint_6": 5.0,
                "iiwa7_joint_7": 5.0,
            },
        ),
        "gripper": ImplicitActuatorCfg(
            joint_names_expr=["drive_joint"],
            effort_limit=10.0,
            velocity_limit=0.2,
            stiffness=10.0,
            damping=5.0,
        ),
    },
    soft_joint_pos_limit_factor=1.0,
)
"""Configuration of KUKA LBR IIWA7 robot with SCHUNK WSG 50 gripper."""


LBR_IIWA7_ALLEGRO_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ISAACLAB_EXTENDED_ASSETS_DATA_DIR}/Robots/USD/KUKA/iiwa7_allegro/iiwa_allegro.usd",
        activate_contact_sensors=False,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=True,
            max_depenetration_velocity=5.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True,
            solver_position_iteration_count=32,
            solver_velocity_iteration_count=4,
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        joint_pos={
            "iiwa7_joint_1": 0.0,
            "iiwa7_joint_2": 0.611,
            "iiwa7_joint_3": 0.0,
            "iiwa7_joint_4": -1.31,
            "iiwa7_joint_5": 0.0,
            "iiwa7_joint_6": 1.22,
            "iiwa7_joint_7": 1.57,
            "index_joint.*": 0.04,
        },
    ),
    actuators={
        "arm": ImplicitActuatorCfg(
            joint_names_expr=[
                "iiwa7_joint_1",
                "iiwa7_joint_2",
                "iiwa7_joint_3",
                "iiwa7_joint_4",
                "iiwa7_joint_5",
                "iiwa7_joint_6",
                "iiwa7_joint_7",
            ],
            velocity_limit=100.0,
            effort_limit={
                "iiwa7_joint_1": 39.0,
                "iiwa7_joint_2": 39.0,
                "iiwa7_joint_3": 39.0,
                "iiwa7_joint_4": 39.0,
                "iiwa7_joint_5": 9.0,
                "iiwa7_joint_6": 9.0,
                "iiwa7_joint_7": 9.0,
            },
            stiffness={
                "iiwa7_joint_1": 40.0,
                "iiwa7_joint_2": 40.0,
                "iiwa7_joint_3": 40.0,
                "iiwa7_joint_4": 40.0,
                "iiwa7_joint_5": 15.0,
                "iiwa7_joint_6": 15.0,
                "iiwa7_joint_7": 15.0,
            },
            damping={
                "iiwa7_joint_1": 1.0,
                "iiwa7_joint_2": 1.0,
                "iiwa7_joint_3": 1.0,
                "iiwa7_joint_4": 1.0,
                "iiwa7_joint_5": 0.5,
                "iiwa7_joint_6": 0.5,
                "iiwa7_joint_7": 0.5,
            },
        ),
        "gripper": ImplicitActuatorCfg(
            joint_names_expr=["index_joint.*"],
            effort_limit=100.0,
            velocity_limit=0.2,
            stiffness=2e3,
            damping=1e2,
        ),
    },
    soft_joint_pos_limit_factor=1.0,
)
"""Configuration of KUKA LBR IIWA7 robot with allegro hand."""
