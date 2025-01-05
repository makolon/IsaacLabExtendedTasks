import gymnasium as gym

from . import agents, franka_env_cfg

gym.register(
    id="Isaac-Siemens-Gearbox-Assembly-Franka-v0",
    entry_point="omni.isaac.lab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": franka_env_cfg.FrankaAssemblyEnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:AssemblyPPORunnerCfg",
    },
    disable_env_checker=True,
)
