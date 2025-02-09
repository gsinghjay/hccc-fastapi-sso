"""
Central router configuration for all API endpoints.
"""
from fastapi import APIRouter

from app.api.v1 import health
from app.core.config import get_settings

settings = get_settings()

# Create the main API router
api_router = APIRouter()

# Include all API version routers
api_router.include_router(health.router, prefix=f"/{settings.API_V1_STR}")

# Add additional version routers here as needed
# api_router.include_router(v2_router, prefix="/v2") 