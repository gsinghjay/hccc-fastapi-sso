"""
Main FastAPI application module.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp
from starlette.requests import Request
from starlette.responses import Response
import os

from app.api.router import api_router
from app.core.middleware import setup_middleware
from app.core.config import get_settings

settings = get_settings()

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="app/templates")


class HTTPSRedirectMiddleware(BaseHTTPMiddleware):
    """Middleware to handle scheme setting."""

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Preserve the original scheme in development
        if "headers" in request.scope:
            # Get the original scheme from X-Forwarded-Proto if present
            forwarded_proto = next(
                (
                    value.decode()
                    for key, value in request.scope["headers"]
                    if key.decode().lower() == "x-forwarded-proto"
                ),
                request.url.scheme,
            )
            request.scope["scheme"] = forwarded_proto
        return await call_next(request)


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: The configured FastAPI application instance
    """
    swagger_ui_params = {
        "persistAuthorization": True,
        "displayRequestDuration": True,
        "filter": True,
        "syntaxHighlight.theme": "monokai",
        "docExpansion": "list",
        "defaultModelsExpandDepth": 3,
        "defaultModelExpandDepth": 3,
        "tryItOutEnabled": True,
        "requestSnippetsEnabled": True,
        "deepLinking": True,
        "showExtensions": True,
        "showCommonExtensions": True,
        "supportedSubmitMethods": [
            "get",
            "put",
            "post",
            "delete",
            "options",
            "head",
            "patch",
            "trace",
        ],
        "dom_id": "#swagger-ui",
        "layout": "BaseLayout",
        "validatorUrl": None,  # Disable validator
        "oauth2RedirectUrl": None,  # Disable OAuth2 redirect
        "displayOperationId": True,
        "withCredentials": True,
        "queryConfigEnabled": True,
        "defaultModelRendering": "model",
        "displaySchemas": True,
    }

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="HCCC Single Sign-On API Service",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        swagger_ui_parameters=swagger_ui_params,
        debug=settings.DEBUG,
        root_path="",
        root_path_in_servers=False,
        servers=[
            {
                "url": "https://localhost",  # Always use HTTPS since Traefik handles SSL
                "description": (
                    "Development server" if settings.DEBUG else "Production server"
                ),
            }
        ],
        openapi_prefix="",  # Important: This ensures the OpenAPI schema uses the correct base URL
    )

    # Mount static files directory
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    # Add template routes
    @app.get("/", include_in_schema=False)
    async def home(request: Request):
        """Render the home page."""
        return templates.TemplateResponse(
            "base.html",
            {"request": request, "title": "Welcome to HCCC SSO"}
        )

    # Setup middleware
    setup_middleware(app)

    # Include API router with version prefix
    app.include_router(api_router, prefix=settings.API_PREFIX)

    return app


app = create_application()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.DEBUG)
