#!/bin/bash

# Activate  virtual environment
# source /path/to/your/venv/bin/activate
workon condominio

echo "Starting Redis server (if needed)..."
# Uncomment if you want to start redis-server here (optional)
# redis-server &

echo "Starting Celery worker with events enabled..."
celery -A core worker --loglevel=info -E &

echo "Starting Celery Beat scheduler..."
celery -A core beat --loglevel=info &

echo "Starting Flower monitoring tool..."
celery -A core flower --broker=redis://localhost:6379/0 &

echo "All services started."

# Wait to keep the script running and display output
wait
