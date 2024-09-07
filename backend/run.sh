#!/bin/bash
cd "$(dirname "$0")" || exit
source .venv/bin/activate
gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
