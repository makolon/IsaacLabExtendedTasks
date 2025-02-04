"""Launch Isaac Sim Simulator first."""

import argparse

from isaaclab.app import AppLauncher

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
    "--import-sites",
    action="store_true",
    default=False,
    help="Import sites by parsing the <site> tag.",
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

from isaaclab.sim.converters import MjcfConverter, MjcfConverterCfg
from isaaclab.utils.assets import check_file_path
from isaaclab.utils.dict import print_dict

# Conveniences to other module directories via relative paths
ISAACLAB_EXTENDED_ASSETS_DATA_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../../", "data")
)


def main():
    # check valid file path
    mjcf_paths = args_cli.input
    if mjcf_paths is None:
        raise ValueError("MJCF paths does not exist.")
    else:
        print("MJCF paths:", mjcf_paths)

    for mjcf_path in mjcf_paths:
        if not os.path.isabs(mjcf_path):
            mjcf_path = os.path.abspath(mjcf_path)
        if not check_file_path(mjcf_path):
            raise ValueError(f"Invalid file path: {mjcf_path}")

        # Create destination directory under "Props" directory
        base_name = os.path.basename(os.path.dirname(mjcf_path))
        usd_dir = os.path.join(
            ISAACLAB_EXTENDED_ASSETS_DATA_DIR, "Props", "USD", base_name
        )
        os.makedirs(usd_dir, exist_ok=True)

        # Define USD file name based on directory name
        usd_file_name = f"{base_name}.usd"

        print("USD directory:", usd_dir)
        print("USD file name:", usd_file_name)

        # create the converter configuration
        mjcf_converter_cfg = MjcfConverterCfg(
            asset_path=mjcf_path,
            usd_dir=usd_dir,
            usd_file_name=usd_file_name,
            fix_base=args_cli.fix_base,
            import_sites=args_cli.import_sites,
            force_usd_conversion=True,
            make_instanceable=args_cli.make_instanceable,
        )

        # Print info
        print("-" * 80)
        print("-" * 80)
        print(f"Input MJCF file: {mjcf_path}")
        print("MJCF importer config:")
        print_dict(mjcf_converter_cfg.to_dict(), nesting=0)
        print("-" * 80)
        print("-" * 80)

        # Create mjcf converter and import the file
        mjcf_converter = MjcfConverter(mjcf_converter_cfg)
        # print output
        print("MJCF importer output:")
        print(f"Generated USD file: {mjcf_converter.usd_path}")
        print("-" * 80)
        print("-" * 80)


if __name__ == "__main__":
    # run the main function
    main()
    # close sim app
    simulation_app.close()
