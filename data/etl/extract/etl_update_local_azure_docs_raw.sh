#!/bin/bash
# etl_update_local_azure_docs_raw.sh
# This script updates commuter-copilot's local copy of the azure-docs repository
# by merging in changes from the upstream MicrosoftDocs repository on GitHub to the main local branch.
# todo: incorporate this script into main pipeline

# Function to handle errors
error_exit() {
    echo "Error: $1" >&2
    exit 1
}

TARGET_DIR="data/raw/azure-docs"

if [ -d "$TARGET_DIR" ]; then
    echo "fetching latest changes from upstream's main branch"
    cd "$TARGET_DIR" || error_exit "Failed to change directory to $TARGET_DIR."
fi

git checkout main || error_exit "Failed to checkout main branch."
git pull || error_exit "Failed to pull upstream changes."
echo "Latest changes merged successfully merged to local main."

exit 0

# update_azure_docs.sh
# This script updates commuter-copilot's fork of the azure-docs repository on GitHub
# by merging in changes from the upstream MicrosoftDocs repository,
# and then clones the updated fork to your local "data/raw/azure-docs" folder.
#
# Requirements:
# - SSH access to git@github.com:commuter-copilot/azure-docs.git must be set up.
# - No local modifications in the upstream repo (we only pull in updates).
#
# Basic error handling is included along with a final notification.

# # Save the current working directory
# ORIGINAL_DIR=$(pwd)

# # Step 1: Delete the local azure-docs folder if it exists
# TARGET_DIR="data/raw/azure-docs"
# if [ -d "$TARGET_DIR" ]; then
#     echo "Deleting existing local directory: $TARGET_DIR"
#     rm -rf "$TARGET_DIR" || error_exit "Failed to delete $TARGET_DIR"
# else
#     echo "Local directory $TARGET_DIR does not exist. Nothing to delete."
# fi

# # Step 2: Update the forked repo on GitHub by merging changes from upstream

# # Create a temporary directory for the update process
# TEMP_DIR=$(mktemp -d) || error_exit "Failed to create a temporary directory."
# echo "Cloning your forked repository into temporary directory: $TEMP_DIR"

# # Clone your fork (the remote URL for your fork)
# git clone git@github.com:commuter-copilot/azure-docs.git "$TEMP_DIR/azure-docs" ||
#     error_exit "Failed to clone your forked repository."

# cd "$TEMP_DIR/azure-docs" || error_exit "Failed to change directory to the temporary clone."

# # Add the upstream remote if it doesn't already exist
# if ! git remote | grep -q upstream; then
#     echo "Adding upstream remote (MicrosoftDocs repository)..."
#     git remote add upstream https://github.com/MicrosoftDocs/azure-docs.git ||
#         error_exit "Failed to add upstream remote."
# fi

# echo "Fetching upstream repository..."
# git fetch upstream || error_exit "Failed to fetch upstream repository."

# # Check out your main branch (adjust branch name if necessary)
# git checkout main || error_exit "Failed to checkout main branch."

# echo "Merging changes from upstream/main into local main..."
# git merge upstream/main || error_exit "Failed to merge upstream changes."

# echo "Pushing updated main branch to your fork on GitHub..."
# git push origin main || error_exit "Failed to push updates to your fork."

# # Step 3: Clone the updated fork into the local target directory
# cd "$ORIGINAL_DIR" || error_exit "Failed to return to original directory."

# echo "Cloning updated fork into local directory: $TARGET_DIR"
# git clone git@github.com:commuter-copilot/azure-docs.git "$TARGET_DIR" ||
#     error_exit "Failed to clone updated fork to local directory."

# # Clean up the temporary directory
# rm -rf "$TEMP_DIR" || echo "Warning: Failed to remove temporary directory $TEMP_DIR."

# echo "Notification: Update and clone completed successfully."
# exit 0
