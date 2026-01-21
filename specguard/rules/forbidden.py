from typing import List, Optional, Tuple
from .base import Rule

class ForbiddenPhrasesRule(Rule):
    """Fails if any forbidden phrase is found in the output."""
    def __init__(self, rule_id: str, description: str, phrases: List[str]):
        super().__init__(rule_id, description)
        if not phrases:
            raise ValueError("ForbiddenPhrasesRule requires a non-empty list of phrases.")
        self.phrases = [phrase.lower() for phrase in phrases]

    def evaluate(self, output: str) -> Optional[Tuple[str, str]]:
        output_lower = output.lower()
        for phrase in self.phrases:
            if phrase in output_lower:
                return (self.id, f'Found forbidden phrase: "{phrase}"')
        return None