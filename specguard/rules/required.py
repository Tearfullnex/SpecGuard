from typing import Optional, Tuple
from .base import Rule

class RequiredPhraseRule(Rule):
    """Fails if the required phrase is not found in the output."""
    def __init__(self, rule_id: str, description: str, phrase: str):
        super().__init__(rule_id, description)
        if not phrase:
            raise ValueError("RequiredPhraseRule requires a non-empty phrase.")
        self.phrase = phrase

    def evaluate(self, output: str) -> Optional[Tuple[str, str]]:
        if self.phrase.lower() not in output.lower():
            return (self.id, f'Missing required phrase: "{self.phrase}"')
        return None
