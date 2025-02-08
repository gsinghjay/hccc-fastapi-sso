"""
Tests for the health check endpoint.
"""
import pytest
from httpx import AsyncClient

from app.schemas import HealthResponse, HealthStatus


@pytest.mark.anyio
async def test_health_check(async_client: AsyncClient) -> None:
    """
    Test the health check endpoint returns the expected response.
    
    Args:
        async_client (AsyncClient): Async client fixture for making HTTP requests
    """
    response = await async_client.get("/v1/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "healthy"}
    
    # Validate against our Pydantic model
    health_response = HealthResponse(**data)
    assert health_response.status == HealthStatus.HEALTHY 