#!/bin/bash
echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

echo "Applying migrations..."
alembic upgrade head

echo "Starting API..."
python -m uvicorn app.main:app --host $APP_HOST --port $APP_PORT --reload