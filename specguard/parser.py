import yaml
from typing import List, Dict, Any

from .rules.base import Rule
from .rules.forbidden import ForbiddenPhrasesRule
from .rules.required import RequiredPhraseRule
from .rules.length import LengthRule
from .rules.tone import ToneRule

RULE_TYPE_MAP = {
    "forbidden_phrases": ForbiddenPhrasesRule,
    "required_phrase": RequiredPhraseRule,
    "length": LengthRule,
    "tone": ToneRule,
}

def parse_spec(spec_path: str) -> List[Rule]:
    """Parses a YAML spec file and returns a list of Rule objects."""
    try:
        with open(spec_path, 'r', encoding='utf-8') as f:
            spec_data = yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Spec file not found at: {spec_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML spec file: {e}")

    if not isinstance(spec_data, dict) or "rules" not in spec_data:
        raise ValueError("Spec file must be a dictionary with a 'rules' key.")

    rules_config = spec_data["rules"]
    if not isinstance(rules_config, list):
        raise ValueError("The 'rules' key must contain a list of rule configurations.")

    rules = []
    for config in rules_config:
        rule_type_str = config.get("type")
        if not rule_type_str:
            raise ValueError("Each rule must have a 'type' defined.")

        rule_class = RULE_TYPE_MAP.get(rule_type_str)
        if not rule_class:
            raise ValueError(f"Unknown rule type: '{rule_type_str}'")
        
        rule_id = config.get("id")
        if not rule_id:
            raise ValueError("Each rule must have an 'id'.")
            
        description = config.get("description", "")

        # Create a copy of config and remove processed keys
        rule_params = config.copy()
        del rule_params["type"]
        del rule_params["id"]
        if "description" in rule_params:
            del rule_params["description"]

        try:
            # Pass id and description explicitly
            rule_instance = rule_class(rule_id=rule_id, description=description, **rule_params)
            rules.append(rule_instance)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Error creating rule '{rule_id}' (type: {rule_type_str}): {e}") from e

    return rules