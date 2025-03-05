# Isaac Lab Extended Tasks: Environment Suite

Using the core framework developed as part of Isaac Lab, we provide various learning environments for robotics research.
These environments follow the `gym.Env` API from OpenAI Gym version `0.21.0`. The environments are registered using
the Gym registry.

Each environment's name is composed of `Isaac-<Task>-<Robot>-v<X>`, where `<Task>` indicates the skill to learn
in the environment, `<Robot>` indicates the embodiment of the acting agent, and `<X>` represents the version of
the environment (which can be used to suggest different observation or action spaces).

The environments are configured using either Python classes (wrapped using `configclass` decorator) or through
YAML files. The template structure of the environment is always put at the same level as the environment file
itself. However, its various instances are included in directories within the environment directory itself.
This looks like as follows:

```tree
isaaclab_extasks/assembly/
├── __init__.py
├── config
│   ├── franka
│   │   ├── agent  # <- this is where we store the learning agent configurations
│   │   ├── __init__.py  # <- this is where we register the environment and configurations to gym registry
│   │   └── franka_env_cfg.py
│   └── universal_robots
│       ├── agent  # <- this is where we store the learning agent configurations
│       ├── __init__.py  # <- this is where we register the environment and configurations to gym registry
│       └── ur10_env_cfg.py
├── mdp
│   ├── __init__.py
│   ├── observations.py
│   ├── rewards.py
│   └── terminations.py
├── __init__.py
└── assembly_env_cfg.py  # <- this is the base assembly task configuration
```

```tree
isaaclab_extasks/cooking/
├── __init__.py
├── config
│   ├── franka
│   │   ├── agent  # <- this is where we store the learning agent configurations
│   │   ├── __init__.py  # <- this is where we register the environment and configurations to gym registry
│   │   └── franka_env_cfg.py
│   └── universal_robots
│       ├── agent  # <- this is where we store the learning agent configurations
│       ├── __init__.py  # <- this is where we register the environment and configurations to gym registry
│       └── ur10_env_cfg.py
├── mdp
│   ├── __init__.py
│   ├── observations.py
│   ├── rewards.py
│   └── terminations.py
├── __init__.py
└── cooking_env_cfg.py  # <- this is the base cooking task configuration
```

The environments are then registered in the `isaaclab_extasks/assembly/config/franka/__init__.py`:

```python
gym.register(
    id="Isaac-Assembly-Franka-v0",
    entry_point="omni.isaac.lab.envs:RLTaskEnv",
    disable_env_checker=True,
    kwargs={"env_cfg_entry_point": f"{__name__}.rough_env_cfg:FrankaAssemblyEnvCfg"},
)

```

The environments are then registered in the `isaaclab_extasks/cooking/config/universal_robots/__init__.py`:

```
gym.register(
    id="Isaac-Cooking-UR10-v0",
    entry_point="omni.isaac.lab.envs:RLTaskEnv",
    disable_env_checker=True,
    kwargs={"env_cfg_entry_point": f"{__name__}.flat_env_cfg:UR10CookingEnvCfg"},
)
```

> **Note:** As a practice, we specify all the environments in a single file to avoid name conflicts between different
> tasks or environments. However, this practice is debatable and we are open to suggestions to deal with a large
> scaling in the number of tasks or environments.