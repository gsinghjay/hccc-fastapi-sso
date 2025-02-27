"""
Health check endpoints for monitoring API status.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.schemas import HealthResponse, HTTPError
from app.services.health import HealthService

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "",
    response_model=HealthResponse,
    summary="Health Check",
    description="Comprehensive health check endpoint that monitors system metrics, database connectivity, and service status",
    responses={
        500: {"model": HTTPError, "description": "Internal server error"},
        503: {"model": HTTPError, "description": "Service unavailable"},
    },
)
async def health_check(db: AsyncSession = Depends(get_db)) -> HealthResponse:
    """
    Perform a comprehensive health check of the API service.

    Args:
        db: Database session dependency

    Returns:
        HealthResponse: The current health status of the service with detailed metrics

    Raises:
        HTTPException: If the service is unhealthy or degraded
    """
    health_status = await HealthService.get_health_status(db)

    if health_status.status == "unhealthy":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is currently unhealthy. Please check the logs for more details.",
        )

    return health_status
