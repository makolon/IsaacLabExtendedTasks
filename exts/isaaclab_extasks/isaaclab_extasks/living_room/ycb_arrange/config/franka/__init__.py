import gymnasium as gym

from . import agents, franka_env_cfg

gym.register(
    id="Isaac-LivingRoom-YCB-Arrange-Franka-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": franka_env_cfg.FrankaYCBArrangeEnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:ArrangePPORunnerCfg",
    },
    disable_env_checker=True,
)
