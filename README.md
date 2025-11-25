# Test Framework CLI

A test framework CLI tool built with Python, LangChain, LangGraph, and Playwright that uses a **ReAct agent** to intelligently execute test steps from markdown files and outputs verification results to JSON.

## Features

- 🤖 **ReAct Agent-Based Execution**: Uses LangChain's ReAct agent for intelligent test step execution
- 🛠️ **Rich Playwright Toolkit**: 20+ tools for browser automation (navigation, clicking, form filling, etc.)
- ✅ **Automated Verification**: Verification tools automatically inject results into LangGraph state
- 📊 **State Management**: LangGraph tracks all verifications throughout test execution
- 📝 **Markdown Test Format**: Write tests in simple markdown format
- 📦 **JSON Output**: Comprehensive test results with pass/fail status

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install
```

3. Set up Azure OpenAI credentials (required for the ReAct agent):
```bash
cp .env.example .env
# Edit .env and configure the following:
# - AZURE_OPENAI_ENDPOINT: Your Azure OpenAI resource endpoint
# - AZURE_OPENAI_API_KEY: Your Azure OpenAI API key
# - AZURE_OPENAI_API_VERSION: API version (default: 2024-02-15-preview)
# - AZURE_OPENAI_DEPLOYMENT_NAME: Your GPT-4 deployment name
```

4. Install the package:
```bash
pip install -e .
```

## Usage

Run tests from a markdown file:
```bash
test-cli example_test.md
```

Specify custom output file:
```bash
test-cli example_test.md -o my_results.json
```

Or run directly with Python:
```bash
python -m test_framework.cli example_test.md
```

## Markdown Test Format

Test files should follow this format:

```markdown
## Step 1: Description of the step
- Action: navigate to https://example.com
- Action: click "#submit-button"
- Verify: title contains "Expected Title"
- Verify: ".success-message" visible

## Step 2: Another step
- Action: fill "#username" with "testuser"
- Action: press "Enter"
- Verify: url contains "dashboard"
```

### Available Tools

The ReAct agent has access to 20+ tools organized into three categories:

#### Navigation & Basic Actions
- `navigate_to_url` - Navigate to a URL
- `click_element` - Click on an element
- `fill_input` - Fill an input field
- `press_key` - Press a keyboard key
- `wait_for_timeout` - Wait for milliseconds
- `get_page_title` - Get current page title
- `get_current_url` - Get current URL
- `take_screenshot` - Capture screenshot

#### Verification Tools (Auto-inject to State)
- `verify_title_contains` - Verify page title
- `verify_element_visible` - Verify element visibility
- `verify_element_text_contains` - Verify element text
- `verify_url_contains` - Verify URL content
- `add_verification_result` - Add custom verification

#### Interaction Tools
- `hover_element` - Hover over element
- `double_click_element` - Double-click element
- `right_click_element` - Right-click element
- `select_option` - Select dropdown option
- `check_checkbox` - Check a checkbox
- `uncheck_checkbox` - Uncheck a checkbox
- `upload_file` - Upload file to input
- `scroll_to_element` - Scroll to element
- `get_element_text` - Get element text
- `get_element_attribute` - Get element attribute
- `wait_for_element` - Wait for element to appear

## Architecture

### Technology Stack
- **LangGraph**: Workflow orchestration with state management
- **LangChain**: ReAct agent framework and tool integration
- **Azure OpenAI GPT-4**: Powers the ReAct agent reasoning
- **Playwright**: Browser automation engine
- **Click**: CLI interface

### How It Works

1. **Markdown Parsing**: Test steps are parsed from markdown files
2. **LangGraph Workflow**: Creates a state machine that loops through each test step
3. **ReAct Agent Execution**: For each step, the agent:
   - Receives the step description, actions, and verifications
   - Reasons about what tools to use
   - Executes browser actions using Playwright tools
   - Performs verifications using verification tools
   - Verification tools automatically inject results into the shared state
4. **State Tracking**: LangGraph maintains verification results across all steps
5. **JSON Output**: Final state is compiled and exported to JSON

### Components

- `cli.py` - CLI entry point
- `parser.py` - Markdown test file parser
- `state.py` - LangGraph state schema with verification tracking
- `agent.py` - ReAct agent configuration with tool access
- `workflow.py` - LangGraph workflow with agent integration
- `executor.py` - Main test execution orchestrator
- `tools/` - Playwright, verification, and interaction tools
  - `playwright_tools.py` - Basic browser automation
  - `verification_tools.py` - Verification tools with state injection
  - `interaction_tools.py` - Advanced interaction tools

## Output Format

Results are saved as JSON:

```json
{
  "summary": {
    "total_steps": 3,
    "passed": 5,
    "failed": 1
  },
  "verifications": [
    {
      "step_number": 1,
      "description": "Navigate to homepage",
      "verification": "title contains \"Example\"",
      "status": "passed",
      "details": "Title contains 'Example'"
    }
  ],
  "steps_executed": 3
}
```
