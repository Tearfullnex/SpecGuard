from typing import Optional, Tuple
from .base import Rule

class LengthRule(Rule):
    """Fails if the output exceeds a maximum token/word count."""
    def __init__(self, rule_id: str, description: str, max_tokens: int):
        super().__init__(rule_id, description)
        if max_tokens <= 0:
            raise ValueError("LengthRule requires max_tokens to be positive.")
        self.max_tokens = max_tokens

    def evaluate(self, output: str) -> Optional[Tuple[str, str]]:
        # A simple whitespace-based tokenizer.
        num_tokens = len(output.split())
        if num_tokens > self.max_tokens:
            return (self.id, f"Output length ({num_tokens} tokens) exceeds maximum of {self.max_tokens}")
        return None
