"""
Tests for the configuration management module.
"""
import os
from typing import Any
from unittest.mock import patch

import pytest
from pydantic import SecretStr, ValidationError

from app.core.config import Settings, get_settings


@pytest.fixture
def test_settings() -> Settings:
    """Fixture to provide a Settings instance for testing."""
    return Settings(
        DEBUG=True,
        POSTGRES_DB="test_db",
        POSTGRES_USER="test_user",
        POSTGRES_PASSWORD=SecretStr("test_password"),
        SECRET_KEY=SecretStr("x" * 32),
        ACCESS_TOKEN_EXPIRE_MINUTES=11520
    )


class TestSettingsConfiguration:
    """Group related settings tests together"""
    
    def test_settings_defaults(self, test_settings: Settings) -> None:
        """Test default values are set correctly."""
        assert test_settings.PROJECT_NAME == "FastAPI User Management"
        assert test_settings.API_PREFIX == "/api"
        assert test_settings.API_V1_STR == "v1"
        assert test_settings.DEBUG is True
        assert test_settings.ACCESS_TOKEN_EXPIRE_MINUTES == 11520
        assert test_settings.RATE_LIMIT_PER_MINUTE == 60
        assert test_settings.POSTGRES_SERVER == "localhost"
        assert test_settings.POSTGRES_USER == "test_user"
        assert test_settings.POSTGRES_DB == "test_db"
        assert test_settings.POSTGRES_PORT == 5432

    def test_api_v1_path_construction(self) -> None:
        """Test API v1 path is constructed correctly."""
        settings = Settings()
        assert settings.API_V1_PATH == "/api/v1"
        
        # Test with custom values
        settings = Settings(API_PREFIX="/custom", API_V1_STR="version1")
        assert settings.API_V1_PATH == "/custom/version1"

    def test_database_uri_construction(self) -> None:
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

    @pytest.mark.parametrize(
        "key,expected_error",
        [
            ("short", "SECRET_KEY must be at least 32 characters long"),
            (123, "SECRET_KEY must be a string or SecretStr"),
        ],
    )
    def test_secret_key_validation(self, key: str | int, expected_error: str) -> None:
        """Test secret key validation with different inputs."""
        with pytest.raises(ValidationError) as exc_info:
            Settings(SECRET_KEY=key)  # type: ignore[arg-type]
        assert expected_error in str(exc_info.value)

    @pytest.mark.parametrize(
        "origins,expected",
        [
            ("http://localhost,http://example.com", ["http://localhost", "http://example.com"]),
            (["http://localhost", "http://example.com"], ["http://localhost", "http://example.com"]),
        ],
    )
    def test_valid_cors_origins(self, origins: str | list[str], expected: list[str]) -> None:
        """Test valid CORS origins configurations."""
        settings = Settings(BACKEND_CORS_ORIGINS=origins)
        assert settings.BACKEND_CORS_ORIGINS == expected

    @pytest.mark.parametrize(
        "origins,expected_error",
        [
            ([123, 456], "All CORS origins must be strings"),
            ("[invalid format]", "String input should be comma-separated URLs"),
            (123, "BACKEND_CORS_ORIGINS should be a comma separated string or a list of strings"),
        ],
    )
    def test_invalid_cors_origins(self, origins: Any, expected_error: str) -> None:
        """Test invalid CORS origins configurations."""
        with pytest.raises(ValidationError) as exc_info:
            Settings(BACKEND_CORS_ORIGINS=origins)
        assert expected_error in str(exc_info.value)

    @pytest.mark.parametrize(
        "env_vars,expected_attrs",
        [
            (
                {
                    "PROJECT_NAME": "Test Project",
                    "API_PREFIX": "/test-api",
                    "API_V1_STR": "v2",
                    "DEBUG": "true",
                    "SECRET_KEY": "x" * 32,
                    "POSTGRES_SERVER": "testdb.example.com",
                    "POSTGRES_USER": "admin",
                    "POSTGRES_PASSWORD": "secure123",
                    "POSTGRES_DB": "testdb",
                    "POSTGRES_PORT": "5434"
                },
                {
                    "PROJECT_NAME": "Test Project",
                    "API_PREFIX": "/test-api",
                    "API_V1_STR": "v2",
                    "DEBUG": True,
                    "POSTGRES_SERVER": "testdb.example.com",
                    "POSTGRES_USER": "admin",
                    "POSTGRES_DB": "testdb",
                    "POSTGRES_PORT": 5434
                }
            ),
        ],
    )
    def test_settings_from_env(self, env_vars: dict[str, str], expected_attrs: dict[str, Any]) -> None:
        """Test settings are loaded correctly from environment variables."""
        with patch.dict(os.environ, env_vars, clear=True):
            settings = Settings()
            for key, value in expected_attrs.items():
                assert getattr(settings, key) == value

    def test_settings_cache(self) -> None:
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