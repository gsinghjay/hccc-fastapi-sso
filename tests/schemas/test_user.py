"""
Tests for user schema validation and behavior.
"""

import pytest
from datetime import datetime, timezone
from pydantic import ValidationError
from uuid import UUID

from app.schemas.user import UserBase, UserCreate, UserUpdate, UserResponse


def test_user_base_valid() -> None:
    """Test UserBase schema with valid data."""
    user_data = {"email": "test@example.com", "full_name": "Test User"}
    user = UserBase(**user_data)
    assert user.email == user_data["email"]
    assert user.full_name == user_data["full_name"]


def test_user_base_invalid_email() -> None:
    """Test UserBase schema with invalid email."""
    with pytest.raises(ValidationError) as exc_info:
        UserBase(email="invalid-email", full_name="Test User")
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["type"] == "value_error"
    assert "email" in errors[0]["loc"]


@pytest.mark.parametrize(
    "full_name,expected_error",
    [
        ("", "string_too_short"),  # Empty string
        ("a" * 101, "string_too_long"),  # Too long
    ],
)
def test_user_base_invalid_full_name(full_name: str, expected_error: str) -> None:
    """Test UserBase schema with invalid full name."""
    with pytest.raises(ValidationError) as exc_info:
        UserBase(email="test@example.com", full_name=full_name)
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["type"] == expected_error
    assert "full_name" in errors[0]["loc"]


def test_user_create_valid() -> None:
    """Test UserCreate schema with valid data."""
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "securepass123",
    }
    user = UserCreate(**user_data)
    assert user.email == user_data["email"]
    assert user.full_name == user_data["full_name"]
    assert user.password == user_data["password"]


@pytest.mark.parametrize(
    "password,expected_error",
    [
        ("short", "string_too_short"),  # Too short
        ("a" * 101, "string_too_long"),  # Too long
    ],
)
def test_user_create_invalid_password(password: str, expected_error: str) -> None:
    """Test UserCreate schema with invalid password."""
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": password,
    }
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**user_data)
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["type"] == expected_error
    assert "password" in errors[0]["loc"]


def test_user_update_empty() -> None:
    """Test UserUpdate schema with no fields (valid empty update)."""
    user = UserUpdate()
    assert user.email is None
    assert user.full_name is None
    assert user.password is None


def test_user_update_partial() -> None:
    """Test UserUpdate schema with partial update."""
    user_data = {"full_name": "New Name"}
    user = UserUpdate(**user_data)
    assert user.email is None
    assert user.full_name == "New Name"
    assert user.password is None


def test_user_update_full() -> None:
    """Test UserUpdate schema with all fields."""
    user_data = {
        "email": "new@example.com",
        "full_name": "New Name",
        "password": "newpassword123",
    }
    user = UserUpdate(**user_data)
    assert user.email == user_data["email"]
    assert user.full_name == user_data["full_name"]
    assert user.password == user_data["password"]


def test_user_update_invalid_fields() -> None:
    """Test UserUpdate schema with invalid field values."""
    user_data = {
        "email": "invalid-email",
        "full_name": "",  # Too short
        "password": "short",  # Too short
    }
    with pytest.raises(ValidationError) as exc_info:
        UserUpdate(**user_data)
    errors = exc_info.value.errors()
    assert len(errors) == 3
    error_locs = {error["loc"][0] for error in errors}
    assert error_locs == {"email", "full_name", "password"}


def test_user_response_valid() -> None:
    """Test UserResponse schema with valid data."""
    test_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    test_time = datetime.now(timezone.utc)
    user = UserResponse(
        id=test_id,
        email="test@example.com",
        full_name="Test User",
        created_at=test_time,
        updated_at=test_time,
    )
    assert isinstance(user.id, UUID)
    assert user.id == test_id
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)


def test_user_response_missing_fields() -> None:
    """Test UserResponse schema with missing required fields."""
    with pytest.raises(ValidationError) as exc_info:
        # Test with missing required fields
        UserResponse(
            email="test@example.com",
            full_name="Test User",
        )  # type: ignore[call-arg]  # Intentionally missing required fields for test
    errors = exc_info.value.errors()
    assert len(errors) == 3
    error_locs = {error["loc"][0] for error in errors}
    assert error_locs == {"id", "created_at", "updated_at"}


def test_user_response_invalid_id() -> None:
    """Test UserResponse schema with invalid UUID."""
    test_time = datetime.now(timezone.utc)
    test_data = {
        "id": "invalid-uuid",  # Invalid UUID string to trigger validation error
        "email": "test@example.com",
        "full_name": "Test User",
        "created_at": test_time,
        "updated_at": test_time,
    }
    with pytest.raises(ValidationError) as exc_info:
        UserResponse(**test_data)  # type: ignore[arg-type]  # Invalid ID type for test
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["type"] == "uuid_parsing"
    assert "id" in errors[0]["loc"]


def test_user_response_invalid_timestamps() -> None:
    """Test UserResponse schema with invalid timestamps."""
    test_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    test_data = {
        "id": test_id,
        "email": "test@example.com",
        "full_name": "Test User",
        "created_at": "not-a-datetime",  # Invalid datetime string
        "updated_at": "also-not-a-datetime",  # Invalid datetime string
    }
    with pytest.raises(ValidationError) as exc_info:
        UserResponse(**test_data)  # type: ignore[arg-type]  # Invalid datetime types for test
    errors = exc_info.value.errors()
    assert len(errors) == 2
    error_locs = {error["loc"][0] for error in errors}
    assert error_locs == {"created_at", "updated_at"}
