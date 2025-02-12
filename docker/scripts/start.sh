#!/bin/bash
set -e

echo "[$(date -u)] Starting application initialization..."

# Function to check if database is ready
check_db() {
    pg_isready -h "${POSTGRES_SERVER}" -p "${POSTGRES_PORT}" -U "${POSTGRES_USER}" -d "${POSTGRES_DB}"
}

# Wait for database to be ready with timeout
echo "[$(date -u)] Waiting for database to be ready..."
RETRIES=30
until check_db || [ $RETRIES -eq 0 ]; do
    echo "[$(date -u)] Database is unavailable - retries left: $RETRIES"
    RETRIES=$((RETRIES-1))
    sleep 1
done

if [ $RETRIES -eq 0 ]; then
    echo "[$(date -u)] Failed to connect to database"
    exit 1
fi

echo "[$(date -u)] Database is ready!"

# Apply database migrations with retry logic
echo "[$(date -u)] Applying database migrations..."
MAX_MIGRATION_ATTEMPTS=3
MIGRATION_ATTEMPT=1

while [ $MIGRATION_ATTEMPT -le $MAX_MIGRATION_ATTEMPTS ]; do
    if alembic upgrade head; then
        echo "[$(date -u)] Database migrations completed successfully!"
        break
    else
        if [ $MIGRATION_ATTEMPT -eq $MAX_MIGRATION_ATTEMPTS ]; then
            echo "[$(date -u)] Migration failed after $MAX_MIGRATION_ATTEMPTS attempts"
            exit 1
        fi
        echo "[$(date -u)] Migration attempt $MIGRATION_ATTEMPT failed, retrying..."
        MIGRATION_ATTEMPT=$((MIGRATION_ATTEMPT+1))
        sleep 2
    fi
done

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