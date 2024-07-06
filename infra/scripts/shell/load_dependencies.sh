#!/usr/bin/env bash

# This script loads all the pip3 dependencies for the project.
# It is intended to be run from the root of the project.

# Check if the script is being run from the root of the project
if [ ! -f "$DT_HOME/infra/scripts/shell/build_dependencies.sh" ]; then
    echo "This script must be run from the root of the project."
    exit 1
fi

# Check if the build directory exists
if [ ! -d "$ARTIFACT_HOME_DIR" ]; then
    echo "The artifact home directory does not exist. Creating it."
    mkdir -p $ARTIFACT_HOME_DIR
fi

arch=$(uname -sm)
arch=${arch// /_}

# Check if the dependencies tarball exists
if [ ! -f "$ARTIFACT_HOME_DIR/dependencies.tar.$arch.gz" ]; then
    echo "The dependencies tarball does not exist. Running build_dependencies.sh."
    $DT_HOME/src/utils/shell/build_dependencies.sh
fi

# Extract the dependencies tarball
tar -xzvf $ARTIFACT_HOME_DIR/dependencies.tar.$arch.gz -C $ARTIFACT_HOME_DIR

# Install the dependencies
$DT_PIP install --no-index --find-links=$ARTIFACT_HOME_DIR/dependencies -r $DT_HOME/requirements.txt

# Clean up the dependencies directory
rip $ARTIFACT_HOME_DIR/dependencies