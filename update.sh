#!/bin/bash

# Dynamically find the script's directory
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Starting Convert-Commander update process..."

# Step 1: Change to the project directory
cd "$PROJECT_DIR" || { echo "Project directory not found! Aborting."; exit 1; }

# Step 2: Pull the latest changes from Git
echo "Pulling latest changes from GitHub..."
git pull || { echo "Error pulling changes from GitHub! Aborting."; exit 1; }

# Step 3: Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || { echo "Error activating virtual environment! Aborting."; exit 1; }

# Step 4: Update dependencies
echo "Updating Python dependencies..."
pip install --upgrade -r requirements.txt || { echo "Error updating dependencies! Aborting."; exit 1; }

# Step 5: Restart the service (optional)
SERVICE_NAME="convert-commander" # Adjust the service name
if systemctl is-active --quiet "$SERVICE_NAME"; then
    echo "Restarting the Convert-Commander service..."
    sudo systemctl restart "$SERVICE_NAME" || { echo "Error restarting the service! Aborting."; exit 1; }
else
    echo "Service is not running, skipping restart."
fi

echo "Update process completed successfully!"
