"""E2E tests for the health endpoint."""

from typing import cast, Any
from httpx import AsyncClient, ASGITransport
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from tests.conftest import get_settings_override

# Create a new settings instance for testing
settings = get_settings_override()


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_health_endpoint(test_db: AsyncSession) -> None:
    """Test the health endpoint returns correct status and metrics."""
    # Cast the FastAPI app to Any to satisfy the type checker
    asgi_app = cast(Any, app)
    async with AsyncClient(
        transport=ASGITransport(app=asgi_app), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "database" in data["checks"]
        assert data["checks"]["database"]["status"] == "pass"
        assert data["checks"]["database"]["latency_ms"] > 0
