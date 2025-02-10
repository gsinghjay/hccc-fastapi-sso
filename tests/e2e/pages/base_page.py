"""Base page object model for E2E tests."""

from playwright.sync_api import Page
from typing import Any, Dict, TypeVar, cast

T = TypeVar("T")


class BasePage:
    """Base page object with common methods for all pages."""

    def __init__(self, page: Page):
        """Initialize the base page.

        Args:
            page: Playwright page object
        """
        self.page = page

    def navigate(self, url: str) -> None:
        """Navigate to a specific URL.

        Args:
            url: The URL to navigate to
        """
        self.page.goto(url)

    def get_network_response(self, url: str) -> Dict[str, Any]:
        """Get the response from a network request.

        Args:
            url: The URL to wait for

        Returns:
            The response JSON
        """
        with self.page.expect_response(
            lambda response: response.url == url and response.status == 200
        ) as response_info:
            response = response_info.value
            return cast(Dict[str, Any], response.json())

    def wait_for_selector(self, selector: str) -> None:
        """Wait for an element to be present on the page.

        Args:
            selector: The selector to wait for
        """
        self.page.wait_for_selector(selector)

    def get_text_content(self, selector: str) -> str:
        """Get the text content of an element.

        Args:
            selector: The selector to get text from

        Returns:
            The text content of the element
        """
        element = self.page.wait_for_selector(selector)
        if element is None:
            return ""
        return element.text_content() or ""
