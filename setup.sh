#!/bin/bash

# Create virtual environment if it doesn't exist
python3 -m venv backend/.venv

# Activate virtual environment
source backend/.venv/bin/activate

# Install requirements
pip install -r backend/requirements.txt

echo "Virtual environment activated and dependencies installed!"
