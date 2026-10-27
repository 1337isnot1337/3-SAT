"""Exact finite-block self-Fourier dual search, not a rate extrapolation."""

from fractions import Fraction as F
from functools import reduce
from hashlib import sha256
import importlib.util
import json
from math import gcd, lcm
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("refined_for_dual", HERE / "refined.py")
refined = importlib.util.module_from_spec(spec)
spec.loader.exec_module(refined)
require = refined.require


def eliminate(vector, basis):
    vector = list(map(F, vector))
    for pivot, row in sorted(basis.items()):
        c = vector[pivot]
        if c:
            vector = [x - c * y for x, y in zip(vector, row)]
    return vector


def insert(vector, basis):
    vector = eliminate(vector, basis)
    pivot = next((j for j, x in enumerate(vector) if x), None)
    if pivot is not None:
        basis[pivot] = [x / vector[pivot] for x in vector]


def certificate(data):
    T, weights, q = data["transform"], data["weights"], data["target"]
    n, N = len(T), 8 ** data["R"]
    basis = {}
    for weight in sorted(set(weights)):
        before = {p: list(row) for p, row in basis.items()}
        for j, w in enumerate(weights):
            if w == weight:
                insert([T[i][j] + N * int(i == j) for i in range(n)], basis)
        if not any(eliminate(q, basis)):
            remainder = eliminate(q, before)
            free = next(j for j, x in enumerate(remainder) if x)
            require(free not in before, "Dual free coordinate")
            functional = [F(0)] * n
            functional[free] = 1
            for p, row in sorted(before.items(), reverse=True):
                functional[p] = -sum((row[j] * functional[j] for j in range(p + 1, n)), F(0))
            h = [sum((F(T[j][i] + N * int(i == j)) * functional[j] for j in range(n)), F(0))
                 / weights[i] for i in range(n)]
            den = lcm(*(x.denominator for x in h))
            integer = [int(x * den) for x in h]
            common = reduce(gcd, integer)
            integer = [x // common for x in integer]
            require(all(not x or w >= weight for x, w in zip(integer, weights)), "Dual support floor")
            require([sum(x * y for x, y in zip(row, integer)) for row in T] == [N * x for x in integer],
                    "Dual self-Fourier identity")
            pairing = sum(w * x * y for w, x, y in zip(weights, integer, q))
            require(pairing != 0, "Dual target pairing")
            return {"macros": data["R"], "minimum_type_cardinality": weight,
                    "nonzero_types": sum(bool(x) for x in integer),
                    "target_pairing": str(pairing),
                    "witness": [{"type": alpha, "value": x}
                                for alpha, x in zip(data["types"], integer) if x]}
    raise ValueError("No separating dual found")


def main():
    profiles = []
    for R in range(1, 6):
        result = certificate(refined.construct(R))
        profiles.append(result)
        print(f"dual R={R}, threshold={result['minimum_type_cardinality']}", file=sys.stderr, flush=True)
    print(json.dumps({"status": "PASS", "scope": "exact finite-block support-dual thresholds, R=1..5",
                      "profiles": profiles,
                      "bindings": {name + "_sha256": sha256((HERE / (name + ".py")).read_bytes()).hexdigest()
                                   for name in ["block_dual", "refined", "schemes", "macro"]}}, indent=2))


if __name__ == "__main__":
    main()
