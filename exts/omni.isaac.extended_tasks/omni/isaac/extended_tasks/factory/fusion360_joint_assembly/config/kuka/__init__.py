import gymnasium as gym

from . import agents, lbr_iiwa7_env_cfg

gym.register(
    id="Isaac-Assembly-LBRIIWA7-v0",
    entry_point="omni.isaac.lab.envs:ManagerBasedRLEnv",
    kwargs={
        "env_cfg_entry_point": lbr_iiwa7_env_cfg.LBRIIWA7AssemblyEnvCfg,
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:AssemblyPPORunnerCfg",
    },
    disable_env_checker=True,
)
