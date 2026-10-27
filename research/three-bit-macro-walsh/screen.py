"""Registered first screen: three-bit macro counts R=1..12, exact arithmetic."""

from fractions import Fraction as F
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location("macro_construction", HERE / "macro.py")
macro = importlib.util.module_from_spec(spec)
spec.loader.exec_module(macro)
require = macro.require


def local_character_check() -> int:
    labels = list(product(range(8), repeat=2))
    require([sum(macro.class_of(a, b) == j for a, b in labels) for j in range(3)]
            == list(macro.CLASS_WEIGHTS), "Macro class sizes")
    for c, d in labels:
        row = [0, 0, 0]
        for a, b in labels:
            row[macro.class_of(a, b)] += (-1) ** (((b & c).bit_count() + (a & d).bit_count()) % 2)
        require(row == list(macro.CLASS_WALSH[macro.class_of(c, d)]), "Direct macro class transform")
    return len(labels) ** 2


def check(R: int) -> dict:
    data = macro.construct(R)
    T, weights, pieces = data["transform"], data["weights"], data["pieces"]
    size = len(T)
    require(sum(weights) == 64 ** R, "Weighted type cardinality")
    for i in range(size):
        require(all(weights[i] * T[i][j] == weights[j] * T[j][i] for j in range(size)),
                "Weighted Walsh self-adjointness")
        squared = [0] * size
        for k, x in enumerate(T[i]):
            if x:
                for j, y in enumerate(T[k]):
                    squared[j] += x * y
        require(squared == [(64 ** R if i == j else 0) for j in range(size)], "Macro transform square")
    require(macro.engine.multiply_matrix(T, data["target"]) == [8 ** R * x for x in data["target"]],
            "Macro quadratic target eigenvector")
    for piece in pieces:
        require(macro.engine.multiply_matrix(T, piece["function"]) == piece["transformed"],
                "Exact macro piece transform")
    require(all(sum((p["function"][j] for p in pieces), F(0)) == data["target"][j]
                for j in range(size)), "Macro crossing target sum")
    worst = max(pieces, key=lambda p: p["shared_bits"])
    payload = [[p["basis_index"], list(map(str, p["function"])), list(map(str, p["transformed"]))]
               for p in pieces]
    return {"macros": R, "input_bits": 3 * R, "type_dimension": size, "pieces": len(pieces),
            "worst_shared_bits": worst["shared_bits"],
            "finite_bits_per_macro": str(F(worst["shared_bits"], R)),
            "worst_piece": {k: worst[k] for k in ["basis_index", "pivot", "row_support", "col_support"]},
            "common_denominator_bits": data["denominator"].bit_length(),
            "max_coefficient_bits": max(abs(v.numerator).bit_length() + v.denominator.bit_length()
                                        for p in pieces for v in p["function"] + p["transformed"]),
            "piece_data_sha256": sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()}


def main() -> None:
    characters = local_character_check()
    profiles = [check(R) for R in range(1, 13)]
    report = {"status": "PASS", "scope": "exact R=1..12 macro-family screen; no asymptotic gain",
              "direct_local_characters": characters, "profiles": profiles,
              "bindings": {"base_commit": json.loads((HERE / "CLAIM.json").read_text())["base_commit"],
                           "predecessor_module_sha256": macro.PREDECESSOR_SHA256,
                           "construction_sha256": sha256((HERE / "CONSTRUCTION.md").read_bytes()).hexdigest(),
                           "module_sha256": sha256((HERE / "macro.py").read_bytes()).hexdigest(),
                           "screen_sha256": sha256(Path(__file__).read_bytes()).hexdigest()}}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
