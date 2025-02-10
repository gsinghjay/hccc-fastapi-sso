"""
Unit tests for health check endpoints.
"""

from typing import Any, Generator
import pytest
from unittest.mock import AsyncMock, patch
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.schemas.health import HealthStatus, ServiceStatus, SystemMetrics
from app.main import app
from app.db.base import get_db

settings = get_settings()


@pytest.fixture
def override_get_db(mock_db: AsyncSession) -> Generator[None, None, None]:
    """Override the database dependency."""
    app.dependency_overrides[get_db] = lambda: mock_db
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_health_check_healthy(
    mock_db: AsyncSession, override_get_db: Any
) -> None:
    """Test health check endpoint returns healthy status when all systems are operational."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        with (
            patch(
                "app.services.health.HealthService.get_system_metrics"
            ) as mock_metrics,
            patch("app.services.health.time.time", return_value=1000.0),
            patch("os.getenv", return_value="1.0.0"),
        ):
            # Mock system metrics
            mock_metrics.return_value = SystemMetrics(
                cpu_usage=50.0,
                memory_usage=60.0,
                disk_usage=70.0,
            )

            # Create a new AsyncMock for execute
            mock_execute = AsyncMock()
            # Assign the mock to the execute attribute
            mock_db.execute = mock_execute  # type: ignore[method-assign]

            response = await client.get(f"{settings.API_PREFIX}/v1/health")

            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["status"] == HealthStatus.HEALTHY
            assert data["version"] == "1.0.0"
            assert isinstance(data["uptime_seconds"], float)
            assert data["system_metrics"]["cpu_usage"] == 50.0
            assert data["system_metrics"]["memory_usage"] == 60.0
            assert data["system_metrics"]["disk_usage"] == 70.0
            assert data["checks"]["database"]["status"] == ServiceStatus.PASS


@pytest.mark.asyncio
async def test_health_check_degraded(
    mock_db: AsyncSession, override_get_db: Any
) -> None:
    """Test health check endpoint returns degraded status when system resources are strained."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        with (
            patch(
                "app.services.health.HealthService.get_system_metrics"
            ) as mock_metrics,
            patch("app.services.health.time.time", return_value=1000.0),
            patch("os.getenv", return_value="1.0.0"),
        ):
            # Mock high system metrics
            mock_metrics.return_value = SystemMetrics(
                cpu_usage=95.0,
                memory_usage=60.0,
                disk_usage=70.0,
            )

            # Create a new AsyncMock for execute
            mock_execute = AsyncMock()
            # Assign the mock to the execute attribute
            mock_db.execute = mock_execute  # type: ignore[method-assign]

            response = await client.get(f"{settings.API_PREFIX}/v1/health")

            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["status"] == HealthStatus.DEGRADED
            assert data["checks"]["database"]["status"] == ServiceStatus.PASS


@pytest.mark.asyncio
async def test_health_check_unhealthy(
    mock_db: AsyncSession, override_get_db: Any
) -> None:
    """Test health check endpoint returns 503 when database is down."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        with (
            patch(
                "app.services.health.HealthService.get_system_metrics"
            ) as mock_metrics,
            patch("app.services.health.time.time", return_value=1000.0),
            patch("os.getenv", return_value="1.0.0"),
        ):
            # Mock normal system metrics
            mock_metrics.return_value = SystemMetrics(
                cpu_usage=50.0,
                memory_usage=60.0,
                disk_usage=70.0,
            )

            # Create a new AsyncMock for execute with an error
            mock_execute = AsyncMock(
                side_effect=Exception("Database connection failed")
            )
            # Assign the mock to the execute attribute
            mock_db.execute = mock_execute  # type: ignore[method-assign]

            response = await client.get(f"{settings.API_PREFIX}/v1/health")

            assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
            data = response.json()
            assert "Service is currently unhealthy" in data["detail"]
