#!/bin/bash

# Directory and file structure
BASEDIR="text-to-structured-service"
APPDIR="$BASEDIR/app"

# Create directories
mkdir -p "$APPDIR"

# Create files
touch "$BASEDIR/Dockerfile"
touch "$BASEDIR/requirements.txt"
touch "$BASEDIR/README.md"
touch "$APPDIR/__init__.py"
touch "$APPDIR/main.py"
touch "$APPDIR/schemas.py"

echo "Microservice directory and files have been created."