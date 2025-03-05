import gymnasium as gym

from . import agents, ur5e_env_cfg, ur10e_env_cfg

gym.register(
    id="Isaac-Block-Stack-UR5e-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": ur5e_env_cfg.UR5eStackEnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:StackPPORunnerCfg",
    },
    disable_env_checker=True,
)


gym.register(
    id="Isaac-Block-Stack-UR10e-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": ur10e_env_cfg.UR10eStackEnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:StackPPORunnerCfg",
    },
    disable_env_checker=True,
)
