import gymnasium as gym

from . import agents, ur5e_env_cfg, ur10e_env_cfg

gym.register(
    id="Isaac-Cooking-UR5e-v0",
    entry_point="omni.isaac.lab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": ur5e_env_cfg.UR5eCookingEnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:CookingPPORunnerCfg",
    },
    disable_env_checker=True,
)

gym.register(
    id="Isaac-Cooking-UR10e-v0",
    entry_point="omni.isaac.lab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": ur10e_env_cfg.UR10eCookingEnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:CookingPPORunnerCfg",
    },
    disable_env_checker=True,
)
