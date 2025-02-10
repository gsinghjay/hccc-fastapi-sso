"""
Health check response schemas.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, Optional
from pydantic import BaseModel, Field


class ServiceStatus(str, Enum):
    """Enumeration of possible service check statuses."""

    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


class HealthStatus(str, Enum):
    """Enumeration of possible overall health check statuses."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class SystemMetrics(BaseModel):
    """System resource metrics."""

    cpu_usage: float = Field(..., description="CPU usage percentage", ge=0, le=100)
    memory_usage: float = Field(
        ..., description="Memory usage percentage", ge=0, le=100
    )
    disk_usage: float = Field(..., description="Disk usage percentage", ge=0, le=100)


class ServiceCheck(BaseModel):
    """Individual service check result."""

    status: ServiceStatus = Field(..., description="Status of the service check")
    latency_ms: float = Field(..., description="Latency of the check in milliseconds")
    message: Optional[str] = Field(None, description="Additional status message")
    last_checked: datetime = Field(..., description="Timestamp of the last check")


class HealthResponse(BaseModel):
    """
    Schema for health check response.

    Attributes:
        status (HealthStatus): The overall health status of the service
        version (str): The current version of the service
        uptime_seconds (float): How long the service has been running
        system_metrics (SystemMetrics): Current system resource metrics
        checks (Dict[str, ServiceCheck]): Results of individual service checks
    """

    status: HealthStatus = Field(
        default=HealthStatus.HEALTHY,
        description="The overall health status of the service",
    )
    version: str = Field(..., description="The current version of the service")
    uptime_seconds: float = Field(..., description="Service uptime in seconds")
    system_metrics: SystemMetrics = Field(..., description="System resource metrics")
    checks: Dict[str, ServiceCheck] = Field(
        ..., description="Results of individual service checks"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "uptime_seconds": 3600.0,
                "system_metrics": {
                    "cpu_usage": 45.2,
                    "memory_usage": 62.7,
                    "disk_usage": 78.1,
                },
                "checks": {
                    "database": {
                        "status": "pass",
                        "latency_ms": 12.3,
                        "message": "Connected successfully",
                        "last_checked": "2024-03-14T12:00:00Z",
                    }
                },
            }
        }
    }
