"""Registered six-class screen, R=1..5. All pass/fail arithmetic is exact."""

from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("refined_macro", HERE / "refined.py")
refined = importlib.util.module_from_spec(spec)
spec.loader.exec_module(refined)
require = refined.require


def check(R: int) -> dict:
    data = refined.construct(R)
    T, weights, pieces = data["transform"], data["weights"], data["pieces"]
    size = len(T)
    require(sum(weights) == 64 ** R, "Refined weighted cardinality")
    for i in range(size):
        require(all(weights[i] * T[i][j] == weights[j] * T[j][i] for j in range(size)),
                "Refined weighted self-adjointness")
        squared = [0] * size
        for k, x in enumerate(T[i]):
            if x:
                for j, y in enumerate(T[k]):
                    squared[j] += x * y
        require(squared == [64 ** R if i == j else 0 for j in range(size)], "Refined transform square")
    require(refined.coarse.engine.multiply_matrix(T, data["target"])
            == [8 ** R * x for x in data["target"]], "Refined target eigenvector")
    for piece in pieces:
        require(refined.coarse.engine.multiply_matrix(T, piece["function"]) == piece["transformed"],
                "Refined exact piece transform")
    require(all(sum((p["function"][j] for p in pieces), F(0)) == data["target"][j]
                for j in range(size)), "Refined target sum")
    worst = max(pieces, key=lambda p: p["shared_bits"])
    payload = [[p["basis_index"], list(map(str, p["function"])), list(map(str, p["transformed"]))]
               for p in pieces]
    return {"macros": R, "input_bits": 3 * R, "type_dimension": size, "pieces": len(pieces),
            "worst_shared_bits": worst["shared_bits"], "finite_bits_per_macro": str(F(worst["shared_bits"], R)),
            "worst_piece": {k: worst[k] for k in ["basis_index", "pivot", "row_support", "col_support"]},
            "common_denominator_bits": data["denominator"].bit_length(),
            "max_coefficient_bits": max(abs(v.numerator).bit_length() + v.denominator.bit_length()
                                        for p in pieces for v in p["function"] + p["transformed"]),
            "piece_data_sha256": sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()}


def main() -> None:
    profiles = []
    for R in range(1, 6):
        profile = check(R)
        profiles.append(profile)
        print(f"checked R={R}, dimension={profile['type_dimension']}, bits={profile['worst_shared_bits']}",
              file=sys.stderr, flush=True)
    report = {"status": "PASS", "scope": "exact six-class R=1..5 screen; no eventual support rate",
              "local_scheme": {key: value for key, value in refined.SCHEME.items() if key != "classes"},
              "profiles": profiles,
              "bindings": {"base_commit": json.loads((HERE / "CLAIM.json").read_text())["base_commit"],
                           "predecessor_sha256": refined.coarse.PREDECESSOR_SHA256,
                           "refinement_proof_sha256": sha256((HERE / "SCHEME-REFINEMENT.md").read_bytes()).hexdigest(),
                           **{name + "_sha256": sha256((HERE / (name + ".py")).read_bytes()).hexdigest()
                              for name in ["refined", "refined_screen", "macro", "schemes"]}}}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
