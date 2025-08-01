import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg

from . import ISAACLAB_EXTENDED_ASSETS_DATA_DIR

##
# Configuration
##

KINOVA_GEN3_N7_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ISAACLAB_EXTENDED_ASSETS_DATA_DIR}/Robots/USD/Kinova/gen3n7/gen3n7.usd",
        activate_contact_sensors=False,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=True,
            max_depenetration_velocity=5.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=False,
            solver_position_iteration_count=192,
            solver_velocity_iteration_count=1,
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        joint_pos={
            "joint_1": 0.0,
            "joint_2": 0.0,
            "joint_3": 0.0,
            "joint_4": 1.57,
            "joint_5": 0.0,
            "joint_6": 1.57,
            "joint_7": 0.0,
            "finger_joint": 0.0,
        },
    ),
    actuators={
        "arm": ImplicitActuatorCfg(
            joint_names_expr=[
                "joint_1",
                "joint_2",
                "joint_3",
                "joint_4",
                "joint_5",
                "joint_6",
                "joint_7",
            ],
            velocity_limit=100.0,
            effort_limit={
                "joint_1": 390.0,
                "joint_2": 390.0,
                "joint_3": 390.0,
                "joint_4": 390.0,
                "joint_5": 90.0,
                "joint_6": 90.0,
                "joint_7": 90.0,
            },
            stiffness={
                "joint_1": 400.0,
                "joint_2": 400.0,
                "joint_3": 400.0,
                "joint_4": 500.0,
                "joint_5": 150.0,
                "joint_6": 150.0,
                "joint_7": 150.0,
            },
            damping={
                "joint_1": 10.0,
                "joint_2": 10.0,
                "joint_3": 10.0,
                "joint_4": 10.0,
                "joint_5": 5.0,
                "joint_6": 5.0,
                "joint_7": 5.0,
            },
        ),
        "gripper": ImplicitActuatorCfg(
            joint_names_expr=["finger_joint"],
            effort_limit=5.0,
            velocity_limit=2.0,
            stiffness=0.05,
            damping=0.01,
        ),
    },
)
"""Configuration of Kinova Gen3 (7-Dof) arm with gripper."""


KINOVA_JACO_7N_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ISAACLAB_EXTENDED_ASSETS_DATA_DIR}/Robots/USD/Kinova/jaco_7n/jaco_7n.usd",
        activate_contact_sensors=False,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=True,
            max_depenetration_velocity=5.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True,
            solver_position_iteration_count=192,
            solver_velocity_iteration_count=1,
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        joint_pos={
            "j2n7s300_joint_1": 0.0,
            "j2n7s300_joint_2": 4.0,
            "j2n7s300_joint_3": 0.0,
            "j2n7s300_joint_4": 5.0,
            "j2n7s300_joint_5": 0.0,
            "j2n7s300_joint_6": 3.0,
            "j2n7s300_joint_7": 0.0,
            "j2n7s300_joint_finger_[1-3]": 0.2,  # close: 1.2, open: 0.2
            "j2n7s300_joint_finger_tip_[1-3]": 0.2,  # close: 1.2, open: 0.2
        },
    ),
    actuators={
        "arm": ImplicitActuatorCfg(
            joint_names_expr=[".*_joint_[1-7]"],
            velocity_limit=100.0,
            effort_limit={
                ".*_joint_[1-2]": 80.0,
                ".*_joint_[3-4]": 40.0,
                ".*_joint_[5-7]": 20.0,
            },
            stiffness={
                ".*_joint_[1-4]": 40.0,
                ".*_joint_[5-7]": 15.0,
            },
            damping={
                ".*_joint_[1-4]": 1.0,
                ".*_joint_[5-7]": 0.5,
            },
        ),
        "gripper": ImplicitActuatorCfg(
            joint_names_expr=[".*_finger_[1-3]", ".*_finger_tip_[1-3]"],
            velocity_limit=100.0,
            effort_limit=2.0,
            stiffness=1.2,
            damping=0.01,
        ),
    },
)
"""Configuration of Kinova Jaco7n (7-Dof) arm with gripper."""


KINOVA_JACO_7S_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ISAACLAB_EXTENDED_ASSETS_DATA_DIR}/Robots/USD/Kinova/jaco_7s/jaco_7s.usd",
        activate_contact_sensors=False,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=True,
            max_depenetration_velocity=5.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True,
            solver_position_iteration_count=192,
            solver_velocity_iteration_count=1,
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        joint_pos={
            "j2s7s300_joint_1": 0.0,
            "j2s7s300_joint_2": 4.0,
            "j2s7s300_joint_3": 0.0,
            "j2s7s300_joint_4": 5.0,
            "j2s7s300_joint_5": 0.0,
            "j2s7s300_joint_6": 3.0,
            "j2s7s300_joint_7": 0.0,
            "j2s7s300_joint_finger_[1-3]": 0.2,  # close: 1.2, open: 0.2
            "j2s7s300_joint_finger_tip_[1-3]": 0.2,  # close: 1.2, open: 0.2
        },
    ),
    actuators={
        "arm": ImplicitActuatorCfg(
            joint_names_expr=[".*_joint_[1-7]"],
            velocity_limit=100.0,
            effort_limit={
                ".*_joint_[1-2]": 80.0,
                ".*_joint_[3-4]": 40.0,
                ".*_joint_[5-7]": 20.0,
            },
            stiffness={
                ".*_joint_[1-4]": 40.0,
                ".*_joint_[5-7]": 15.0,
            },
            damping={
                ".*_joint_[1-4]": 1.0,
                ".*_joint_[5-7]": 0.5,
            },
        ),
        "gripper": ImplicitActuatorCfg(
            joint_names_expr=[".*_finger_[1-3]", ".*_finger_tip_[1-3]"],
            velocity_limit=100.0,
            effort_limit=2.0,
            stiffness=1.2,
            damping=0.01,
        ),
    },
)
"""Configuration of Kinova Jaco7s (7-Dof) arm with gripper."""
