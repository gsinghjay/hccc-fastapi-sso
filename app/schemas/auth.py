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
        email (EmailStr): User's email address
        password (str): User's password
    """

    email: EmailStr = Field(
        ..., description="User's email address", examples=["user@example.com"]
    )
    password: str = Field(
        ..., description="User's password", examples=["securepassword123"]
    )

    model_config = {
        "json_schema_extra": {
            "example": {"email": "user@example.com", "password": "securepassword123"}
        }
    }
