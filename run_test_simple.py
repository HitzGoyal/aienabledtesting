"""
Simple minimal example of running a test programmatically.
"""

from test_framework.executor import TestExecutor

# Create executor and run test
executor = TestExecutor()
results = executor.execute_from_markdown('example_test.md')

# Print results
print(f"Passed: {results['summary']['passed']}")
print(f"Failed: {results['summary']['failed']}")
