"""Package containing asset and sensor configuration."""

import os

import toml

# Conveniences to other module directories via relative paths
ISAACLAB_EXTENDED_ASSETS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../")
)
"""Path to the extension source directory."""

ISAACLAB_EXTENDED_ASSETS_DATA_DIR = os.path.join(ISAACLAB_EXTENDED_ASSETS_DIR, "data")
"""Path to the extension data directory."""

ISAACLAB_EXTENDED_ASSETS_METADATA = toml.load(
    os.path.join(ISAACLAB_EXTENDED_ASSETS_DIR, "config", "extension.toml")
)
"""Extension metadata dictionary parsed from the extension.toml file."""

# Configure the module-level variables
__version__ = ISAACLAB_EXTENDED_ASSETS_METADATA["package"]["version"]


##
# Configuration for different assets.
##

from .franka import *
from .kinova import *
from .kuka import *
from .ufactory import *
from .universal_robots import *
