"""
Main FastAPI application module.
"""
from fastapi import FastAPI

from app.api.router import api_router
from app.core.middleware import setup_middleware


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: The configured FastAPI application instance
    """
    app = FastAPI(
        title="HCCC FastAPI SSO",
        description="HCCC Single Sign-On API Service",
        version="1.0.0",
    )

    # Setup middleware
    setup_middleware(app)

    # Include API router
    app.include_router(api_router)

    return app


app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
