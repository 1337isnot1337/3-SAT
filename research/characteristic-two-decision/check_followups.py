#!/usr/bin/env python3
"""Exact checks of failed aggregation and even-node routes, and a matroid identity."""

from fractions import Fraction as F
from math import comb, prod
import json


def require(value, message):
    if not value:
        raise ValueError(message)


def rank(columns):
    basis = {}
    for column in columns:
        while column:
            bit = column.bit_length() - 1
            if bit in basis:
                column ^= basis[bit]
            else:
                basis[bit] = column
                break
    return len(basis)


def matroid_check():
    checked = 0
    for encoded in range(1 << 8):
        columns = [(encoded >> (2 * j)) & 3 for j in range(4)]
        independent = [rank([columns[j] for j in range(4) if s >> j & 1]) == s.bit_count()
                       for s in range(16)]
        for v in range(16):
            syndrome = 0
            for j in range(4):
                if v >> j & 1:
                    syndrome ^= columns[j]
            expansion = sum(independent[s] for s in range(16) if s & v == s) % 2
            require(expansion == (syndrome == 0), "matroid independence identity failed")
            checked += 1
    return {"all_binary_2_by_4_matrices": 256, "syndrome_evaluations": checked}


def even_node_check():
    L = 4
    nodes = list(range(-L, L))
    denominator = prod(-t for t in nodes if t)
    def w(x, y, t):
        return F(prod(t - q for q in nodes if q != y - x), denominator)
    require(w(0, 0, 0) == 1 and w(0, 0, -2) == 0, "parity counterexample changed")
    require(w(2, 0, -2) == F(5, 3), "surviving local entry mismatch")
    coefficients = [F(1)]
    for q in nodes:
        if not q:
            continue
        updated = [F(0)] * (len(coefficients) + 1)
        for j, c in enumerate(coefficients):
            updated[j] -= q * c
            updated[j + 1] += c
        coefficients = updated
    coefficients = [c / denominator for c in coefficients]
    require(coefficients[1] == F(1, 4), "nonintegral coefficient control changed")
    integral_charts = 0
    for t in nodes:
        shifted = [sum((coefficients[j] * comb(j, k) * t**(j-k) * 8**k
                        for j in range(k, len(coefficients))), F(0))
                   for k in range(len(coefficients))]
        require(all(c.denominator % 2 for c in shifted), "local integral chart failed")
        integral_charts += 1
    return {"packet_length": L, "even_node": -2, "F_at_zero": "1", "F_at_even_node": "0",
            "F_linear_coefficient": "1/4", "nonzero_local_entry": "5/3",
            "integral_shifted_charts_checked": integral_charts,
            "conclusion": "even-node parity preservation is false despite integral local charts"}


def aggregation_check():
    # n=2^128, J=8, h=n/J, R=n^(1/4). Top-degree support of the explicit
    # disjoint-block product has J^h monomials. At most (h+1)^R arrays split it.
    n = 2**128
    J = 8
    h = n // J
    R = 2**32
    wire_target = 3 * n
    # log2(h+1) < bit_length(h+1), so this is a conservative integer floor.
    degree_lower = 3 * h - R * (h + 1).bit_length()
    require(degree_lower > 0 and degree_lower**10 > wire_target**9,
            "aggregate degree no longer exceeds s^(9/10)")
    return {"n": str(n), "test_groups": J, "equations_in_example_group": str(h),
            "variable_groups": R, "candidate_s": str(wire_target),
            "rigorous_tensor_degree_lower_bound": str(degree_lower),
            "exact_check": "degree_lower^10 > candidate_s^9",
            "scope": "counterexample to automatic degree admissibility of this monomial-index aggregation"}


if __name__ == "__main__":
    print(json.dumps({"status": "PASS", "even_node": even_node_check(),
                      "matroid": matroid_check(), "aggregation": aggregation_check()}, indent=2))
