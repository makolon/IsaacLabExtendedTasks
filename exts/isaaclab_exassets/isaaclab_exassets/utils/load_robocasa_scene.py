import argparse

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description="Utility to convert a mesh file into USD format.")
parser.add_argument("--input", type=str, default="env_config.json", help="The path to the input mesh file.")
parser.add_argument("--task", type=str, default="PnPCounterToCab", help="task")
parser.add_argument("--layout", type=int, help="kitchen layout (choose number 0-9)")
parser.add_argument("--style", type=int, help="kitchen style (choose number 0-11)")
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

"""Rest everything follows."""
import os
import json
import torch
import numpy as np
import isaacsim.core.utils.prims as prim_utils
import isaaclab.sim as sim_utils
from isaaclab.assets import AssetBase, ArticulationCfg, AssetBaseCfg, RigidObjectCfg, RigidObject
from isaaclab.sim import SimulationContext
from pxr import Sdf, UsdShade, Usd, UsdGeom
ISAACLAB_EXTENDED_ASSETS_DATA_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../../", "data")
)


class SceneBuilder:
    def __init__(self, config_path):
        with open(config_path, "rb") as f:
            config = json.load(f)

        self.others, self.fixtures = config["others"], config["fixture"]

    def design_scene(self):
        """Designs the scene."""
        prim_utils.create_prim(f"/World/Kitchen", "Xform", translation=[0.0, 0.0, 0.0])

        # Initialize scene entities
        scene_entities = {}

        # Fixture
        for fixture in self.fixtures:
            name = fixture["name"]
            type = fixture["type"]
            position = fixture["position"]
            rotation = fixture["rotation"]
            size = fixture["size"]
            path = fixture["path"]
            if path is None:
                continue

            if f"{path.split('/')[-1]}" == "model.xml":
                file_name = f"{path.split('/')[-2]}.usd"
            else:
                obj_name = path.split('/')[-1].split('.')[0]
                file_name = f"{obj_name}/{obj_name}.usd"
            usd_path = os.path.join(
                ISAACLAB_EXTENDED_ASSETS_DATA_DIR,
                "Props/USD/objaverse",
                os.path.dirname(path),
                file_name
            )
            print("[INFO]: USD Path:", usd_path)

            # Fixed object
            if type == "fixed":
                rigid_cfg = RigidObjectCfg(
                    prim_path=f"/World/Kitchen/{name}",
                    spawn=sim_utils.UsdFileCfg(
                        usd_path=usd_path,
                        scale=size,
                        rigid_props=sim_utils.RigidBodyPropertiesCfg(
                            kinematic_enabled=True,
                            disable_gravity=True,
                            enable_gyroscopic_forces=True,
                            solver_position_iteration_count=8,
                            solver_velocity_iteration_count=0,
                            sleep_threshold=0.005,
                            stabilization_threshold=0.0025,
                            max_depenetration_velocity=1000.0,
                        ),
                        mass_props=sim_utils.MassPropertiesCfg(density=1000.0),
                    ),
                    init_state=RigidObjectCfg.InitialStateCfg(pos=position, rot=rotation),
                )
                fixed_asset = RigidObject(cfg=rigid_cfg)
                scene_entities[name] = fixed_asset

            # Articulated object
            elif type == "articulation":
                articulated_asset = ArticulationCfg(
                    prim_path=f"/World/Kitchen/{name}",
                    spawn=sim_utils.UsdFileCfg(
                        usd_path=usd_path,
                        scale=size,
                        activate_contact_sensors=False,
                    ),
                    init_state=ArticulationCfg.InitialStateCfg(
                        pos=position,
                        rot=rotation,
                    ),
                )
                scene_entities[name] = articulated_asset

        return scene_entities
    
    def save_scene(self):
        pass


def main():
    """Main function."""
    # Load kit helper
    sim_cfg = sim_utils.SimulationCfg(device=args_cli.device)
    sim = SimulationContext(sim_cfg)
    # Set main camera
    sim.set_camera_view(eye=[1.5, 0.0, 1.0], target=[0.0, 0.0, 0.0])
    # Scene buidler
    scene_builder = SceneBuilder(args_cli.input)
    # Design scene
    scene_entities = scene_builder.design_scene()
    # Play the simulator
    sim.reset()
    # Now we are ready!
    print("[INFO]: Setup complete...")

    while simulation_app.is_running():
        # perform step
        sim.step()

    # Save scene
    scene_builder.save_scene()


if __name__ == "__main__":
    main()