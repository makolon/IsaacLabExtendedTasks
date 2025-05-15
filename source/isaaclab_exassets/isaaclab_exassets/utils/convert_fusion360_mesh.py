import argparse

from isaaclab.app import AppLauncher

# add argparse arguments
parser = argparse.ArgumentParser(
    description="Utility to convert a mesh file into USD format."
)
parser.add_argument(
    "input", type=str, nargs="+", help="The path to the input mesh file."
)
parser.add_argument(
    "--make-instanceable",
    action="store_true",
    default=False,
    help="Make the asset instanceable for efficient cloning.",
)
parser.add_argument(
    "--collision-approximation",
    type=str,
    default="meshSimplification",
    choices=["convexDecomposition", "convexHull", "meshSimplification", "none"],
    help=(
        'The method used for approximating collision mesh. Set to "none" '
        "to not add a collision mesh to the converted mesh."
    ),
)
parser.add_argument(
    "--mass",
    type=float,
    default=None,
    help="The mass (in kg) to assign to the converted asset. If not provided, then no mass is added.",
)
# append AppLauncher cli args
AppLauncher.add_app_launcher_args(parser)
# parse the arguments
args_cli = parser.parse_args()

# launch omniverse app
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

"""Rest everything follows."""

import os

from isaaclab.sim.converters import MeshConverter, MeshConverterCfg
from isaaclab.sim.schemas import schemas_cfg
from isaaclab.utils.assets import check_file_path
from isaaclab.utils.dict import print_dict

# Conveniences to other module directories via relative paths
ISAACLAB_EXTENDED_ASSETS_DATA_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../../", "data")
)


def main():
    # check valid file path
    mesh_paths = args_cli.input
    if mesh_paths is None:
        raise ValueError("Mesh paths does not exist.")
    else:
        print("Mesh paths:", mesh_paths)

    for mesh_path in mesh_paths:
        if not os.path.isabs(mesh_path):
            mesh_path = os.path.abspath(mesh_path)
        if not check_file_path(mesh_path):
            raise ValueError(f"Invalid mesh file path: {mesh_path}")

        # Create destination directory under "Props" directory
        body_type = os.path.basename(os.path.dirname(mesh_path))
        body_name = os.path.basename(mesh_path).split(".")[0]
        usd_dir = os.path.join(
            ISAACLAB_EXTENDED_ASSETS_DATA_DIR,
            "Props",
            "USD",
            "fusion360",
            body_type,
            body_name,
        )
        os.makedirs(usd_dir, exist_ok=True)

        # Define USD file name based on directory name
        usd_file_name = f"{body_name}.usd"

        print("USD directory:", usd_dir)
        print("USD file name:", usd_file_name)

        # Mass properties
        if args_cli.mass is not None:
            mass_props = schemas_cfg.MassPropertiesCfg(mass=args_cli.mass)
            rigid_props = schemas_cfg.RigidBodyPropertiesCfg()
        else:
            mass_props = None
            rigid_props = None

        # Collision properties
        collision_props = schemas_cfg.CollisionPropertiesCfg(
            collision_enabled=args_cli.collision_approximation != "none"
        )

        # Create Mesh converter config
        mesh_converter_cfg = MeshConverterCfg(
            mass_props=mass_props,
            rigid_props=rigid_props,
            collision_props=collision_props,
            asset_path=mesh_path,
            force_usd_conversion=True,
            usd_dir=usd_dir,
            usd_file_name=usd_file_name,
            make_instanceable=args_cli.make_instanceable,
            collision_approximation=args_cli.collision_approximation,
        )

        # Print info
        print("-" * 80)
        print("-" * 80)
        print(f"Input Mesh file: {mesh_path}")
        print("Mesh importer config:")
        print_dict(mesh_converter_cfg.to_dict(), nesting=0)
        print("-" * 80)
        print("-" * 80)

        # Create Mesh converter and import the file
        mesh_converter = MeshConverter(mesh_converter_cfg)
        # print output
        print("Mesh importer output:")
        print(f"Generated USD file: {mesh_converter.usd_path}")
        print("-" * 80)
        print("-" * 80)


if __name__ == "__main__":
    # run the main function
    main()
    # close sim app
    simulation_app.close()
