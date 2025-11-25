from typing import TypedDict, List, Annotated
from langgraph.graph import add_messages


class VerificationResult(TypedDict):
    """Individual verification result."""
    step_number: int
    description: str
    verification: str
    status: str  # 'passed' or 'failed'
    details: str


class TestState(TypedDict):
    """State for the test execution graph."""
    messages: Annotated[list, add_messages]
    current_step: int
    total_steps: int
    test_steps: List[dict]
    verifications: List[VerificationResult]
    browser_context: dict
    execution_complete: bool
