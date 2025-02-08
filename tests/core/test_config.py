"""
Tests for the configuration management module.
"""
import os
from typing import Any
from unittest.mock import patch

import pytest
from pydantic import SecretStr, ValidationError, Field
from pydantic_settings import BaseSettings

from app.core.config import Settings, get_settings


@pytest.fixture
def test_settings() -> Settings:
    """Fixture to provide a Settings instance for testing."""
    return Settings()


def test_settings_defaults(test_settings: Settings) -> None:
    """Test default values are set correctly."""
    assert test_settings.PROJECT_NAME == "FastAPI User Management"
    assert test_settings.API_PREFIX == "/api"
    assert test_settings.API_V1_STR == "v1"
    assert test_settings.ENVIRONMENT == "development"
    assert test_settings.DEBUG is False
    assert test_settings.ACCESS_TOKEN_EXPIRE_MINUTES == 60 * 24 * 8
    assert test_settings.RATE_LIMIT_PER_MINUTE == 60
    assert test_settings.POSTGRES_SERVER == "localhost"
    assert test_settings.POSTGRES_USER == "postgres"
    assert test_settings.POSTGRES_DB == "user_management"
    assert test_settings.POSTGRES_PORT == 5432


def test_api_v1_path_construction() -> None:
    """Test API v1 path is constructed correctly."""
    settings = Settings()
    assert settings.API_V1_PATH == "/api/v1"
    
    # Test with custom values
    settings = Settings(API_PREFIX="/custom", API_V1_STR="version1")
    assert settings.API_V1_PATH == "/custom/version1"


def test_database_uri_construction() -> None:
    """Test database URI is constructed correctly."""
    settings = Settings(
        POSTGRES_SERVER="testhost",
        POSTGRES_USER="testuser",
        POSTGRES_PASSWORD=SecretStr("testpass"),
        POSTGRES_DB="testdb",
        POSTGRES_PORT=5433
    )
    
    # PostgresDsn adds an extra slash before the database name
    expected_uri = "postgresql://testuser:testpass@testhost:5433//testdb"
    assert str(settings.SQLALCHEMY_DATABASE_URI) == expected_uri


def test_secret_key_validation() -> None:
    """Test secret key length validation."""
    # Test with valid length key
    valid_key = "x" * 32
    settings = Settings(SECRET_KEY=SecretStr(valid_key))
    assert settings.SECRET_KEY.get_secret_value() == valid_key
    
    # Test with SecretStr input
    settings = Settings(SECRET_KEY=SecretStr(valid_key))
    assert settings.SECRET_KEY.get_secret_value() == valid_key
    
    # Test with short key (string input)
    with pytest.raises(ValidationError) as exc_info:
        Settings(SECRET_KEY=SecretStr("short"))
    assert "SECRET_KEY must be at least 32 characters long" in str(exc_info.value)
    
    # Test with short key (SecretStr input)
    with pytest.raises(ValidationError) as exc_info:
        Settings(SECRET_KEY=SecretStr("short"))
    assert "SECRET_KEY must be at least 32 characters long" in str(exc_info.value)
    
    # Test with invalid type
    with pytest.raises(ValidationError) as exc_info:
        Settings(SECRET_KEY=123)  # type: ignore
    assert "SECRET_KEY must be a string or SecretStr" in str(exc_info.value)


def test_cors_origins_validation() -> None:
    """Test CORS origins validation and processing."""
    # Test with comma-separated string input
    origins_str = "http://localhost,http://example.com"
    settings = Settings(BACKEND_CORS_ORIGINS=origins_str)
    assert settings.BACKEND_CORS_ORIGINS == ["http://localhost", "http://example.com"]
    
    # Test with list input
    origins_list = ["http://localhost", "http://example.com"]
    settings = Settings(BACKEND_CORS_ORIGINS=origins_list)
    assert settings.BACKEND_CORS_ORIGINS == origins_list
    
    # Test with invalid type (non-string list items)
    with pytest.raises(ValidationError) as exc_info:
        Settings(BACKEND_CORS_ORIGINS=[123, 456])  # type: ignore
    assert "All CORS origins must be strings" in str(exc_info.value)
    
    # Test with invalid string format
    with pytest.raises(ValidationError) as exc_info:
        Settings(BACKEND_CORS_ORIGINS="[invalid format]")
    assert "String input should be comma-separated URLs" in str(exc_info.value)
    
    # Test with invalid type
    with pytest.raises(ValidationError) as exc_info:
        Settings(BACKEND_CORS_ORIGINS=123)  # type: ignore
    assert "BACKEND_CORS_ORIGINS should be a comma separated string or a list of strings" in str(exc_info.value)


def test_environment_validation() -> None:
    """Test environment validation."""
    valid_environments = ["development", "staging", "production"]
    for env in valid_environments:
        settings = Settings(ENVIRONMENT=env)
        assert settings.ENVIRONMENT == env
    
    with pytest.raises(ValidationError) as exc_info:
        Settings(ENVIRONMENT="invalid")
    assert "String should match pattern" in str(exc_info.value)


def test_settings_from_env() -> None:
    """Test settings are loaded from environment variables."""
    env_vars = {
        "PROJECT_NAME": "Test Project",
        "API_PREFIX": "/test-api",
        "API_V1_STR": "v2",
        "ENVIRONMENT": "production",
        "DEBUG": "true",
        "SECRET_KEY": "x" * 32,
        "POSTGRES_SERVER": "testdb.example.com",
        "POSTGRES_USER": "admin",
        "POSTGRES_PASSWORD": "secure123",
        "POSTGRES_DB": "testdb",
        "POSTGRES_PORT": "5434"
    }
    
    with patch.dict(os.environ, env_vars, clear=True):
        settings = Settings()
        
        assert settings.PROJECT_NAME == "Test Project"
        assert settings.API_PREFIX == "/test-api"
        assert settings.API_V1_STR == "v2"
        assert settings.ENVIRONMENT == "production"
        assert settings.DEBUG is True
        assert settings.SECRET_KEY.get_secret_value() == "x" * 32
        assert settings.POSTGRES_SERVER == "testdb.example.com"
        assert settings.POSTGRES_USER == "admin"
        assert settings.POSTGRES_PASSWORD.get_secret_value() == "secure123"
        assert settings.POSTGRES_DB == "testdb"
        assert settings.POSTGRES_PORT == 5434


def test_settings_cache() -> None:
    """Test settings caching behavior."""
    # First call should create settings
    settings1 = get_settings()
    
    # Second call should return cached instance
    settings2 = get_settings()
    
    # Should be the same instance
    assert settings1 is settings2
    
    # Modify environment and verify cache is used
    with patch.dict(os.environ, {"PROJECT_NAME": "New Name"}, clear=False):
        settings3 = get_settings()
        # Should still be the same cached instance
        assert settings3 is settings1
        assert settings3.PROJECT_NAME == settings1.PROJECT_NAME 