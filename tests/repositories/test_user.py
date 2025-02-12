"""
Tests for UserRepository.

This module contains tests for all CRUD operations and edge cases
in the UserRepository class.
"""

import pytest
from unittest.mock import AsyncMock
from uuid import UUID
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.repositories.user import SQLAlchemyUserRepository


class TestUserRepository:
    """Test cases for UserRepository."""

    @pytest.mark.asyncio
    async def test_create_user(
        self,
        user_repository: SQLAlchemyUserRepository,
        test_user: User,
        mock_db_session: AsyncMock,
    ) -> None:
        """Test creating a new user."""
        # Setup mock
        mock_db_session.refresh.return_value = None

        # Create user
        created_user = await user_repository.create(test_user)

        # Verify behavior
        mock_db_session.add.assert_called_once_with(test_user)
        await mock_db_session.commit()
        await mock_db_session.refresh(test_user)
        assert created_user == test_user

    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(
        self,
        user_repository: SQLAlchemyUserRepository,
        test_user: User,
        mock_db_session: AsyncMock,
    ) -> None:
        """Test that creating a user with duplicate email raises an error."""
        # Setup mock to raise IntegrityError
        mock_db_session.commit.side_effect = IntegrityError(
            statement="",
            params={},
            orig=Exception("Duplicate key value violates unique constraint"),
        )

        # Verify it raises an integrity error
        with pytest.raises(IntegrityError):
            await user_repository.create(test_user)

        mock_db_session.add.assert_called_once_with(test_user)

    @pytest.mark.asyncio
    async def test_get_user_by_id(
        self,
        user_repository: SQLAlchemyUserRepository,
        test_user: User,
        mock_db_session: AsyncMock,
    ) -> None:
        """Test retrieving a user by ID."""
        # Setup mock
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = test_user
        mock_db_session.execute.return_value = mock_result

        # Get user by ID
        retrieved_user = await user_repository.get_by_id(test_user.id)

        # Verify behavior
        mock_db_session.execute.assert_called_once()
        assert retrieved_user == test_user

    @pytest.mark.asyncio
    async def test_get_user_by_id_not_found(
        self,
        user_repository: SQLAlchemyUserRepository,
        mock_db_session: AsyncMock,
    ) -> None:
        """Test retrieving a non-existent user by ID returns None."""
        # Setup mock
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result

        # Get non-existent user
        non_existent_id = UUID("11111111-1111-1111-1111-111111111111")
        user = await user_repository.get_by_id(non_existent_id)

        # Verify behavior
        mock_db_session.execute.assert_called_once()
        assert user is None

    @pytest.mark.asyncio
    async def test_get_user_by_email(
        self,
        user_repository: SQLAlchemyUserRepository,
        test_user: User,
        mock_db_session: AsyncMock,
    ) -> None:
        """Test retrieving a user by email."""
        # Setup mock
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = test_user
        mock_db_session.execute.return_value = mock_result

        # Get user by email
        retrieved_user = await user_repository.get_by_email(test_user.email)

        # Verify behavior
        mock_db_session.execute.assert_called_once()
        assert retrieved_user == test_user

    @pytest.mark.asyncio
    async def test_get_user_by_email_not_found(
        self,
        user_repository: SQLAlchemyUserRepository,
        mock_db_session: AsyncMock,
    ) -> None:
        """Test retrieving a non-existent user by email returns None."""
        # Setup mock
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result

        # Get non-existent user
        user = await user_repository.get_by_email("nonexistent@example.com")

        # Verify behavior
        mock_db_session.execute.assert_called_once()
        assert user is None

    @pytest.mark.asyncio
    async def test_update_user(
        self,
        user_repository: SQLAlchemyUserRepository,
        test_user: User,
        mock_db_session: AsyncMock,
    ) -> None:
        """Test updating a user's information."""
        # Setup mock
        mock_db_session.refresh.return_value = None

        # Update user
        updated_user = await user_repository.update(test_user)

        # Verify behavior
        mock_db_session.add.assert_called_once_with(test_user)
        await mock_db_session.commit()
        await mock_db_session.refresh(test_user)
        assert updated_user == test_user

    @pytest.mark.asyncio
    async def test_delete_user(
        self,
        user_repository: SQLAlchemyUserRepository,
        test_user: User,
        mock_db_session: AsyncMock,
    ) -> None:
        """Test deleting a user."""
        # Setup mock
        mock_result = AsyncMock()
        mock_result.rowcount = 1
        mock_db_session.execute.return_value = mock_result

        # Delete user
        deleted = await user_repository.delete(test_user.id)

        # Verify behavior
        mock_db_session.execute.assert_called_once()
        await mock_db_session.commit()
        assert deleted is True

    @pytest.mark.asyncio
    async def test_delete_user_not_found(
        self,
        user_repository: SQLAlchemyUserRepository,
        mock_db_session: AsyncMock,
    ) -> None:
        """Test deleting a non-existent user returns False."""
        # Setup mock
        mock_result = AsyncMock()
        mock_result.rowcount = 0
        mock_db_session.execute.return_value = mock_result

        # Delete non-existent user
        non_existent_id = UUID("11111111-1111-1111-1111-111111111111")
        deleted = await user_repository.delete(non_existent_id)

        # Verify behavior
        mock_db_session.execute.assert_called_once()
        await mock_db_session.commit()
        assert deleted is False

    @pytest.mark.asyncio
    async def test_list_users(
        self,
        user_repository: SQLAlchemyUserRepository,
        test_user: User,
        mock_db_session: AsyncMock,
    ) -> None:
        """Test listing all users."""
        # Setup mock
        mock_result = AsyncMock()
        mock_result.all.return_value = [test_user]
        mock_db_session.scalars.return_value = mock_result

        # List users
        users = await user_repository.list()

        # Verify behavior
        mock_db_session.scalars.assert_called_once()
        assert len(users) == 1
        assert users[0] == test_user

    @pytest.mark.asyncio
    async def test_list_users_empty(
        self,
        user_repository: SQLAlchemyUserRepository,
        mock_db_session: AsyncMock,
    ) -> None:
        """Test listing users when there are none returns empty list."""
        # Setup mock
        mock_result = AsyncMock()
        mock_result.all.return_value = []
        mock_db_session.scalars.return_value = mock_result

        # List users
        users = await user_repository.list()

        # Verify behavior
        mock_db_session.scalars.assert_called_once()
        assert len(users) == 0
