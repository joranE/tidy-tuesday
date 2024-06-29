#!/bin/bash

# Create a virtual environment for the project
python3 -m venv env

# Activate the virtual environment
source env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install the required packages
pip install numpy pandas matplotlib seaborn polars pyarrow sklearn sktime ipykernel

# Deactivate the virtual environment
deactivate