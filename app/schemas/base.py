"""
Base schema models for common use cases.
"""
from pydantic import BaseModel, Field


class HTTPError(BaseModel):
    """
    Standard HTTP error response model.

    Attributes:
        detail (str): A human-readable error message
    """
    detail: str = Field(
        ...,
        description="A human-readable error message explaining what went wrong"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "An error occurred while processing your request"
            }
        }
    }
