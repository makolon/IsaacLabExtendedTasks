import gymnasium as gym

from . import agents, gen3n7_env_cfg

gym.register(
    id="Isaac-Cooking-Gen3n7-v0",
    entry_point="omni.isaac.lab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": gen3n7_env_cfg.Gen3N7CookingEnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:CookingPPORunnerCfg",
    },
    disable_env_checker=True,
)
