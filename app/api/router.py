"""
Central router configuration for all API endpoints.
"""
from fastapi import APIRouter

from app.api.v1 import health


# Create the main API router
api_router = APIRouter()

# Include all API version routers
api_router.include_router(health.router, prefix="/v1")

# Add additional version routers here as needed
# api_router.include_router(v2_router, prefix="/v2") 