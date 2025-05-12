#!/bin/bash

# The following repositories are private, so they need to be added as submodules under the third_party directory.
# To use them as Python modules, you need to install them by executing the provided Shell script.
# This script will handle copying the submodules to the appropriate locations and installing them as Python packages.

# Define source directories
SOURCE_ASSETS="$ISAACEXTASKS_PATH/source/isaaclab_exassets"
SOURCE_TASKS="$ISAACEXTASKS_PATH/source/isaaclab_extasks"

# Function to link and install a package
install_source() {
    local SOURCE_PATH=$1
    local PACKAGE_NAME=$(basename "$SOURCE_DIR")

    if [ -d "$SOURCE_PATH" ]; then
        # Install the package
        cd "$SOURCE_PATH" || { echo "Failed to enter directory: $SOURCE_PATH"; exit 1; }
        echo "Installing $PACKAGE_NAME with pip"
        ${ISAACLAB_PATH}/_isaac_sim/python.sh -m pip install -e . || { echo "Failed to install $PACKAGE_NAME"; exit 1; }
        cd - > /dev/null
    else
        echo "Source directory $SOURCE_PATH does not exist. Skipping."
    fi
}

# Install isaaclab_exassets
install_source "$SOURCE_ASSETS"

# Install isaaclab_extasks
install_source "$SOURCE_TASKS"

echo "All tasks completed successfully."

# Execute any additional commands provided to the container
exec "$@"