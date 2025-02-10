"""
User schema models for request/response validation.
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID


class UserBase(BaseModel):
    """
    Base user schema with shared attributes.

    Attributes:
        email (EmailStr): User's email address
        full_name (str): User's full name (1-100 characters)
    """

    email: EmailStr = Field(
        ..., description="User's email address", examples=["user@example.com"]
    )
    full_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="User's full name",
        examples=["John Doe"],
    )


class UserCreate(UserBase):
    """
    Schema for user creation requests.

    Extends UserBase to add password field.

    Attributes:
        password (str): User's password (8-100 characters)
    """

    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="User's password",
        examples=["securepassword123"],
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "full_name": "John Doe",
                "password": "securepassword123",
            }
        }
    }


class UserUpdate(BaseModel):
    """
    Schema for user update requests.

    All fields are optional to allow partial updates.

    Attributes:
        email (EmailStr | None): New email address
        full_name (str | None): New full name
        password (str | None): New password
    """

    email: EmailStr | None = Field(
        None, description="New email address", examples=["newemail@example.com"]
    )
    full_name: str | None = Field(
        None,
        min_length=1,
        max_length=100,
        description="New full name",
        examples=["John Smith"],
    )
    password: str | None = Field(
        None,
        min_length=8,
        max_length=100,
        description="New password",
        examples=["newpassword123"],
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "newemail@example.com",
                "full_name": "John Smith",
                "password": "newpassword123",
            }
        }
    }


class UserResponse(UserBase):
    """
    Schema for user response data.

    Extends UserBase to add system fields.

    Attributes:
        id (UUID): User's unique identifier
        created_at (datetime): Timestamp of user creation
        updated_at (datetime): Timestamp of last update
    """

    id: UUID = Field(..., description="User's unique identifier")
    created_at: datetime = Field(..., description="Timestamp of user creation")
    updated_at: datetime = Field(..., description="Timestamp of last update")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "full_name": "John Doe",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
            }
        },
    )
