import argparse
from pathlib import Path

from . import parser
from . import engine
from . import report

def read_file_content(path: str) -> str:
    """Reads and returns the content of a file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {path}")
        exit(1)
    except Exception as e:
        print(f"Error reading file at {path}: {e}")
        exit(1)

def main():
    cli_parser = argparse.ArgumentParser(description="SpecGuard - AI Specification Enforcement Engine")
    subparsers = cli_parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Runs the SpecGuard enforcement engine.")
    run_parser.add_argument("--output", "-o", required=True, help="Path to the AI model's output file (text or JSON).")
    run_parser.add_argument("--spec", "-s", required=True, help="Path to the specification YAML file.")
    run_parser.add_argument("--prompt", "-p", help="Path to the prompt file (optional).")

    args = cli_parser.parse_args()

    if args.command == "run":
        try:
            output_content = read_file_content(args.output)
            if args.prompt:
                read_file_content(args.prompt)
            
            rules = parser.parse_spec(args.spec)
            violations = engine.run_checks(args.output, output_content, rules)
            report.print_report(violations)

            if violations:
                exit(1)

        except (ValueError, FileNotFoundError) as e:
            print(f"Error: {e}")
            exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            exit(1)

if __name__ == "__main__":
    main()
