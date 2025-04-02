import inspect
import json
import os
import re
from typing import Dict

import numpy as np
import trimesh.transformations as tra
from omegaconf import DictConfig

from scene_synthesizer import procedural_assets as pa
from scene_synthesizer import procedural_scenes as ps
from scene_synthesizer.procedural_assets import TrimeshSceneAsset, URDFAsset

from isaaclab_scenesynth.llm_manager import LLMManager


def get_explicit_args(cls):
    """
    Returns all explicit constructor arguments for a class,
    excluding 'self' and '**kwargs'.
    """
    signature = inspect.signature(cls.__init__)
    parameters = signature.parameters
    explicit = [
        name for name, param in parameters.items()
        if name != 'self' and param.kind != param.VAR_KEYWORD  # Exclude **kwargs
    ]
    return explicit


def convert_ndarray_to_list(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_ndarray_to_list(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_ndarray_to_list(x) for x in obj]
    else:
        return obj


class SceneConstructor:
    def __init__(self, cfg: DictConfig):
        self.cfg = cfg
        self.llm_manager = LLMManager(cfg)
        self.asset_classes = self._discover_asset_classes()

    def _discover_asset_classes(self):
        """
        Dynamically discover all procedural asset classes and map to asset_type names.
        """
        asset_classes = {}
        for name, cls in inspect.getmembers(pa, inspect.isclass):
            if (issubclass(cls, TrimeshSceneAsset) or issubclass(cls, URDFAsset)) and cls is not TrimeshSceneAsset:
                asset_type = self._camel_to_snake(name.replace("Asset", ""))
                asset_classes[asset_type] = cls
        return asset_classes

    def _camel_to_snake(self, name: str) -> str:
        """
        Convert CamelCase to snake_case.
        """
        name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name).lower()

    def construct_scene(self):
        """
        Main scene construction loop.
        """
        scene = ps.Scene()

        # Ask user for scene description
        user_input = self.get_user_input("What kind of scene would you like to create?\n")

        # Ask LLM for types of assets
        asset_types = self.llm_manager.query_asset_types(user_input, list(self.asset_classes.keys()))

        # For each type, get required arguments
        asset_arg_templates = {}
        for atype in asset_types:
            if atype not in self.asset_classes:
                print(f"Warning: asset type '{atype}' is not currently supported.")
                continue
            required_args = get_explicit_args(self.asset_classes[atype])
            asset_arg_templates[atype] = required_args

        # Ask LLM for detailed component specs
        components = self.llm_manager.query_asset_instances(asset_arg_templates.keys(), asset_arg_templates)

        # Build scene
        for comp in components:
            asset = self.create_asset(comp)
            scene.add_object(asset=asset, obj_id=comp["id"], transform=comp["transform"])

        # Preview
        scene.show()

        # Refine if needed
        confirmation = self.get_user_input("Is this scene okay? (yes/no): ")
        if confirmation.lower() != "yes":
            scene = self.refine_scene(scene)

        # Save
        scene.export('constructed_scene.usd')
        self.write_scene_cfg(scene)

    def create_asset(self, component: Dict):
        """
        Create an asset instance from the component dictionary.
        """
        atype = component["type"]
        if atype not in self.asset_classes:
            raise ValueError(f"Unsupported asset type: {atype}")
        cls = self.asset_classes[atype]
        required_args = get_explicit_args(cls)

        kwargs = {arg: component[arg] for arg in required_args if arg in component}

        # Clean up invalid keys for handle_shape_args
        if "handle_shape_args" in kwargs:
            kwargs["handle_shape_args"].pop("shape", None)
            kwargs["handle_shape_args"].pop("radius", None)
            kwargs["handle_offset"] = [0.0, 0.0, 0.0]

        # Clean up invalid keys for door_shape_args
        if "door_shape_args" in kwargs:
            kwargs["door_shape_args"].pop("shape", None)
            kwargs["door_shape_args"].pop("radius", None)

        return cls(**kwargs)

    def refine_scene(self, scene):
        """
        Ask LLM to modify the scene and rebuild it.
        """
        refinement_input = self.get_user_input("How would you like to modify the scene?")
        refined_components = self.llm_manager.query(refinement_input)

        scene.remove_object(".*")  # Remove all objects
        for comp in refined_components:
            asset = self.create_asset(comp)
            scene.add_object(asset=asset, obj_id=comp["id"], transform=comp["transform"])
        scene.show()
        return scene

    def write_scene_cfg(self, scene):
        """
        Save metadata, graph, and configuration.
        """
        config = convert_ndarray_to_list(scene.get_configuration())
        metadata = convert_ndarray_to_list(scene.metadata)
        graph = convert_ndarray_to_list(scene.graph.to_dict())

        with open("scene_configuration.json", "w") as f:
            json.dump(config, f, indent=4)
        with open("scene_metadata.json", "w") as f:
            json.dump(metadata, f, indent=4)
        with open("scene_graph.json", "w") as f:
            json.dump(graph, f, indent=4)

    def get_user_input(self, prompt):
        return input(prompt)
