"""
Health check response schemas.
"""

from enum import Enum
from pydantic import BaseModel, Field


class HealthStatus(str, Enum):
    """Enumeration of possible health check statuses."""

    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class HealthResponse(BaseModel):
    """
    Schema for health check response.

    Attributes:
        status (HealthStatus): The current health status of the service
    """

    status: HealthStatus = Field(
        default=HealthStatus.HEALTHY,
        description="The current health status of the service",
    )

    model_config = {"json_schema_extra": {"example": {"status": "healthy"}}}
