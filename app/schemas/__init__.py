"""
Schema models for the application.
"""

from app.schemas.base import HTTPError
from app.schemas.health import HealthResponse, HealthStatus

__all__ = [
    "HealthResponse",
    "HealthStatus",
    "HTTPError",
]
