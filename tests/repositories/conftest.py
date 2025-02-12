"""
Repository test fixtures.
"""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user import SQLAlchemyUserRepository


@pytest.fixture
def test_user_id() -> UUID:
    """Fixture for test user ID."""
    return UUID("12345678-1234-5678-1234-567812345678")


@pytest.fixture
def test_user_email() -> str:
    """Fixture for test user email."""
    return "test@example.com"


@pytest.fixture
def test_user_hashed_password() -> str:
    """Fixture for test user hashed password."""
    return "hashed_password123"


@pytest.fixture
def test_user_full_name() -> str:
    """Fixture for test user full name."""
    return "Test User"


@pytest.fixture
def test_user(
    test_user_id: UUID,
    test_user_email: str,
    test_user_full_name: str,
    test_user_hashed_password: str,
) -> User:
    """
    Fixture for a test user.

    This fixture creates a User instance with consistent test data
    that can be used across different test cases.
    """
    return User(
        id=test_user_id,
        email=test_user_email,
        hashed_password=test_user_hashed_password,
        full_name=test_user_full_name,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


@pytest.fixture
def mock_db_session() -> AsyncMock:
    """
    Fixture that provides a mock database session.

    Returns:
        AsyncMock: A mock async database session with common methods mocked
    """
    session = AsyncMock(spec=AsyncSession)

    # Mock the execute method to return a result proxy
    result_mock = AsyncMock()
    result_mock.scalar_one_or_none = AsyncMock()

    # Create a mock for the scalars chain
    scalars_mock = AsyncMock()
    scalars_mock.all = AsyncMock()
    result_mock.scalars = AsyncMock()
    result_mock.scalars.return_value = scalars_mock

    session.execute = AsyncMock(return_value=result_mock)

    # Mock other common session methods
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.refresh = AsyncMock()

    return session


@pytest.fixture
def user_repository(mock_db_session: AsyncMock) -> SQLAlchemyUserRepository:
    """
    Fixture that provides a UserRepository instance with mocked session.

    Args:
        mock_db_session: The mocked database session

    Returns:
        SQLAlchemyUserRepository: A repository instance for user operations
    """
    return SQLAlchemyUserRepository(mock_db_session)
