"""
Health check endpoints for monitoring API status.
"""
from fastapi import APIRouter
from app.schemas import HealthResponse, HealthStatus, HTTPError

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)

@router.get(
    "",
    response_model=HealthResponse,
    summary="Health Check",
    description="Endpoint to verify API service status",
    responses={
        500: {"model": HTTPError, "description": "Internal server error"}
    }
)
async def health_check() -> HealthResponse:
    """
    Perform a health check of the API service.

    Returns:
        HealthResponse: The current health status of the service

    Raises:
        HTTPException: If the service is unhealthy
    """
    # For now, we'll just return healthy. In the future, we can add more checks
    # like database connectivity, external services, etc.
    return HealthResponse(status=HealthStatus.HEALTHY) 