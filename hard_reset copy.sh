#!/bin/bash

# Sync the 'codex' branch to match 'main' exactly

set -e  # Exit immediately if a command fails

echo "Checking out 'codex' branch..."
git checkout codex

echo "Fetching latest changes from origin..."
git fetch origin

echo "Resetting 'codex' to match 'origin/main'..."
git reset --hard origin/main

echo "Force pushing 'codex' to remote..."
git push --force origin codex

echo "'codex' is now synced with 'main'."
