import inspect
import json
import os
import random
import re
from typing import Dict

import numpy as np
import trimesh
import trimesh.transformations as tra
from omegaconf import DictConfig

from scene_synthesizer import procedural_assets as pa
from scene_synthesizer import procedural_scenes as ps
from scene_synthesizer.usd_import import get_scene_paths
from scene_synthesizer.exchange.usd_export import add_mdl_material, bind_material_to_prims
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

        # Ask user for scene description
        user_input = self.get_user_input("What kind of scene would you like to create?: ")

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
        scene = ps.Scene()
        for comp in components:
            asset = self.create_asset(comp)
            scene.add_object(asset=asset, obj_id=comp["id"], transform=comp["transform"])

        # Refine if needed
        confirmation = self.get_user_input("Is this scene okay? (yes/no): ")
        if confirmation.lower() != "yes":
            if self.cfg.method == "analytical":
                scene = self.refine_scene_analytical(scene)
            elif self.cfg.method == "llm_feedback":
                scene = self.refine_scene_llm(scene)

        # Preview
        print("Previewing the scene...")
        scene.show()

        # Save
        if self.cfg.add_material:
            self.add_material(scene, usd_filename=self.cfg.usd_filename)
        else:
            scene.export(self.cfg.usd_filename)

        # Save scene mata information
        self.save_scene_meta_info(scene)

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

        # Clean up invalid keys for door_shape_args
        if "door_shape_args" in kwargs:
            kwargs["door_shape_args"].pop("shape", None)
            kwargs["door_shape_args"].pop("radius", None)

        return cls(**kwargs)

    def save_scene_meta_info(self, scene: trimesh.Scene):
        """
        Save metadata, graph, and configuration.
        """
        config = convert_ndarray_to_list(scene.get_configuration())
        metadata = convert_ndarray_to_list(scene.metadata)
        graph = convert_ndarray_to_list(scene.graph.to_edgelist())

        with open("scene_configuration.json", "w") as f:
            json.dump(config, f, indent=4)
        with open("scene_metadata.json", "w") as f:
            json.dump(metadata, f, indent=4)
        with open("scene_graph.json", "w") as f:
            json.dump(graph, f, indent=4)

    def write_scene_cfg(self, scene):
        """
        Write scene configuration to a file.
        """
        scene_graph = scene.graph.to_edgelist()

        # Ask user for robot selection
        user_input = self.get_user_input("Would you select a robot for this scene?: ")

        # Ask LLM for write interactive scene config
        scene_cfg = self.llm_manager.query_scene_cfg(user_input, scene_graph)

        return scene_cfg

    def add_material(self, scene: trimesh.Scene, usd_filename: str):
        """
        Add material to the scene.
        """
        random.seed(42)
        DEFAULT_TEXTURE_SCALE = 0.25

        # A manually defined dictionary mapping specific materials to types of objects and parts
        url_mdl_material = 'http://omniverse-content-production.s3.us-west-2.amazonaws.com/Materials/'
        materials = {
            'sink': [
                ('Base/Stone/Ceramic_Smooth_Fired.mdl', None, DEFAULT_TEXTURE_SCALE)
            ],
            'countertop': [
                ('vMaterials_2/Metal/Copper_Hammered.mdl', 'Copper_Hammered_Shiny', 0.5),
                ('Base/Stone/Marble.mdl', None, DEFAULT_TEXTURE_SCALE),
                ('Base/Stone/Granite_Dark.mdl', 'Granite_Dark', DEFAULT_TEXTURE_SCALE),
                ('Base/Stone/Granite_Light.mdl', None, DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Metal/Stainless_Steel_Milled.mdl', 'Stainless_Steel_Milled_Worn', DEFAULT_TEXTURE_SCALE),
                ('Base/Stone/Terrazzo.mdl', None, DEFAULT_TEXTURE_SCALE),
                ('Base/Stone/Slate.mdl', None, DEFAULT_TEXTURE_SCALE),
                ('Base/Stone/Porcelain_Tile_4.mdl', None, DEFAULT_TEXTURE_SCALE),
                ('Base/Stone/Porcelain_Tile_4_Linen.mdl', None, DEFAULT_TEXTURE_SCALE),
                ('Base/Stone/Ceramic_Tile_12.mdl', None, DEFAULT_TEXTURE_SCALE),
                ('Base/Stone/Porcelain_Smooth.mdl', None, DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Stone/Terrazzo.mdl', None, DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Stone/Stone_Natural_Black.mdl', 'Stone_Natural_Black_Shiny', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Stone/Steel_Grey.mdl', 'Steel_Grey_Bright', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Stone/Basaltite.mdl', 'Basaltite_Worn', DEFAULT_TEXTURE_SCALE),
            ],
            'glass': [
                ('Base/Glass/Tinted_Glass_R85.mdl', None, DEFAULT_TEXTURE_SCALE)
            ],
            'tinted glass': [
                ('Base/Glass/Tinted_Glass_R75.mdl', None, DEFAULT_TEXTURE_SCALE)
            ],
            'cabinet': [
                ('vMaterials_2/Paint/Paint_Eggshell.mdl', 'Paint_Eggshell_White', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Paint/Paint_Eggshell.mdl', 'Paint_Eggshell_Vanilla', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Paint/Paint_Eggshell.mdl', 'Paint_Eggshell_Cashmere', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Paint/Paint_Eggshell.mdl', 'Paint_Eggshell_Peach', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Paint/Paint_Eggshell.mdl', 'Paint_Eggshell', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Paint/Paint_Eggshell.mdl', 'Paint_Eggshell_Taupe', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Paint/Paint_Eggshell.mdl', 'Paint_Eggshell_Leaf', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Paint/Paint_Eggshell.mdl', 'Paint_Eggshell_Ash', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Paint/Paint_Eggshell.mdl', 'Paint_Eggshell_Denim', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Paint/Paint_Eggshell.mdl', 'Paint_Eggshell_Light_Denim', DEFAULT_TEXTURE_SCALE),
                ('Base/Wood/Bamboo.mdl', None, DEFAULT_TEXTURE_SCALE),
                ('Base/Wood/Birch.mdl', None, DEFAULT_TEXTURE_SCALE),
                ('Base/Wood/Cherry.mdl', None, DEFAULT_TEXTURE_SCALE),
                ('Base/Wood/Oak.mdl', None, DEFAULT_TEXTURE_SCALE),
                ('Base/Wood/Oak_Planks.mdl', None, DEFAULT_TEXTURE_SCALE),
                ('Base/Wood/Birch.mdl', None, DEFAULT_TEXTURE_SCALE),
                ('Base/Wood/Birch_Planks.mdl', None, DEFAULT_TEXTURE_SCALE),
                ('Base/Wood/Ash.mdl', None, DEFAULT_TEXTURE_SCALE),
                ('Base/Wood/Ash_Planks.mdl', None, DEFAULT_TEXTURE_SCALE),
                ('Base/Wood/Walnut.mdl', None, DEFAULT_TEXTURE_SCALE),
                ('Base/Wood/Walnut_Planks.mdl', None, DEFAULT_TEXTURE_SCALE),
            ],
            'rusted metal': [
                ('Base/Metals/RustedMetal.mdl', None, DEFAULT_TEXTURE_SCALE)
            ],
            'glossy black': [
                ('vMaterials_2/Paint/Carpaint/Carpaint_Solid.mdl', 'Black', DEFAULT_TEXTURE_SCALE)
            ],
            'handle': [
                ('vMaterials_2/Metal/Silver_Foil.mdl', None, DEFAULT_TEXTURE_SCALE)
            ],
            'appliances': [
                ('vMaterials_2/Metal/Aluminum_Brushed.mdl', None, DEFAULT_TEXTURE_SCALE)
            ],
            'wall': [
                ('vMaterials_2/Paint/Paint_Eggshell.mdl', 'Paint_Eggshell_Pale_Rose', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Paint/Paint_Eggshell.mdl', 'Paint_Eggshell_Lime', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Paint/Paint_Eggshell.mdl', 'Paint_Eggshell_White', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Paint/Paint_Eggshell.mdl', 'Paint_Eggshell_Vanilla', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Paint/Paint_Eggshell.mdl', 'Paint_Eggshell_Cashmere', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Paint/Paint_Eggshell.mdl', 'Paint_Eggshell_Peach', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Paint/Paint_Eggshell.mdl', 'Paint_Eggshell', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Paint/Paint_Eggshell.mdl', 'Paint_Eggshell_Taupe', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Paint/Paint_Eggshell.mdl', 'Paint_Eggshell_Leaf', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Wood/Wood_Tiles_Pine.mdl', 'Wood_Tiles_Pine_Brickbond', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Diamond.mdl', 'Ceramic_Tiles_Diamond_Mint', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Diamond.mdl', 'Ceramic_Tiles_Diamond_Red_Varied', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Diamond.mdl', 'Ceramic_Tiles_Diamond_White_Matte', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Diamond_Offset.mdl', 'Ceramic_Tiles_Offset_Diamond_Graphite_Matte', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Diamond.mdl', 'Ceramic_Tiles_Diamond_White_Matte', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Subway.mdl', 'Ceramic_Tiles_Glazed_Subway', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Masonry/Facade_Brick_Red_Clinker.mdl', 'Facade_Brick_Red_Clinker_Painted_White', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Masonry/Facade_Brick_Red_Clinker.mdl', 'Facade_Brick_Red_Clinker_Painted_Yellow', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Masonry/Facade_Brick_Red_Clinker.mdl', 'Facade_Brick_Red_Clinker_Sloppy_Paint_Job', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Plaster/Plaster_Wall.mdl', 'Plaster_Wall', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Plaster/Plaster_Wall.mdl', 'Plaster_Wall_Cracked', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Subway.mdl', 'Ceramic_Tiles_Subway_Cappucino', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Subway.mdl', 'Ceramic_Tiles_Subway_White', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Subway.mdl', 'Ceramic_Tiles_Subway_White_Matte', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Subway.mdl', 'Ceramic_Tiles_Subway_White_Worn_Matte', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Subway.mdl', 'Ceramic_Tiles_Subway_Gray', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Subway.mdl', 'Ceramic_Tiles_Subway_Dark_Gray_Matte', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Subway.mdl', 'Ceramic_Tiles_Subway_Dark_Gray', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Penny.mdl', 'Ceramic_Tiles_Penny_Antique_White', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Penny.mdl', 'Ceramic_Tiles_Penny_White_Matte', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Penny.mdl', 'Ceramic_Tiles_Penny_Lime_Green_Varied', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Penny.mdl', 'Ceramic_Tiles_Penny_Graphite_Varied', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Penny.mdl', 'Ceramic_Tiles_Penny_Mint_Varied', DEFAULT_TEXTURE_SCALE),
            ],
            'floor': [
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Diamond.mdl', 'Ceramic_Tiles_Diamond_White_Matte', DEFAULT_TEXTURE_SCALE),
                ('Base/Wood/Parquet_Floor.mdl', 'Parquet_Floor', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Concrete/Concrete_Floor_Damage.mdl', 'Concrete_Floor_Damage', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Wood/Wood_Tiles_Beech.mdl', 'Wood_Tiles_Beech_Herringbone', DEFAULT_TEXTURE_SCALE),
                ('Base/Stone/Adobe_Octagon_Dots.mdl', 'Adobe_Octagon_Dots', None),
                ('vMaterials_2/Wood/Wood_Tiles_Pine.mdl', 'Wood_Tiles_Pine_Brickbond', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Wood/Wood_Tiles_Pine.mdl', 'Wood_Tiles_Pine_Herringbone', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Wood/Wood_Tiles_Pine.mdl', 'Wood_Tiles_Pine_Mosaic', DEFAULT_TEXTURE_SCALE),
                ('Base/Wood/Oak.mdl', None, DEFAULT_TEXTURE_SCALE),
                ('Base/Wood/Oak_Planks.mdl', None, DEFAULT_TEXTURE_SCALE),
                ('Base/Stone/Terracotta.mdl', 'Terracotta', None),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Versailles.mdl', 'Ceramic_Tiles_Versailles_Antique_White_Dirty', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Versailles.mdl', 'Ceramic_Tiles_Versailles_White_Matte', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Square.mdl', 'Ceramic_Tiles_Square_White_Matte', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Pinwheel.mdl', 'Ceramic_Tiles_Pinwheel_White_Matte', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Pinwheel.mdl', 'Ceramic_Tiles_Pinwheel_Antique_White_Dirty', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Paseo.mdl', 'Ceramic_Tiles_Paseo_White_Worn_Matte', DEFAULT_TEXTURE_SCALE),
                ('vMaterials_2/Ceramic/Ceramic_Tiles_Glazed_Diamond_Offset.mdl', 'Ceramic_Tiles_Offset_Diamond_Antique_White_Dirty', DEFAULT_TEXTURE_SCALE),
            ],
        }

        # A dictionary mapping scene object/part names to types the general types of objects/parts defined above
        # The keys are regular expressions of prim_paths in the USD
        geometries = scene.get_geometries()
        geometry2material = {}
        for geom in geometries:
            geom_name = str(geom) if isinstance(geom, str) else getattr(geom, "name", None)
            if geom_name is None:
                continue
            for geom_regex, material_group in materials.items():
                if re.match(geom_regex, geom_name):
                    geometry2material[geom_name] = material_group
                    break

        # Generate UV coordinates for certain primitives
        # scene.unwrap_geometries('(sink_cabinet/sink_countertop|countertop_.*|.*countertop)')  # TODO: Fix this

        # Export the scene to a USD stage (in memory, not written to disk yet)
        stage = scene.export(file_type='usd')

        # Attach MDL materials to prims in USD stage
        for geom_regex, material_group in geometry2material.items():
            # Find all geometry prims of a particular category
            paths = get_scene_paths(
                stage=stage,
                prim_types=["Mesh", "Capsule", "Cube", "Cylinder", "Sphere"],
                scene_path_regex=geom_regex,
            )

            # select random material
            if len(materials[material_group]) == 0:
                print(f"Warning: No materials for {material_group}")
                continue
            
            mtl_url, mtl_name, texture_scale = random.choice(materials[material_group])
            
            # add material to USD stage and bind to geometry prims
            mtl = add_mdl_material(
                stage=stage,
                mtl_url=url_mdl_material + mtl_url,
                mtl_name=mtl_name,
                texture_scale=texture_scale
            )
            bind_material_to_prims(
                stage=stage,
                material=mtl,
                prim_paths=paths
            )
        # Export scene to USD file
        stage.Export(usd_filename)

    def refine_scene_llm(self, scene: trimesh.Scene) -> trimesh.Scene:
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

    def refine_scene_analytical(self, scene: trimesh.Scene, spacing: float = 0.2) -> trimesh.Scene:
        """
        Rearranges the connected components of a Trimesh Scene along the x-axis
        to avoid overlap between objects.

        Args:
            scene (trimesh.Scene): Input scene containing multiple objects/components.
            spacing (float): Space between each component.

        Returns:
            trimesh.Scene: Rearranged scene with non-overlapping components.
        """
        new_scene = trimesh.Scene()
        offset = 0.0

        # Extract connected components as sub-scenes
        components = scene.connected_components_geometry()

        for i, component in enumerate(components):
            # Merge geometries in component to compute bounding box
            merged = component.dump().sum()
            size_x = merged.bounds[1][0] - merged.bounds[0][0]
            center = merged.bounding_box.centroid

            # Compute transformation: center at origin then move to offset
            translation_to_origin = -center
            translation_to_position = [offset + size_x / 2, 0, 0]
            total_translation = trimesh.transformations.translation_matrix(
                translation_to_origin + translation_to_position
            )

            # Apply transform and add to new scene
            component.apply_transform(total_translation)
            new_scene = new_scene + component

            # Update offset
            offset += size_x + spacing

        return new_scene

    def get_user_input(self, prompt: str) -> str:
        return input(prompt)
