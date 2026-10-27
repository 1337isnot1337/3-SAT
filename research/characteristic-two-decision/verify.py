#!/usr/bin/env python3
"""Exhaustive small characteristic-two fingerprint and incidence identities."""

from itertools import product
import json


def require(value, message):
    if not value:
        raise ValueError(message)


def raw_multiply(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        b >>= 1
    return result


def reduce_field(value):
    # V^3 + V + 1; neither 0 nor 1 is a root, so this cubic is irreducible.
    while value.bit_length() > 3:
        value ^= 0b1011 << (value.bit_length() - 4)
    return value


def multiply(a, b):
    return reduce_field(raw_multiply(a, b))


def polynomial_value(polynomial, assignment):
    value = 0
    for monomial in range(4):
        if polynomial >> monomial & 1 and assignment & monomial == monomial:
            value ^= 1
    return value


def weighted_truth_sum(system, weights):
    result = 0
    for assignment in range(4):
        if any(polynomial_value(p, assignment) for p in system):
            continue
        term = 1
        for j, weight in enumerate(weights):
            if assignment >> j & 1:
                term = multiply(term, weight)
        result ^= term
    return result


def incidence_sum(system, weights, raw=False):
    # A monomial is its 2-bit variable support. Each factor is exactly 1+P_i.
    factors = [[mask for mask in range(4) if (p ^ 1) >> mask & 1]
               for p in system]
    result = 0
    for selected in product(*factors):
        support = 0
        for mask in selected:
            support |= mask
        # Separate variable vertices have entries r_v or 1+r_v.
        entries = [weight if support >> j & 1 else weight ^ 1
                   for j, weight in enumerate(weights)]
        term = 1
        for entry in entries:
            term = raw_multiply(term, entry) if raw else multiply(term, entry)
        result ^= term
    return result


def main():
    for a in range(1, 8):
        require(any(multiply(a, b) == 1 for b in range(1, 8)), "field inverse missing")
    systems = fingerprints = unsatisfiable = 0
    worst_zeros = 0
    for system in product(range(16), repeat=2):
        solutions = [x for x in range(4)
                     if all(polynomial_value(p, x) == 0 for p in system)]
        zeros = 0
        for weights in product(range(8), repeat=2):
            direct = weighted_truth_sum(system, weights)
            expanded = incidence_sum(system, weights)
            lifted = incidence_sum(system, weights, raw=True)
            require(direct == expanded, "incidence expansion mismatch")
            require(reduce_field(lifted) == direct, "truncated-ring embedding mismatch")
            require(lifted.bit_length() <= 5, "unreduced product degree exceeds vertex budget")
            zeros += direct == 0
            fingerprints += 1
        if solutions:
            require(zeros <= 2 * 8, "degree-over-field-size failure bound violated")
            worst_zeros = max(worst_zeros, zeros)
        else:
            require(zeros == 64, "false positive on an unsatisfiable system")
            unsatisfiable += 1
        systems += 1
    # Unweighted parity is not a valid substitute: P=x0 has two solutions.
    require(weighted_truth_sum((0b0010,), (1, 1)) == 0, "parity failure control changed")
    require(any(weighted_truth_sum((0b0010,), r) for r in product(range(8), repeat=2)),
            "weighted detector failed its parity control")
    print(json.dumps({
        "status": "PASS", "field": "GF(8), V^3+V+1", "variables": 2,
        "all_ordered_two_equation_systems": systems,
        "field_point_evaluations": fingerprints,
        "unsatisfiable_systems": unsatisfiable,
        "maximum_zero_fingerprints_for_nonempty_solution_set": worst_zeros,
        "field_points_per_system": 64,
        "certified_failure_upper_bound": "2/8",
        "identities": ["weighted truth sum = incidence expansion",
                       "unreduced scalar-polynomial contraction reduces to field contraction"],
        "control": "unweighted parity can miss a nonempty solution set",
        "scope": "finite exhaustive algebra checks; no larger alpha or implementation of the accepted contraction"
    }, indent=2))


if __name__ == "__main__":
    main()
