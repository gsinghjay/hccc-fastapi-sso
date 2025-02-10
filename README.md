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

This roadmap outlines the steps for building the application using Test-Driven Development. Each step involves writing tests *before* implementing the corresponding code. Status indicators: ✅ Complete, 🟡 Partially Complete, 🔴 Not Started/Empty.

1.  **Project Setup:** ✅
    *   Initialize Poetry project: `poetry init` and configure `pyproject.toml`.
    *   Create project directory structure using the `create_project.sh` script.
    *   Create a basic `.gitignore`.
    *   Set up Ruff, Black, and Mypy configurations in `pyproject.toml`.
    *   Create `.env.example`.

2.  **Core Configuration:** ✅
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

3.  **Database Setup (SQLAlchemy & PostgreSQL):** 🟡
    *   🟡 **Test:** Write tests for `app/db/session.py` to ensure it creates a database engine and session correctly.
    *   🔴 **Implement:** Create `app/db/session.py` to establish a SQLAlchemy engine and session (empty file).
    *   ✅ **Test & Implement:** Base class for declarative models in `app/db/base.py`.

4.  **User Model (SQLAlchemy):** 🟡
    *   🔴 **Test:** Tests for `app/models/user.py` not implemented.
    *   🟡 **Implement:** Basic file structure created, implementation pending.

5.  **User Schemas (Pydantic):** 🟡
    *   ✅ **Test & Implement:** Base schemas in `app/schemas/base.py`.
    *   ✅ **Test & Implement:** Health check schemas in `app/schemas/health.py`.
    *   🟡 **Test & Implement:** Basic file structure for user schemas created.

6.  **Authentication Dependencies:** 🟡
    *   🔴 **Test:** Tests for `app/dependencies/auth.py` not implemented.
    *   🟡 **Implement:** Basic file structure created, implementation pending.

7.  **Security Utilities:** 🟡
    *   🔴 **Test:** Tests for `app/core/security.py` not implemented.
    *   🟡 **Implement:** Basic file structure created, implementation pending.

8.  **API Endpoints (Authentication):** 🟡
    *   🔴 **Test:** Authentication endpoint tests not implemented.
    *   🟡 **Implement:** Basic file structure and routing setup created.

9.  **API Endpoints (User Management):** 🟡
    *   🔴 **Test:** User management endpoint tests not implemented.
    *   🟡 **Implement:** Basic file structure and routing setup created.

10. **Main Application File:** ✅
    *   ✅ **Test:** FastAPI app creation and setup tests implemented.
    *   ✅ **Implement:** `app/main.py` fully implemented with FastAPI initialization and middleware setup.

11. **API Router:** ✅
    *   ✅ **Implement:** `app/api/router.py` implemented with proper route configuration.

12. **Middleware:** ✅
    *   ✅ **Test:** Middleware tests implemented.
    *   ✅ **Implement:** `app/core/middleware.py` implemented with:
        - Request ID tracking
        - Timing middleware
        - Security headers
        - CORS configuration
        - Rate limiting

13. **Logging:** 🟡
    *   🔴 **Test:** Logging tests not implemented.
    *   🟡 **Implement:** Basic file structure created, implementation pending.

14. **Alembic Migrations:** 🟡
    *   ✅ Initialize Alembic: `alembic init alembic`.
    *   ✅ Configure `alembic/env.py`.
    *   🔴 Generate initial migration for user table.
    *   🔴 Apply migrations.

15. **Testing Setup (conftest.py):** 🟡
    *   ✅ Basic test configuration implemented.
    *   ✅ E2E testing framework with Playwright set up.
    *   🟡 Some fixtures implemented (async_client).
    *   🔴 Database session fixture not implemented.

16. **Docker Compose:** ✅
    *   ✅ Create `docker-compose.yml` with all required services.
    *   ✅ Configure Traefik for both development and production.
    *   ✅ SSL termination configuration.

17. **Run and Test:** 🟡
    *   ✅ Local development setup working.
    *   ✅ Docker Compose setup working.
    *   🟡 Partial test coverage (config, health endpoint).
    *   🔴 Comprehensive test suite pending.

18. **Services Layer:** 🟡
    *   🔴 **Test:** Service layer tests not implemented.
    *   🟡 **Implement:** Basic service layer structure created in `app/services/`.

## Future Enhancements

*   **QR Code Plugin:** Implement the QR code functionality as a separate module, following the same TDD approach.
*   **Rate Limiting:** Add rate limiting to prevent abuse.
*   **More Advanced Authentication:** Explore options like social login, multi-factor authentication, etc.
*   **Email Verification:** Implement email verification for new user registrations.
*   **Password Reset:** Add functionality for users to reset their passwords.
*   **Admin Panel:** Create an admin interface for managing users and other resources.