import os
import glob
from isaaclab_exassets import ISAACLAB_EXTENDED_ASSETS_DATA_DIR


# Fusion360 Assembly Parts USD Directory
FUSION360_ASSEMBLY_DIR = glob.glob(os.path.join(ISAACLAB_EXTENDED_ASSETS_DATA_DIR, "Props/USD/fusion360/*"))
# Fusion360 Assembly Fixture USD Paths
FUSION360_OBJECT_PATH = glob.glob(os.path.join(ISAACLAB_EXTENDED_ASSETS_DATA_DIR, "Props/USD/fusion360/*/model_0/model_0.usd"))
# Fusion360 Assembly Object USD Paths
FUSION360_FIXTURE_PATH = glob.glob(os.path.join(ISAACLAB_EXTENDED_ASSETS_DATA_DIR, "Props/USD/fusion360/*/model_1/model_1.usd"))