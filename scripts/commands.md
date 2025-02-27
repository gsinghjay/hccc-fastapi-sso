# Project Commands Reference

This document contains commonly used commands for the HCCC FastAPI SSO project. These commands can be used as a reference for creating Ansible playbooks or other automation scripts.

## Development Setup

### Initialize Project
```bash
# Create required networks
docker network create web
docker network create backend

# Copy environment file
cp .env.example .env

# Start all services
docker compose up -d

# Install Playwright browsers
docker compose run --rm app playwright install --with-deps chromium
```

## Testing Commands

### Run All Tests
```bash
# Run all tests
docker compose run --rm app poetry run pytest -v

# Run tests in parallel
docker compose run --rm app poetry run pytest -n auto

# Run tests with specific markers
docker compose run --rm app poetry run pytest -m "db"  # Database tests
docker compose run --rm app poetry run pytest -m "e2e"  # E2E tests
docker compose run --rm app poetry run pytest -m "unit"  # Unit tests

# Run tests with output streaming
docker compose run --rm app poetry run pytest -v --capture=no
```

### Coverage Reports
```bash
# Generate coverage reports (XML and Terminal)
docker compose run --rm app poetry run pytest -v --cov=app --cov-report=xml:coverage-reports/coverage.xml --cov-report=term-missing

# Generate only terminal report with missing lines
docker compose run --rm app poetry run pytest -v --cov=app --cov-report=term-missing

# Fix coverage report permissions
sudo chown -R $USER:$USER coverage-reports/
chmod -R 777 coverage-reports/
```

## Database Operations

### Database Management
```bash
# Create database migrations
docker compose run --rm app alembic revision --autogenerate -m "migration_name"

# Apply migrations
docker compose run --rm app alembic upgrade head

# Rollback migrations
docker compose run --rm app alembic downgrade -1

# Reset test database
docker compose stop test_db
docker compose rm -f test_db
docker compose up -d test_db
```

### Database Backup and Restore
```bash
# Backup main database
docker compose exec db pg_dump -U ${POSTGRES_USER} -d ${POSTGRES_DB} > backup.sql

# Restore main database
docker compose exec -T db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} < backup.sql

# Create timestamped backup
docker compose exec db pg_dump -U ${POSTGRES_USER} -d ${POSTGRES_DB} > backup_$(date +%Y%m%d_%H%M%S).sql
```

## Code Quality

### Project Structure
```bash
# Show project structure (respecting .gitignore)
tree --gitignore

# Show project structure with additional details
tree --gitignore -a -I '.git'  # Show hidden files except .git
tree --gitignore -L 2          # Limit to 2 levels deep
tree --gitignore -P '*.py'     # Show only Python files
```

### Linting and Formatting
```bash
# Run all code quality checks
docker compose run --rm app poetry run ruff check .
docker compose run --rm app poetry run black --check .
docker compose run --rm app poetry run mypy .

# Fix code formatting
docker compose run --rm app poetry run ruff check --fix .
docker compose run --rm app poetry run black .

# Run all checks in sequence
docker compose run --rm app sh -c "poetry run ruff check . && poetry run black --check . && poetry run mypy ."
```

## Dependency Management

### Poetry Commands
```bash
# Add new dependency
docker compose run --rm app poetry add package_name

# Add development dependency
docker compose run --rm app poetry add --group dev package_name

# Update dependencies
docker compose run --rm app poetry update

# Export requirements
docker compose run --rm app poetry export -f requirements.txt --output requirements.txt

# Export dev requirements
docker compose run --rm app poetry export --with dev -f requirements.txt --output requirements-dev.txt
```

## Docker Operations

### Container Management
```bash
# Rebuild specific service
docker compose build app

# View logs
docker compose logs -f app

# Restart services
docker compose restart app

# Clean up
docker compose down -v  # Remove volumes
docker system prune -f  # Clean unused resources

# Remove orphaned containers
docker compose down --remove-orphans
```

### Health Checks
```bash
# Check application health
curl -f "http://localhost:8000/api/v1/health"

# Check database connection
docker compose exec db pg_isready -U ${POSTGRES_USER}

# Check test database connection
docker compose exec test_db pg_isready -U ${TEST_POSTGRES_USER}

# Check all services health
docker compose ps --format 'table {{.Name}}\t{{.Status}}'
```

## Production Deployment

### SSL/TLS
```bash
# Generate self-signed certificates for development
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ./docker/traefik/certs/local-key.pem \
  -out ./docker/traefik/certs/local-cert.pem \
  -subj "/CN=localhost"

# Verify SSL configuration
curl -k https://localhost/api/v1/health
```

### Performance Testing
```bash
# Run load test with wrk
wrk -t12 -c400 -d30s http://localhost:8000/api/v1/health

# Monitor resource usage
docker stats app db test_db traefik

# Run load test with Apache Benchmark
ab -n 1000 -c 100 http://localhost:8000/api/v1/health
```

## Ansible Variables Example
```yaml
# Example variables for Ansible playbook
project_vars:
  project_name: "hccc-fastapi-sso"
  docker_networks:
    - "web"
    - "backend"
  containers:
    - name: "app"
      image: "fastapi_app"
    - name: "db"
      image: "postgres:16-alpine"
    - name: "test_db"
      image: "postgres:16-alpine"
    - name: "traefik"
      image: "traefik:v2.10"
  env_files:
    template: ".env.example"
    target: ".env"
  test_commands:
    all: "docker compose run --rm app poetry run pytest -v"
    coverage: "docker compose run --rm app poetry run pytest -v --cov=app --cov-report=html:coverage-reports/html --cov-report=term-missing"
    db: "docker compose run --rm app poetry run pytest -m 'db'"
    e2e: "docker compose run --rm app poetry run pytest -m 'e2e'"
  coverage_dir: "/app/coverage-reports"
  database:
    main:
      name: "user_management"
      port: 5432
    test:
      name: "test_user_management"
      port: 5432
  resource_limits:
    test_db:
      cpu: 0.5
      memory: "512M"
```

## Common Issues and Solutions

### Permission Issues
```bash
# Fix coverage report permissions
sudo chown -R $USER:$USER coverage-reports/
chmod -R 777 coverage-reports/

# Fix Docker socket permissions
sudo chmod 666 /var/run/docker.sock

# Fix mounted volume permissions
docker compose run --rm app chown -R 1000:1000 /app/coverage-reports
```

### Database Issues
```bash
# Reset database connections
docker compose exec db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '${POSTGRES_DB}';"

# Verify database migrations
docker compose run --rm app alembic current

# Check database size
docker compose exec db psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "SELECT pg_size_pretty(pg_database_size('${POSTGRES_DB}'));"
```

### Container Issues
```bash
# Full reset of environment
docker compose down -v
docker system prune -f
docker compose up -d

# Check container logs for specific service
docker compose logs -f --tail=100 app

# Inspect container configuration
docker compose config

# Check container resource usage
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
```

Note: Replace environment variables (${VARIABLE}) with actual values when using in Ansible playbooks or scripts. 
