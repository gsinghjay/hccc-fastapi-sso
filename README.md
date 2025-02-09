# HCCC FastAPI SSO

This project implements a production-ready FastAPI application for HCCC (Hudson County Community College), designed for extensibility and starting with user management. It follows best practices for security, maintainability, and scalability.

## Project Overview

This backend API is built using FastAPI and Python 3.12, emphasizing a modular structure, asynchronous operations, and robust testing. It's designed to serve as a foundation for a Single Sign-On (SSO) system, initially focusing on user management, with future extensions planned (like a QR code plugin).

## Key Technologies & Features

*   **FastAPI:** A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
*   **Python 3.12:** The latest Python version, offering improved performance and syntax.
*   **SQLAlchemy:** A powerful and flexible SQL toolkit and Object-Relational Mapper (ORM).
*   **PostgreSQL:** A robust, open-source relational database system.  We'll use separate databases for production and testing.
*   **OAuth2 with JWT Tokens:** Integrated directly into FastAPI for secure authentication and authorization.
*   **CORS (Cross-Origin Resource Sharing):** Enabled to allow requests from different origins (e.g., your frontend).
*   **Environment Variables:** Used for configuration, keeping sensitive data out of the codebase.
*   **Alembic:** Database migrations for managing schema changes.
*   **Ruff, Black, Mypy:** Code linting, formatting, and static type checking for code quality and consistency.
*   **Poetry:** Dependency management and packaging.
*   **UUIDs:** Used as primary keys for database records, enhancing security and scalability.
*   **Asynchronous Operations:** `async` and `await` are used extensively for non-blocking I/O operations.
*   **Gunicorn:** A production-ready WSGI HTTP Server for Python applications.
*   **Structured Logging (Loki):** Logs are formatted for easy ingestion by Loki, including file, class, function name, and event details, output to stdout.
*   **Test-Driven Development (TDD):** Comprehensive unit and integration tests using pytest and `httpx.AsyncClient`.
*   **Docker Compose:** Used for containerization and orchestration of the application, database, and reverse proxy.
*   **Traefik:** A modern reverse proxy and load balancer to handle routing, SSL termination, and potentially other middleware concerns.
*   **Vanilla JavaScript Frontend:** The initial frontend will be built with vanilla JavaScript.

## Project Structure

The project follows a modular structure, promoting separation of concerns and maintainability:

```
hccc-fastapi-sso/
├── app/                     # Main application code
│   ├── api/                 # API endpoints
│   │   ├── v1/              # Version 1 of the API
│   │   │   ├── __init__.py
│   │   │   ├── auth.py      # Authentication endpoints
│   │   │   ├── health.py    # Health check endpoint
│   │   │   └── users.py     # User management endpoints
│   │   ├── router.py        # API router configuration
│   │   └── __init__.py
│   ├── core/                # Core application logic
│   │   ├── config.py        # Configuration settings
│   │   ├── security.py      # Security utilities
│   │   ├── logging.py       # Logging configuration
│   │   ├── middleware.py    # Custom middleware
│   │   └── __init__.py
│   ├── db/                  # Database-related code
│   │   ├── base.py          # Base class for models
│   │   ├── session.py       # Database session management
│   │   └── __init__.py
│   ├── dependencies/        # Dependency injection
│   │   ├── auth.py          # Authentication dependencies
│   │   └── __init__.py
│   ├── models/              # SQLAlchemy models
│   │   ├── base.py          # Base model configuration
│   │   ├── user.py          # User model
│   │   └── __init__.py
│   ├── schemas/             # Pydantic models
│   │   ├── base.py          # Base schemas
│   │   ├── health.py        # Health check schemas
│   │   ├── user.py          # User schemas
│   │   └── __init__.py
│   ├── services/            # Business logic layer
│   │   ├── user.py          # User service
│   │   └── __init__.py
│   ├── main.py              # Application entry point
│   └── __init__.py
├── local-docs/              # Local documentation (gitignored)
├── local-research/          # Research notes (gitignored)
├── scripts/                 # Utility scripts
│   └── run_e2e_tests.sh     # E2E test runner
├── tests/                   # Test suite
│   ├── api/                 # API tests
│   │   └── v1/              # Version 1 API tests
│   │       └── test_health.py
│   ├── core/                # Core module tests
│   │   └── test_config.py
│   ├── db/                  # Database tests
│   ├── e2e/                 # End-to-end tests
│   │   ├── pages/           # Page object models
│   │   │   └── base_page.py
│   │   ├── conftest.py      # E2E test configuration
│   │   └── test_health.py
│   ├── services/            # Service layer tests
│   ├── conftest.py          # Main test configuration
│   └── __init__.py
├── alembic/                 # Database migrations
│   └── env.py               # Alembic configuration
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore rules
├── pyproject.toml           # Poetry configuration
├── poetry.lock              # Dependency lock file
├── README.md                # Project documentation
├── SPEC.md                  # Technical specifications
└── create_project.sh        # Initial project structure setup script
```

## Development Roadmap (TDD)

This roadmap outlines the steps for building the application using Test-Driven Development.  Each step involves writing tests *before* implementing the corresponding code.

1.  **Project Setup:**
    *   Initialize Poetry project: `poetry init` and configure `pyproject.toml`.
    *   Create project directory structure using the `create_project.sh` script.
    *   Create a basic `.gitignore`.
    *   Set up Ruff, Black, and Mypy configurations in `pyproject.toml`.
    *   Create `.env.example`.

2.  **Core Configuration:**
    *   ✅ **Test:** Write tests for `app/core/config.py` to ensure it correctly loads environment variables and provides default values.
    *   ✅ **Implement:** Create `app/core/config.py` to load settings from environment variables using `pydantic-settings`.
    *   Key features implemented:
        - Type-safe configuration using Pydantic v2
        - Secure handling of sensitive data with `SecretStr`
        - Environment variable support with `.env` fallback
        - Validation for critical settings (SECRET_KEY, CORS origins)
        - Computed properties for API paths and database URI
        - Settings caching for performance
        - 98% test coverage

3.  **Database Setup (SQLAlchemy & PostgreSQL):**
    *   **Test:** Write tests for `app/db/session.py` to ensure it creates a database engine and session correctly, using the configured database URL.  Test both production and testing database configurations.
    *   **Implement:** Create `app/db/session.py` to establish a SQLAlchemy engine and session, using `asyncpg` for asynchronous database interaction.  Create separate settings for the production and testing databases.
    ```python:app/db/session.py
    startLine: 1
    endLine: 1
    ```
    *   **Test:** Write tests for `app/db/base.py` to ensure it provides a base class for declarative models.
    *   **Implement:** Create `app/db/base.py` to define a base class for SQLAlchemy models.
    ```python:app/db/base.py
    startLine: 1
    endLine: 1
    ```

4.  **User Model (SQLAlchemy):**
    *   **Test:** Write tests for `app/models/user.py` to ensure the User model has the correct fields (id: UUID, username, email, hashed_password, etc.) and relationships.
    *   **Implement:** Create `app/models/user.py` defining the SQLAlchemy User model. Use UUID as the primary key.
    ```python:app/models/user.py
    startLine: 1
    endLine: 1
    ```

5.  **User Schemas (Pydantic):**
    *   **Test:** Write tests for `app/schemas/user.py` to ensure the User schemas (UserCreate, UserRead, UserUpdate, UserInDB) correctly validate and serialize/deserialize user data. Test for required fields, email validation, password constraints, etc.
    *   **Implement:** Create `app/schemas/user.py` defining Pydantic schemas for user-related data.  Create separate schemas for input (creation, update), output (reading), and database representation.
    ```python:app/schemas/user.py
    startLine: 1
    endLine: 1
    ```
    *   **Test:** Write tests for `app/schemas/base.py`
    *   **Implement:** Create `app/schemas/base.py`
    ```python:app/schemas/base.py
    startLine: 1
    endLine: 25
    ```

6.  **Authentication Dependencies:**
    *   **Test:** Write tests for `app/dependencies/auth.py` to verify the OAuth2PasswordBearer setup, token URL, and any helper functions for dependency injection.
    *   **Implement:** Create `app/dependencies/auth.py` to define authentication-related dependencies, including the `OAuth2PasswordBearer` instance.
    ```python:app/dependencies/auth.py
    startLine: 1
    endLine: 1
    ```

7.  **Security Utilities:**
    *   **Test:** Write tests for `app/core/security.py` to ensure password hashing (using `passlib` and bcrypt) and JWT creation/verification (using `python-jose`) work correctly.
    *   **Implement:** Create `app/core/security.py` with functions for password hashing and JWT handling.
    ```python:app/core/security.py
    startLine: 1
    endLine: 1
    ```

8.  **API Endpoints (Authentication):**
    *   **Test:** Write tests for `app/api/v1/auth.py` to cover:
        *   Token creation (POST /token): Test with valid/invalid credentials, different grant types, and error handling.
        *   Getting the current user (GET /users/me): Test with valid/invalid tokens, expired tokens, and error handling.
    *   **Implement:** Create `app/api/v1/auth.py` with endpoints for user authentication:
        *   `/token`: For obtaining JWT tokens (using OAuth2 password flow).
        *   `/users/me`: For retrieving the current user's information.
    ```python:app/api/v1/auth.py
    startLine: 1
    endLine: 1
    ```

9.  **API Endpoints (User Management):**
    *   **Test:** Write tests for `app/api/v1/users.py` to cover:
        *   User creation (POST /users/): Test with valid/invalid data, duplicate usernames/emails, and error handling.
        *   Reading users (GET /users/{user_id}): Test with valid/invalid user IDs, non-existent users, and error handling.
        *   Updating users (PUT /users/{user_id}): Test with valid/invalid data, updating different fields, and error handling.
        *   Deleting users (DELETE /users/{user_id}): Test with valid/invalid user IDs, and error handling.
    *   **Implement:** Create `app/api/v1/users.py` with CRUD (Create, Read, Update, Delete) endpoints for user management. Use dependency injection to get the database session and current user.
    ```python:app/api/v1/users.py
    startLine: 1
    endLine: 1
    ```

10. **Main Application File:**
    *   **Test:** Write tests for `app/main.py` to ensure the FastAPI app is created correctly, middleware is set up, and API routers are included.
    *   **Implement:** Create `app/main.py` to initialize the FastAPI application, include API routers, and set up middleware (CORS).
    ```python:app/main.py
    startLine: 1
    endLine: 36
    ```

11. **API Router:**
     *   **Implement:** Create `app/api/router.py`
     ```python:app/api/router.py
     startLine: 1
     endLine: 13
     ```

12. **Middleware:**
    *   **Test:** Write tests for `app/core/middleware.py` to ensure CORS middleware is configured correctly.
    *   **Implement:** Create `app/core/middleware.py` to set up CORS middleware.
    ```python:app/core/middleware.py
    startLine: 1
    endLine: 21
    ```

13. **Logging:**
    *   **Test:** Write tests for `app/core/logging.py` to verify that the logging configuration outputs structured logs in the correct format (including file, class, function, and message) to stdout.
    *   **Implement:** Create `app/core/logging.py` to configure structured logging for Gunicorn, targeting Loki.

14. **Alembic Migrations:**
    *   Initialize Alembic: `alembic init alembic`.
    *   Configure `alembic/env.py` to connect to the database using the settings from `app/core/config.py`.
    *   Generate initial migration: `alembic revision -m "Create user table"`.
    *   Apply migrations: `alembic upgrade head`.

15. **Testing Setup (conftest.py):**
    *   Create `tests/conftest.py` to define pytest fixtures:
        *   `async_client`: An asynchronous HTTP client for testing the API (using `httpx.AsyncClient`).
        *   `db_session`: A database session fixture that creates and drops tables before/after each test, using a separate testing database.  Use transactions and rollbacks for test isolation.

16. **Docker Compose:**
    *   Create `docker-compose.yml` to define services:
        *   `app`: The FastAPI application (using Gunicorn).
        *   `db`: The PostgreSQL database.
        *   `traefik`: The Traefik reverse proxy.
    *   Configure Traefik to handle routing and SSL termination (using Let's Encrypt or similar).

17. **Run and Test:**
    *   Run the application locally using Poetry: `poetry run uvicorn app.main:app --reload`.
    *   Run tests using Poetry: `poetry run pytest`.
    *   Run the application and database using Docker Compose: `docker-compose up --build`.

18. **Continuous Integration (CI):**
     * Configure the CI to run tests, linting, and type checking on every push and pull request.

## Future Enhancements

*   **QR Code Plugin:** Implement the QR code functionality as a separate module, following the same TDD approach.
*   **Rate Limiting:** Add rate limiting to prevent abuse.
*   **More Advanced Authentication:** Explore options like social login, multi-factor authentication, etc.
*   **Email Verification:** Implement email verification for new user registrations.
*   **Password Reset:** Add functionality for users to reset their passwords.
*   **Admin Panel:** Create an admin interface for managing users and other resources.