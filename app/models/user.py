"""
User model for database operations.
"""

from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4

from app.db.base import Base


class User(Base):
    """User model for authentication and profile management."""

    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, index=True)
    email: Mapped[str] = mapped_column(
        String(length=255), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(length=255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(length=255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        """String representation of the user."""
        return f"<User {self.email}>"
