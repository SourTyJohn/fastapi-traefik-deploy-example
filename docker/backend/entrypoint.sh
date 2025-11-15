#!/bin/sh
echo "Running migrations..."
alembic -c alembic.ini upgrade head

echo "Launching uvicorn for backend..."
exec uvicorn task_manager.bootstrap.main:app --host 0.0.0.0 --port $NETWORK_BACKEND_PORT
