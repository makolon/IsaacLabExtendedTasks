import numpy as np
import trimesh.transformations as tra

from scene_synthesizer import utils
from scene_synthesizer import procedural_assets as pa
from scene_synthesizer import procedural_scenes as ps


class SceneConstructor:
    def __init__(self, scene_config):
        self.scene_config = scene_config

        self.llm_manager = LLMManager()

    def construct_scene(self):
        scene = ps.Scene()

        # Query the LLM for the scene construction
        assets = self.llm_manager.query(scene_config)
        for asset in assets:
            if asset['type'] == 'table':
                table = pa.TableAsset(
                    asset["width"],
                    asset["depth"],
                    asset["height"],
                    asset["thichness"],
                    asset["leg_thichness"]
                )

            scene.add_object(asset=table, obj_id=asset["id"], transform=asset["transform"])

        return scene

    def add_mdl_materials(self, scene):
        pass

    def refine_scene(self, scene):
        """
        Refine the scene using the mesh collision detection
        Args:
            scene (_type_): _description_
        """
        pass
