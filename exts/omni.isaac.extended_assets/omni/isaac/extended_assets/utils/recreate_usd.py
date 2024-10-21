import argparse

from omni.isaac.lab.app import AppLauncher

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
from pxr import Sdf, Gf, UsdPhysics, UsdLux, PhysxSchema, Usd, UsdGeom
from omni.isaac.lab.utils.assets import check_file_path

def fix_stage(usd_path, instanceable=True):
    # Open instanceable usd stage
    stage = Usd.Stage.Open(usd_path)

    # Create an xform which should be set as the default prim
    default_prim = UsdGeom.Xform.Define(stage, Sdf.Path("/object")).GetPrim()

    # Make the xform the default prim
    stage.SetDefaultPrim(default_prim)
    
    new_object_prim = stage.GetPrimAtPath("/object/object")

    if not new_object_prim:
        return False

    UsdPhysics.RigidBodyAPI.Apply(new_object_prim)
    UsdPhysics.MassAPI.Apply(new_object_prim)

    new_object_prim.CreateAttribute('physics:density', Sdf.ValueTypeNames.Float, custom=False).Set(0.0)
    new_object_prim.CreateAttribute("xformOp:orient", Sdf.ValueTypeNames.Quatd).Set(Gf.Quatd(1.0, 0.0, 0.0, 0.0))
    new_object_prim.CreateAttribute("xformOp:scale", Sdf.ValueTypeNames.Double3).Set(Gf.Vec3d(1.0, 1.0, 1.0))
    new_object_prim.CreateAttribute("xformOp:translate", Sdf.ValueTypeNames.Double3).Set(Gf.Vec3d(0.0, 0.0, 0.0))        
    new_object_prim.CreateAttribute('xformOpOrder', Sdf.ValueTypeNames.TokenArray, custom=False).Set(["xformOp:transform"])
    new_object_prim.CreateAttribute("physics:angularVelocity", Sdf.ValueTypeNames.Vector3f).Set(Gf.Vec3f(0.0, 0.0, 0.0))
    new_object_prim.CreateAttribute("physics:kinematicEnabled", Sdf.ValueTypeNames.Bool).Set(True)
    new_object_prim.CreateAttribute("physics:mass", Sdf.ValueTypeNames.Float).Set(10.0)
    new_object_prim.CreateAttribute("physics:rigidBodyEnabled", Sdf.ValueTypeNames.Bool).Set(True)
    new_object_prim.CreateAttribute("physxRigidBody:maxLinearVelocity", Sdf.ValueTypeNames.Float).Set(1000.0)
    new_object_prim.CreateAttribute("ui:displayGroup", Sdf.ValueTypeNames.Token).Set("Material Graphs")
    new_object_prim.CreateAttribute("ui:displayName", Sdf.ValueTypeNames.Token).Set("object")
    new_object_prim.CreateAttribute("ui:order", Sdf.ValueTypeNames.Int).Set(1024)

    visuals_path = "/object/object/visuals"
    visuals_prim = stage.DefinePrim(Sdf.Path(visuals_path), "Xform")
    if instanceable:
        visuals_prim.GetReferences().AddReference('./Props/instanceable_meshes.usd', '/object_visuals')
        visuals_prim.CreateAttribute("instanceable", Sdf.ValueTypeNames.Bool).Set(True)
        visuals_prim.CreateAttribute("references", Sdf.ValueTypeNames.Asset).Set(Sdf.AssetPath('./Props/instanceable_meshes.usd</object_visuals>'))

    collisions_path = "/object/object/collisions"
    collisions_prim = stage.DefinePrim(Sdf.Path(collisions_path), "Xform")
    if instanceable:
        collisions_prim.GetReferences().AddReference('./Props/instanceable_meshes.usd', '/object_collisions')
        collisions_prim.CreateAttribute("instanceable", Sdf.ValueTypeNames.Bool).Set(True)
        collisions_prim.CreateAttribute("references", Sdf.ValueTypeNames.Asset).Set(Sdf.AssetPath('./Props/instanceable_meshes.usd</object_collisions>'))

    stage.RemovePrim(Sdf.Path("/worldBody"))

    # Save usd
    # print(stage.GetRootLayer().ExportToString())
    stage.GetRootLayer().Save()
    return True


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

        # get instanceable usd path
        instanceable_usd_path = os.path.join(os.path.dirname(usd_path), "Props/instanceable_meshes.usd")

        fix_stage(usd_path, instanceable=True)
        # fix_stage(instanceable_usd_path, instanceable=False)

        print(f"[INFO] Usd path is {usd_path}")
        print("[INFO] Modification complete!")
    
    simulation_app.close()
    

if __name__ == "__main__":
    main()