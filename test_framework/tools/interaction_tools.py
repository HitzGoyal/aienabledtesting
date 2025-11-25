from langchain_classic.tools import tool
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from typing import Optional


# Global page reference - will be injected by the agent
_page: Optional[Page] = None


def set_page(page: Page):
    """Set the global page reference for interaction tools."""
    global _page
    _page = page


def get_page() -> Page:
    """Get the global page reference."""
    if _page is None:
        raise RuntimeError("Page not initialized. Call set_page() first.")
    return _page


@tool
def hover_element(selector: str) -> str:
    """
    Hover over an element.

    Args:
        selector: CSS selector for the element to hover

    Returns:
        Success or error message
    """
    try:
        page = get_page()
        page.hover(selector, timeout=10000)
        return f"Successfully hovered over element: {selector}"
    except PlaywrightTimeoutError:
        return f"Error: Element '{selector}' not found"
    except Exception as e:
        return f"Error hovering over element '{selector}': {str(e)}"


@tool
def double_click_element(selector: str) -> str:
    """
    Double-click on an element.

    Args:
        selector: CSS selector for the element to double-click

    Returns:
        Success or error message
    """
    try:
        page = get_page()
        page.dblclick(selector, timeout=10000)
        return f"Successfully double-clicked element: {selector}"
    except PlaywrightTimeoutError:
        return f"Error: Element '{selector}' not found"
    except Exception as e:
        return f"Error double-clicking element '{selector}': {str(e)}"


@tool
def right_click_element(selector: str) -> str:
    """
    Right-click (context menu) on an element.

    Args:
        selector: CSS selector for the element to right-click

    Returns:
        Success or error message
    """
    try:
        page = get_page()
        page.click(selector, button='right', timeout=10000)
        return f"Successfully right-clicked element: {selector}"
    except PlaywrightTimeoutError:
        return f"Error: Element '{selector}' not found"
    except Exception as e:
        return f"Error right-clicking element '{selector}': {str(e)}"


@tool
def select_option(selector: str, value: str) -> str:
    """
    Select an option from a dropdown/select element.

    Args:
        selector: CSS selector for the select element
        value: Value or label of the option to select

    Returns:
        Success or error message
    """
    try:
        page = get_page()
        page.select_option(selector, value, timeout=10000)
        return f"Successfully selected option '{value}' in '{selector}'"
    except PlaywrightTimeoutError:
        return f"Error: Select element '{selector}' not found"
    except Exception as e:
        return f"Error selecting option in '{selector}': {str(e)}"


@tool
def check_checkbox(selector: str) -> str:
    """
    Check a checkbox or radio button.

    Args:
        selector: CSS selector for the checkbox element

    Returns:
        Success or error message
    """
    try:
        page = get_page()
        page.check(selector, timeout=10000)
        return f"Successfully checked checkbox: {selector}"
    except PlaywrightTimeoutError:
        return f"Error: Checkbox '{selector}' not found"
    except Exception as e:
        return f"Error checking checkbox '{selector}': {str(e)}"


@tool
def uncheck_checkbox(selector: str) -> str:
    """
    Uncheck a checkbox.

    Args:
        selector: CSS selector for the checkbox element

    Returns:
        Success or error message
    """
    try:
        page = get_page()
        page.uncheck(selector, timeout=10000)
        return f"Successfully unchecked checkbox: {selector}"
    except PlaywrightTimeoutError:
        return f"Error: Checkbox '{selector}' not found"
    except Exception as e:
        return f"Error unchecking checkbox '{selector}': {str(e)}"


@tool
def upload_file(selector: str, file_path: str) -> str:
    """
    Upload a file to a file input element.

    Args:
        selector: CSS selector for the file input element
        file_path: Path to the file to upload

    Returns:
        Success or error message
    """
    try:
        page = get_page()
        page.set_input_files(selector, file_path, timeout=10000)
        return f"Successfully uploaded file '{file_path}' to '{selector}'"
    except PlaywrightTimeoutError:
        return f"Error: File input '{selector}' not found"
    except Exception as e:
        return f"Error uploading file to '{selector}': {str(e)}"


@tool
def scroll_to_element(selector: str) -> str:
    """
    Scroll to make an element visible in the viewport.

    Args:
        selector: CSS selector for the element to scroll to

    Returns:
        Success or error message
    """
    try:
        page = get_page()
        page.locator(selector).scroll_into_view_if_needed(timeout=10000)
        return f"Successfully scrolled to element: {selector}"
    except PlaywrightTimeoutError:
        return f"Error: Element '{selector}' not found"
    except Exception as e:
        return f"Error scrolling to element '{selector}': {str(e)}"


@tool
def get_element_text(selector: str) -> str:
    """
    Get the text content of an element.

    Args:
        selector: CSS selector for the element

    Returns:
        The element's text content or error message
    """
    try:
        page = get_page()
        text = page.locator(selector).text_content(timeout=5000)
        return f"Element '{selector}' text: {text}"
    except PlaywrightTimeoutError:
        return f"Error: Element '{selector}' not found"
    except Exception as e:
        return f"Error getting text from '{selector}': {str(e)}"


@tool
def get_element_attribute(selector: str, attribute: str) -> str:
    """
    Get an attribute value from an element.

    Args:
        selector: CSS selector for the element
        attribute: Name of the attribute to get (e.g., 'href', 'class', 'id')

    Returns:
        The attribute value or error message
    """
    try:
        page = get_page()
        value = page.locator(selector).get_attribute(attribute, timeout=5000)
        return f"Element '{selector}' attribute '{attribute}': {value}"
    except PlaywrightTimeoutError:
        return f"Error: Element '{selector}' not found"
    except Exception as e:
        return f"Error getting attribute from '{selector}': {str(e)}"


@tool
def wait_for_element(selector: str, timeout_ms: int = 10000) -> str:
    """
    Wait for an element to appear on the page.

    Args:
        selector: CSS selector for the element to wait for
        timeout_ms: Timeout in milliseconds (default: 10000)

    Returns:
        Success or error message
    """
    try:
        page = get_page()
        page.wait_for_selector(selector, timeout=timeout_ms)
        return f"Element '{selector}' appeared on the page"
    except PlaywrightTimeoutError:
        return f"Error: Element '{selector}' did not appear within {timeout_ms}ms"
    except Exception as e:
        return f"Error waiting for element '{selector}': {str(e)}"
