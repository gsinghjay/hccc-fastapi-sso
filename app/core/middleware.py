"""
Middleware configuration for the FastAPI application.
"""

from typing import DefaultDict
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp
from app.core.config import get_settings
import time
from datetime import datetime
import asyncio
from collections import defaultdict
import uuid

settings = get_settings()


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware using a token bucket algorithm."""

    def __init__(self, app: ASGIApp, rate_limit: int = 60):
        super().__init__(app)
        self.rate_limit = rate_limit
        self.tokens: DefaultDict[str, float] = defaultdict(lambda: self.rate_limit)
        self.last_update: DefaultDict[str, datetime] = defaultdict(datetime.now)
        self.lock = asyncio.Lock()

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        client_ip = request.client.host if request.client else "unknown"

        async with self.lock:
            now = datetime.now()
            time_passed = (now - self.last_update[client_ip]).total_seconds()
            self.tokens[client_ip] = min(
                self.rate_limit,
                self.tokens[client_ip] + time_passed * (self.rate_limit / 60),
            )

            if self.tokens[client_ip] >= 1:
                self.tokens[client_ip] -= 1
                self.last_update[client_ip] = now
                return await call_next(request)

        return Response(
            content="Rate limit exceeded",
            status_code=429,
            headers={"Retry-After": "60"},
        )


class HTTPSRedirectMiddleware(BaseHTTPMiddleware):
    """Middleware to handle scheme setting and HTTPS redirection."""

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if settings.DEBUG:
            # Development mode: allow both HTTP and HTTPS
            return await call_next(request)
        else:
            # Production mode: ensure HTTPS
            if request.url.scheme != "https":
                return Response(
                    status_code=301,
                    headers={"Location": str(request.url.replace(scheme="https"))},
                )
            return await call_next(request)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware to add request ID to all requests."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


class TimingMiddleware(BaseHTTPMiddleware):
    """Middleware to track request timing."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers to all responses."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        # Basic security headers
        security_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }

        if not settings.DEBUG:
            # Production security headers
            security_headers.update(
                {
                    "X-Frame-Options": "DENY",
                    "X-Permitted-Cross-Domain-Policies": "none",
                    "Cross-Origin-Opener-Policy": "same-origin",
                    "Cross-Origin-Resource-Policy": "same-origin",
                    "Cross-Origin-Embedder-Policy": "require-corp",
                }
            )

            # Production CSP - Strict security
            response.headers["Content-Security-Policy"] = "; ".join(
                [
                    "default-src 'self'",
                    "script-src 'self'",
                    "style-src 'self'",
                    "img-src 'self' data:",
                    "font-src 'self' data:",
                    "form-action 'self'",
                    "frame-ancestors 'none'",
                    "base-uri 'self'",
                    "object-src 'none'",
                    "connect-src 'self'",
                    "media-src 'none'",
                    "worker-src 'none'",
                ]
            )

            # HSTS in production
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )

            # Permissions Policy in production
            response.headers["Permissions-Policy"] = "; ".join(
                [
                    "accelerometer=()",
                    "camera=()",
                    "geolocation=()",
                    "gyroscope=()",
                    "magnetometer=()",
                    "microphone=()",
                    "payment=()",
                    "usb=()",
                ]
            )
        else:
            # Development CSP - Allow Swagger UI and development resources
            response.headers["Content-Security-Policy"] = "; ".join(
                [
                    "default-src 'self' 'unsafe-inline' 'unsafe-eval' https: http: data:",
                    "script-src 'self' 'unsafe-inline' 'unsafe-eval' https: http:",
                    "style-src 'self' 'unsafe-inline' https: http:",
                    "img-src 'self' https: http: data:",
                    "font-src 'self' https: http: data:",
                    "connect-src 'self' https: http:",
                    "frame-ancestors 'self'",
                    "form-action 'self'",
                ]
            )

            # Allow iframe in development for Swagger UI
            security_headers["X-Frame-Options"] = "SAMEORIGIN"

        response.headers.update(security_headers)
        return response


def setup_middleware(app: FastAPI) -> None:
    """
    Configure middleware for the FastAPI application.

    Sets up:
    - Request ID tracking
    - Request timing
    - Security headers
    - CORS with configured origins
    - Rate limiting

    Args:
        app (FastAPI): The FastAPI application instance
    """
    # Order matters! Add middleware in the correct sequence
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(TimingMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)

    # Configure CORS with environment-specific settings
    if settings.DEBUG:
        # Development: Allow all origins
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=[
                "X-Request-ID",
                "X-Process-Time",
                "Content-Disposition",
                "Content-Type",
                "Authorization",
            ],
            max_age=3600,
        )
    else:
        # Production: Strict CORS
        origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            allow_headers=[
                "Authorization",
                "Content-Type",
                "X-Request-ID",
                "Accept",
                "Origin",
                "X-Requested-With",
            ],
            expose_headers=["X-Request-ID", "X-Process-Time", "Content-Disposition"],
            max_age=3600,
        )

    # Rate limiting (if enabled)
    if settings.RATE_LIMIT_PER_MINUTE > 0:
        app.add_middleware(
            RateLimitMiddleware, rate_limit=settings.RATE_LIMIT_PER_MINUTE
        )
