"""
Example script showing how to run markdown tests programmatically.
This demonstrates how to use the TestExecutor class directly without CLI.
"""

import json
from pathlib import Path
from test_framework.executor import TestExecutor


def run_single_test(test_file: str, output_file: str = None):
    """
    Run a single test file and return results.

    Args:
        test_file: Path to the markdown test file
        output_file: Optional path to save JSON results

    Returns:
        Dictionary containing test results
    """
    print(f"Running test: {test_file}")
    print("-" * 50)

    # Create executor
    executor = TestExecutor()

    # Execute the test
    results = executor.execute_from_markdown(test_file)

    # Display summary
    summary = results['summary']
    print(f"\n📊 Test Summary:")
    print(f"  Total steps: {summary['total_steps']}")
    print(f"  ✅ Passed: {summary['passed']}")
    print(f"  ❌ Failed: {summary['failed']}")
    print(f"  Steps executed: {results.get('steps_executed', 0)}")

    # Display verification details
    if results['verifications']:
        print(f"\n📋 Verification Results:")
        for i, verification in enumerate(results['verifications'], 1):
            status_icon = "✅" if verification['status'] == 'passed' else "❌"
            print(f"  {i}. {status_icon} {verification['step']}")
            if verification.get('message'):
                print(f"     Message: {verification['message']}")

    # Save to file if requested
    if output_file:
        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to: {output_file}")

    return results


def run_multiple_tests(test_files: list):
    """
    Run multiple test files and aggregate results.

    Args:
        test_files: List of markdown test file paths

    Returns:
        Dictionary with aggregated results
    """
    executor = TestExecutor()
    all_results = []
    total_passed = 0
    total_failed = 0
    total_steps = 0

    print("Running multiple test files...")
    print("=" * 50)

    for test_file in test_files:
        print(f"\n📝 Running: {test_file}")
        results = executor.execute_from_markdown(test_file)
        all_results.append({
            'file': test_file,
            'results': results
        })

        summary = results['summary']
        total_passed += summary['passed']
        total_failed += summary['failed']
        total_steps += summary['total_steps']

        print(f"  Passed: {summary['passed']}, Failed: {summary['failed']}")

    print("\n" + "=" * 50)
    print(f"📊 Overall Summary:")
    print(f"  Total files: {len(test_files)}")
    print(f"  Total steps: {total_steps}")
    print(f"  ✅ Total passed: {total_passed}")
    print(f"  ❌ Total failed: {total_failed}")

    return {
        'total_files': len(test_files),
        'total_steps': total_steps,
        'total_passed': total_passed,
        'total_failed': total_failed,
        'results': all_results
    }


def check_test_passed(results: dict) -> bool:
    """
    Check if all tests passed.

    Args:
        results: Test results dictionary

    Returns:
        True if all tests passed, False otherwise
    """
    return results['summary']['failed'] == 0


def main():
    """Main function demonstrating various usage patterns."""

    # Example 1: Run a single test
    print("=" * 50)
    print("Example 1: Running single test")
    print("=" * 50)
    results = run_single_test('example_test.md', 'results.json')

    # Check if test passed
    if check_test_passed(results):
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")

    # Example 2: Run test without saving results
    print("\n\n" + "=" * 50)
    print("Example 2: Running without saving results")
    print("=" * 50)
    results = run_single_test('example_test.md')

    # Example 3: Run multiple tests (if you have multiple test files)
    # Uncomment this section if you have multiple test files
    # print("\n\n" + "=" * 50)
    # print("Example 3: Running multiple tests")
    # print("=" * 50)
    # test_files = ['example_test.md', 'another_test.md']
    # aggregate_results = run_multiple_tests(test_files)

    # Example 4: Programmatically create executor and customize
    print("\n\n" + "=" * 50)
    print("Example 4: Custom execution with direct executor usage")
    print("=" * 50)

    executor = TestExecutor()
    results = executor.execute_from_markdown('example_test.md')

    # Custom processing of results
    verifications = results['verifications']
    failed_verifications = [v for v in verifications if v['status'] == 'failed']

    if failed_verifications:
        print("\n⚠️  Failed verifications:")
        for v in failed_verifications:
            print(f"  - {v['step']}: {v.get('message', 'No message')}")
    else:
        print("\n✅ All verifications passed!")


if __name__ == '__main__':
    main()
