import gymnasium as gym

from . import agents, franka_env_cfg

gym.register(
    id="Isaac-Block-Sort-Franka-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": franka_env_cfg.FrankaSortEnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:SortPPORunnerCfg",
    },
    disable_env_checker=True,
)
