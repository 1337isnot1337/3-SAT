"""Create a source-pinned draft package, without fabricating evidence or a result."""

import argparse
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug")
    parser.add_argument("--task", required=True)
    parser.add_argument("--author", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.slug):
        parser.error("Use a lowercase alphanumeric slug with optional hyphens")
    catalogue = json.loads((ROOT / "docs/tasks.json").read_text())
    if args.task not in {t["id"] for t in catalogue["tasks"]}:
        parser.error("Unknown task ID")
    try:
        base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                       text=True, stderr=subprocess.DEVNULL).strip()
    except subprocess.CalledProcessError:
        parser.error("Commit the repository first so the draft can pin a real base")
    selected = json.loads((ROOT / "certificates/selected-result.json").read_text())
    claim = {
        "schema_version": 1, "id": args.slug, "task": args.task,
        "status": "draft", "kind": "research_attempt", "author": args.author,
        "base_commit": base, "baseline_result": selected["result_id"],
        "upstream_commit": selected["source_commit"],
        "statement": "Draft: no result claimed", "improves_bound": False,
        "evidence": [], "reproduce": [], "remaining_obligations": ["State and check the proposed result"],
    }
    dest = ROOT / "research" / args.slug
    try:
        dest.mkdir()
    except FileExistsError:
        parser.error(f"Package already exists: {dest}")
    (dest / "CLAIM.json").write_text(json.dumps(claim, indent=2) + "\n")
    (dest / "README.md").write_text(
        f"# {args.slug}\n\nStatus: draft. No result claimed.\n\n"
        f"Task: `{args.task}`. Base commit: `{base}`.\n\n"
        f"Contributor: {args.author}. Disclose substantial AI assistance.\n\n"
        "## Question and changed premise\n\nState one precise change and its source labels. Accept the OpenAI theorem.\n\n"
        "## Statement and scope\n\nState the exact guarantee, assumptions, and success/stop test.\n\n"
        "## Complete cost\n\nCharge reductions, entries, branches, queries, modes, precision, recursion, recovery, and error.\n\n"
        "## Evidence and reproduction\n\nRecord exact inputs, hashes, commands, dependencies, outputs and unrun checks.\n\n"
        "## Limits and open next questions\n\nName the unresolved obligation and a concrete next step.\n\n"
        "## Sources and credit\n\nRetain predecessor attribution and identify the frozen source commit.\n")
    print(dest.relative_to(ROOT))


if __name__ == "__main__":
    main()
