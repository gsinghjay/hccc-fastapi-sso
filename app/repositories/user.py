"""
SQLAlchemy implementation of the user repository.
"""

from typing import Protocol
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository(Protocol):
    """Protocol defining the interface for user repositories."""

    async def get_by_id(self, user_id: UUID) -> User | None:
        """
        Get user by ID.

        Args:
            user_id: User's UUID

        Returns:
            User | None: User if found, None otherwise
        """
        ...

    async def get_by_email(self, email: str) -> User | None:
        """
        Get user by email.

        Args:
            email: User's email address

        Returns:
            User | None: User if found, None otherwise
        """
        ...

    async def create(self, user: User) -> User:
        """
        Create a new user.

        Args:
            user: User to create

        Returns:
            User: Created user
        """
        ...

    async def update(self, user: User) -> User:
        """
        Update an existing user.

        Args:
            user: User to update

        Returns:
            User: Updated user
        """
        ...


class SQLAlchemyUserRepository:
    """SQLAlchemy implementation of the UserRepository protocol."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        """
        Get user by ID.

        Args:
            user_id: User's UUID

        Returns:
            User | None: User if found, None otherwise
        """
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """
        Get user by email.

        Args:
            email: User's email address

        Returns:
            User | None: User if found, None otherwise
        """
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        """
        Create a new user.

        Args:
            user: User to create

        Returns:
            User: Created user
        """
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user: User) -> User:
        """
        Update an existing user.

        Args:
            user: User to update

        Returns:
            User: Updated user
        """
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
