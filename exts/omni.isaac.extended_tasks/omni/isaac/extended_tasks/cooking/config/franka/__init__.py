import gymnasium as gym

from . import agents, franka_env_cfg

gym.register(
    id="Isaac-Cooking-Franka-v0",
    entry_point="omni.isaac.lab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": franka_env_cfg.FrankaCookingEnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:CookingPPORunnerCfg",
    },
    disable_env_checker=True,
)
