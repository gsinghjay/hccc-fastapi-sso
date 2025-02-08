"""
Test configuration and fixtures.
"""
from typing import Any, AsyncGenerator, Awaitable, Callable, cast, Coroutine

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app

# Type alias for ASGI application
ASGIApp = Callable[
    [
        dict[str, Any],  # scope
        Callable[[], Awaitable[dict[str, Any]]],  # receive
        Callable[[dict[str, Any]], Coroutine[None, None, None]]  # send
    ],
    Coroutine[None, None, None]
]


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Async client fixture for testing FastAPI endpoints.
    
    Yields:
        AsyncClient: An async client configured to make requests to the test app
    """
    # Cast the FastAPI app to the correct ASGI application type
    asgi_app = cast(ASGIApp, app)
    
    async with AsyncClient(
        transport=ASGITransport(app=asgi_app), base_url="http://test"
    ) as client:
        yield client
