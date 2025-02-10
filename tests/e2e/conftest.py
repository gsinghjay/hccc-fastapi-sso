"""E2E test configuration with Playwright."""
import pytest
from typing import Generator
from playwright.sync_api import Browser, Page, Playwright
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import get_settings
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
def api_client() -> Generator[TestClient, None, None]:
    """Create a FastAPI test client."""
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture(scope="session")
def base_url() -> str:
    """Get the base URL for the application."""
    settings = get_settings_override()
    return f"http://localhost{settings.API_V1_PATH}" 