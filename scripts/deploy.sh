#!/bin/bash

# Exit on error
set -e

# Default values
ENV="dev"
COMPOSE_FILE="docker-compose.yml"
TRAEFIK_CONFIG="docker/traefik/traefik.dev.yml"

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -e|--environment) ENV="$2"; shift ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Set environment-specific configurations
if [ "$ENV" = "prod" ]; then
    COMPOSE_FILE="docker-compose.prod.yml"
    TRAEFIK_CONFIG="docker/traefik/traefik.prod.yml"
    
    # Ensure all required environment variables are set
    required_vars=(
        "DOMAIN"
        "ACME_EMAIL"
        "POSTGRES_PASSWORD"
        "JWT_SECRET_KEY"
        "TRAEFIK_DASHBOARD_PASSWORD_HASH"
    )
    
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            echo "Error: Required environment variable $var is not set"
            exit 1
        fi
    done
fi

# Create external network if it doesn't exist
docker network inspect web >/dev/null 2>&1 || docker network create web

# Ensure Traefik ACME directory exists with correct permissions
if [ "$ENV" = "prod" ]; then
    mkdir -p docker/traefik/acme
    chmod 600 docker/traefik/acme
fi

# Pull latest images
echo "Pulling latest images..."
docker-compose -f $COMPOSE_FILE pull

# Deploy the stack
echo "Deploying stack for $ENV environment..."
docker-compose -f $COMPOSE_FILE up -d

# Wait for services to be healthy
echo "Waiting for services to be healthy..."
timeout=300
elapsed=0
while [ $elapsed -lt $timeout ]; do
    if docker-compose -f $COMPOSE_FILE ps | grep -q "unhealthy"; then
        echo "Waiting for services to become healthy... ($elapsed seconds)"
        sleep 5
        elapsed=$((elapsed + 5))
    else
        echo "All services are healthy!"
        break
    fi
done

if [ $elapsed -ge $timeout ]; then
    echo "Timeout waiting for services to become healthy"
    exit 1
fi

# Display service status
echo "Service status:"
docker-compose -f $COMPOSE_FILE ps

echo "Deployment completed successfully!" 