#!/bin/bash
# Change to the src directory
cd "$(dirname "$0")/src" || exit

# Activate the virtual environment
source ../.venv/bin/activate

# Add the current directory and the src directory to the PYTHONPATH
PYTHONPATH=$PYTHONPATH:$(pwd):$(pwd)/src
export PYTHONPATH

# Cleanup function
cleanup() {
    echo "Stopping Gunicorn gracefully..."
    kill -TERM "$child" 2>/dev/null
}

# Trap SIGTERM and call cleanup
trap cleanup SIGTERM

# Run the application using gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 &

child=$!
wait "$child"
