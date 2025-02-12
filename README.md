# HCCC FastAPI SSO

This project implements a production-ready FastAPI application for HCCC (Hudson County Community College), designed for extensibility and starting with user management. It follows best practices for security, maintainability, and scalability.

## Project Overview

This backend API is built using FastAPI and Python 3.12, emphasizing a modular structure, asynchronous operations, and robust testing. It's designed to serve as a foundation for a Single Sign-On (SSO) system, initially focusing on user management, with future extensions planned (like a QR code plugin).

## Key Technologies & Features

*   **FastAPI:** A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
*   **Python 3.12:** The latest Python version, offering improved performance and syntax.
*   **SQLAlchemy:** A powerful and flexible SQL toolkit and Object-Relational Mapper (ORM).
*   **PostgreSQL:** A robust, open-source relational database system with dedicated test database support:
    - Separate databases for development, testing, and production
    - Automated test database setup and teardown
    - Resource-limited test database container (0.5 CPU, 512MB RAM)
    - Database healthchecks and proper isolation
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
*   **Test-Driven Development (TDD):** Comprehensive testing infrastructure:
    - Unit tests with pytest
    - Integration tests with `httpx.AsyncClient`
    - E2E tests with Playwright
    - Parallel test execution support
    - Isolated test database environment
    - Coverage reporting with proper permissions
    - Detailed test documentation and examples
*   **Docker Compose:** Used for containerization and orchestration of the application, databases, and reverse proxy.
*   **Traefik:** A modern reverse proxy and load balancer to handle routing, SSL termination, and potentially other middleware concerns.
*   **Vanilla JavaScript Frontend:** The initial frontend will be built with vanilla JavaScript.

## Project Structure

The project follows a modular structure, promoting separation of concerns and maintainability:

```
hccc-fastapi-sso/
├── alembic/                 # Database migrations
│   └── env.py               # Alembic configuration
├── app/                     # Main application code
│   ├── api/                 # API endpoints
│   │   ├── v1/              # Version 1 of the API
│   │   │   ├── auth.py      # Authentication endpoints
│   │   │   ├── health.py    # Health check endpoint
│   │   │   └── users.py     # User management endpoints
│   │   └── router.py        # API router configuration
│   ├── core/                # Core application logic
│   │   ├── config.py        # Configuration settings
│   │   ├── logging.py       # Logging configuration
│   │   ├── middleware.py    # Custom middleware
│   │   └── security.py      # Security utilities
│   ├── db/                  # Database-related code
│   │   ├── base.py          # Base class for models
│   │   └── session.py       # Database session management
│   ├── dependencies/        # Dependency injection
│   │   └── auth.py          # Authentication dependencies
│   ├── models/              # SQLAlchemy models
│   │   ├── base.py          # Base model configuration
│   │   └── user.py          # User model
│   ├── schemas/             # Pydantic models
│   │   ├── base.py          # Base schemas
│   │   ├── health.py        # Health check schemas
│   │   └── user.py          # User schemas
│   ├── services/            # Business logic layer
│   │   ├── health.py        # Health service
│   │   └── user.py          # User service
│   └── main.py              # Application entry point
├── coverage-reports/        # Test coverage reports
├── data/                    # Application data
│   ├── app/                 # App-specific data
│   ├── certs/               # SSL certificates
│   └── postgres/            # PostgreSQL data
├── docker/                  # Docker configuration
│   ├── postgres/            # PostgreSQL configuration
│   │   └── init-scripts/    # DB initialization scripts
│   └── traefik/             # Traefik configuration
│       ├── certs/           # SSL certificates
│       ├── dynamic/           # Dynamic configuration
│       │   ├── auth.dev.yml   # Dev auth config
│       │   └── auth.prod.yml  # Prod auth config
│       ├── traefik.dev.yml    # Dev Traefik config
│       └── traefik.prod.yml   # Prod Traefik config
├── docs/                    # Project documentation
├── scripts/                 # Utility scripts
│   ├── commands.md          # Command documentation
│   ├── deploy.sh            # Deployment script
│   └── run_e2e_tests.sh     # E2E test runner
├── tests/                   # Test suite
│   ├── api/                 # API tests
│   │   └── v1/              # Version 1 API tests
│   │       ├── conftest.py    # Test configuration
│   │       └── test_health.py # Health endpoint tests
│   ├── core/                # Core module tests
│   │   └── test_config.py   # Config tests
│   ├── db/                  # Database tests
│   ├── e2e/                 # End-to-end tests
│   │   ├── conftest.py      # E2E test configuration
│   │   ├── pages/             # Page object models
│   │   │   └── base_page.py   # Base page class
│   │   └── test_health.py     # Health E2E tests
│   ├── services/              # Service layer tests
│   └── conftest.py          # Main test configuration
├── CHANGELOG.md             # Project changelog
├── DOC.md                   # Additional documentation
├── Dockerfile               # Docker build configuration
├── docker-compose.yml       # Development compose config
├── docker-compose.prod.yml  # Production compose config
├── poetry.lock              # Dependency lock file
├── pyproject.toml           # Poetry configuration
├── pytest.ini               # Pytest configuration
└── README.md                # Project documentation
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

3.  **Database Setup (SQLAlchemy & PostgreSQL):** ✅
    *   ✅ **Test:** Write tests for `app/db/session.py` to ensure it creates a database engine and session correctly.
    *   ✅ **Implement:** Create `app/db/session.py` to establish a SQLAlchemy engine and session.
    *   ✅ **Test & Implement:** Base class for declarative models in `app/db/base.py`.
    *   Key features implemented:
        - Separate test database configuration
        - Resource-limited test database container
        - Database healthchecks
        - Proper test isolation
        - Parallel test execution support

4.  **User Model (SQLAlchemy):** ✅
    *   ✅ **Test:** Service layer tests implemented in `tests/services/test_user.py`.
    *   ✅ **Implement:** User model fully implemented in `app/models/user.py` with UUID primary key, email, password, and timestamps.

5.  **User Schemas (Pydantic):** 🔴
    *   ✅ **Test & Implement:** Base schemas in `app/schemas/base.py`.
    *   ✅ **Test & Implement:** Health check schemas in `app/schemas/health.py`.
    *   🔴 **Test & Implement:** User schemas not implemented, though referenced in code.

6.  **Authentication Dependencies:** 🟡
    *   🔴 **Test:** Tests for `app/dependencies/auth.py` not implemented.
    *   ✅ **Implement:** Basic authentication dependencies implemented with JWT token validation.

7.  **Security Utilities:** ✅
    *   ✅ **Test:** Security utility tests implemented in service layer tests.
    *   ✅ **Implement:** Security utilities implemented with password hashing and JWT token management.

8.  **API Endpoints (Authentication):** 🟡
    *   🔴 **Test:** API level tests not implemented.
    *   ✅ **Implement:** Authentication endpoints fully implemented (`/login`, `/verify`).
    *   ✅ **Service Tests:** Authentication service tests implemented.

9.  **API Endpoints (User Management):** 🟡
    *   🔴 **Test:** API level tests not implemented.
    *   ✅ **Implement:** User management endpoints implemented (`/users`, `/me`).
    *   ✅ **Service Tests:** User service tests implemented.

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
    *   🟡 **Implement:** Basic logging configuration present, needs enhancement.

14. **Alembic Migrations:** ✅
    *   ✅ Initialize Alembic: `alembic init alembic`.
    *   ✅ Configure `alembic/env.py`.
    *   ✅ Generate initial migration for user table.
    *   ✅ Apply migrations.
    *   Key features implemented:
        - Async-compatible migration setup
        - Proper SQLAlchemy model detection
        - Index creation for performance
        - Proper upgrade/downgrade paths
        - Migration history tracking

15. **Testing Setup (conftest.py):** ✅
    *   ✅ Basic test configuration implemented.
    *   ✅ E2E testing framework with Playwright set up.
    *   ✅ Database fixtures implemented.
    *   ✅ Test isolation and parallel execution configured.
    *   Key features implemented:
        - Separate test database support
        - Proper test isolation
        - Coverage reporting with permissions
        - Browser automation with Playwright
        - Database cleanup procedures
        - Comprehensive test documentation
        - Example test cases for all layers
        - Service layer test patterns

16. **Docker Compose:** ✅
    *   ✅ Create `docker-compose.yml` with all required services.
    *   ✅ Configure Traefik for both development and production.
    *   ✅ SSL termination configuration.
    *   ✅ Test database configuration with resource limits.

17. **Documentation:** ✅
    *   ✅ Comprehensive API documentation with examples
    *   ✅ Detailed architecture documentation
    *   ✅ Service layer documentation with docstrings
    *   ✅ Testing documentation with examples
    *   ✅ Deployment guides for development and production
    *   Key features documented:
        - Clean architecture patterns
        - Service layer design
        - Repository pattern implementation
        - Testing strategies and examples
        - Security configurations
        - Database management
        - Docker deployment

18. **Run and Test:** 🟡
    *   ✅ Local development setup working.
    *   ✅ Docker Compose setup working.
    *   ✅ Database testing infrastructure complete.
    *   ✅ Service layer tests implemented.
    *   ✅ Test documentation complete.
    *   🔴 API level tests pending.
    *   🔴 E2E tests pending.

19. **Services Layer:** ✅
    *   ✅ **Test:** Service layer tests fully implemented for both auth and user services.
    *   ✅ **Implement:** Service layer fully implemented with proper error handling and business logic.
    *   ✅ **Document:** Comprehensive service layer documentation with examples.

## Future Enhancements

*   **QR Code Plugin:** Implement the QR code functionality as a separate module, following the same TDD approach.
*   **Rate Limiting:** Add rate limiting to prevent abuse.
*   **More Advanced Authentication:** Explore options like social login, multi-factor authentication, etc.
*   **Email Verification:** Implement email verification for new user registrations.
*   **Password Reset:** Add functionality for users to reset their passwords.
*   **Admin Panel:** Create an admin interface for managing users and other resources.

## Quick Start for Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/hccc-fastapi-sso.git
   cd hccc-fastapi-sso
   ```

2. Copy environment variables:
   ```bash
   cp .env.example .env
   # Update the variables as needed
   ```

3. Start the services:
   ```bash
   docker compose up -d
   ```

4. Run the tests:
   ```bash
   # Run all tests
   docker compose run --rm app poetry run pytest

   # Run only database tests
   docker compose run --rm app poetry run pytest -m "db"

   # Run tests in parallel
   docker compose run --rm app poetry run pytest -n auto
   ```

5. View the coverage report:
   ```bash
   # Open coverage-reports/html/index.html in your browser
   ```

## Database Testing Guide

### Running Database Tests
- Use the `db` marker to run database-specific tests:
  ```bash
  docker compose run --rm app poetry run pytest -m "db"
  ```

### Test Database Configuration
- Separate test database container with resource limits
- Automatic database cleanup between tests
- Support for parallel test execution
- Proper test isolation

### Writing Database Tests
```python
@pytest.mark.db
async def test_database_operation():
    # Your test code here
    pass
```

See `tests/db/` directory for examples and patterns.