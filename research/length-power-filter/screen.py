"""Exact finite scalar filters after a quadratic-length charge shift.

The local premise is Q_s^(q)(mu,nu) -> q^(2(len(mu)+len(nu))) Q_s^(q).
No all-size or asymptotic claim is made by this bounded checker.
"""
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "charge-polynomial-filter"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


generalized = load("length_power_generalized", PARENT / "generalized.py")
screen = generalized.screen
poly = generalized.poly
require = poly.require


def length_power(raw, pair_degrees, size, power=2):
    """Coefficient e=d+power*(len(mu)+len(nu)), exact integer arithmetic."""
    answer = {}
    for (degree, shift), column in raw.items():
        for index, value in enumerate(column):
            if value:
                key = (degree + power * pair_degrees[index], shift)
                if key not in answer:
                    answer[key] = [0] * size
                answer[key][index] = value
    return answer


def classify_case(data, raw, pair_degrees, raw_degree, family, power, cutoff):
    N, h = data["N"], data["h"]
    if family == "raw":
        tensors = raw
        degree = raw_degree
    else:
        tensors = length_power(raw, pair_degrees, N ** 4, power)
        degree = raw_degree + power * max(pair_degrees)
    result = screen.classify(tensors, N, h, degree, cutoff)
    result["family"] = family
    result["length_power"] = power
    generalized.finite_rank_bits(result, h, N, degree)
    print(f"classified {family}, power={power}, cutoff={cutoff}: "
          f"space={result['label_matrix_space_dimension']}, "
          f"invertible={result['full_rank_scalar_pairing_exists']}",
          file=sys.stderr, flush=True)
    # The complete witness and its weights are checked in memory; keep the
    # saved report compact and hash-bind the code that reconstructs them.
    if "witness" in result:
        result["witness"] = {key: value for key, value in result["witness"].items()
                             if key not in {"weights", "label_matrix", "determinant"}}
    return result


def main():
    cases = []
    for bits in (1, 2):
        data = poly.model.construct(bits)
        N, h = data["N"], data["h"]
        raw, pair_degrees, raw_degree, evaluation_checks = generalized.build_raw(data)
        bands = []
        if bits == 1:
            specifications = [("length_power", 2, 4, True),
                              ("length_power", 2, 5, False)]
        else:
            specifications = [("raw", 0, 5, False),
                              ("length_power", 2, 6, True),
                              ("length_power", 2, 7, False)]
        for family, power, cutoff, expected in specifications:
            result = classify_case(data, raw, pair_degrees, raw_degree,
                                   family, power, cutoff)
            require(result["full_rank_scalar_pairing_exists"] == expected,
                    f"registered boundary changed at h={h}, cutoff={cutoff}")
            bands.append(result)
        cases.append({"lambda": bits, "h": h, "N": N,
                      "maximum_raw_charge_degree": raw_degree,
                      "charge_evaluation_checks": evaluation_checks,
                      "bands": bands})
    result = {
        "status": "PASS",
        "scope": "complete registered finite scalar spaces; no all-size gain",
        "construction": "coefficient e=d+2(len(mu)+len(nu)) of q^(2(len(mu)+len(nu)))Q_s^(q)",
        "cases": cases,
        "bindings": {name: sha256((HERE / name).read_bytes()).hexdigest()
                     for name in ("README.md", "screen.py")},
    }
    (HERE / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
