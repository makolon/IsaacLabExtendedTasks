"""Launch Isaac Sim Simulator first."""

import argparse

from omni.isaac.lab.app import AppLauncher

# add argparse arguments
parser = argparse.ArgumentParser(
    description="Utility to convert a MJCF into USD format."
)
parser.add_argument("input", type=str, nargs="+", help="Paths to the input MJCF files.")
parser.add_argument(
    "--fix-base",
    action="store_true",
    default=False,
    help="Fix the base to where it is imported.",
)
parser.add_argument(
    "--merge-joints",
    action="store_true",
    default=False,
    help="Consolidate links that are connected by fixed joints.",
)
parser.add_argument(
    "--make-instanceable",
    action="store_true",
    default=False,
    help="Make the asset instanceable for efficient cloning.",
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

from omni.isaac.lab.sim.converters import UrdfConverter, UrdfConverterCfg
from omni.isaac.lab.utils.assets import check_file_path
from omni.isaac.lab.utils.dict import print_dict

# Conveniences to other module directories via relative paths
ISAACLAB_EXTENDED_ASSETS_DATA_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../../", "data")
)


def main():
    # check valid file path
    urdf_paths = args_cli.input
    if urdf_paths is None:
        raise ValueError("URDF paths does not exist.")
    else:
        print("URDF paths:", urdf_paths)

    for urdf_path in urdf_paths:
        if not os.path.isabs(urdf_path):
            urdf_path = os.path.abspath(urdf_path)
        if not check_file_path(urdf_path):
            raise ValueError(f"Invalid file path: {urdf_path}")

        # Create destination directory under "Props" directory
        base_name = os.path.basename(os.path.dirname(urdf_path))
        usd_dir = os.path.join(
            ISAACLAB_EXTENDED_ASSETS_DATA_DIR, "Props", "USD", "gapartnet", base_name
        )
        os.makedirs(usd_dir, exist_ok=True)

        # Define USD file name based on directory name
        usd_file_name = f"{base_name}.usd"

        print("USD directory:", usd_dir)
        print("USD file name:", usd_file_name)

        # create the converter configuration
        urdf_converter_cfg = UrdfConverterCfg(
            asset_path=urdf_path,
            usd_dir=usd_dir,
            usd_file_name=usd_file_name,
            fix_base=args_cli.fix_base,
            merge_fixed_joints=args_cli.merge_joints,
            force_usd_conversion=True,
            make_instanceable=args_cli.make_instanceable,
        )

        # Print info
        print("-" * 80)
        print("-" * 80)
        print(f"Input URDF file: {urdf_path}")
        print("URDF importer config:")
        print_dict(urdf_converter_cfg.to_dict(), nesting=0)
        print("-" * 80)
        print("-" * 80)

        # Create urdf converter and import the file
        urdf_converter = UrdfConverter(urdf_converter_cfg)
        # print output
        print("URDF importer output:")
        print(f"Generated USD file: {urdf_converter.usd_path}")
        print("-" * 80)
        print("-" * 80)


if __name__ == "__main__":
    # run the main function
    main()
    # close sim app
    simulation_app.close()
