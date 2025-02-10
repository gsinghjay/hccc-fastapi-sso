"""
Tests for authentication service.
"""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock
from uuid import UUID
from pytest_mock import MockFixture

from app.core.config import get_settings
from app.models.user import User
from app.services.auth import AuthService
from app.services.exceptions import AuthenticationError, UserNotFoundError

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
    return mock


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
