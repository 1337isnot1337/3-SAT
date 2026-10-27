"""Check frozen source bytes offline; optionally fetch only missing pinned files."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def entries(root: Path) -> list[dict]:
    manifest = json.loads((root / "SOURCES.json").read_text())
    if manifest["schema_version"] != 1:
        raise ValueError("Unsupported source manifest schema")
    result = manifest["files"]
    seen = set()
    commit = manifest["upstream_commit"]
    for item in result:
        path = Path(item["path"])
        if (path.is_absolute() or ".." in path.parts
                or path.parts[:2] != ("upstream", "openai-eth-2026")
                or item["path"] in seen):
            raise ValueError(f"Invalid or duplicate source path: {path}")
        seen.add(item["path"])
        expected = f"https://raw.githubusercontent.com/openai/math/{commit}/{item['upstream_path']}"
        if item["url"] != expected:
            raise ValueError(f"Source URL is not bound to its manifest commit: {path}")
    return result


def verify_sources(root: Path = ROOT) -> int:
    items = entries(root)
    declared = {item["path"] for item in items}
    actual = {p.relative_to(root).as_posix()
              for p in (root / "upstream").rglob("*") if p.is_file()}
    if actual != declared:
        raise ValueError(f"Frozen source inventory differs: {sorted(actual ^ declared)}")
    for item in items:
        path = root / item["path"]
        if any(parent.is_symlink() for parent in (path, *path.parents)):
            raise ValueError(f"Frozen source must not be a symlink: {path}")
        data = path.read_bytes()
        if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
            raise ValueError(f"Frozen source hash/size mismatch: {item['path']}")
    return len(items)


def fetch_missing(root: Path = ROOT) -> None:
    for item in entries(root):
        path = root / item["path"]
        if path.exists():
            continue
        if path.is_symlink() or any(p.is_symlink() for p in path.parents):
            raise ValueError(f"Refusing source path through symlink: {path}")
        with urllib.request.urlopen(item["url"], timeout=60) as response:
            data = response.read(item["bytes"] + 1)
        if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
            raise ValueError(f"Downloaded source mismatch: {item['path']}")
        path.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation preserves another writer's file; mismatches are never overwritten.
        with path.open("xb") as stream:
            stream.write(data)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch-missing", action="store_true")
    args = parser.parse_args()
    try:
        if args.fetch_missing:
            fetch_missing()
        checked = verify_sources()
    except (OSError, ValueError, KeyError) as exc:
        parser.error(str(exc))
    print(f"PASS: {checked} frozen source files match their pinned bytes (integrity only)")


if __name__ == "__main__":
    main()
