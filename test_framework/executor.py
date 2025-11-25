from typing import Dict, Any
from langgraph.graph import StateGraph, END
from playwright.sync_api import sync_playwright, Browser, Page
from .parser import MarkdownParser
from .state import TestState, VerificationResult
from .workflow import create_workflow


class TestExecutor:
    """Main test executor that orchestrates the testing workflow."""

    def __init__(self):
        self.parser = MarkdownParser()

    def execute_from_markdown(self, file_path: str) -> Dict[str, Any]:
        """
        Execute tests from a markdown file.

        Args:
            file_path: Path to the markdown file containing test steps

        Returns:
            Dictionary containing test results and verifications
        """
        # Parse test steps from markdown
        test_steps = self.parser.parse(file_path)

        if not test_steps:
            return {
                'summary': {
                    'total_steps': 0,
                    'passed': 0,
                    'failed': 0
                },
                'verifications': [],
                'error': 'No test steps found in markdown file'
            }

        # Create workflow
        workflow = create_workflow()
        app = workflow.compile()

        # Initialize state
        initial_state: TestState = {
            'messages': [],
            'current_step': 0,
            'total_steps': len(test_steps),
            'test_steps': test_steps,
            'verifications': [],
            'browser_context': {},
            'execution_complete': False
        }

        # Execute workflow with Playwright
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            page = browser.new_page()

            initial_state['browser_context'] = {
                'browser': browser,
                'page': page
            }

            # Run the workflow
            final_state = None
            for state in app.stream(initial_state):
                final_state = state

            # Close browser
            browser.close()

        # Extract final state from the last node
        if final_state:
            final_state_data = list(final_state.values())[0]
        else:
            final_state_data = initial_state

        # Compile results
        verifications = final_state_data.get('verifications', [])
        passed = sum(1 for v in verifications if v['status'] == 'passed')
        failed = sum(1 for v in verifications if v['status'] == 'failed')

        return {
            'summary': {
                'total_steps': len(test_steps),
                'passed': passed,
                'failed': failed
            },
            'verifications': verifications,
            'steps_executed': final_state_data.get('current_step', 0)
        }
