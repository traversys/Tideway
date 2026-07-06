#!/bin/bash
set -e

# Ensure we're in a git repo
if [ ! -d ".git" ]; then
  echo "Not a git repository. Run this inside a repo."
  exit 1
fi

# Get current branch
branch=$(git rev-parse --abbrev-ref HEAD)

echo "Resetting all local changes..."
git fetch origin
git reset --hard origin/$branch
git clean -fd

echo "Updating branch '$branch' from origin..."
git pull origin $branch

echo "Repository is now clean and up to date."
