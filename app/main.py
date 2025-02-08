"""
Main FastAPI application module.
"""
from fastapi import FastAPI

from app.api.router import api_router
from app.core.middleware import setup_middleware
from app.core.config import get_settings

settings = get_settings()

def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: The configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="HCCC Single Sign-On API Service",
        version="1.0.0",
        docs_url="/docs",
        openapi_url="/openapi.json",
        debug=settings.DEBUG
    )

    # Setup middleware
    setup_middleware(app)

    # Include API router with version prefix
    app.include_router(api_router, prefix=settings.API_PREFIX)

    return app


app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=settings.DEBUG
    )
