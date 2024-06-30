#!/usr/bin/env bash

# This script is used to build the dependencies for the project.
# It is intended to be run from the root of the project.

cecho() {
    ${CECHO} "$@"
}

# If $artifact_home_dir doesn't exist, create it
if [ ! -d "$ARTIFACT_HOME_DIR" ]; then
    mkdir -p $ARTIFACT_HOME_DIR
fi

# Check if the script is being run from the root of the project
if [ ! -f "$DT_HOME/infra/scripts/shell/build_dependencies.sh" ]; then
    echo "This script must be run from the root of the project."
    exit 1
fi

# Create the build directory if it doesn't exist
if [ ! -d "$ARTIFACT_HOME_DIR" ]; then
    echo "The artifact home directory does not exist. Creating it."
    mkdir $ARTIFACT_HOME_DIR
fi

# Create the dependencies directory if it doesn't exist
if [ ! -d "$ARTIFACT_HOME_DIR/dependencies" ]; then
    mkdir $ARTIFACT_HOME_DIR/dependencies
fi

# Create the requirements_hash file if it doesn't exist
if [ ! -f "$DT_HOME/infra/artifacts/requirements_hash" ]; then
    echo "Creating requirements_hash file..."
    touch $DT_HOME/infra/artifacts/requirements_hash
fi

# Overwrite the requirements_hash file with the hash of the requirements file
hash=$(sha256sum $DT_HOME/requirements.txt | awk '{print $1}')
echo $hash > $DT_HOME/infra/artifacts/requirements_hash

cecho -c yellow -t "Building dependencies..."

# Download pip3 dependencies into the dependencies directory
$DT_PIP download -r $DT_HOME/requirements.txt -d $ARTIFACT_HOME_DIR/dependencies

cd $ARTIFACT_HOME_DIR

# Create a tarball of the dependencies directory
arch=$(uname -sm)
arch=${arch// /_}
tar -czvf dependencies.tar.$arch.gz dependencies

# Clean up the dependencies directory
rip dependencies

cecho -c green -t "Dependencies built successfully."

cd $DT_HOME 
