"""
Authentication endpoints for user login and token management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.core.security import verify_token
from app.db.base import get_db
from app.repositories.user import SQLAlchemyUserRepository
from app.schemas.auth import (
    TokenResponse,
    LoginRequest,
    TokenData,
)
from app.schemas.base import HTTPError
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="User Login",
    description="Authenticates a user and returns a JWT access token",
    responses={
        400: {"model": HTTPError, "description": "Invalid credentials"},
        401: {"model": HTTPError, "description": "Authentication failed"},
        500: {"model": HTTPError, "description": "Internal server error"},
    },
)
async def login(
    credentials: LoginRequest, db: Annotated[AsyncSession, Depends(get_db)]
) -> TokenResponse:
    """
    Authenticate a user and generate an access token.

    Args:
        credentials: User login credentials (email and password)
        db: Database session dependency

    Returns:
        TokenResponse: JWT access token and token type

    Raises:
        HTTPException: If authentication fails or credentials are invalid
    """
    user_repo = SQLAlchemyUserRepository(db)
    auth_service = AuthService(user_repo)
    try:
        token = await auth_service.authenticate_user(
            credentials.email, credentials.password
        )
        return TokenResponse(access_token=token, token_type="bearer")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post(
    "/verify",
    response_model=TokenData,
    summary="Verify Token",
    description="Verifies a JWT token and returns the decoded token data",
    responses={
        401: {"model": HTTPError, "description": "Invalid or expired token"},
        500: {"model": HTTPError, "description": "Internal server error"},
    },
)
async def verify_token_endpoint(
    token_data: Annotated[TokenData, Depends(verify_token)]
) -> TokenData:
    """
    Verify a JWT token and return its decoded data.

    Args:
        token_data: Decoded token data from verify_token dependency

    Returns:
        TokenData: Decoded token data containing user information

    Raises:
        HTTPException: If token is invalid or expired
    """
    return token_data
