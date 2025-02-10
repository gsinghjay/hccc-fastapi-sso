"""
Tests for user service.
"""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from typing import Any
from uuid import UUID
from pytest_mock import MockFixture

from app.core.config import get_settings
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.user import UserService
from app.repositories.user import UserRepository
from app.services.exceptions import (
    EmailAlreadyExistsError,
    UserNotFoundError,
)

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


class MockUserRepository(MagicMock):
    """Mock implementation of UserRepository for testing."""

    def __init__(
        self,
        mock_user: User | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize the mock repository."""
        super().__init__(spec=UserRepository, *args, **kwargs)
        self.mock_user = mock_user
        self.get_by_id = AsyncMock()
        self.get_by_email = AsyncMock()
        self.create = AsyncMock()
        self.update = AsyncMock()


@pytest.fixture
def mock_db(mock_user: User) -> MockUserRepository:
    """Fixture for a mock database repository."""
    return MockUserRepository(mock_user)


class TestUserService:
    """Test cases for UserService."""

    @pytest.mark.asyncio
    async def test_create_user_success(
        self,
        mock_db: MockUserRepository,
        mock_user: User,
        mocker: MockFixture,
    ) -> None:
        """Test successful user creation."""
        # Mock dependencies
        mock_db.get_by_email.return_value = None
        mock_db.create.return_value = mock_user
        mock_hash = mocker.patch(
            "app.services.user.get_password_hash", return_value="hashed_password123"
        )

        # Create service and user
        service = UserService(mock_db)
        user_data = UserCreate(
            email="new@example.com", password="password123", full_name="New User"
        )
        created_user = await service.create_user(user_data)

        # Verify behavior
        mock_db.get_by_email.assert_awaited_once_with("new@example.com")
        mock_hash.assert_called_once_with("password123")
        mock_db.create.assert_awaited_once()
        assert created_user.email == mock_user.email
        assert created_user.full_name == mock_user.full_name

    @pytest.mark.asyncio
    async def test_create_user_email_exists(
        self,
        mock_db: MockUserRepository,
        mock_user: User,
    ) -> None:
        """Test user creation with existing email."""
        # Mock email exists
        mock_db.get_by_email.return_value = mock_user

        # Create service and attempt user creation
        service = UserService(mock_db)
        user_data = UserCreate(
            email="test@example.com", password="password123", full_name="Test User"
        )
        with pytest.raises(EmailAlreadyExistsError) as _:
            await service.create_user(user_data)

        # Verify behavior
        mock_db.get_by_email.assert_awaited_once_with("test@example.com")
        mock_db.create.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_get_user_success(
        self,
        mock_db: MockUserRepository,
        mock_user: User,
    ) -> None:
        """Test successful user retrieval."""
        # Mock user exists
        mock_db.get_by_id.return_value = mock_user

        # Get user
        service = UserService(mock_db)
        user = await service.get_user(mock_user.id)

        # Verify behavior
        mock_db.get_by_id.assert_awaited_once_with(mock_user.id)
        assert user.id == mock_user.id
        assert user.email == mock_user.email
        assert user.full_name == mock_user.full_name

    @pytest.mark.asyncio
    async def test_get_user_not_found(
        self,
        mock_db: MockUserRepository,
    ) -> None:
        """Test user retrieval when user doesn't exist."""
        # Mock user not found
        mock_db.get_by_id.return_value = None

        # Attempt to get user
        service = UserService(mock_db)
        user_id = UUID("00000000-0000-0000-0000-000000000000")
        with pytest.raises(UserNotFoundError) as _:
            await service.get_user(user_id)

        # Verify behavior
        mock_db.get_by_id.assert_awaited_once_with(user_id)

    @pytest.mark.asyncio
    async def test_update_user_success(
        self,
        mock_db: MockUserRepository,
        mock_user: User,
        mocker: MockFixture,
    ) -> None:
        """Test successful user update."""
        # Mock dependencies
        mock_db.get_by_id.return_value = mock_user
        mock_db.get_by_email.return_value = None
        mock_db.update.return_value = mock_user
        mock_hash = mocker.patch(
            "app.services.user.get_password_hash", return_value="new_hashed_password"
        )

        # Update user
        service = UserService(mock_db)
        update_data = UserUpdate(
            email="new@example.com", password="newpassword123", full_name="Updated Name"
        )
        updated_user = await service.update_user(mock_user.id, update_data)

        # Verify behavior
        mock_db.get_by_id.assert_awaited_once_with(mock_user.id)
        mock_db.get_by_email.assert_awaited_once_with("new@example.com")
        mock_hash.assert_called_once_with("newpassword123")
        mock_db.update.assert_awaited_once()
        assert updated_user.email == mock_user.email
        assert updated_user.full_name == mock_user.full_name

    @pytest.mark.asyncio
    async def test_update_user_email_exists(
        self,
        mock_db: MockUserRepository,
        mock_user: User,
    ) -> None:
        """Test user update with existing email."""
        # Mock dependencies
        mock_db.get_by_id.return_value = mock_user
        mock_db.get_by_email.return_value = User(
            id=UUID("00000000-0000-0000-0000-000000000000"),
            email="existing@example.com",
            hashed_password="hashed_password123",
            full_name="Existing User",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        # Attempt update
        service = UserService(mock_db)
        update_data = UserUpdate(email="existing@example.com")
        with pytest.raises(EmailAlreadyExistsError) as _:
            await service.update_user(mock_user.id, update_data)

        # Verify behavior
        mock_db.get_by_id.assert_awaited_once_with(mock_user.id)
        mock_db.get_by_email.assert_awaited_once_with("existing@example.com")
        mock_db.update.assert_not_awaited()
