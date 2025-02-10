"""
Shared fixtures for service tests.
"""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock
from uuid import UUID

from app.models.user import User


@pytest.fixture
def test_user_id() -> UUID:
    """Fixture for test user ID."""
    return UUID("12345678-1234-5678-1234-567812345678")


@pytest.fixture
def test_user_email() -> str:
    """Fixture for test user email."""
    return "test@example.com"


@pytest.fixture
def test_user_password() -> str:
    """Fixture for test user password."""
    return "password123"


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
def mock_session() -> AsyncMock:
    """
    Fixture for a mock database session.

    This fixture provides a base AsyncMock that can be used
    to create more specific mock database sessions in tests.
    """
    return AsyncMock()
