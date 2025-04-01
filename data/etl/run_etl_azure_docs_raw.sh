#!/bin/bash
# etl_update_local_azure_docs_raw.sh
# This script updates commuter-copilot's local copy of the azure-docs repository
# by merging in changes from the upstream MicrosoftDocs repository on GitHub to the main local branch.
# todo: incorporate this script into main pipeline
# todo: add more repos - architecture-center, azure-docs-sdk-python, azure-docs-cli, +580 more
# todo: add logic -->
'''
    if !repo exists, 
        shallow clone it; 
        echo "repo does not exist, shallow cloning it. this might take a while." || error_exit "Repo does not exist & failed to shallow clone the repository."
        exit 0;
    else, if there are no changes, 
        echo "no changes to pull, exiting." || error_exit "No changes to pull."
        exit 0; 
    else, pull changes to main
        echo "pulling changes to main." || error_exit "Failed to pull changes to main."
        exit 0;
    fi
'''

# Function to handle errors
error_exit() {
    echo "Error: $1" >&2
    exit 1
}

TARGET_DIR="Users/alex/Desktop/code_projects/commuter_copilot/local_files/data/raw/azure-docs"

if [ -d "$TARGET_DIR" ]; then
    echo "fetching latest changes from upstream's main branch"
    cd "$TARGET_DIR" || error_exit "Failed to change directory to $TARGET_DIR."
fi

git checkout main || error_exit "Failed to checkout main branch."
git pull || error_exit "Failed to pull upstream changes."
echo "Latest changes merged successfully merged to local main."

exit 0
