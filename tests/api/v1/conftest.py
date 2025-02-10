"""
Test fixtures for API v1 tests.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def mock_db() -> AsyncSession:
    """
    Fixture that provides a mock database session.

    Returns:
        AsyncSession: A mock async database session
    """
    mock = MagicMock(spec=AsyncSession)
    mock.execute = AsyncMock()
    return mock
