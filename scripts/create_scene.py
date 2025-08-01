import argparse

from isaaclab.app import AppLauncher

# Add argparse arguments
parser = argparse.ArgumentParser(
    description="Sample code for demonstrating IsaacLabExtendedTasks."
)
parser.add_argument("--task", type=str, default=None, help="Name of the task.")
parser.add_argument("--robot_name", type=str, default="robot", help="Name of the robot.")
parser.add_argument(
    "--num_envs", type=int, default=1, help="Number of environments to spawn."
)
# Append AppLauncher cli args
AppLauncher.add_app_launcher_args(parser)
# Parse the arguments
args_cli = parser.parse_args()

# Launch omniverse app
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

"""Rest everything follows."""

import gymnasium as gym
import isaaclab_exassets  # noqa: F401
import isaaclab_extasks  # noqa: F401
import torch
from isaaclab_tasks.utils import parse_env_cfg


def main():
    """Main function."""
    # Create environment configuration
    env_cfg = parse_env_cfg(
        task_name=args_cli.task, device=args_cli.device, num_envs=args_cli.num_envs
    )
    env = gym.make(args_cli.task, cfg=env_cfg)

    # print info (this is vectorized environment)
    print(f"[INFO]: Gym observation space: {env.observation_space}")
    print(f"[INFO]: Gym action space: {env.action_space}")

    # Reset environment
    env.reset()

    # Simulate physics
    count = 0
    while simulation_app.is_running():
        with torch.inference_mode():
            # Reset
            if count % 300 == 0:
                count = 0
                env.reset()
                print("-" * 80)
                print("[INFO]: Resetting environment...")
            # Sample random actions
            actions = torch.tensor(
                list(env.unwrapped.scene[args_cli.robot_name].cfg.init_state.joint_pos.values()),
                dtype=torch.float32,
                device=args_cli.device,
            ).unsqueeze(0)
            print("[INFO]: Actions: ", actions)
            # Step the environment
            obs, rew, terminated, truncated, info = env.step(actions)
            # Update counter
            count += 1

    # Close the environment
    env.close()


if __name__ == "__main__":
    # run the main function
    main()
    # Close sim app
    simulation_app.close()
