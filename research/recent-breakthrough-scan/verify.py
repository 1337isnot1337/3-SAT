"""Offline integrity and scope checks; no cited theorem or Lean build is checked."""
from hashlib import sha256
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    sources = json.loads((HERE/"SOURCES.json").read_text())
    scan = json.loads((HERE/"SCAN.json").read_text())
    selected = json.loads((ROOT/"certificates/selected-result.json").read_text())
    require(selected["source_commit"] == sources["baseline_openai_commit"], "baseline pin")
    require(selected["alpha"] == "1/2", "baseline alpha")
    require(re.fullmatch("[0-9a-f]{40}",sources["commit"]) is not None,"external commit pin")
    require(not sources["formal_build_replayed"] and not sources["full_formalization_vendored"],
            "verification scope")
    require(not sources["publisher_ci"]["independent_replay"], "publisher scope")
    require(sources["publisher_ci"]["head_sha"] == sources["commit"], "publisher binding")
    paths = []
    for item in sources["files"]:
        path = ROOT/item["path"]
        require(path.is_relative_to(HERE) and not path.is_symlink(), "unsafe source path")
        data = path.read_bytes()
        require(len(data) == item["bytes"] and sha256(data).hexdigest() == item["sha256"],
                "source integrity: "+item["path"])
        require(item["license"] in {"Apache-2.0","CC-BY-4.0"}, "missing license")
        if item["license"] == "Apache-2.0":
            require("/"+sources["commit"]+"/" in item["url"], "unversioned source")
        paths.append(item["path"])
    require(len(set(paths)) == len(paths),"duplicate source path")
    require((HERE/"sources/anthropic/HEXAGON-LICENSE.txt").is_file(),"Hexagon attribution")
    ids = []
    domains = {"hexagonmath.org","eccc.weizmann.ac.il","arxiv.org","ijcai.org"}
    for paper in scan["papers"]:
        require(urlsplit(paper["primary_url"]).netloc in domains,"nonprimary citation")
        for key in ("title","authors","date","evidence_scope","reported_result","action"):
            require(bool(paper[key]),"missing literature metadata: "+key)
        ids.append(paper["id"])
    require(len(ids) == len(set(ids)) == 12,"literature coverage drift")
    anthropic = HERE/"sources/anthropic"
    require((anthropic/"lean-toolchain").read_text().strip() == "leanprover/lean4:v4.33.1",
            "Lean pin")
    dependencies = json.loads((anthropic/"lake-manifest.json").read_text())
    mathlib = [p for p in dependencies["packages"] if p["name"] == "mathlib"]
    require(len(mathlib)==1 and mathlib[0]["rev"]=="0df444a360eaa60ab8c11dca51a86af692955474",
            "Mathlib pin")
    solution = (anthropic/"Solution.lean").read_text()
    require("theorem MainResults.ethIsFalse" in solution
            and "theorem MainResults.mainTheorem" in solution,"theorem names")
    print(json.dumps({"result":"PASS","scope":"source integrity and metadata only; no theorem or Lean replay",
                      "as_of":scan["as_of"],"primary_papers":len(ids),
                      "pinned_external_files":len(paths),
                      "pinned_external_bytes":sum(x["bytes"] for x in sources["files"]),
                      "anthropic_commit":sources["commit"],
                      "formal_build_replayed":False,"selected_alpha":selected["alpha"]},
                     indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
