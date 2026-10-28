"""Bounded exact checks for the aggregate packing tradeoff.

This checks the stated representation-specific identities and numerical
fixtures. It does not implement the accepted contraction or prove an
asymptotic theorem by computation.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = 64


def ceil_log2_fraction(value: Fraction) -> int:
    """Return the least d with value <= 2**d, exactly."""
    if value <= 1:
        return 0
    d = max(0, value.numerator.bit_length() - value.denominator.bit_length())
    while Fraction(2**d) < value:
        d += 1
    while d and Fraction(2 ** (d - 1)) >= value:
        d -= 1
    return d


def integer_fourth_root_ceiling(n: int) -> int:
    x = math.isqrt(math.isqrt(n))
    while x**4 < n:
        x += 1
    while x and (x - 1) ** 4 >= n:
        x -= 1
    return x


def exact_support_checks() -> tuple[int, int]:
    evaluations = 0
    max_code_bits = 0
    for h in range(1, 6):
        for j in range(2, 5):
            monomials = list(itertools.product(range(j), repeat=h))
            assert len(monomials) == j**h
            for groups in range(1, 4):
                buckets: dict[tuple[int, ...], int] = {}
                for monomial in monomials:
                    # Assign variable (block, coordinate) to a deterministic
                    # variable group. Only group degrees are retained.
                    degrees = [0] * groups
                    for block, coordinate in enumerate(monomial):
                        group = (block * j + coordinate) % groups
                        degrees[group] += 1
                    buckets[tuple(degrees)] = buckets.get(tuple(degrees), 0) + 1
                    evaluations += 1
                assert len(buckets) <= (h + 1) ** groups
                largest = max(buckets.values())
                assert largest * (h + 1) ** groups >= j**h
                information = Fraction(j**h, (h + 1) ** groups)
                code_bits = ceil_log2_fraction(information)
                assert 2**code_bits * (h + 1) ** groups >= j**h
                if code_bits:
                    assert 2 ** (code_bits - 1) * (h + 1) ** groups < j**h
                assert code_bits >= h * math.log2(j) - groups * math.log2(h + 1) - 1
                max_code_bits = max(max_code_bits, code_bits)
    return evaluations, max_code_bits


def asymptotic_fixture(lam: int, j: int) -> dict[str, float | int]:
    n = 2**lam
    h = n // j
    groups = integer_fourth_root_ceiling(n)
    degree_lower = h * math.log2(j) - groups * math.log2(h + 1)
    nominal_wires = n * math.log2(j)
    log_s = math.log2(nominal_wires)
    leaf_scale = nominal_wires / math.sqrt(log_s)
    return {
        "log2_n": lam,
        "J": j,
        "log2_J": math.log2(j),
        "degree_lower": degree_lower,
        "nominal_wires": nominal_wires,
        "leaf_scale": leaf_scale,
        "degree_lower_over_leaf_scale": degree_lower / leaf_scale,
        "active_degree_edge_floor": (R / 3) * degree_lower,
    }


def main() -> None:
    evaluations, max_code_bits = exact_support_checks()

    # The balance obstruction is independent of the center's chosen symbol.
    star_cases = []
    for edges in (4, 16, 257):
        allowed = Fraction(3 * edges, R)
        assert allowed < edges
        for symbol in range(R):
            center_ports_at_symbol = edges
            assert center_ports_at_symbol > allowed
        star_cases.append({"edges": edges, "max_balanced_ports": float(allowed)})

    fixtures = []
    for lam in (64, 128, 256, 512):
        nu = math.log2(lam)
        choices = dict.fromkeys((8, math.ceil(nu), 2 ** math.ceil(nu), 2 ** math.ceil(math.sqrt(lam))))
        for j in choices:
            fixture = asymptotic_fixture(lam, j)
            assert fixture["degree_lower"] > 0
            fixtures.append(fixture)

    # Fixed J and J=log(log(n)) illustrate the growing obstruction. The
    # sqrt(lambda) fixture retains a constant fraction of nu in its wire log.
    small_j_ratios = []
    for fixture in fixtures:
        lam = fixture["log2_n"]
        j = fixture["J"]
        if j == 8 or j == math.ceil(math.log2(lam)):
            assert fixture["degree_lower"] > fixture["leaf_scale"]
            small_j_ratios.append(fixture["degree_lower_over_leaf_scale"])
        if j >= 2 ** math.ceil(math.sqrt(lam)):
            assert fixture["log2_J"] >= math.sqrt(lam)
    for lam in (64, 128, 256, 512):
        j = math.ceil(math.log2(lam))
        ratios = [f["degree_lower_over_leaf_scale"] for f in fixtures
                  if f["log2_n"] == lam and f["J"] == j]
        assert len(ratios) == 1
    iterated_log_ratios = [f["degree_lower_over_leaf_scale"] for f in fixtures
                           if f["J"] == math.ceil(math.log2(f["log2_n"]))]
    assert all(b > a for a, b in zip(iterated_log_ratios, iterated_log_ratios[1:]))

    result = {
        "status": "pass",
        "scope": (
            "Exact finite support/array identities, star balance controls, "
            "and numerical instances of the written asymptotic formulas; "
            "not an implementation or independent proof review"
        ),
        "exact_support_evaluations": evaluations,
        "small_support_families": 45,
        "largest_exact_code_bit_bound": max_code_bits,
        "star_balance_controls": star_cases,
        "asymptotic_formula_fixtures": fixtures,
        "accepted_contraction_implemented": False,
        "new_sat_bound_claimed": False,
    }
    result["proof_sha256"] = hashlib.sha256((HERE / "PROOF.md").read_bytes()).hexdigest()
    result["checker_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (HERE / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "asymptotic_formula_fixtures"}, indent=2))
    print(f"PASS: {len(fixtures)} asymptotic formula fixtures")


if __name__ == "__main__":
    main()
