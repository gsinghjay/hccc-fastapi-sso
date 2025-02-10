"""E2E test configuration with Playwright."""

import pytest
from typing import Generator, AsyncGenerator, Any, cast
from playwright.sync_api import Browser, Page, Playwright
from httpx import ASGITransport, AsyncClient
from app.main import app
from tests.conftest import get_settings_override


@pytest.fixture(scope="session")
def browser_context(playwright: Playwright) -> Generator[Browser, None, None]:
    """Create a browser context for testing."""
    browser = playwright.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture
def page(browser_context: Browser) -> Generator[Page, None, None]:
    """Create a new page for each test."""
    context = browser_context.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="session")
async def api_client() -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client."""
    settings = get_settings_override()
    # Cast the FastAPI app to Any to satisfy the type checker
    # This is safe because FastAPI implements the ASGI interface
    asgi_app = cast(Any, app)
    async with AsyncClient(
        transport=ASGITransport(app=asgi_app),
        base_url=f"http://test{settings.API_V1_PATH}",
    ) as client:
        yield client


@pytest.fixture(scope="session")
def base_url() -> str:
    """Get the base URL for the application."""
    settings = get_settings_override()
    return f"http://fastapi_app:8000{settings.API_V1_PATH}"
