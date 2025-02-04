import argparse

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description="Utility to convert a mesh file into USD format.")
parser.add_argument("input", type=str, nargs="+", help="The path to the input mesh file.")
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

"""Rest everything follows."""
import os
import omni
import omni.usd
import omni.kit.commands
import omni.kit.app as app
from pxr import Sdf, UsdShade, Usd, UsdGeom
from isaaclab.utils.assets import check_file_path


def main():
    # check valid file path
    usd_paths = args_cli.input
    if usd_paths is None:
        raise ValueError("USD paths does not exist.")
    else:
        print("USD paths:", usd_paths)

    for usd_path in usd_paths:
        if not os.path.isabs(usd_path):
            usd_path = os.path.abspath(usd_path)
        if not check_file_path(usd_path):
            raise ValueError(f"Invalid usd file path: {usd_path}")

        # Extract model_name from usd_path
        model_name = os.path.basename(os.path.dirname(usd_path))

        # Open usd stage
        stage = Usd.Stage.Open(usd_path)

        # Create a material.
        material_path = Sdf.Path("/World/material")
        material = UsdShade.Material.Define(stage, material_path)

        # Create a shader for the material.
        shader = UsdShade.Shader.Define(stage, material_path.AppendChild('PBRShader'))
        shader.CreateIdAttr('UsdPreviewSurface')

        # Create an input for the diffuse color.
        diffuse_color_input = shader.CreateInput('diffuseColor', Sdf.ValueTypeNames.Color3f)

        # Create a texture for the diffuse color.
        texture_path = material_path.AppendChild('diffuseTexture')
        texture = UsdShade.Shader.Define(stage, texture_path)
        texture.CreateIdAttr('UsdUVTexture')

        # Set the file path of the texture.
        texture.CreateInput('file', Sdf.ValueTypeNames.Asset).Set('path/to/your/texture.png')

        # Connect the texture to the diffuse color input.
        texture.CreateOutput('rgb', Sdf.ValueTypeNames.Float3).ConnectToSource(diffuse_color_input)

        # Open instanceable usd stage
        instanceable_usd_path = os.path.join(os.path.dirname(usd_path), "Props/instanceable_meshes.usd")  # TODO: Fix here
        refstage = Usd.Stage.Open(instanceable_usd_path)

        mesh_prim = refstage.GetPrimAtPath(f"/{model_name}/geometry/mesh")  # TODO: Fix here

        # Check if the prim is valid and is a Mesh
        if mesh_prim and mesh_prim.IsA(UsdGeom.Mesh):
            mesh = UsdGeom.Mesh(mesh_prim)
            print("Mesh Prim Retrieved Successfully")
        else:
            print("Mesh Prim not found or not a Mesh")

        # Bind the material to the mesh.
        UsdShade.MaterialBindingAPI(mesh).Bind(material)

        # Connecting Material to Shader.
        mdlOutput = material.CreateSurfaceOutput("mdl")
        mdlOutput.ConnectToSource(shader.ConnectableAPI(), "out")

        # Save usd
        refstage.GetRootLayer().Save()
        
        print(f"[INFO] Usd path is {usd_path}")
        print("[INFO] Pivotting is done!")

    simulation_app.close()
    

if __name__ == "__main__":
    main()