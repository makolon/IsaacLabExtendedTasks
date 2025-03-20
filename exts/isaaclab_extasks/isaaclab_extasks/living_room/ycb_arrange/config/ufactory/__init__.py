import gymnasium as gym

from . import agents, xarm7_env_cfg

gym.register(
    id="Isaac-LivingRoom-YCB-Arrange-XArm7-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": xarm7_env_cfg.XArm7YCBArrangeEnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:ArrangePPORunnerCfg",
    },
    disable_env_checker=True,
)
