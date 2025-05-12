"""Launch Isaac Sim Simulator first."""

import argparse

from isaaclab.app import AppLauncher

# add argparse arguments
parser = argparse.ArgumentParser(
    description="Utility to convert a MJCF into USD format."
)
parser.add_argument("input_urdf", type=str, nargs="+", help="Paths to the input URDF files.")
parser.add_argument("input_meta", type=str, nargs="+", help="Paths to the input json files.")
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

import re
import os
import json

from collections import defaultdict
from isaaclab.sim.converters import UrdfConverter, UrdfConverterCfg
from isaaclab.utils.assets import check_file_path
from isaaclab.utils.dict import print_dict

# Conveniences to other module directories via relative paths
ISAACLAB_EXTENDED_ASSETS_DATA_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../../", "data")
)


def extract_meta_number(path):
    match = re.search(r'/(\d+)/result\.json$', path)
    return int(match.group(1)) if match else float('inf')


def extract_urdf_number(path):
    match = re.search(r'(\d+)', path)
    return int(match.group(1)) if match else None


def extract_number_from_path(path):
    match = re.search(r'(\d+)', path)
    return int(match.group(1)) if match else None


def get_category_list(meta_paths):
    category_list = []
    for meta_path in meta_paths:
        if not os.path.isabs(meta_path):
            meta_path = os.path.abspath(meta_path)
        with open(meta_path, "r") as f:
            data = json.load(f)
            category_list.append(data[0]["text"])

    unique_categories = defaultdict(int)
    renamed_list = []

    for category in category_list:
        cleaned_category = category.replace(" ", "")
        unique_categories[cleaned_category] += 1
        renamed_category = f"{cleaned_category}{unique_categories[cleaned_category]}"
        renamed_list.append(renamed_category)

    return renamed_list


def main():
    # check valid file path
    urdf_paths = args_cli.input_urdf[0].splitlines()
    meta_paths = args_cli.input_meta[0].splitlines()

    if urdf_paths is None:
        raise ValueError("URDF paths do not exist.")
    else:
        print("URDF paths:", urdf_paths)

    if meta_paths is None:
        raise ValueError("Meta paths do not exist.")
    else:
        print("Meta paths:", meta_paths)

    urdf_paths = sorted(urdf_paths, key=extract_urdf_number)
    meta_paths = sorted(meta_paths, key=extract_meta_number)
    urdf_numbers = [extract_number_from_path(path) for path in urdf_paths]
    meta_numbers = [extract_number_from_path(path) for path in meta_paths]

    unmatched_paths = []
    for i, (urdf_num, meta_num) in enumerate(zip(urdf_numbers, meta_numbers)):
        if urdf_num != meta_num:
            unmatched_paths.append((urdf_paths[i], meta_paths[i]))

    if unmatched_paths:
        print("Unmatched paths found:")
        for urdf_path, meta_path in unmatched_paths:
            print(f"URDF: {urdf_path}  | Meta: {meta_path}")
    else:
        print("All paths match.")

    category_lists = get_category_list(meta_paths)
    for urdf_path, category_list in zip(urdf_paths, category_lists):
        if not os.path.isabs(urdf_path):
            urdf_path = os.path.abspath(urdf_path)
        if not check_file_path(urdf_path):
            raise ValueError(f"Invalid file path: {urdf_path}")

        # Create destination directory under "Props" directory
        usd_dir = os.path.join(
            ISAACLAB_EXTENDED_ASSETS_DATA_DIR, "Props", "USD", "gapartnet", category_list
        )
        os.makedirs(usd_dir, exist_ok=True)

        # Define USD file name based on directory name
        usd_file_name = f"{category_list}.usd"

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
