"""E2E tests for the health endpoint."""
import pytest
from playwright.sync_api import Page
from typing import Dict, Any, cast
from tests.e2e.pages.base_page import BasePage

class HealthPage(BasePage):
    """Page object for health endpoint testing."""
    
    def get_health_status(self, base_url: str) -> Dict[str, Any]:
        """Get the health status from the API.
        
        Args:
            base_url: The base URL of the API
            
        Returns:
            The health status response
        """
        health_url = f"{base_url}/health"
        with self.page.expect_response(
            lambda response: response.url == health_url and response.status == 200
        ) as response_info:
            self.navigate(health_url)
            response = response_info.value
            return cast(Dict[str, Any], response.json())

@pytest.mark.e2e
def test_health_endpoint(page: Page, base_url: str) -> None:
    """Test the health endpoint returns correct status.
    
    Args:
        page: Playwright page fixture
        base_url: Base URL fixture
    """
    health_page = HealthPage(page)
    response = health_page.get_health_status(base_url)
    
    assert response["status"] == "healthy" 