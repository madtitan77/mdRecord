#!/bin/bash

# Directory containing your addon files
ADDON_DIR="$HOME/code/kodi/mdRecord"

# Base name for the zip file
BASE_NAME="madtitan.mdrecord.id-1.0"

# Find the highest version number
LATEST_VERSION=$(ls ${BASE_NAME}.*.zip 2>/dev/null | sed -E 's/^.*\.([0-9]+)\.zip$/\1/' | sort -n | tail -1)

# If no previous version found, start with 1, else increment by 1
if [ -z "$LATEST_VERSION" ]; then
  NEW_VERSION=1
else
  NEW_VERSION=$((LATEST_VERSION + 1))
fi

# Name of the new zip file
ZIP_NAME="${BASE_NAME}.${NEW_VERSION}.zip"

# Temporary directory for packaging
TEMP_DIR="packaging_temp"

# Desired root directory name inside the zip
ROOT_DIR_NAME="madtitan.mdrecord.id"

# Create temporary directory and subdirectory structure
mkdir -p "$TEMP_DIR/$ROOT_DIR_NAME"

# Copy files and directories into the temporary structure
cp addon.xml build.sh default.py "$TEMP_DIR/$ROOT_DIR_NAME"
cp -r resources "$TEMP_DIR/$ROOT_DIR_NAME"

# Create the zip file from the temporary directory contents
(cd "$TEMP_DIR" && zip -r "../$ZIP_NAME" "$ROOT_DIR_NAME")

# Remove the temporary directory
rm -rf "$TEMP_DIR"

echo "Packaged into $ZIP_NAME with root directory $ROOT_DIR_NAME"