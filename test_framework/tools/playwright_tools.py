from langchain_classic.tools import tool
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from typing import Optional


# Global page reference - will be injected by the agent
_page: Optional[Page] = None


def set_page(page: Page):
    """Set the global page reference for tools to use."""
    global _page
    _page = page


def get_page() -> Page:
    """Get the global page reference."""
    if _page is None:
        raise RuntimeError("Page not initialized. Call set_page() first.")
    return _page


@tool
def navigate_to_url(url: str) -> str:
    """
    Navigate to a URL in the browser.

    Args:
        url: The URL to navigate to (e.g., 'https://example.com')

    Returns:
        Success or error message
    """
    try:
        page = get_page()
        page.goto(url, wait_until='networkidle', timeout=30000)
        return f"Successfully navigated to {url}"
    except Exception as e:
        return f"Error navigating to {url}: {str(e)}"


@tool
def click_element(selector: str) -> str:
    """
    Click on an element using a CSS selector.

    Args:
        selector: CSS selector for the element (e.g., '#submit-btn', '.button', 'button[type="submit"]')

    Returns:
        Success or error message
    """
    try:
        page = get_page()
        page.click(selector, timeout=10000)
        return f"Successfully clicked element: {selector}"
    except PlaywrightTimeoutError:
        return f"Error: Element '{selector}' not found or not clickable"
    except Exception as e:
        return f"Error clicking element '{selector}': {str(e)}"


@tool
def fill_input(selector: str, value: str) -> str:
    """
    Fill an input field with a value.

    Args:
        selector: CSS selector for the input element
        value: The text to fill in the input

    Returns:
        Success or error message
    """
    try:
        page = get_page()
        page.fill(selector, value, timeout=10000)
        return f"Successfully filled '{selector}' with '{value}'"
    except PlaywrightTimeoutError:
        return f"Error: Input field '{selector}' not found"
    except Exception as e:
        return f"Error filling input '{selector}': {str(e)}"


@tool
def press_key(key: str) -> str:
    """
    Press a keyboard key.

    Args:
        key: Key to press (e.g., 'Enter', 'Escape', 'Tab', 'ArrowDown')

    Returns:
        Success or error message
    """
    try:
        page = get_page()
        page.keyboard.press(key)
        return f"Successfully pressed key: {key}"
    except Exception as e:
        return f"Error pressing key '{key}': {str(e)}"


@tool
def wait_for_timeout(milliseconds: int) -> str:
    """
    Wait for a specified number of milliseconds.

    Args:
        milliseconds: Number of milliseconds to wait

    Returns:
        Success message
    """
    try:
        page = get_page()
        page.wait_for_timeout(milliseconds)
        return f"Waited for {milliseconds}ms"
    except Exception as e:
        return f"Error waiting: {str(e)}"


@tool
def get_page_title() -> str:
    """
    Get the current page title.

    Returns:
        The page title
    """
    try:
        page = get_page()
        title = page.title()
        return f"Page title: {title}"
    except Exception as e:
        return f"Error getting page title: {str(e)}"


@tool
def get_current_url() -> str:
    """
    Get the current page URL.

    Returns:
        The current URL
    """
    try:
        page = get_page()
        url = page.url
        return f"Current URL: {url}"
    except Exception as e:
        return f"Error getting current URL: {str(e)}"


@tool
def take_screenshot(filename: str) -> str:
    """
    Take a screenshot of the current page.

    Args:
        filename: Filename to save the screenshot (e.g., 'screenshot.png')

    Returns:
        Success or error message
    """
    try:
        page = get_page()
        page.screenshot(path=filename)
        return f"Screenshot saved to {filename}"
    except Exception as e:
        return f"Error taking screenshot: {str(e)}"
