"""
User service for managing user operations.
"""

from uuid import UUID
from typing import Protocol

from app.core.hashing import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.exceptions import UserNotFoundError, EmailAlreadyExistsError


class UserRepository(Protocol):
    """Protocol defining required user repository methods."""

    async def get_by_id(self, user_id: UUID) -> User | None:
        """Get user by ID."""
        ...

    async def get_by_email(self, email: str) -> User | None:
        """Get user by email."""
        ...

    async def create(self, user: User) -> User:
        """Create a new user."""
        ...

    async def update(self, user: User) -> User:
        """Update an existing user."""
        ...


class UserService:
    """Service for handling user operations."""

    def __init__(self, user_repo: UserRepository):
        """
        Initialize the user service.

        Args:
            user_repo: User repository implementation
        """
        self.user_repo = user_repo

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """
        Create a new user.

        Args:
            user_data: User creation data

        Returns:
            UserResponse: Created user information

        Raises:
            EmailAlreadyExistsError: If email is already registered
        """
        # Check if email already exists
        if await self.user_repo.get_by_email(user_data.email):
            raise EmailAlreadyExistsError(email=user_data.email)

        # Create user instance
        user = User(
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
            full_name=user_data.full_name,
        )

        # Save to database
        created_user = await self.user_repo.create(user)
        return UserResponse.model_validate(created_user)

    async def get_user(self, user_id: UUID) -> UserResponse:
        """
        Get a user by ID.

        Args:
            user_id: User's UUID

        Returns:
            UserResponse: User information

        Raises:
            UserNotFoundError: If user does not exist
        """
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id=user_id)
        return UserResponse.model_validate(user)

    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> UserResponse:
        """
        Update a user's information.

        Args:
            user_id: User's UUID
            user_data: User update data

        Returns:
            UserResponse: Updated user information

        Raises:
            UserNotFoundError: If user does not exist
            EmailAlreadyExistsError: If new email is already registered
        """
        # Get existing user
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id=user_id)

        # Check if new email is available
        if user_data.email and user_data.email != user.email:
            if await self.user_repo.get_by_email(user_data.email):
                raise EmailAlreadyExistsError(email=user_data.email)
            user.email = user_data.email

        # Update other fields
        if user_data.full_name is not None:
            user.full_name = user_data.full_name
        if user_data.password:
            user.hashed_password = get_password_hash(user_data.password)

        # Save changes
        updated_user = await self.user_repo.update(user)
        return UserResponse.model_validate(updated_user)
