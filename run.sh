#!/bin/bash

# Soldier Sign-in System Launcher Script
# This script launches the Soldier Sign-in System application

echo "Starting Soldier Sign-in System..."
echo "======================================"

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    echo "Please install Python 3.x to run this application"
    exit 1
fi

# Try python3 first, then python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

echo "Using Python: $PYTHON_CMD"

# Check if required dependencies are available
echo "Checking dependencies..."
$PYTHON_CMD -c "import tkinter; import PIL; print('✓ All dependencies available')" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "⚠ Warning: Some dependencies may be missing"
    echo "Installing Pillow..."
    pip install Pillow
fi

# Launch the application
echo "Launching application..."
$PYTHON_CMD main.py

echo "Application closed."
