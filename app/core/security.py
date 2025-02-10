"""
Security utilities for JWT token management and user authentication.
"""

from datetime import datetime, timedelta
from typing import Any, Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.db.base import get_db
from app.repositories.user import SQLAlchemyUserRepository
from app.schemas.auth import TokenData
from app.schemas.user import UserResponse
from app.services.user import UserService

settings = get_settings()

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def create_access_token(
    subject: str, email: EmailStr, expires_delta: timedelta | None = None
) -> str:
    """
    Create a JWT access token.

    Args:
        subject (str): The subject of the token (usually user ID)
        email (EmailStr): The user's email address
        expires_delta (timedelta | None): Optional expiration time delta.
            If not provided, uses settings.ACCESS_TOKEN_EXPIRE_MINUTES

    Returns:
        str: The encoded JWT token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {
        "sub": str(subject),
        "email": str(email),
        "exp": expire,
    }
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


def decode_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT token.

    Args:
        token (str): The JWT token to decode

    Returns:
        dict[str, Any]: The decoded token data

    Raises:
        JWTError: If the token is invalid or expired
    """
    return jwt.decode(
        token,
        settings.SECRET_KEY.get_secret_value(),
        algorithms=[settings.JWT_ALGORITHM],
    )


async def verify_token(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    """
    Verify and decode a JWT token from the Authorization header.
    This function is designed to be used as a FastAPI dependency.

    Args:
        token: JWT token from authorization header (injected by FastAPI)

    Returns:
        TokenData: Decoded token data containing user information

    Raises:
        HTTPException: If token is invalid or expired
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_id: str | None = payload.get("sub")
        email: str | None = payload.get("email")
        exp: datetime | None = datetime.fromtimestamp(payload.get("exp", 0))
        if user_id is None or email is None or exp is None:
            raise credentials_exception
        return TokenData(sub=user_id, email=email, exp=exp)
    except JWTError:
        raise credentials_exception


async def get_current_user(
    token_data: Annotated[TokenData, Depends(verify_token)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserResponse:
    """
    Get the current authenticated user based on the JWT token.
    This function is designed to be used as a FastAPI dependency.

    Args:
        token_data: Decoded token data from verify_token dependency
        db: Database session from get_db dependency

    Returns:
        UserResponse: The current authenticated user

    Raises:
        HTTPException: If user not found or inactive
    """
    user_repository = SQLAlchemyUserRepository(db)
    user_service = UserService(user_repository)
    try:
        user = await user_service.get_user(UUID(token_data.sub))
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
