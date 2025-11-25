from typing import Literal
from langgraph.graph import StateGraph, END
from playwright.sync_api import Page
from .state import TestState
from .agent import TestAgent


# Global agent instance - initialized when workflow is created
_agent: TestAgent = None


def set_agent(agent: TestAgent):
    """Set the global agent instance."""
    global _agent
    _agent = agent


def get_agent() -> TestAgent:
    """Get the global agent instance."""
    if _agent is None:
        # Create default agent if none exists
        return TestAgent(verbose=True)
    return _agent


def execute_step_node(state: TestState) -> TestState:
    """Execute a single test step using the ReAct agent."""
    current_step_index = state['current_step']
    test_steps = state['test_steps']

    if current_step_index >= len(test_steps):
        state['execution_complete'] = True
        return state

    step = test_steps[current_step_index]
    page: Page = state['browser_context']['page']

    # Get agent and execute the step
    agent = get_agent()
    agent.execute_step(
        page=page,
        state=state,
        step=step,
        step_number=current_step_index + 1
    )

    state['current_step'] += 1
    return state




def should_continue(state: TestState) -> Literal["continue", "end"]:
    """Determine if the workflow should continue or end."""
    if state['execution_complete'] or state['current_step'] >= state['total_steps']:
        return "end"
    return "continue"


def create_workflow() -> StateGraph:
    """Create and configure the LangGraph workflow."""
    workflow = StateGraph(TestState)

    # Add nodes
    workflow.add_node("execute_step", execute_step_node)

    # Add edges
    workflow.set_entry_point("execute_step")
    workflow.add_conditional_edges(
        "execute_step",
        should_continue,
        {
            "continue": "execute_step",
            "end": END
        }
    )

    return workflow
