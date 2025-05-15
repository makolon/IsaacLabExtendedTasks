import hydra
from omegaconf import DictConfig
from isaaclab_scenesynth.scene_constructor import SceneConstructor


@hydra.main(config_path="configs", config_name="scene_cfg", version_base=None)
def main(cfg: DictConfig):    
    scene_builder = SceneConstructor(cfg)
    scene_builder.construct_scene()


if __name__ == "__main__":
    main()
