import os
import glob
from omni.isaac.extended_assets import ISAACLAB_EXTENDED_ASSETS_DATA_DIR


# IndustReal Assembly Parts USD Directory
INDUSTREAL_ASSEMBLY_DIR = os.path.join(ISAACLAB_EXTENDED_ASSETS_DATA_DIR, "Props/USD/industreal")
# IndustReal Assembly Parts USD Paths
INDUSTREAL_OBJECT_PATH = glob.glob(os.path.join(ISAACLAB_EXTENDED_ASSETS_DATA_DIR, "Props/USD/industreal/*/*.usd"))
