# HCCC FastAPI SSO

## Documentation

### Overview

This repository contains a FastAPI application designed for user management and Single Sign-On (SSO). It is built for Hudson County Community College (HCCC). The application is designed to be production-ready, extensible, and follows security best practices. It uses Python 3.12, FastAPI, and PostgreSQL.

### Quick Start

1.  **Install Poetry**: Follow the official Poetry installation guide.
2.  **Clone Repository**: Clone this repository to your local machine.
3.  **Navigate to Project**:  `cd <repository-directory>`
4.  **Install Dependencies**: Run `poetry install` to install project dependencies.
5.  **Run Application**: Execute `poetry run fastapi dev app/main.py` to start the development server.
6.  **Access Documentation**: Open your browser and go to `/docs` to view the interactive API documentation.

### Configuration

The application is configured using environment variables. You can set these directly or using a `.env` file in the project root.

Key configuration parameters include:

*   **`PROJECT_NAME`**: Name of the project (default: `FastAPI User Management`).
*   **`API_PREFIX`**: Global API prefix (default: `/api`).
*   **`API_V1_STR`**: API version 1 path component (default: `v1`).
*   **`DEBUG`**: Enable debug mode (default: `False`).
*   **`SECRET_KEY`**: Secret key for JWT token generation (minimum 32 characters).
*   **`ACCESS_TOKEN_EXPIRE_MINUTES`**: JWT token expiration time in minutes (default: `11520` - 8 days).
*   **`BACKEND_CORS_ORIGINS`**: Allowed CORS origins (comma-separated string or list).
*   **`RATE_LIMIT_PER_MINUTE`**: Number of requests allowed per minute per client (default: `60`).
*   **`POSTGRES_SERVER`**: PostgreSQL server hostname (default: `localhost`).
*   **`POSTGRES_USER`**: PostgreSQL username (default: `postgres`).
*   **`POSTGRES_PASSWORD`**: PostgreSQL password (default: `your-secure-password`).
*   **`POSTGRES_DB`**: PostgreSQL database name (default: `user_management`).
*   **`POSTGRES_PORT`**: PostgreSQL port (default: `5432`).

Refer to `app/core/config.py` for complete configuration details and default values.

### API Documentation

Currently, the application implements a health check endpoint.

#### Health Check (`/health`)

*   **Endpoint**: `/api/v1/health`
*   **Method**: `GET`
*   **Summary**: Verifies the API service status.
*   **Response**:
    *   **200 OK**: Service is healthy. Returns a `HealthResponse` with status `healthy`.
    *   **500 Internal Server Error**: Service is unhealthy. Returns an `HTTPError` with error details.

    **Response Model (`HealthResponse`)**:

    ```json
    {
      "status": "healthy"
    }
    ```

    **Response Model (`HTTPError`)**:

    ```json
    {
      "detail": "Error message"
    }
    ```

### Dependencies

*   **Python**: `>=3.12`
*   **FastAPI**: `>=0.115.0`
*   **Pydantic**: `>=2.7.0`
*   **Pydantic-Settings**: `>=2.2.1`
*   **Uvicorn**: `>=0.27.0`
*   **SQLAlchemy**: `>=2.0.27`
*   **Alembic**: `>=1.13.1`
*   **Asyncpg**: `>=0.29.0`
*   **Poetry**: For dependency management.
*   **PostgreSQL**: Database.
*   **Docker**: For containerization and deployment (optional).

Refer to `pyproject.toml` for a complete list of dependencies.

### Advanced Usage

*   **Docker Deployment**: The repository includes `Dockerfile`, `docker-compose.yml`, and `docker-compose.prod.yml` for containerized deployment using Docker and Traefik as a reverse proxy.
*   **Database Migrations**: Alembic is configured for database schema migrations. Use `alembic` commands to manage database changes.
*   **Testing**:  `pytest` is used for unit and end-to-end testing. Run tests using `poetry run pytest`. End-to-end tests require Playwright and can be run with `poetry run pytest tests/e2e/ -m e2e`.
*   **Security Headers**: Traefik is configured to set security headers as defined in `docker/traefik/dynamic/security-headers.yml`.
*   **CORS Middleware**: CORS is configured via middleware in `app/core/middleware.py` using the `BACKEND_CORS_ORIGINS` setting.