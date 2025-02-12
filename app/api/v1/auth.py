"""
Authentication endpoints for user login and token management.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

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
from app.services.exceptions import AuthenticationError, UserNotFoundError

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Add security scheme for Bearer token
security = HTTPBearer(
    description="JWT access token",
    scheme_name="Bearer",
    auto_error=True,
)


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
    except (AuthenticationError, UserNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/verify",
    response_model=TokenData,
    summary="Verify Token",
    description="Verifies a JWT token and returns the decoded token data. Requires a valid Bearer token in the Authorization header.",
    responses={
        401: {"model": HTTPError, "description": "Invalid or expired token"},
        500: {"model": HTTPError, "description": "Internal server error"},
    },
)
async def verify_token_endpoint(
    credentials: Annotated[HTTPAuthorizationCredentials, Security(security)]
) -> TokenData:
    """
    Verify a JWT token and return its decoded data.

    Args:
        credentials: Bearer token credentials from Authorization header

    Returns:
        TokenData: Decoded token data containing user information

    Raises:
        HTTPException: If token is invalid or expired
    """
    token_data = await verify_token(credentials.credentials)
    return token_data
