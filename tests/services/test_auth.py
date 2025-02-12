"""
Tests for authentication service and dependencies.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID
from pytest_mock import MockFixture
from jose import jwt
from fastapi import HTTPException

from app.core.config import get_settings
from app.models.user import User
from app.services.auth import AuthService
from app.services.exceptions import UserNotFoundError, AuthenticationError
from app.dependencies.auth import get_current_user, get_current_user_optional

settings = get_settings()


@pytest.fixture
def mock_user() -> User:
    """Fixture for a mock user."""
    return User(
        id=UUID("12345678-1234-5678-1234-567812345678"),
        email="test@example.com",
        hashed_password="hashed_password123",
        full_name="Test User",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


@pytest.fixture
def mock_db(mock_user: User) -> AsyncMock:
    """Fixture for a mock database session."""
    mock = AsyncMock()
    mock.get_by_email = AsyncMock()

    # Set up the execute chain to return a mock user
    scalar_mock = AsyncMock()
    scalar_mock.return_value = mock_user

    result_mock = AsyncMock()
    result_mock.scalar_one_or_none = scalar_mock

    execute_mock = AsyncMock()
    execute_mock.return_value = result_mock
    mock.execute = execute_mock

    return mock


@pytest.fixture
def valid_token(mock_user: User) -> str:
    """Fixture for a valid JWT token."""
    return jwt.encode(
        {
            "sub": mock_user.email,
            "exp": datetime.utcnow() + timedelta(minutes=15),
        },
        settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.JWT_ALGORITHM,
    )


@pytest.fixture
def expired_token(mock_user: User) -> str:
    """Fixture for an expired JWT token."""
    return jwt.encode(
        {
            "sub": mock_user.email,
            "exp": datetime.utcnow() - timedelta(minutes=15),
        },
        settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.JWT_ALGORITHM,
    )


class TestAuthService:
    """Test cases for AuthService."""

    @pytest.mark.asyncio
    async def test_authenticate_user_success(
        self,
        mock_db: AsyncMock,
        mock_user: User,
        mocker: MockFixture,
    ) -> None:
        """Test successful user authentication."""
        # Mock dependencies
        mock_db.get_by_email.return_value = mock_user
        mock_verify = mocker.patch(
            "app.services.auth.verify_password", return_value=True
        )
        mock_create_token = mocker.patch(
            "app.services.auth.create_access_token", return_value="mock_token"
        )

        # Create service and authenticate
        service = AuthService(mock_db)
        token = await service.authenticate_user(
            email="test@example.com", password="password123"
        )

        # Verify behavior
        mock_db.get_by_email.assert_called_once_with("test@example.com")
        mock_verify.assert_called_once_with("password123", mock_user.hashed_password)
        mock_create_token.assert_called_once_with(
            subject=str(mock_user.id), email=mock_user.email
        )
        assert token == "mock_token"

    @pytest.mark.asyncio
    async def test_authenticate_user_not_found(
        self,
        mock_db: AsyncMock,
    ) -> None:
        """Test authentication with non-existent user."""
        # Mock user not found
        mock_db.get_by_email.return_value = None

        # Create service and attempt authentication
        service = AuthService(mock_db)
        with pytest.raises(UserNotFoundError) as exc_info:
            await service.authenticate_user(
                email="nonexistent@example.com", password="password123"
            )

        # Verify behavior
        assert exc_info.value.code == 404
        assert "nonexistent@example.com" in str(exc_info.value)
        mock_db.get_by_email.assert_called_once_with("nonexistent@example.com")

    @pytest.mark.asyncio
    async def test_authenticate_user_invalid_password(
        self,
        mock_db: AsyncMock,
        mock_user: User,
        mocker: MockFixture,
    ) -> None:
        """Test authentication with invalid password."""
        # Mock dependencies
        mock_db.get_by_email.return_value = mock_user
        mocker.patch("app.services.auth.verify_password", return_value=False)

        # Create service and attempt authentication
        service = AuthService(mock_db)
        with pytest.raises(AuthenticationError) as exc_info:
            await service.authenticate_user(
                email="test@example.com", password="wrong_password"
            )

        # Verify behavior
        assert exc_info.value.code == 401
        assert "Invalid password" in str(exc_info.value)
        mock_db.get_by_email.assert_called_once_with("test@example.com")


class TestAuthDependencies:
    """Test cases for authentication dependencies."""

    @pytest.mark.asyncio
    async def test_get_current_user_success(
        self,
        mock_db: AsyncMock,
        mock_user: User,
        valid_token: str,
    ) -> None:
        """Test successful user retrieval from valid token."""
        # Mock database query
        result_mock = MagicMock()
        result_mock.scalar_one_or_none.return_value = mock_user
        mock_db.execute = AsyncMock(return_value=result_mock)

        # Get user from token
        user = await get_current_user(token=valid_token, db=mock_db)

        # Verify behavior
        assert isinstance(user, User)  # Ensure we got a User instance
        assert user.id == mock_user.id
        assert user.email == mock_user.email
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_current_user_expired_token(
        self,
        mock_db: AsyncMock,
        expired_token: str,
    ) -> None:
        """Test error handling for expired token."""
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(token=expired_token, db=mock_db)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Could not validate credentials"
        headers = exc_info.value.headers
        assert isinstance(headers, dict)
        assert headers.get("WWW-Authenticate") == "Bearer"

    @pytest.mark.asyncio
    async def test_get_current_user_invalid_token(
        self,
        mock_db: AsyncMock,
    ) -> None:
        """Test error handling for invalid token."""
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(token="invalid_token", db=mock_db)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Could not validate credentials"
        headers = exc_info.value.headers
        assert isinstance(headers, dict)
        assert headers.get("WWW-Authenticate") == "Bearer"

    @pytest.mark.asyncio
    async def test_get_current_user_not_found(
        self,
        mock_db: AsyncMock,
        valid_token: str,
    ) -> None:
        """Test error handling for valid token but non-existent user."""
        # Mock user not found
        result_mock = MagicMock()
        result_mock.scalar_one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=result_mock)

        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(token=valid_token, db=mock_db)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "User not found"
        headers = exc_info.value.headers
        assert isinstance(headers, dict)
        assert headers.get("WWW-Authenticate") == "Bearer"
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_current_user_optional_with_valid_token(
        self,
        mock_db: AsyncMock,
        mock_user: User,
        valid_token: str,
    ) -> None:
        """Test optional authentication with valid token."""
        # Mock database query
        result_mock = MagicMock()
        result_mock.scalar_one_or_none.return_value = mock_user
        mock_db.execute = AsyncMock(return_value=result_mock)

        # Get user from token
        user = await get_current_user_optional(db=mock_db, token=valid_token)

        # Verify behavior
        assert isinstance(user, User)  # Ensure we got a User instance
        assert user.id == mock_user.id
        assert user.email == mock_user.email
        mock_db.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_current_user_optional_with_no_token(
        self,
        mock_db: AsyncMock,
    ) -> None:
        """Test optional authentication with no token."""
        user = await get_current_user_optional(db=mock_db, token=None)
        assert user is None
        mock_db.execute.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_current_user_optional_with_invalid_token(
        self,
        mock_db: AsyncMock,
    ) -> None:
        """Test optional authentication with invalid token."""
        user = await get_current_user_optional(db=mock_db, token="invalid_token")
        assert user is None
        mock_db.execute.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_current_user_optional_with_expired_token(
        self,
        mock_db: AsyncMock,
        expired_token: str,
    ) -> None:
        """Test optional authentication with expired token."""
        user = await get_current_user_optional(db=mock_db, token=expired_token)
        assert user is None
        mock_db.execute.assert_not_called()
