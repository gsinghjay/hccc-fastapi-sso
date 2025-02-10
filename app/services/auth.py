"""
Authentication service for user login and token management.
"""

from typing import Protocol

from app.core.hashing import verify_password
from app.core.security import create_access_token
from app.models.user import User
from app.services.exceptions import AuthenticationError, UserNotFoundError


class UserRepository(Protocol):
    """Protocol defining required user repository methods."""

    async def get_by_email(self, email: str) -> User | None:
        """Get user by email."""
        ...


class AuthService:
    """Service for handling authentication operations."""

    def __init__(self, user_repo: UserRepository):
        """
        Initialize the auth service.

        Args:
            user_repo: User repository implementation
        """
        self.user_repo = user_repo

    async def authenticate_user(self, email: str, password: str) -> str:
        """
        Authenticate a user and generate an access token.

        Args:
            email: User's email address
            password: User's password

        Returns:
            str: JWT access token

        Raises:
            AuthenticationError: If credentials are invalid
            UserNotFoundError: If user does not exist
        """
        # Get user by email
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise UserNotFoundError(email=email)

        # Verify password
        if not verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid password")

        # Create and return access token
        return create_access_token(subject=str(user.id), email=user.email)
