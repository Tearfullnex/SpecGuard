from typing import List, Tuple
import json

from .rules.base import Rule

def extract_text_from_output(output_path: str, output_content: str) -> str:
    """Extracts the relevant text from the model output file."""
    if output_path.lower().endswith('.json'):
        try:
            data = json.loads(output_content)
            # Look for common keys that might contain the response.
            possible_keys = ["response", "output", "text", "completion", "content"]
            for key in possible_keys:
                if key in data and isinstance(data[key], str):
                    return data[key]
            # If no common key is found, stringify the whole JSON.
            return json.dumps(data)
        except json.JSONDecodeError:
            # If JSON is invalid, treat it as plain text.
            return output_content
    # For non-JSON files, return the content directly.
    return output_content


def run_checks(output_path: str, output_content: str, rules: List[Rule]) -> List[Tuple[str, str]]:
    """
    Runs all rules against the model output and collects violations.

    Args:
        output_path: Path to the output file (to determine file type).
        output_content: The content of the model's output file.
        rules: A list of Rule objects to evaluate.

    Returns:
        A list of violations, where each violation is a (rule_id, message) tuple.
    """
    violations = []
    
    # Extract the actual text to be evaluated
    text_to_evaluate = extract_text_from_output(output_path, output_content)

    for rule in rules:
        result = rule.evaluate(text_to_evaluate)
        if result:
            violations.append(result)
            
    return violations
