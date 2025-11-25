from langchain_classic.tools import tool
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from typing import Optional, Dict, Any
from ..state import VerificationResult


# Global references - will be injected by the agent
_page: Optional[Page] = None
_state: Optional[Dict[str, Any]] = None
_current_step_number: int = 0
_current_step_description: str = ""


def set_verification_context(page: Page, state: Dict[str, Any], step_number: int, step_description: str):
    """Set the context for verification tools."""
    global _page, _state, _current_step_number, _current_step_description
    _page = page
    _state = state
    _current_step_number = step_number
    _current_step_description = step_description


def get_page() -> Page:
    """Get the global page reference."""
    if _page is None:
        raise RuntimeError("Page not initialized. Call set_verification_context() first.")
    return _page


def add_verification_to_state(verification: str, status: str, details: str) -> None:
    """Add a verification result to the state."""
    if _state is None:
        return

    result: VerificationResult = {
        'step_number': _current_step_number,
        'description': _current_step_description,
        'verification': verification,
        'status': status,
        'details': details
    }

    if 'verifications' not in _state:
        _state['verifications'] = []

    _state['verifications'].append(result)


@tool
def verify_title_contains(expected_text: str) -> str:
    """
    Verify that the page title contains the expected text.

    Args:
        expected_text: Text that should be in the page title

    Returns:
        Verification result message
    """
    try:
        page = get_page()
        title = page.title()

        if expected_text.lower() in title.lower():
            add_verification_to_state(
                f"title contains '{expected_text}'",
                'passed',
                f"Page title '{title}' contains '{expected_text}'"
            )
            return f"✓ PASSED: Page title '{title}' contains '{expected_text}'"
        else:
            add_verification_to_state(
                f"title contains '{expected_text}'",
                'failed',
                f"Page title '{title}' does not contain '{expected_text}'"
            )
            return f"✗ FAILED: Page title '{title}' does not contain '{expected_text}'"
    except Exception as e:
        add_verification_to_state(
            f"title contains '{expected_text}'",
            'failed',
            f"Error: {str(e)}"
        )
        return f"✗ FAILED: Error checking title - {str(e)}"


@tool
def verify_element_visible(selector: str) -> str:
    """
    Verify that an element is visible on the page.

    Args:
        selector: CSS selector for the element to check

    Returns:
        Verification result message
    """
    try:
        page = get_page()
        is_visible = page.is_visible(selector, timeout=5000)

        if is_visible:
            add_verification_to_state(
                f"element '{selector}' is visible",
                'passed',
                f"Element '{selector}' is visible on the page"
            )
            return f"✓ PASSED: Element '{selector}' is visible"
        else:
            add_verification_to_state(
                f"element '{selector}' is visible",
                'failed',
                f"Element '{selector}' is not visible"
            )
            return f"✗ FAILED: Element '{selector}' is not visible"
    except Exception as e:
        add_verification_to_state(
            f"element '{selector}' is visible",
            'failed',
            f"Error: {str(e)}"
        )
        return f"✗ FAILED: Error checking visibility - {str(e)}"


@tool
def verify_element_text_contains(selector: str, expected_text: str) -> str:
    """
    Verify that an element's text content contains the expected text.

    Args:
        selector: CSS selector for the element
        expected_text: Text that should be in the element's content

    Returns:
        Verification result message
    """
    try:
        page = get_page()
        element = page.locator(selector)
        actual_text = element.text_content(timeout=5000)

        if actual_text and expected_text.lower() in actual_text.lower():
            add_verification_to_state(
                f"element '{selector}' text contains '{expected_text}'",
                'passed',
                f"Element text '{actual_text}' contains '{expected_text}'"
            )
            return f"✓ PASSED: Element '{selector}' text contains '{expected_text}'"
        else:
            add_verification_to_state(
                f"element '{selector}' text contains '{expected_text}'",
                'failed',
                f"Element text '{actual_text}' does not contain '{expected_text}'"
            )
            return f"✗ FAILED: Element text '{actual_text}' does not contain '{expected_text}'"
    except PlaywrightTimeoutError:
        add_verification_to_state(
            f"element '{selector}' text contains '{expected_text}'",
            'failed',
            f"Element '{selector}' not found"
        )
        return f"✗ FAILED: Element '{selector}' not found"
    except Exception as e:
        add_verification_to_state(
            f"element '{selector}' text contains '{expected_text}'",
            'failed',
            f"Error: {str(e)}"
        )
        return f"✗ FAILED: Error checking text - {str(e)}"


@tool
def verify_url_contains(expected_text: str) -> str:
    """
    Verify that the current URL contains the expected text.

    Args:
        expected_text: Text that should be in the URL

    Returns:
        Verification result message
    """
    try:
        page = get_page()
        current_url = page.url

        if expected_text.lower() in current_url.lower():
            add_verification_to_state(
                f"URL contains '{expected_text}'",
                'passed',
                f"Current URL '{current_url}' contains '{expected_text}'"
            )
            return f"✓ PASSED: URL '{current_url}' contains '{expected_text}'"
        else:
            add_verification_to_state(
                f"URL contains '{expected_text}'",
                'failed',
                f"Current URL '{current_url}' does not contain '{expected_text}'"
            )
            return f"✗ FAILED: URL '{current_url}' does not contain '{expected_text}'"
    except Exception as e:
        add_verification_to_state(
            f"URL contains '{expected_text}'",
            'failed',
            f"Error: {str(e)}"
        )
        return f"✗ FAILED: Error checking URL - {str(e)}"


@tool
def add_verification_result(verification_description: str, status: str, details: str) -> str:
    """
    Manually add a custom verification result to the state.

    Args:
        verification_description: Description of what was verified
        status: 'passed' or 'failed'
        details: Additional details about the verification

    Returns:
        Confirmation message
    """
    add_verification_to_state(verification_description, status, details)
    symbol = "✓" if status == "passed" else "✗"
    return f"{symbol} Added verification: {verification_description} - {status.upper()}"
