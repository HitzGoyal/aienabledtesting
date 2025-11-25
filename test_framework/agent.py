from typing import Dict, Any, List
import os
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_openai import AzureChatOpenAI
from langchain_classic.prompts import PromptTemplate
from langchain_classic.tools import BaseTool
from playwright.sync_api import Page
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from .tools import (
    navigate_to_url,
    click_element,
    fill_input,
    press_key,
    wait_for_timeout,
    get_page_title,
    get_current_url,
    take_screenshot,
    verify_title_contains,
    verify_element_visible,
    verify_element_text_contains,
    verify_url_contains,
    add_verification_result,
    hover_element,
    double_click_element,
    right_click_element,
    select_option,
    check_checkbox,
    uncheck_checkbox,
    upload_file,
    scroll_to_element,
    get_element_text,
    get_element_attribute,
    wait_for_element,
    set_playwright_page,
    set_verification_context,
    set_interaction_page
)


REACT_PROMPT_TEMPLATE = """You are a web testing agent that executes test steps using browser automation tools.

You have access to the following tools:

{tools}

Use the following format:

Question: the test step you must execute
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: a summary of what was executed and verified

IMPORTANT RULES:
1. Execute ALL actions specified in the test step description
2. Execute ALL verifications specified in the test step description
3. Use the verification tools (verify_*) to add results to the state - they automatically track pass/fail
4. Be thorough and complete all requested actions and verifications
5. If a verification fails, still continue with remaining verifications
6. Always provide a clear summary of what was done and what passed/failed

Begin!

Question: {input}
Thought: {agent_scratchpad}"""


class TestAgent:
    """ReAct agent for executing test steps with Playwright tools."""

    def __init__(self, llm: AzureChatOpenAI = None, verbose: bool = True):
        """
        Initialize the test agent.

        Args:
            llm: Language model to use (defaults to Azure OpenAI GPT-4)
            verbose: Whether to print agent reasoning
        """
        if llm is None:
            llm = AzureChatOpenAI(
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
                deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                temperature=0
            )

        self.llm = llm
        self.verbose = verbose
        self.tools = self._get_tools()
        self.agent_executor = self._create_agent_executor()

    def _get_tools(self) -> List[BaseTool]:
        """Get all available tools for the agent."""
        return [
            # Navigation and basic actions
            navigate_to_url,
            click_element,
            fill_input,
            press_key,
            wait_for_timeout,
            get_page_title,
            get_current_url,
            take_screenshot,
            # Verification tools
            verify_title_contains,
            verify_element_visible,
            verify_element_text_contains,
            verify_url_contains,
            add_verification_result,
            # Interaction tools
            hover_element,
            double_click_element,
            right_click_element,
            select_option,
            check_checkbox,
            uncheck_checkbox,
            upload_file,
            scroll_to_element,
            get_element_text,
            get_element_attribute,
            wait_for_element,
        ]

    def _create_agent_executor(self) -> AgentExecutor:
        """Create the ReAct agent executor."""
        prompt = PromptTemplate.from_template(REACT_PROMPT_TEMPLATE)

        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )

        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=self.verbose,
            handle_parsing_errors=True,
            max_iterations=15
        )

    def execute_step(
        self,
        page: Page,
        state: Dict[str, Any],
        step: Dict[str, Any],
        step_number: int
    ) -> str:
        """
        Execute a test step using the ReAct agent.

        Args:
            page: Playwright page object
            state: Current test state (for injecting verifications)
            step: Test step containing description, actions, and verifications
            step_number: The step number

        Returns:
            Agent's output/summary
        """
        # Set the page context for all tools
        set_playwright_page(page)
        set_interaction_page(page)
        set_verification_context(page, state, step_number, step['description'])

        # Build the input prompt for the agent
        input_text = self._build_step_prompt(step)

        print(f"\n{'='*60}")
        print(f"Step {step_number}: {step['description']}")
        print(f"{'='*60}")

        # Execute the agent
        try:
            result = self.agent_executor.invoke({"input": input_text})
            return result.get('output', 'Step completed')
        except Exception as e:
            error_msg = f"Error executing step: {str(e)}"
            print(f"ERROR: {error_msg}")
            return error_msg

    def _build_step_prompt(self, step: Dict[str, Any]) -> str:
        """Build a detailed prompt for the agent based on the test step."""
        prompt_parts = [f"Test Step: {step['description']}\n"]

        if step.get('actions'):
            prompt_parts.append("Actions to execute:")
            for i, action in enumerate(step['actions'], 1):
                prompt_parts.append(f"  {i}. {action}")
            prompt_parts.append("")

        if step.get('verifications'):
            prompt_parts.append("Verifications to perform:")
            for i, verification in enumerate(step['verifications'], 1):
                prompt_parts.append(f"  {i}. {verification}")
            prompt_parts.append("")

        prompt_parts.append(
            "Execute all actions in order, then perform all verifications. "
            "Use the appropriate verification tools to check and record results."
        )

        return "\n".join(prompt_parts)
