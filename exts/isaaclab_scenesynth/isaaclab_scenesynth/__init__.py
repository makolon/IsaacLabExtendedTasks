"""Package containing task implementations for various robotic environments."""

import os

import toml

# Conveniences to other module directories via relative paths
ISAACLAB_SCENESYNTH_EXT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
"""Path to the extension source directory."""

ISAACLAB_SCENESYNTH_METADATA = toml.load(
    os.path.join(ISAACLAB_SCENESYNTH_EXT_DIR, "config", "extension.toml")
)
"""Extension metadata dictionary parsed from the extension.toml file."""

# Configure the module-level variables
__version__ = ISAACLAB_SCENESYNTH_METADATA["package"]["version"]
