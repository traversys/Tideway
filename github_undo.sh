#!/bin/bash

# Undo the last commit on the current branch and force push the change.

git reset --hard HEAD^
git push origin HEAD --force