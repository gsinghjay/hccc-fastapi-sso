# Stage 1: Build stage
FROM python:3.12-slim as builder

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_HOME=/opt/poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && cd /usr/local/bin \
    && ln -s /opt/poetry/bin/poetry

# Set work directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Configure Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --only main

# Stage 2: Runtime stage
FROM python:3.12-slim

# Create non-root user
RUN useradd -m -u 1000 appuser

# Set work directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Set ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Configure worker settings
# Number of workers per CPU core
ENV WEB_CONCURRENCY=2
# Maximum number of workers
ENV MAX_WORKERS=8
ENV HOST=0.0.0.0
ENV PORT=8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Command to run the application with Gunicorn and Uvicorn workers
CMD gunicorn app.main:app \
    --bind ${HOST}:${PORT} \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers ${MAX_WORKERS} \
    --worker-connections 1000 \
    --forwarded-allow-ips "*" \
    --proxy-allow-from "*" \
    --log-level info \
    --error-logfile - \
    --access-logfile - \
    --timeout 120 