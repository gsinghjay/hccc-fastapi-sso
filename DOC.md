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

### Architecture

The application follows a clean architecture pattern with the following layers:

#### Presentation Layer (API Endpoints)
- Handled by FastAPI routers in `app/api/v1/`
- Validates input using Pydantic schemas
- Returns standardized responses

#### Service Layer (Business Logic)
- Located in `app/services/`
- Encapsulates business logic
- Orchestrates operations between repositories
- Independent of web framework and database

#### Repository Layer (Data Access)
- Defined in `app/repositories/`
- Provides abstraction over data access
- Implements repository pattern using SQLAlchemy

#### Data Model Layer
- SQLAlchemy models in `app/models/`
- Defines database structure
- Provides ORM interface

#### Core Layer
- Configuration management (`app/core/config.py`)
- Security utilities (`app/core/security.py`)
- Password hashing (`app/core/hashing.py`)
- Middleware (`app/core/middleware.py`)

### Service Layer

The application implements several services that encapsulate business logic:

#### Auth Service (`app/services/auth.py`)

```python
class AuthService:
    async def authenticate_user(self, email: str, password: str) -> str:
        """
        Authenticates user and returns JWT token.
        
        Args:
            email: User's email address
            password: User's password
            
        Returns:
            str: JWT access token
            
        Raises:
            UserNotFoundError: If user not found
            AuthenticationError: If password is invalid
        """
```

#### Health Service (`app/services/health.py`)

```python
class HealthService:
    async def get_health_status(self) -> HealthResponse:
        """
        Checks system health including database connectivity.
        
        Returns:
            HealthResponse: Health check results including:
                - System metrics (CPU, memory, disk usage)
                - Database connectivity status
                - Service uptime
        """
        
    async def get_system_metrics(self) -> SystemMetrics:
        """
        Retrieves current system resource usage.
        
        Returns:
            SystemMetrics: CPU, memory and disk usage metrics
        """
```

#### User Service (`app/services/user.py`)

```python
class UserService:
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """
        Creates a new user.
        
        Args:
            user_data: User creation data including email and password
            
        Returns:
            UserResponse: Created user data
            
        Raises:
            EmailAlreadyExistsError: If email is already registered
        """
    
    async def get_user(self, user_id: UUID) -> UserResponse:
        """
        Retrieves a user by ID.
        
        Args:
            user_id: UUID of the user
            
        Returns:
            UserResponse: User data if found
            
        Raises:
            UserNotFoundError: If user not found
        """
    
    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> UserResponse:
        """
        Updates user information.
        
        Args:
            user_id: UUID of the user to update
            user_data: Updated user data
            
        Returns:
            UserResponse: Updated user data
            
        Raises:
            UserNotFoundError: If user not found
            EmailAlreadyExistsError: If new email is already registered
        """
```

### Domain Exceptions

Custom exceptions provide rich error context:

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

### Testing

The application includes comprehensive test coverage using pytest. Tests are organized by layer and type:

#### Service Tests (`tests/services/`)

- **Auth Service Tests** (`test_auth.py`):
  ```python
  def test_authenticate_user_success():
      """Test successful user authentication."""
      
  def test_authenticate_user_invalid_password():
      """Test authentication with invalid password."""
      
  def test_authenticate_user_not_found():
      """Test authentication with non-existent user."""
  ```

- **User Service Tests** (`test_user.py`):
  ```python
  def test_create_user_success():
      """Test successful user creation."""
      
  def test_create_user_duplicate_email():
      """Test user creation with existing email."""
      
  def test_update_user_success():
      """Test successful user update."""
  ```

#### API Tests (`tests/api/`)

- **Auth API Tests** (`test_auth_api.py`):
  ```python
  async def test_login_success():
      """Test successful login endpoint."""
      
  async def test_verify_token():
      """Test token verification endpoint."""
  ```

- **User API Tests** (`test_user_api.py`):
  ```python
  async def test_register_user():
      """Test user registration endpoint."""
      
  async def test_get_current_user():
      """Test get current user endpoint."""
  ```

#### Test Configuration

Test-specific settings and fixtures:

```python
# tests/conftest.py
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

### Dependencies

Core dependencies include:

*   **Python**: `>=3.12`
    - Modern Python features and type hints
*   **FastAPI**: `>=0.115.0`
    - High-performance async web framework
*   **Pydantic**: `>=2.7.0`
    - Data validation using Python type annotations
*   **Pydantic-Settings**: `>=2.2.1`
    - Settings management using Pydantic
*   **Uvicorn**: `>=0.27.0`
    - Lightning-fast ASGI server
*   **SQLAlchemy**: `>=2.0.27`
    - SQL toolkit and ORM
*   **Alembic**: `>=1.13.1`
    - Database migration tool
*   **Asyncpg**: `>=0.29.0`
    - Async PostgreSQL driver
*   **Poetry**: For dependency management
*   **PostgreSQL**: Database
*   **Docker**: For containerization and deployment

Development dependencies:

*   **Pytest**: `>=8.0.0`
    - Testing framework
*   **Pytest-asyncio**: `>=0.23.5`
    - Async test support
*   **Pytest-cov**: `>=4.1.0`
    - Test coverage reporting
*   **Black**: `>=24.1.1`
    - Code formatting
*   **Ruff**: `>=0.2.1`
    - Fast Python linter
*   **Mypy**: `>=1.8.0`
    - Static type checking

Refer to `pyproject.toml` for a complete list of dependencies.

### Advanced Usage

#### Docker Deployment

The repository includes comprehensive Docker support:

- **Development**: Use `docker-compose.yml`
  ```bash
  docker compose up -d
  ```

- **Production**: Use `docker-compose.prod.yml` with Traefik
  ```bash
  docker compose -f docker-compose.prod.yml up -d
  ```

#### Database Migrations

Alembic is configured for database schema migrations:

```bash
# Create a new migration
docker compose run --rm app alembic revision --autogenerate -m "description"

# Run migrations
docker compose run --rm app alembic upgrade head

# Rollback one version
docker compose run --rm app alembic downgrade -1
```

#### Security Headers

Traefik is configured with security headers in `docker/traefik/dynamic/security-headers.yml`:

```yaml
headers:
  customResponseHeaders:
    X-Frame-Options: "DENY"
    X-Content-Type-Options: "nosniff"
    X-XSS-Protection: "1; mode=block"
    Referrer-Policy: "strict-origin-when-cross-origin"
    Strict-Transport-Security: "max-age=31536000; includeSubDomains"
```

#### CORS Middleware

CORS is configured via middleware in `app/core/middleware.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```