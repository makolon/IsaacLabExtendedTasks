import gymnasium as gym

from . import agents, gen3n7_env_cfg, jaco7n_env_cfg, jaco7s_env_cfg

gym.register(
    id="Isaac-Sorting-Gen3n7-v0",
    entry_point="omni.isaac.lab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": gen3n7_env_cfg.Gen3N7SortingEnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:SortingPPORunnerCfg",
    },
    disable_env_checker=True,
)

gym.register(
    id="Isaac-Sorting-Jaco7N-v0",
    entry_point="omni.isaac.lab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": jaco7n_env_cfg.Jaco7NSortingEnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:SortingPPORunnerCfg",
    },
    disable_env_checker=True,
)

gym.register(
    id="Isaac-Sorting-Jaco7S-v0",
    entry_point="omni.isaac.lab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": jaco7s_env_cfg.Jaco7SSortingEnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:SortingPPORunnerCfg",
    },
    disable_env_checker=True,
)
