import os
import glob
from omni.isaac.extended_assets import ISAACLAB_EXTENDED_ASSETS_DATA_DIR


# Siemens Assembly Parts USD Directory
SIEMENS_ASSEMBLY_DIR = os.path.join(ISAACLAB_EXTENDED_ASSETS_DATA_DIR, "Props/USD/siemens_gearbox")
# Siemens Assembly Parts USD Paths
SIEMENS_OBJECT_PATH = glob.glob(os.path.join(ISAACLAB_EXTENDED_ASSETS_DATA_DIR, "Props/USD/siemens_gearbox/*/*.usd"))
