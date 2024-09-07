#!/bin/bash
# Change to the src directory
cd "$(dirname "$0")/src" || exit

# Activate the virtual environment
source ../.venv/bin/activate

# Add the current directory and the src directory to the PYTHONPATH
PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/src
export PYTHONPATH

# Run the application using gunicorn
gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
