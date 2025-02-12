"""
Authentication schema models for request/response validation.
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class TokenData(BaseModel):
    """
    Schema for JWT token data.

    Attributes:
        sub (str): Subject identifier (user ID)
        email (EmailStr): User's email address
        exp (datetime): Token expiration timestamp
    """

    sub: str = Field(..., description="Subject identifier (user ID)")
    email: EmailStr = Field(..., description="User's email address")
    exp: datetime = Field(..., description="Token expiration timestamp")


class TokenResponse(BaseModel):
    """
    Schema for token response.

    Attributes:
        access_token (str): JWT access token
        token_type (str): Token type (always "bearer")
    """

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
            }
        }
    }


class LoginRequest(BaseModel):
    """
    Schema for login requests.

    Attributes:
        email (EmailStr): User's email address for authentication
        password (str): User's password for authentication
    """

    email: EmailStr = Field(
        ...,
        description="User's email address for authentication",
        examples=["john.doe@example.com", "jane.smith@company.com"],
    )
    password: str = Field(
        ...,
        description="User's password for authentication (minimum 8 characters, must contain letters, numbers, and special characters)",
        examples=["SecureP@ssw0rd123"],
        min_length=8,
        max_length=100,
        pattern=r"[A-Za-z\d@$!%*#?&]{8,}",  # At least 8 chars, allowing letters, numbers, and special chars
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecureP@ssw0rd123",
            },
            "examples": [
                {
                    "email": "john.doe@example.com",
                    "password": "SecureP@ssw0rd123",
                    "summary": "Standard user login",
                },
                {
                    "email": "jane.smith@company.com",
                    "password": "MySecureP@ss2024",
                    "summary": "Business user login",
                },
            ],
        }
    }
