"""
Tests for the health check endpoint.
"""
from fastapi.testclient import TestClient

from app.schemas import HealthResponse, HealthStatus
from app.core.config import get_settings

settings = get_settings()


def test_read_health_check(client: TestClient) -> None:
    """Test successful health check"""
    response = client.get(f"{settings.API_V1_PATH}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_health_check_validation(client: TestClient) -> None:
    """Test response validates against schema"""
    response = client.get(f"{settings.API_V1_PATH}/health")
    data = response.json()
    # Validate against our Pydantic model
    health_response = HealthResponse(**data)
    assert health_response.status == HealthStatus.HEALTHY 