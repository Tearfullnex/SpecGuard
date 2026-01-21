from typing import Optional, Tuple
from .base import Rule

# Simple keyword-based heuristics for tone detection.
INSTRUCTIVE_KEYWORDS = ["how to", "follow these steps", "first,", "second,", "third,", "step 1", "you must"]
SPECULATIVE_KEYWORDS = ["could", "might", "perhaps", "possibly", "may", "it is possible", "speculate", "if"]

class ToneRule(Rule):
    """Fails if the detected tone does not match the expected tone."""
    def __init__(self, rule_id: str, description: str, expected: str):
        super().__init__(rule_id, description)
        self.expected = expected.lower()
        if self.expected not in ["instructive", "speculative", "neutral"]:
            raise ValueError("ToneRule expected tone must be 'instructive', 'speculative', or 'neutral'.")

    def _detect_tone(self, output: str) -> str:
        """Detects the tone of the output based on keywords."""
        output_lower = output.lower()
        
        is_instructive = any(keyword in output_lower for keyword in INSTRUCTIVE_KEYWORDS)
        if is_instructive:
            return "instructive"

        is_speculative = any(keyword in output_lower for keyword in SPECULATIVE_KEYWORDS)
        if is_speculative:
            return "speculative"
            
        return "neutral"

    def evaluate(self, output: str) -> Optional[Tuple[str, str]]:
        detected_tone = self._detect_tone(output)
        if detected_tone != self.expected:
            return (self.id, f"Expected tone {self.expected}, but found {detected_tone}")
        return None
