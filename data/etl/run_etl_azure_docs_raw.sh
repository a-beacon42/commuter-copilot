#!/bin/bash
# etl_update_local_azure_docs_raw.sh
# This script updates commuter-copilot's local copy of the azure-docs repository
# by merging in changes from the upstream MicrosoftDocs repository on GitHub to the main local branch.
# todo: move out of commuter-copilot repo. this doesn't work as is
# todo: incorporate this script into main pipeline
# todo: add more repos - architecture-center, azure-docs-sdk-python, azure-docs-cli, +580 more
# todo: add logic -->
#    if !repo exists, 
#        shallow clone it; 
#        echo "repo does not exist, shallow cloning it. this might take a while." || error_exit "Repo does not exist & failed to shallow clone the repository."
#        exit 0;
#    else, if there are no changes, 
#        echo "no changes to pull, exiting." || error_exit "No changes to pull."
#        exit 0; 
#    else, pull changes to main
#        echo "pulling changes to main." || error_exit "Failed to pull changes to main."
#        exit 0;
#    fi

error_exit() {
    echo "Error: $1" >&2
    exit 1
}


if [ -d "$AZ_DOCS_TARGET_DIR" ]; then
    echo "Fetching latest changes from upstream's main branch"
    cd "$AZ_DOCS_TARGET_DIR" || error_exit "Failed to change directory to $AZ_DOCS_TARGET_DIR."
fi

git fetch --depth 1 origin main || error_exit "Failed to fetch shallow copy of main branch."
git checkout main || error_exit "Failed to checkout main branch."
git reset --hard origin/main || error_exit "Failed to reset local main branch."
echo "Latest shallow changes merged successfully from origin/main."

exit 0
