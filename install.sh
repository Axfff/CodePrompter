#!/bin/bash

# Check if a virtual environment directory exists, if not, create one
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
source venv/bin/activate

# Ensure the latest version of pip is installed
pip install --upgrade pip

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Optional: Install the package globally
pip install .

# Confirm installation
echo "Code Prompter is now installed and ready to use!"
