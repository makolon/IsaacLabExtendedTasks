import gymnasium as gym

from . import agents, ur5e_env_cfg, ur10e_env_cfg

gym.register(
    id="Isaac-Block-Sort-UR5e-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": ur5e_env_cfg.UR5eSortEnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:SortPPORunnerCfg",
    },
    disable_env_checker=True,
)


gym.register(
    id="Isaac-Block-Sort-UR10e-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": ur10e_env_cfg.UR10eSortEnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:SortPPORunnerCfg",
    },
    disable_env_checker=True,
)
