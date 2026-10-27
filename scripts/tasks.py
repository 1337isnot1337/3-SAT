"""List current research cards; this does not reserve a task or fetch overlap."""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", help="Show one full task card")
    args = parser.parse_args()
    catalogue = json.loads((ROOT / "docs/tasks.json").read_text())
    if args.task:
        matches = [task for task in catalogue["tasks"] if task["id"] == args.task]
        if not matches:
            parser.error(f"Unknown task: {args.task}")
        print(json.dumps(matches[0], indent=2))
    else:
        print(f"Priority revision {catalogue['priority_revision']}; check live overlap before choosing.")
        for task in catalogue["tasks"]:
            print(f"{task['id']}: {task['question']}")


if __name__ == "__main__":
    main()
