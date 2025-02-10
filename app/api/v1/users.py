"""
User management endpoints for registration and profile management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.core.security import get_current_user
from app.db.base import get_db
from app.repositories.user import SQLAlchemyUserRepository
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.schemas.base import HTTPError
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register User",
    description="Register a new user with email and password",
    responses={
        400: {"model": HTTPError, "description": "Invalid input"},
        409: {"model": HTTPError, "description": "Email already registered"},
        500: {"model": HTTPError, "description": "Internal server error"},
    },
)
async def register_user(
    user_data: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]
) -> UserResponse:
    """
    Register a new user in the system.

    Args:
        user_data: User registration data including email and password
        db: Database session dependency

    Returns:
        UserResponse: Created user information (excluding password)

    Raises:
        HTTPException: If email is already registered or input is invalid
    """
    user_repo = SQLAlchemyUserRepository(db)
    user_service = UserService(user_repo)
    try:
        user = await user_service.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get Current User",
    description="Get the profile of the currently authenticated user",
    responses={
        401: {"model": HTTPError, "description": "Not authenticated"},
        404: {"model": HTTPError, "description": "User not found"},
        500: {"model": HTTPError, "description": "Internal server error"},
    },
)
async def get_current_user_profile(
    current_user: Annotated[UserResponse, Depends(get_current_user)]
) -> UserResponse:
    """
    Retrieve the profile of the currently authenticated user.

    Args:
        current_user: Current authenticated user (injected by dependency)

    Returns:
        UserResponse: Current user's profile information

    Raises:
        HTTPException: If user is not authenticated or not found
    """
    return current_user


@router.patch(
    "/me",
    response_model=UserResponse,
    summary="Update Current User",
    description="Update the profile of the currently authenticated user",
    responses={
        400: {"model": HTTPError, "description": "Invalid input"},
        401: {"model": HTTPError, "description": "Not authenticated"},
        404: {"model": HTTPError, "description": "User not found"},
        500: {"model": HTTPError, "description": "Internal server error"},
    },
)
async def update_current_user(
    user_data: UserUpdate,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserResponse:
    """
    Update the profile of the currently authenticated user.

    Args:
        user_data: User data to update
        current_user: Current authenticated user (injected by dependency)
        db: Database session dependency

    Returns:
        UserResponse: Updated user information

    Raises:
        HTTPException: If user is not authenticated or update fails
    """
    user_repo = SQLAlchemyUserRepository(db)
    user_service = UserService(user_repo)
    try:
        updated_user = await user_service.update_user(current_user.id, user_data)
        return updated_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
