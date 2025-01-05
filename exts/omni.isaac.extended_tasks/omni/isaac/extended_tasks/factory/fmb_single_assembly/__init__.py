import os
import glob
from omni.isaac.extended_assets import ISAACLAB_EXTENDED_ASSETS_DATA_DIR


# FMB Single Assembly Parts USD Directory
FMB_SINGLE_ASSEMBLY_DIR = os.path.join(ISAACLAB_EXTENDED_ASSETS_DATA_DIR, "Props/USD/fmb/simo")
# FMB Single Assembly Parts USD Paths
FMB_SINGLE_OBJECT_PATH = glob.glob(os.path.join(ISAACLAB_EXTENDED_ASSETS_DATA_DIR, "Props/USD/fmb/simo/*/*.usd"))
