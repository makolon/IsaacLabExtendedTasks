import gymnasium as gym

from . import agents, gen3n7_env_cfg, jaco7n_env_cfg, jaco7s_env_cfg

gym.register(
    id="Isaac-Block-Stack-Gen3n7-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": gen3n7_env_cfg.Gen3N7StackEnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:StackPPORunnerCfg",
    },
    disable_env_checker=True,
)

gym.register(
    id="Isaac-Block-Stack-Jaco7N-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": jaco7n_env_cfg.Jaco7NStackEnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:StackPPORunnerCfg",
    },
    disable_env_checker=True,
)

gym.register(
    id="Isaac-Block-Stack-Jaco7S-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": jaco7s_env_cfg.Jaco7SStackEnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:StackPPORunnerCfg",
    },
    disable_env_checker=True,
)
