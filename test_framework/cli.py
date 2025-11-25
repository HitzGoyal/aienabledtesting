import click
import json
from pathlib import Path
from .executor import TestExecutor


@click.command()
@click.argument('test_file', type=click.Path(exists=True))
@click.option('--output', '-o', default='results.json', help='Output JSON file for verification results')
def main(test_file, output):
    """Execute tests from a markdown file and output results to JSON."""
    click.echo(f"Reading test file: {test_file}")

    executor = TestExecutor()
    results = executor.execute_from_markdown(test_file)

    output_path = Path(output)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    click.echo(f"\nResults written to: {output}")
    click.echo(f"Total steps: {results['summary']['total_steps']}")
    click.echo(f"Passed: {results['summary']['passed']}")
    click.echo(f"Failed: {results['summary']['failed']}")


if __name__ == '__main__':
    main()
