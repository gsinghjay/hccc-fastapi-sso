
--- Repository Documentation ---

## HCCC FastAPI SSO Documentation

### 1. Repository Summary

This repository provides a FastAPI-based Single Sign-On (SSO) application. It focuses on user authentication, authorization, and management. The application uses Python, FastAPI, and PostgreSQL. It is designed for production environments with security and extensibility in mind.

### 2. Quick Start

#### Installation

1.  **Install Poetry:** Follow the official Poetry installation guide.
2.  **Clone Repository:** `git clone <repository-url>`
3.  **Navigate to Project:** `cd hccc-fastapi-sso`
4.  **Install Dependencies:** `poetry install`
5.  **Copy Environment File:** `cp .env.example .env` and update variables.
6.  **Start Application:** `docker compose up -d`

#### Basic Usage

After starting the application with Docker Compose, access the API documentation at `/docs` in your browser. This documentation details available endpoints for user management and authentication.

### 3. Configuration

The application is configured using environment variables.  A `.env` file in the project root can be used to set these variables.

**Key Configuration Variables:**

*   **`PROJECT_NAME`**:  Application name.
*   **`API_PREFIX`**: Global API URL prefix.
*   **`API_V1_STR`**: API version path component.
*   **`DEBUG`**: Enable debug mode (True/False).
*   **`SECRET_KEY`**: Secret key for JWT token generation (minimum 32 characters).
*   **`ACCESS_TOKEN_EXPIRE_MINUTES`**: JWT token expiration time (minutes).
*   **`BACKEND_CORS_ORIGINS`**: Allowed CORS origins (comma-separated list or JSON array).
*   **`RATE_LIMIT_PER_MINUTE`**:  Requests allowed per minute per client.
*   **`POSTGRES_SERVER`**: PostgreSQL server hostname.
*   **`POSTGRES_USER`**: PostgreSQL username.
*   **`POSTGRES_PASSWORD`**: PostgreSQL password.
*   **`POSTGRES_DB`**: PostgreSQL database name.
*   **`POSTGRES_PORT`**: PostgreSQL port.

Refer to `app/core/config.py` for a complete list and details.

### 4. API Documentation

The API provides endpoints for health checks, authentication, and user management.

#### Health Check API (`/health`)

*   **Endpoint:** `/api/v1/health`
*   **Method:** `GET`
*   **Summary:** Checks the service health status.
*   **Response (200 OK):** Returns a `HealthResponse` model with service status, version, uptime, system metrics (CPU, memory, disk usage), and database check status.
*   **Response (503 Service Unavailable):** Service is unhealthy.

#### Authentication API (`/auth`)

*   **Login (`/auth/login`)**
    *   **Endpoint:** `/api/v1/auth/login`
    *   **Method:** `POST`
    *   **Summary:** Authenticates user credentials and returns a JWT access token.
    *   **Request Body:** `LoginRequest` model with `email` and `password`.
    *   **Response (200 OK):** Returns a `TokenResponse` model with `access_token` and `token_type` ("bearer").
    *   **Response (401 Unauthorized):** Authentication failed.
    *   **Response (400 Bad Request):** Invalid credentials.

*   **Verify Token (`/auth/verify`)**
    *   **Endpoint:** `/api/v1/auth/verify`
    *   **Method:** `POST`
    *   **Summary:** Verifies a JWT token and returns decoded token data. Requires Bearer token in Authorization header.
    *   **Request Headers:** `Authorization: Bearer <JWT_TOKEN>`
    *   **Response (200 OK):** Returns `TokenData` model with decoded token information (`sub`, `email`, `exp`).
    *   **Response (401 Unauthorized):** Invalid or expired token.

#### User API (`/users`)

*   **Register User (`/users`)**
    *   **Endpoint:** `/api/v1/users`
    *   **Method:** `POST`
    *   **Summary:** Registers a new user.
    *   **Request Body:** `UserCreate` model with `email`, `password`, and `full_name`.
    *   **Response (201 Created):** Returns `UserResponse` model for the created user.
    *   **Response (409 Conflict):** Email already registered.
    *   **Response (400 Bad Request):** Invalid input.

*   **Get Current User (`/users/me`)**
    *   **Endpoint:** `/api/v1/users/me`
    *   **Method:** `GET`
    *   **Summary:** Retrieves the profile of the currently authenticated user. Requires Bearer token.
    *   **Request Headers:** `Authorization: Bearer <JWT_TOKEN>`
    *   **Response (200 OK):** Returns `UserResponse` model for the current user.
    *   **Response (401 Unauthorized):** Not authenticated.
    *   **Response (404 Not Found):** User not found.

*   **Update Current User (`/users/me`)**
    *   **Endpoint:** `/api/v1/users/me`
    *   **Method:** `PATCH`
    *   **Summary:** Updates the profile of the currently authenticated user. Requires Bearer token.
    *   **Request Headers:** `Authorization: Bearer <JWT_TOKEN>`
    *   **Request Body:** `UserUpdate` model with optional fields (`email`, `full_name`, `password`).
    *   **Response (200 OK):** Returns `UserResponse` model for the updated user.
    *   **Response (401 Unauthorized):** Not authenticated.
    *   **Response (404 Not Found):** User not found.
    *   **Response (409 Conflict):** Email already registered.
    *   **Response (400 Bad Request):** Invalid input.

### 5. Dependencies

*   **Python:** `>=3.12`
*   **FastAPI:** `>=0.115.0`
*   **Pydantic:** `>=2.7.0`
*   **Pydantic-Settings:** `>=2.2.1`
*   **Uvicorn:** `>=0.27.0`
*   **SQLAlchemy:** `>=2.0.27`
*   **Alembic:** `>=1.13.1`
*   **Asyncpg:** `>=0.29.0`
*   **Python-jose:** `>=3.3.0`
*   **Passlib:** `>=1.7.4`
*   **Bcrypt:** `>=4.0.1`
*   **Gunicorn:** `>=21.2.0`

Refer to `pyproject.toml` for the complete list of dependencies.

### 6. Advanced Usage Examples

#### Database Migrations

To create a new database migration:

```bash
docker compose run --rm app alembic revision --autogenerate -m "migration_description"
```

To apply migrations:

```bash
docker compose run --rm app alembic upgrade head
```

To rollback migrations:

```bash
docker compose run --rm app alembic downgrade -1
```

#### Running Tests

To run all tests:

```bash
docker compose run --rm app poetry run pytest
```

To run tests with coverage:

```bash
docker compose run --rm app poetry run pytest --cov=app
```

--- End of Documentation ---
