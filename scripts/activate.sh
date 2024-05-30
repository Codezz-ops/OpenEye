#!/bin/bash

# Check if we are already in a virtual environment
if [[ -n "$VIRTUAL_ENV" ]]; then
    echo "Already in a virtual environment."
else
    # Create a virtual environment named 'venv'
    python3 -m venv venv
    
    # Activate the virtual environment
    source venv/bin/activate
    
    # Install required packages within the activated virtual environment
    pip install keyboard rich
fi

# Clear screen
clear

# Run the Python script using sudo if necessary
sudo python3 openeye.py