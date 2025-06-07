#!/bin/bash

# Check if a package name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <package-name>"
  exit 1
fi

PACKAGE=$1

# Install the package
echo "Installing package: $PACKAGE"
pip install "$PACKAGE"

# Freeze requirements to file
echo "Updating requirements.txt"
pip freeze > requirements.txt

# Git add and commit
echo "Staging requirements.txt"
git add requirements.txt

echo "Committing changes"
git commit -m "add: $PACKAGE"

echo "Done"
