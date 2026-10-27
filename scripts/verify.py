"""Offline repository consistency checks; this does not verify the accepted proof."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from satbounds.cost import analyze, rational
from scripts.sources import verify_sources


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def local_path(value: str) -> Path:
    path = ROOT / value
    require(not Path(value).is_absolute() and ".." not in Path(value).parts,
            f"Expected a repository-relative evidence path: {value}")
    require(path.exists(), f"Missing evidence: {value}")
    return path


def check_metadata() -> tuple[int, int]:
    manifest = json.loads((ROOT / "SOURCES.json").read_text())
    selected = json.loads((ROOT / "certificates/selected-result.json").read_text())
    catalogue = json.loads((ROOT / "docs/tasks.json").read_text())
    require(selected["schema_version"] == catalogue["schema_version"] == 1, "Unknown schema")
    require(selected["source_commit"] == manifest["upstream_commit"], "Baseline source commit drift")
    require(re.fullmatch(r"[0-9a-f]{40}", selected["source_commit"]) is not None, "Invalid commit pin")
    require(selected["status"] == "owner_accepted_external_theorem", "Baseline acceptance drift")
    require(rational(selected["alpha"]) > 0, "Invalid baseline alpha")
    require(selected["result_id"] == catalogue["baseline_result"], "Task baseline drift")
    require(selected["source_manifest"] == "SOURCES.json", "Unexpected baseline source manifest")
    papers = [f for f in manifest["files"] if f["path"] == selected["paper"]]
    require(len(papers) == 1 and papers[0]["sha256"] == selected["paper_sha256"], "Paper binding drift")
    tasks = catalogue["tasks"]
    task_ids = {t["id"] for t in tasks}
    require(len(task_ids) == len(tasks) and bool(tasks), "Duplicate or missing tasks")
    for task in tasks:
        for key in ("question", "first_step", "success", "stop", "open_obligations", "overlap_terms"):
            require(bool(task[key]), f"Task {task['id']} lacks {key}")
        source = local_path(task["source_file"]).read_text()
        for label in task["source_labels"]:
            require("\\label{" + label + "}" in source, f"Unresolved source label: {label}")
        for evidence in task["existing_evidence"]:
            local_path(evidence)
    for path in (ROOT / "certificates/models").glob("*.json"):
        model = json.loads(path.read_text())
        require(model["source_result"] == selected["result_id"], f"Unknown model source: {path}")
        require(analyze(model)["alpha"] == selected["alpha"], f"Baseline model alpha drift: {path}")
    statuses = {"draft", "scoped_checked", "reviewed", "refuted", "superseded"}
    claims = list((ROOT / "research").glob("*/CLAIM.json"))
    ids = set()
    for path in claims:
        claim = json.loads(path.read_text())
        require(claim["schema_version"] == 1 and claim["status"] in statuses, f"Invalid claim: {path}")
        require(claim["id"] not in ids, f"Duplicate claim ID: {claim['id']}")
        ids.add(claim["id"])
        require(claim["task"] in task_ids, f"Unknown claim task: {path}")
        require(bool(claim["statement"]) and bool(claim["author"]), f"Incomplete claim: {path}")
        require(type(claim["improves_bound"]) is bool, f"Claim needs an explicit bound flag: {path}")
        require(type(claim["reproduce"]) is list
                and all(isinstance(arg, str) and arg for arg in claim["reproduce"]),
                f"Reproduction command must be an argument list: {path}")
        for evidence in claim["evidence"]:
            local_path(evidence)
        if claim["status"] == "scoped_checked":
            require(bool(claim["evidence"]) and bool(claim["reproduce"]), f"Missing check evidence: {path}")
        if claim["status"] == "reviewed":
            local_path(claim["review"])
    improvement = selected["selected_local_improvement"]
    if improvement is not None:
        claim = json.loads(local_path(improvement["claim"]).read_text())
        require(claim["status"] == "reviewed" and claim["improves_bound"], "Selected improvement lacks reviewed claim")
        local_path(improvement["review"])
        rational(improvement["alpha"])
        require(bool(improvement["full_time"]), "Selected improvement needs its full time bound")
    return len(tasks), len(claims)


def check_links() -> int:
    checked = 0
    for document in ROOT.rglob("*.md"):
        if any(p in {".git", ".venv", "tmp", "output"} for p in document.relative_to(ROOT).parts):
            continue
        for target in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", document.read_text()):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            path = (document.parent / unquote(parsed.path)).resolve()
            require(path.is_relative_to(ROOT) and path.exists(), f"Broken local link in {document}: {target}")
            checked += 1
    return checked


def main() -> None:
    try:
        sources = verify_sources(ROOT)
        tasks, claims = check_metadata()
        links = check_links()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print(f"PASS: {sources} frozen sources, {tasks} tasks, {claims} research claims, {links} local links")
    print("Scope: source integrity and repository consistency; OpenAI theorem accepted by owner instruction")


if __name__ == "__main__":
    main()
