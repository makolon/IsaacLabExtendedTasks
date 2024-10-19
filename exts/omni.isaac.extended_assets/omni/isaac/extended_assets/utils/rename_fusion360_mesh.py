import argparse
import os

# add argparse arguments
parser = argparse.ArgumentParser(
    description="Utility to convert a mesh file into USD format."
)
parser.add_argument(
    "input", type=str, nargs="+", help="The path to the input mesh file."
)
# parse the arguments
args_cli = parser.parse_args()

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
        # Create destination directory under "Props" directory
        root_dir = os.path.dirname(mesh_path)
        body_name = os.path.basename(mesh_path)

        if body_name == "0.obj":
            old_path = os.path.join(root_dir, body_name)
            new_path = os.path.join(root_dir, "model_0.obj")
            # Rename
            os.rename(old_path, new_path)
            print(f"Renamed: {old_path} -> {new_path}")
        elif body_name == "1.obj":
            old_path = os.path.join(root_dir, body_name)
            new_path = os.path.join(root_dir, "model_1.obj")
            # Rename
            os.rename(old_path, new_path)
            print(f"Renamed: {old_path} -> {new_path}")


if __name__ == "__main__":
    # run the main function
    main()
