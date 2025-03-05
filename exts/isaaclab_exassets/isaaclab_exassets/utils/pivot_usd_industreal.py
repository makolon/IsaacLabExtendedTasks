import argparse

from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser(description="Utility to convert a mesh file into USD format.")
parser.add_argument("input", type=str, nargs="+", help="The path to the input mesh file.")
parser.add_argument("--print_stage", action="store_true", help="Whether print out the stage.")
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
from isaaclab.utils.assets import check_file_path


def main():
    # check valid file path
    usd_paths = args_cli.input
    if usd_paths is None:
        raise ValueError("USD paths does not exist.")
    else:
        print("USD paths:", usd_paths)

    # enable immediately
    manager = omni.kit.app.get_app().get_extension_manager()
    manager.set_extension_enabled_immediate("omni.tools.pivot", True)

    for usd_path in usd_paths:
        if not os.path.isabs(usd_path):
            usd_path = os.path.abspath(usd_path)
        if not check_file_path(usd_path):
            raise ValueError(f"Invalid usd file path: {usd_path}")

        model_name = os.path.basename(os.path.dirname(usd_path))
        print("model_name:", model_name)

        # Open original usd stage
        omni.kit.commands.execute("PivotToolAddPivot", prim_paths=[f"/{model_name}/{model_name}"])
        omni.kit.commands.execute("PivotToolSetPivotToBoundingBoxCenter", prim_paths=[f"/{model_name}/{model_name}"])

        # Open instanceable usd stage
        stage = Usd.Stage.Open(usd_path)

        collision_mesh_prim = stage.GetPrimAtPath(f"/{model_name}/{model_name}/collisions")
        visual_mesh_prim = stage.GetPrimAtPath(f"/{model_name}/{model_name}/visuals")

        # Check if the prim is valid and is a Mesh
        if collision_mesh_prim and collision_mesh_prim.IsA(UsdGeom.Mesh):
            collision_mesh = UsdGeom.Mesh(collision_mesh_prim)
            print("Mesh Prim Retrieved Successfully")
        else:
            print("Mesh Prim not found or not a Mesh")
        # Check if the prim is valid and is a Mesh
        if visual_mesh_prim and visual_mesh_prim.IsA(UsdGeom.Mesh):
            visual_mesh = UsdGeom.Mesh(visual_mesh_prim)
            print("Mesh Prim Retrieved Successfully")
        else:
            print("Mesh Prim not found or not a Mesh")

        # Get extent
        extent = collision_mesh.GetExtentAttr().Get()
        center_x = -(extent[0][0] + extent[1][0]) / 2
        center_y = -(extent[0][1] + extent[1][1]) / 2
        center_z = -(extent[0][2] + extent[1][2]) / 2
        center = Gf.Vec3f(center_x, center_y, center_z)

        # Get extent
        extent = visual_mesh.GetExtentAttr().Get()
        center_x = -(extent[0][0] + extent[1][0]) / 2
        center_y = -(extent[0][1] + extent[1][1]) / 2
        center_z = -(extent[0][2] + extent[1][2]) / 2
        center = Gf.Vec3f(center_x, center_y, center_z)

        # Add Xform pivot
        translate_op = None
        for op in collision_mesh.GetOrderedXformOps():
            if op.GetOpName() == "xformOp:translate":
                translate_op = op
                break
        if translate_op:
            translate_op.Set(value=(center))
        else:
            collision_mesh.AddTranslateOp().Set(value=(center))

        # Add Xform pivot
        translate_op = None
        for op in visual_mesh.GetOrderedXformOps():
            if op.GetOpName() == "xformOp:translate":
                translate_op = op
                break
        if translate_op:
            translate_op.Set(value=(center))
        else:
            visual_mesh.AddTranslateOp().Set(value=(center))

        if args_cli.print_stage:
            print(stage.ExportToString())

        # Save usd
        stage.GetRootLayer().Save()
        
        print(f"[INFO] Usd path is {usd_path}")
        print("[INFO] Pivotting is done!")
    
    simulation_app.close()
    

if __name__ == "__main__":
    main()