from typing import List, Tuple

def print_report(violations: List[Tuple[str, str]]):
    """Prints the final report to the console."""
    if not violations:
        print("SpecGuard Result: ✅ PASS")
        print("All specifications satisfied.")
    else:
        print("SpecGuard Result: ❌ FAIL")
        print("\nViolations:")
        for rule_id, message in violations:
            print(f"- {rule_id} → {message}")
