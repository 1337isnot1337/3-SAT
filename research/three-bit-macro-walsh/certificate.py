"""Frozen four-block certificate replay; no adapted-basis or dual search."""

from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import importlib.util
import json
from math import factorial, prod
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("local_certificate_scheme", HERE / "schemes.py")
schemes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schemes)
require = schemes.require


def multiply(left, right):
    result = {}
    for alpha, x in left.items():
        for beta, y in right.items():
            gamma = tuple(a + b for a, b in zip(alpha, beta))
            result[gamma] = result.get(gamma, 0) + x * y
    return {alpha: x for alpha, x in result.items() if x}


def word_count(alpha, weights):
    result = factorial(sum(alpha))
    for x in alpha:
        result //= factorial(x)
    return result * prod(w ** x for w, x in zip(weights, alpha))


def transform_polynomial(polynomial, matrix):
    result = {}
    zero = (0,) * len(matrix)
    for alpha, coefficient in polynomial.items():
        term = {zero: coefficient}
        for row, count in zip(matrix, alpha):
            linear = {tuple(int(i == j) for i in range(len(matrix))): x
                      for j, x in enumerate(row) if x}
            for _ in range(count):
                term = multiply(term, linear)
        for beta, x in term.items():
            result[beta] = result.get(beta, 0) + x
    return {alpha: x for alpha, x in result.items() if x}


def evaluate(polynomial, values):
    return sum(x * prod(z ** a for z, a in zip(values, alpha)) for alpha, x in polynomial.items())


def main():
    scheme = schemes.local_scheme()
    C, weights, q = scheme["matrix"], scheme["weights"], scheme["target"]
    seed = json.loads((HERE / "four-block-dual.json").read_text())
    h = {tuple(term["type"]): term["value"] for term in seed["witness"]}
    require(len(h) == len(seed["witness"]) == 27 and all(sum(a) == 4 for a in h), "Seed format")
    polynomial = {alpha: word_count(alpha, weights) * x for alpha, x in h.items()}
    require(transform_polynomial(polynomial, C) == {alpha: 8 ** 4 * x for alpha, x in polynomial.items()},
            "Weighted polynomial self-Fourier identity")
    pairing = evaluate(polynomial, q)
    require(pairing == 17948262528 == int(seed["target_pairing"]), "Frozen nonzero pairing")
    W = min(word_count(alpha, weights) for alpha in h)
    require(W == 129654 == seed["minimum_type_cardinality"], "Frozen type floor")
    require(W ** 100 > 2 ** 1698 and F(1698, 400) ** 2 > 18, "Strict rate inequality")
    # Polynomial multiplication is the symmetric average of block tensoring,
    # after division of each coefficient by its actual global type size.
    powers = []
    for t in range(1, 5):
        P = {(0,) * 6: 1}
        for _ in range(t):
            P = multiply(P, polynomial)
        require(evaluate(P, q) == pairing ** t, "Tensor pairing")
        minimum = min(word_count(alpha, weights) for alpha in P)
        require(minimum >= W ** t, "Concatenated type floor")
        powers.append({"blocks": t, "degree": 4 * t, "nonzero_types": len(P),
                       "minimum_type_cardinality": minimum})
    # A deliberately wrong unweighted encoding must be rejected.
    require(transform_polynomial(h, C) != {alpha: 8 ** 4 * x for alpha, x in h.items()},
            "Incorrect type normalization escaped negative control")
    print(json.dumps({"status": "PASS", "scope": "frozen dual identity and tensor-support certificate",
                      "minimum_seed_type": W, "seed_pairing": pairing, "tensor_checks": powers,
                      "rate_comparison": "129654^100 > 2^1698; (1698/400)^2 > 18",
                      "bindings": {name: sha256((HERE / name).read_bytes()).hexdigest()
                                   for name in ["four-block-dual.json", "certificate.py", "schemes.py",
                                                "BLOCK-BARRIER.md", "SCHEME-REFINEMENT.md"]}}, indent=2))


if __name__ == "__main__":
    main()
