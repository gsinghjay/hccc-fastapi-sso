"""
SQLAlchemy implementation of the user repository.
"""

from typing import Protocol, List, Sequence, cast, Awaitable
from uuid import UUID
from sqlalchemy import select, delete
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

    async def delete(self, user_id: UUID) -> bool:
        """
        Delete a user by ID.

        Args:
            user_id: ID of the user to delete

        Returns:
            bool: True if user was deleted, False if user was not found
        """
        ...

    async def list(self) -> List[User]:
        """
        List all users.

        Returns:
            List[User]: List of all users
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
        scalar_result = result.scalar_one_or_none()
        if hasattr(scalar_result, "__await__"):
            scalar_result = await cast(Awaitable[User | None], scalar_result)
        return scalar_result

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
        scalar_result = result.scalar_one_or_none()
        if hasattr(scalar_result, "__await__"):
            scalar_result = await cast(Awaitable[User | None], scalar_result)
        return scalar_result

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

    async def delete(self, user_id: UUID) -> bool:
        """
        Delete a user by ID.

        Args:
            user_id: ID of the user to delete

        Returns:
            bool: True if user was deleted, False if user was not found
        """
        stmt = delete(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def list(self) -> List[User]:
        """
        List all users.

        Returns:
            List[User]: List of all users
        """
        stmt = select(User)
        result = await self.session.scalars(stmt)
        all_results = result.all()
        if hasattr(all_results, "__await__"):
            all_results = await cast(Awaitable[Sequence[User]], all_results)
        return list(all_results)
