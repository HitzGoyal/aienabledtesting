from pathlib import Path
from typing import List, Dict
import re


class MarkdownParser:
    """Parse markdown files containing test steps."""

    def parse(self, file_path: str) -> List[Dict[str, str]]:
        """
        Parse a markdown file and extract test steps.

        Expected format:
        ## Step 1: Description
        - Action: navigate to URL
        - Verify: page title contains "Example"

        Returns a list of steps with their actions and verifications.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        steps = []
        current_step = None

        for line in content.split('\n'):
            line = line.strip()

            # Match step headers (## Step N: Description or # Step N: Description)
            step_match = re.match(r'^#{1,2}\s+Step\s+\d+:?\s*(.+)', line, re.IGNORECASE)
            if step_match:
                if current_step:
                    steps.append(current_step)
                current_step = {
                    'description': step_match.group(1).strip(),
                    'actions': [],
                    'verifications': []
                }
                continue

            if current_step:
                # Match action items
                action_match = re.match(r'^[-*]\s+Action:?\s*(.+)', line, re.IGNORECASE)
                if action_match:
                    current_step['actions'].append(action_match.group(1).strip())
                    continue

                # Match verification items
                verify_match = re.match(r'^[-*]\s+Verify:?\s*(.+)', line, re.IGNORECASE)
                if verify_match:
                    current_step['verifications'].append(verify_match.group(1).strip())
                    continue

        # Add the last step
        if current_step:
            steps.append(current_step)

        return steps
