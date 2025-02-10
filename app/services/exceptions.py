"""
Domain-specific exceptions for service layer.
"""

from typing import Any
from uuid import UUID


class DomainError(Exception):
    """Base class for domain-specific errors."""

    def __init__(self, code: int, context: dict[str, Any]):
        """
        Initialize domain error.

        Args:
            code: HTTP status code
            context: Error context dictionary
        """
        self.code = code
        self.context = context
        message = self.format_message()
        super().__init__(message)

    def format_message(self) -> str:
        """Format error message using context."""
        return f"Error {self.code} occurred"


class UserNotFoundError(DomainError):
    """Raised when a user is not found."""

    def __init__(self, user_id: UUID | None = None, email: str | None = None):
        """
        Initialize user not found error.

        Args:
            user_id: User's UUID if searching by ID
            email: User's email if searching by email
        """
        context = {}
        if user_id:
            context["user_id"] = str(user_id)
        if email:
            context["email"] = email
        super().__init__(404, context)

    def format_message(self) -> str:
        """Format user not found message."""
        if "user_id" in self.context:
            return f"User with ID {self.context['user_id']} not found"
        if "email" in self.context:
            return f"User with email {self.context['email']} not found"
        return "User not found"


class EmailAlreadyExistsError(DomainError):
    """Raised when attempting to use an email that's already registered."""

    def __init__(self, email: str):
        """
        Initialize email exists error.

        Args:
            email: The email that's already registered
        """
        super().__init__(409, {"email": email})

    def format_message(self) -> str:
        """Format email exists message."""
        return f"Email {self.context['email']} is already registered"


class AuthenticationError(DomainError):
    """Raised when authentication fails."""

    def __init__(self, message: str):
        """
        Initialize authentication error.

        Args:
            message: Authentication error message
        """
        super().__init__(401, {"message": message})

    def format_message(self) -> str:
        """Format authentication error message."""
        return str(self.context["message"])
