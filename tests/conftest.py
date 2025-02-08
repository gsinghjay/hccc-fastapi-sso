"""
Test configuration and fixtures.
"""
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr

from app.main import app
from app.core.config import Settings, get_settings


def get_settings_override() -> Settings:
    """Override settings for testing"""
    return Settings(
        ENVIRONMENT="development",
        DEBUG=True,
        POSTGRES_DB="test_db",
        POSTGRES_USER="test_user",
        POSTGRES_PASSWORD=SecretStr("test_password"),
        SECRET_KEY=SecretStr("x" * 32)
    )


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """
    Test client fixture that can be used across all tests.
    
    Returns:
        TestClient: A test client configured to make requests to the test app
    """
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_settings() -> Settings:
    """Fixture to provide test Settings instance."""
    return get_settings_override()
