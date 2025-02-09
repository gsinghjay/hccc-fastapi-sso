# Technical Specification

## System Overview
The system is a production-ready FastAPI application designed for user management with a modular and scalable architecture. The primary purpose is to handle user registration, authentication, and profile retrieval. The system utilizes PostgreSQL for data storage, SQLAlchemy for ORM, JWT tokens for authentication, and follows best practices for security, testing, and maintainability. The frontend is a vanilla JavaScript application, and the backend is designed to be expanded with additional features in the future.

### Main Components
- **Frontend**: Vanilla JavaScript application.
- **Backend**: FastAPI application with user management features.
- **Database**: PostgreSQL.
- **Authentication**: OAuth2 with JWT tokens.
- **API Gateway**: Traefik as a reverse proxy.
- **Containerization**: Docker Compose for deployment.
- **Dependency Management**: Poetry.
- **Linting and Formatting**: Ruff and Black.
- **Type Checking**: Mypy with strict settings.
- **Database Migrations**: Alembic.
- **Logging**: Structured logging with Loki integration.

## Core Functionality

### User Management

#### User Registration
- **Endpoint**: `POST /v1/users/`
- **Description**: Allows new users to register by providing an email and password. The password is hashed using bcrypt before storage.
- **File**: `app/api/v1/users/routes.py`
- **Function**: `register_user`
- **Critical Details**: 
  - Validates input using Pydantic models.
  - Hashes the password using bcrypt.
  - Stores user data in PostgreSQL.

#### User Login
- **Endpoint**: `POST /v1/users/login`
- **Description**: Authenticates users by verifying their email and password. Returns a JWT token upon successful authentication.
- **File**: `app/api/v1/users/routes.py`
- **Function**: `login_user`
- **Critical Details**: 
  - Retrieves user from the database.
  - Verifies password using bcrypt.
  - Generates JWT token.

#### User Profile Retrieval
- **Endpoint**: `GET /v1/users/me`
- **Description**: Retrieves the current user's profile information.
- **File**: `app/api/v1/users/routes.py`
- **Function**: `get_current_user`
- **Critical Details**: 
  - Verifies JWT token.
  - Retrieves user profile from the database.

### Authentication

#### JWT Token Generation
- **Description**: Generates a JWT token for authenticated users.
- **File**: `app/core/security.py`
- **Function**: `create_access_token`
- **Critical Details**: 
  - Creates a JWT token with user information and an expiration time.

#### Token Verification
- **Description**: Verifies the validity of a JWT token.
- **File**: `app/core/security.py`
- **Function**: `verify_token`
- **Critical Details**: 
  - Decodes and verifies the JWT token to ensure it is valid and has not expired.

### Database Operations

#### User CRUD Operations
- **Description**: Handles create, read, update, and delete operations for user entities.
- **File**: `app/db/crud/user.py`
- **Functions**: `create_user`, `get_user_by_email`, `update_user`, `delete_user`
- **Critical Details**: 
  - Interacts with PostgreSQL to perform CRUD operations on user data.

## Architecture

### Data Flow

1. **User Registration**
   - **Input**: User provides email and password via `POST /v1/users/`.
   - **Process**: 
     - Validate input using Pydantic models.
     - Hash the password using bcrypt.
     - Store user data in PostgreSQL.
   - **Output**: Return success message or error details.

2. **User Login**
   - **Input**: User provides email and password via `POST /v1/users/login`.
   - **Process**: 
     - Retrieve user from the database.
     - Verify password using bcrypt.
     - Generate JWT token.
   - **Output**: Return JWT token or error message.

3. **User Profile Retrieval**
   - **Input**: Authorized user makes a request to `GET /v1/users/me`.
   - **Process**: 
     - Verify JWT token.
     - Retrieve user profile from the database.
   - **Output**: Return user profile data or error message.

### Component Interaction
- **FastAPI Routers**: Handle incoming requests and route them to appropriate handlers.
- **Service Layer**: Contains business logic and interacts with the database layer.
- **Database Layer**: Manages database operations using SQLAlchemy.
- **Security Module**: Handles authentication and token management.
- **Dependency Injection**: Centralizes dependencies and ensures they are injected where needed.