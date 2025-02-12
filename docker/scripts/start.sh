#!/bin/bash
set -e

echo "[$(date -u)] Starting application initialization..."

# Wait for database to be ready
echo "[$(date -u)] Waiting for database to be ready..."
until pg_isready -h "${POSTGRES_SERVER}" -p "${POSTGRES_PORT}" -U "${POSTGRES_USER}"; do
    echo "[$(date -u)] Database is unavailable - sleeping"
    sleep 1
done
echo "[$(date -u)] Database is ready!"

# Apply database migrations
echo "[$(date -u)] Applying database migrations..."
alembic upgrade head
echo "[$(date -u)] Database migrations completed successfully!"

# Start the FastAPI application
echo "[$(date -u)] Starting FastAPI application..."
exec gunicorn app.main:app \
    --bind $HOST:$PORT \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers $MAX_WORKERS \
    --worker-connections 1000 \
    --forwarded-allow-ips '*' \
    --proxy-allow-from '*' \
    --log-level info \
    --error-logfile - \
    --access-logfile - \
    --timeout 120 