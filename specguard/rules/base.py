from abc import ABC, abstractmethod
from typing import Optional, Tuple

class Rule(ABC):
    """Abstract base class for a SpecGuard rule."""
    def __init__(self, rule_id: str, description: str):
        self.id = rule_id
        self.description = description

    @abstractmethod
    def evaluate(self, output: str) -> Optional[Tuple[str, str]]:
        """
        Evaluates the rule against the given output.

        Args:
            output: The AI model's output text.

        Returns:
            A tuple (rule_id, message) if the rule is violated, otherwise None.
        """
        pass
