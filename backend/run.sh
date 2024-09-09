#!/bin/bash

NAME=liquid-vanilla-backend
DIR=/var/www/liquid-vanilla/backend
DIR_SRC=$DIR/src
USER=jonathan
WORKERS=3
WORKER_CLASS=uvicorn.workers.UvicornWorker
VENV=$DIR/.venv/bin/activate
#BIND=unix:$DIR/run/gunicorn.sock
BIND=0.0.0.0:8000

# Change to the project source directory
cd $DIR_SRC || exit

# Activate the virtual environment
source $VENV

# Add the current directory and the src directory to the PYTHONPATH
PYTHONPATH=$PYTHONPATH:$DIR:$DIR_SRC
export PYTHONPATH

# Cleanup function
cleanup() {
    echo "Stopping Gunicorn gracefully..."
    kill -TERM "$child" 2>/dev/null
}

# Trap SIGTERM and call cleanup
trap cleanup SIGTERM

# Run the application using Gunicorn
gunicorn main:app \
  --name $NAME \
  --workers $WORKERS \
  --worker-class $WORKER_CLASS \
  --user=$USER \
  --bind=$BIND \
  &

child=$!
wait "$child"
