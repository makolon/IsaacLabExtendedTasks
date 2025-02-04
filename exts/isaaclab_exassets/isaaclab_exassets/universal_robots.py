import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg

from . import ISAACLAB_EXTENDED_ASSETS_DATA_DIR

##
# Configuration
##

UR5E_ROBOTIQ_2F_85_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ISAACLAB_EXTENDED_ASSETS_DATA_DIR}/Robots/USD/UniversalRobots/ur5e_robotiq_2f_85/ur5e_robotiq_2f_85.usd",
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
            "shoulder_pan_joint": 0.0,
            "shoulder_lift_joint": -1.72,
            "elbow_joint": 1.72,
            "wrist_1_joint": -1.57,
            "wrist_2_joint": -1.57,
            "wrist_3_joint": 0.0,
            "drive_joint": 0.0,
        },
    ),
    actuators={
        "arm": ImplicitActuatorCfg(
            joint_names_expr=[
                "shoulder_pan_joint",
                "shoulder_lift_joint",
                "elbow_joint",
                "wrist_1_joint",
                "wrist_2_joint",
                "wrist_3_joint",
            ],
            velocity_limit=1.57,
            effort_limit={
                "shoulder_pan_joint": 150.0,
                "shoulder_lift_joint": 150.0,
                "elbow_joint": 150.0,
                "wrist_1_joint": 28.0,
                "wrist_2_joint": 28.0,
                "wrist_3_joint": 28.0,
            },
            stiffness={
                "shoulder_pan_joint": 800.0,
                "shoulder_lift_joint": 800.0,
                "elbow_joint": 800.0,
                "wrist_1_joint": 800.0,
                "wrist_2_joint": 800.0,
                "wrist_3_joint": 800.0,
            },
            damping={
                "shoulder_pan_joint": 40.0,
                "shoulder_lift_joint": 40.0,
                "elbow_joint": 40.0,
                "wrist_1_joint": 40.0,
                "wrist_2_joint": 40.0,
                "wrist_3_joint": 40.0,
            },
        ),
        "gripper:": ImplicitActuatorCfg(
            joint_names_expr=["drive_joint"],
            effort_limit=5.0,
            velocity_limit=0.2,
            stiffness=20.0,
            damping=5.0,
        ),
    },
    soft_joint_pos_limit_factor=1.0,
)
"""Configuration of UR-5e arm with Robotiq 2f 85 using implicit actuator models."""


FACTORY_UR5E_ROBOTIQ_2F_85_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ISAACLAB_EXTENDED_ASSETS_DATA_DIR}/Robots/USD/UniversalRobots/ur5e_robotiq_2f_85/ur5e_robotiq_2f_85.usd",
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
            "shoulder_pan_joint": 0.0,
            "shoulder_lift_joint": -1.72,
            "elbow_joint": 1.72,
            "wrist_1_joint": -1.57,
            "wrist_2_joint": -1.57,
            "wrist_3_joint": 0.0,
            "drive_joint": 0.0,
        },
    ),
    actuators={
        "arm": ImplicitActuatorCfg(
            joint_names_expr=[
                "shoulder_pan_joint",
                "shoulder_lift_joint",
                "elbow_joint",
                "wrist_1_joint",
                "wrist_2_joint",
                "wrist_3_joint",
            ],
            velocity_limit=1.57,
            effort_limit={
                "shoulder_pan_joint": 150.0,
                "shoulder_lift_joint": 150.0,
                "elbow_joint": 150.0,
                "wrist_1_joint": 28.0,
                "wrist_2_joint": 28.0,
                "wrist_3_joint": 28.0,
            },
            stiffness={
                "shoulder_pan_joint": 800.0,
                "shoulder_lift_joint": 800.0,
                "elbow_joint": 800.0,
                "wrist_1_joint": 800.0,
                "wrist_2_joint": 800.0,
                "wrist_3_joint": 800.0,
            },
            damping={
                "shoulder_pan_joint": 40.0,
                "shoulder_lift_joint": 40.0,
                "elbow_joint": 40.0,
                "wrist_1_joint": 40.0,
                "wrist_2_joint": 40.0,
                "wrist_3_joint": 40.0,
            },
        ),
        "gripper:": ImplicitActuatorCfg(
            joint_names_expr=["drive_joint"],
            effort_limit=5.0,
            velocity_limit=0.2,
            stiffness=20.0,
            damping=5.0,
        ),
    },
    soft_joint_pos_limit_factor=1.0,
)
"""Configuration of UR-5e arm with Robotiq 2f 85 using implicit actuator models for contact-rich tasks."""


UR5E_ROBOTIQ_2F_140_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ISAACLAB_EXTENDED_ASSETS_DATA_DIR}/Robots/USD/UniversalRobots/ur5e_robotiq_2f_140/ur5e_robotiq_2f_140.usd",
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
            "shoulder_pan_joint": 0.0,
            "shoulder_lift_joint": -1.712,
            "elbow_joint": 1.712,
            "wrist_1_joint": -1.57,
            "wrist_2_joint": -1.57,
            "wrist_3_joint": 0.0,
            "drive_joint": 0.0,
        },
    ),
    actuators={
        "arm": ImplicitActuatorCfg(
            joint_names_expr=[
                "shoulder_pan_joint",
                "shoulder_lift_joint",
                "elbow_joint",
                "wrist_1_joint",
                "wrist_2_joint",
                "wrist_3_joint",
            ],
            velocity_limit=1.57,
            effort_limit={
                "shoulder_pan_joint": 150.0,
                "shoulder_lift_joint": 150.0,
                "elbow_joint": 150.0,
                "wrist_1_joint": 28.0,
                "wrist_2_joint": 28.0,
                "wrist_3_joint": 28.0,
            },
            stiffness={
                "shoulder_pan_joint": 800.0,
                "shoulder_lift_joint": 800.0,
                "elbow_joint": 800.0,
                "wrist_1_joint": 800.0,
                "wrist_2_joint": 800.0,
                "wrist_3_joint": 800.0,
            },
            damping={
                "shoulder_pan_joint": 40.0,
                "shoulder_lift_joint": 40.0,
                "elbow_joint": 40.0,
                "wrist_1_joint": 40.0,
                "wrist_2_joint": 40.0,
                "wrist_3_joint": 40.0,
            },
        ),
        "gripper:": ImplicitActuatorCfg(
            joint_names_expr=["drive_joint"],
            effort_limit=5.0,
            velocity_limit=0.2,
            stiffness=20.0,
            damping=5.0,
        ),
    },
    soft_joint_pos_limit_factor=1.0,
)
"""Configuration of UR-5e arm with Robotiq 2f 140 using implicit actuator models."""


UR10E_ROBOTIQ_2F_85_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ISAACLAB_EXTENDED_ASSETS_DATA_DIR}/Robots/USD/UniversalRobots/ur10e_robotiq_2f_85/ur10e_robotiq_2f_85.usd",
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
            "shoulder_pan_joint": 0.0,
            "shoulder_lift_joint": -1.712,
            "elbow_joint": 1.712,
            "wrist_1_joint": -1.57,
            "wrist_2_joint": -1.57,
            "wrist_3_joint": 0.0,
            "drive_joint": 0.0,
        },
    ),
    actuators={
        "arm": ImplicitActuatorCfg(
            joint_names_expr=[
                "shoulder_pan_joint",
                "shoulder_lift_joint",
                "elbow_joint",
                "wrist_1_joint",
                "wrist_2_joint",
                "wrist_3_joint",
            ],
            velocity_limit=1.57,
            effort_limit={
                "shoulder_pan_joint": 330.0,
                "shoulder_lift_joint": 330.0,
                "elbow_joint": 150.0,
                "wrist_1_joint": 54.0,
                "wrist_2_joint": 54.0,
                "wrist_3_joint": 54.0,
            },
            stiffness={
                "shoulder_pan_joint": 800.0,
                "shoulder_lift_joint": 800.0,
                "elbow_joint": 800.0,
                "wrist_1_joint": 800.0,
                "wrist_2_joint": 800.0,
                "wrist_3_joint": 800.0,
            },
            damping={
                "shoulder_pan_joint": 40.0,
                "shoulder_lift_joint": 40.0,
                "elbow_joint": 40.0,
                "wrist_1_joint": 40.0,
                "wrist_2_joint": 40.0,
                "wrist_3_joint": 40.0,
            },
        ),
        "gripper:": ImplicitActuatorCfg(
            joint_names_expr=["drive_joint"],
            effort_limit=5.0,
            velocity_limit=0.2,
            stiffness=20.0,
            damping=5.0,
        ),
    },
    soft_joint_pos_limit_factor=1.0,
)
"""Configuration of UR-10e arm with Robotiq 2f 85 using implicit actuator models."""


UR10E_ROBOTIQ_2F_140_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ISAACLAB_EXTENDED_ASSETS_DATA_DIR}/Robots/USD/UniversalRobots/ur10e_robotiq_2f_140/ur10e_robotiq_2f_140.usd",
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
            "shoulder_pan_joint": 0.0,
            "shoulder_lift_joint": -1.712,
            "elbow_joint": 1.712,
            "wrist_1_joint": -1.57,
            "wrist_2_joint": -1.57,
            "wrist_3_joint": 0.0,
            "drive_joint": 0.0,
        },
    ),
    actuators={
        "arm": ImplicitActuatorCfg(
            joint_names_expr=[
                "shoulder_pan_joint",
                "shoulder_lift_joint",
                "elbow_joint",
                "wrist_1_joint",
                "wrist_2_joint",
                "wrist_3_joint",
            ],
            velocity_limit=1.57,
            effort_limit={
                "shoulder_pan_joint": 330.0,
                "shoulder_lift_joint": 330.0,
                "elbow_joint": 150.0,
                "wrist_1_joint": 54.0,
                "wrist_2_joint": 54.0,
                "wrist_3_joint": 54.0,
            },
            stiffness={
                "shoulder_pan_joint": 800.0,
                "shoulder_lift_joint": 800.0,
                "elbow_joint": 800.0,
                "wrist_1_joint": 800.0,
                "wrist_2_joint": 800.0,
                "wrist_3_joint": 800.0,
            },
            damping={
                "shoulder_pan_joint": 40.0,
                "shoulder_lift_joint": 40.0,
                "elbow_joint": 40.0,
                "wrist_1_joint": 40.0,
                "wrist_2_joint": 40.0,
                "wrist_3_joint": 40.0,
            },
        ),
        "gripper:": ImplicitActuatorCfg(
            joint_names_expr=["drive_joint"],
            effort_limit=5.0,
            velocity_limit=0.2,
            stiffness=20.0,
            damping=5.0,
        ),
    },
    soft_joint_pos_limit_factor=1.0,
)
"""Configuration of UR-10e arm with Robotiq 2f 140 using implicit actuator models."""


FACTORY_UR10E_ROBOTIQ_2F_140_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ISAACLAB_EXTENDED_ASSETS_DATA_DIR}/Robots/USD/UniversalRobots/ur10e_robotiq_2f_140/ur10e_robotiq_2f_140.usd",
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
            "shoulder_pan_joint": 0.0,
            "shoulder_lift_joint": -1.712,
            "elbow_joint": 1.712,
            "wrist_1_joint": -1.57,
            "wrist_2_joint": -1.57,
            "wrist_3_joint": 0.0,
            "drive_joint": 0.0,
        },
    ),
    actuators={
        "arm": ImplicitActuatorCfg(
            joint_names_expr=[
                "shoulder_pan_joint",
                "shoulder_lift_joint",
                "elbow_joint",
                "wrist_1_joint",
                "wrist_2_joint",
                "wrist_3_joint",
            ],
            velocity_limit=1.57,
            effort_limit={
                "shoulder_pan_joint": 330.0,
                "shoulder_lift_joint": 330.0,
                "elbow_joint": 150.0,
                "wrist_1_joint": 54.0,
                "wrist_2_joint": 54.0,
                "wrist_3_joint": 54.0,
            },
            stiffness={
                "shoulder_pan_joint": 800.0,
                "shoulder_lift_joint": 800.0,
                "elbow_joint": 800.0,
                "wrist_1_joint": 800.0,
                "wrist_2_joint": 800.0,
                "wrist_3_joint": 800.0,
            },
            damping={
                "shoulder_pan_joint": 40.0,
                "shoulder_lift_joint": 40.0,
                "elbow_joint": 40.0,
                "wrist_1_joint": 40.0,
                "wrist_2_joint": 40.0,
                "wrist_3_joint": 40.0,
            },
        ),
        "gripper:": ImplicitActuatorCfg(
            joint_names_expr=["drive_joint"],
            effort_limit=5.0,
            velocity_limit=0.2,
            stiffness=20.0,
            damping=5.0,
        ),
    },
    soft_joint_pos_limit_factor=1.0,
)
"""Configuration of UR-10e arm with Robotiq 2f 140 using implicit actuator models for contact-rich tasks."""
