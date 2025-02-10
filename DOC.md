# HCCC FastAPI SSO

## Documentation

### Overview

This repository contains a FastAPI application designed for user management and Single Sign-On (SSO). It is built for Hudson County Community College (HCCC). The application is designed to be production-ready, extensible, and follows security best practices. It uses Python 3.12, FastAPI, and PostgreSQL.

### Quick Start

1.  **Install Poetry**: Follow the official Poetry installation guide.
2.  **Clone Repository**: Clone this repository to your local machine.
3.  **Navigate to Project**:  `cd <repository-directory>`
4.  **Install Dependencies**: Run `poetry install` to install project dependencies.
5.  **Copy Environment File**: Run `cp .env.example .env` and update variables as needed.
6.  **Start Application**: Execute `docker compose up -d` to start the application and its dependencies using Docker Compose.
7.  **Access Documentation**: Open your browser and go to `/docs` to view the interactive API documentation.

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

### Service Layer

The application follows a clean architecture pattern with a well-defined service layer that encapsulates business logic.

#### Auth Service

The authentication service (`app/services/auth.py`) handles user authentication and token management:

```python
class AuthService:
    async def authenticate_user(self, email: str, password: str) -> str:
        """Authenticates user and returns JWT token."""
```

#### User Service

The user service (`app/services/user.py`) manages user operations:

```python
class UserService:
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """Creates a new user."""
    
    async def get_user(self, user_id: UUID) -> UserResponse:
        """Retrieves a user by ID."""
    
    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> UserResponse:
        """Updates user information."""
```

#### Domain Exceptions

Custom domain exceptions (`app/services/exceptions.py`) provide rich error context:

```python
class DomainError(Exception):
    """Base class for domain-specific errors."""
    def __init__(self, code: int, context: dict): ...

class UserNotFoundError(DomainError):
    """Raised when a user is not found."""

class EmailAlreadyExistsError(DomainError):
    """Raised when email is already registered."""

class AuthenticationError(DomainError):
    """Raised when authentication fails."""
```

### Testing

The application includes comprehensive test coverage using pytest. Tests are organized by layer and type.

#### Service Tests

Service layer tests (`tests/services/`) verify business logic:

- **Auth Service Tests** (`test_auth.py`):
  - Authentication success/failure scenarios
  - Token verification
  - Error handling

- **User Service Tests** (`test_user.py`):
  - User creation
  - Profile retrieval
  - Profile updates
  - Duplicate email handling

#### Test Configuration

Test-specific settings and fixtures:

```python
# tests/services/conftest.py
@pytest.fixture
def test_user() -> User:
    """Provides a consistent test user."""

@pytest.fixture
def mock_session() -> AsyncMock:
    """Provides a mock database session."""
```

#### Running Tests

Execute tests using Docker Compose:

```bash
# Run all tests
docker compose run --rm app poetry run pytest

# Run specific test file
docker compose run --rm app poetry run pytest tests/services/test_auth.py

# Run with coverage
docker compose run --rm app poetry run pytest --cov=app

# Run in parallel
docker compose run --rm app poetry run pytest -n auto
```

### API Documentation

The application implements several endpoints:

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
      "status": "healthy",
      "version": "1.0.0",
      "uptime_seconds": 3600.0,
      "system_metrics": {
        "cpu_usage": 45.2,
        "memory_usage": 62.7,
        "disk_usage": 78.1
      },
      "checks": {
        "database": {
          "status": "pass",
          "latency_ms": 12.3,
          "message": "Connected successfully",
          "last_checked": "2024-03-14T12:00:00Z"
        }
      }
    }
    ```

#### Authentication (`/auth`)

*   **Login**: `POST /api/v1/auth/login`
    - Authenticates user credentials
    - Returns JWT access token
    
*   **Verify**: `POST /api/v1/auth/verify`
    - Verifies JWT token
    - Returns decoded token data

#### User Management (`/users`)

*   **Register**: `POST /api/v1/users`
    - Creates new user account
    
*   **Profile**: `GET /api/v1/users/me`
    - Retrieves current user profile
    
*   **Update**: `PATCH /api/v1/users/me`
    - Updates user information

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
*   **Testing**: Run tests using `docker compose run --rm app poetry run pytest`. End-to-end tests require Playwright and can be run with `docker compose run --rm app poetry run pytest tests/e2e/ -m e2e`.
*   **Security Headers**: Traefik is configured to set security headers as defined in `docker/traefik/dynamic/security-headers.yml`.
*   **CORS Middleware**: CORS is configured via middleware in `app/core/middleware.py` using the `BACKEND_CORS_ORIGINS` setting.