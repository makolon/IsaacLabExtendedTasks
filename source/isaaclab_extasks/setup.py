"""Installation script for the 'isaaclab_extasks' python package."""

import os

import toml
from setuptools import setup

# Obtain the extension data from the extension.toml file
EXTENSION_PATH = os.path.dirname(os.path.realpath(__file__))
# Read the extension.toml file
EXTENSION_TOML_DATA = toml.load(
    os.path.join(EXTENSION_PATH, "config", "extension.toml")
)

# Installation operation
setup(
    name="isaaclab_extasks",
    author="Makoto Sato",
    maintainer="Makoto Sato",
    url=EXTENSION_TOML_DATA["package"]["repository"],
    version=EXTENSION_TOML_DATA["package"]["version"],
    description=EXTENSION_TOML_DATA["package"]["description"],
    keywords=EXTENSION_TOML_DATA["package"]["keywords"],
    include_package_data=True,
    python_requires=">=3.10",
    packages=["isaaclab_extasks"],
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3.10",
        "Isaac Sim :: 4.5.0",
        "Isaac Sim :: 4.2.0",
        "Isaac Sim :: 4.1.0",
    ],
    zip_safe=False,
)
