"""
Middleware configuration for the FastAPI application.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings

settings = get_settings()

def setup_middleware(app: FastAPI) -> None:
    """
    Configure middleware for the FastAPI application.
    
    Sets up:
    - CORS middleware with configured origins
    - Rate limiting (if enabled)
    
    Args:
        app (FastAPI): The FastAPI application instance
    """
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # TODO: Add rate limiting middleware using settings.RATE_LIMIT_PER_MINUTE 