"""Read-only command line for the public edition's bounded formal checkers."""
import argparse
import json
from pathlib import Path
from .logic import analyse_argument
from .finite_logic import evaluate_in_structure

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("logic", "finite"))
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if args.mode == "logic":
        result = analyse_argument(payload["premises"], payload["conclusion"])
    else:
        result = evaluate_in_structure(payload["formula"], payload["structure"])
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
