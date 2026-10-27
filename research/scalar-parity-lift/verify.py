"""Bounded, deterministic checks of the scalar parity-lift component.

Run from any directory with python3 -I -B /path/to/verify.py. No network,
third-party dependencies, or implementation of the accepted fast contraction.
The saved JSON contains counts, exact witnesses and source hashes, not timings.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
from random import Random
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))

from scalar_lift import (
    bit_ceiling, coefficient, coefficient_table, decode_subset, direct_count,
    grouped_contraction, incidence_sum, normalize, parity, scope,
)
from satbounds.cost import analyze


def require(condition, message):
    if not condition:
        raise ValueError(message)


def all_equations(n, k):
    terms = [mask for mask in range(1 << n) if mask.bit_count() <= k]
    return [tuple(term for j, term in enumerate(terms) if code >> j & 1)
            for code in range(1 << len(terms))]


def check_local():
    stats = {"normalized_polynomials": 0, "coefficient_comparisons": 0,
             "divisibility_checks": 0, "boolean_evaluation_checks": 0}
    for n in range(5):
        for equation in all_equations(n, min(3, n)):
            stats["normalized_polynomials"] += 1
            k = max((1, *(term.bit_count() for term in equation)))
            table = coefficient_table(equation)
            for support in range(1 << n):
                value = table.get(support, 0)
                require(value == coefficient(equation, support), "Local lifts disagree")
                stats["coefficient_comparisons"] += 1
                weight = max(0, (support.bit_count() + k - 1) // k - 1)
                require(value % (1 << weight) == 0, "Local divisibility fails")
                stats["divisibility_checks"] += 1
                evaluated = sum(c for monomial, c in table.items()
                                if support & monomial == monomial)
                require(evaluated == 1 - parity(equation, support), "Wrong projector")
                stats["boolean_evaluation_checks"] += 1
    require(normalize([[0, 0], [0], [], []], 2) == (), "Normalization failure")
    require(normalize([[0, 0, 1], [1, 0]], 2) == (), "Multilinear cancellation failure")
    require(normalize([[], [1, 1]], 3) == (0, 2), "Constant or unused-variable failure")
    return stats


def check_systems():
    stats = {"ordered_two_equation_systems": 0, "precision_cases": 0,
             "retained_nonzero_incidence_terms": 0,
             "discarded_nonzero_integer_coefficients": 0}
    for n in range(4):
        equations = all_equations(n, min(2, n))
        for system in product(equations, repeat=2):
            stats["ordered_two_equation_systems"] += 1
            count = direct_count(system, n)
            k = max((1, *(term.bit_count() for equation in system for term in equation)))
            for precision in range(1, n + 2):
                value, retained, discarded = incidence_sum(system, n, k, precision)
                require(value == count % (1 << precision), "Truncated incidence count fails")
                stats["precision_cases"] += 1
                stats["retained_nonzero_incidence_terms"] += retained
                stats["discarded_nonzero_integer_coefficients"] += discarded
    require(stats["discarded_nonzero_integer_coefficients"] > 0, "No truncation exercised")
    return stats


def check_indexing():
    stats = {"valid_subset_indices": 0, "invalid_subset_indices": 0}
    for size in range(13):
        items = tuple(range(size))
        for degree in range(size + 1):
            expected = list(combinations(items, degree))
            for code in range(1 << bit_ceiling(len(expected))):
                decoded = decode_subset(items, degree, code)
                if code < len(expected):
                    require(decoded == expected[code], "Wrong combinatorial unranking")
                    stats["valid_subset_indices"] += 1
                else:
                    require(decoded is None, "Invalid subset index accepted")
                    stats["invalid_subset_indices"] += 1
    require(stats["invalid_subset_indices"] > 0, "No invalid code exercised")
    return stats


def check_networks():
    rng = Random(20261027)
    cases = [(0, (), 1), (0, ((),), 1), (0, ((0,),), 1),
             (4, (), 5), (4, ((1,),), 5), (4, ((0, 1),), 5),
             (4, ((1, 2, 4, 8), (1, 2, 4, 8)), 1)]
    for a, count in ((1, 8), (2, 24), (3, 8)):
        for j in range(count):
            system = tuple(tuple(t for t in range(16) if rng.randrange(2)) for _ in range(a))
            cases.append((4, system, 1 + j % 5))
    stats = {"network_cases": 0, "arrays": 0, "wire_assignments": 0,
             "invalid_codes": 0, "valid_indices": 0, "zero_wire_pairs": 0,
             "max_wires": 0}
    for n, system, precision in cases:
        k = max((1, *(term.bit_count() for equation in system for term in equation)))
        actual, local = grouped_contraction(system, n, k, precision)
        require(actual == direct_count(system, n) % (1 << precision), "Grouped contraction fails")
        require(actual == incidence_sum(system, n, k, precision)[0], "Network/incidence mismatch")
        stats["network_cases"] += 1
        for key, value in local.items():
            if key == "max_wires":
                stats[key] = max(stats[key], value)
            else:
                stats[key] += value
    require(stats["invalid_codes"] > 0 and stats["zero_wire_pairs"] > 0,
            "Required network edge cases missing")
    return stats


def check_high_incidence_branches():
    witnesses = []
    n = 8
    systems = [
        tuple((1 | (1 << (1 + i % 7)),) for i in range(16)),
        tuple((3,) for _ in range(16)),
    ]
    for system in systems:
        loads = [sum(scope(eq) >> v & 1 for eq in system) for v in range(n)]
        n0 = sum(loads)
        # lambda=3 and ceil(sqrt(lambda))=2 at the declared size n=8.
        threshold = max(1, (n0 + n - 1) // n) * 2
        fixed = [v for v in range(n) if loads[v] > threshold]
        free = [v for v in range(n) if v not in fixed]
        fixed_mask = sum(1 << v for v in fixed)
        counts = []
        for bits in product((0, 1), repeat=len(fixed)):
            fixed_assignment = sum(bit << v for bit, v in zip(bits, fixed))
            branch = []
            for equation in system:
                terms = set()
                for term in equation:
                    if term & fixed_mask & fixed_assignment != term & fixed_mask:
                        continue
                    mask = sum(1 << i for i, v in enumerate(free) if term >> v & 1)
                    terms.symmetric_difference_update((mask,))
                branch.append(tuple(sorted(terms)))
            count = direct_count(branch, len(free))
            # Check the smaller branch modulus, rather than retaining n+1.
            require(incidence_sum(branch, len(free), 2, len(free) + 1)[0] == count,
                    "Branch precision or constant-equation failure")
            counts.append(count)
        require(sum(counts) == direct_count(system, n), "Branch partition fails")
        witnesses.append({"n": n, "N0": n0, "threshold": threshold,
                          "fixed_variables": fixed, "free_variables": len(free),
                          "branch_counts": counts, "total_count": sum(counts)})
    return witnesses


def check_sharpness():
    witnesses = []
    for k, n in ((1, 3), (2, 5), (3, 7)):
        system = tuple(tuple(sum(1 << ((i + offset + j) % n) for j in range(k))
                             for offset in (0, k)) for i in range(n))
        top = 1
        for equation in system:
            top *= coefficient(equation, scope(equation))
        cutoff = k * (len(system) + n)
        require(sum(scope(eq).bit_count() for eq in system) == cutoff, "Wrong top degree")
        require(top == 1 << n, "Sharp top coefficient mismatch")
        require(top % (1 << (n + 1)) != 0, "Sharp coefficient vanished")
        count = direct_count(system, n)
        below_top = (count - top) % (1 << (n + 1))
        require(below_top != count, "Invalid lower cutoff was not rejected")
        witnesses.append({"k": k, "free_variables": n, "equations": n,
                          "sharp_degree": cutoff, "top_coefficient": top,
                          "count": count, "count_with_top_degree_removed": below_top})
    # For the smallest witness explicitly sum every incidence monomial.
    system = ((1, 2), (2, 4), (4, 1))
    tables = [coefficient_table(eq) for eq in system]
    below_top = 0
    for terms in product(*(tuple(table.items()) for table in tables)):
        if sum(s.bit_count() for s, _ in terms) == 6:
            continue
        value, covered = 1, 0
        for support, c in terms:
            value *= c
            covered |= support
        below_top += value << (3 - covered.bit_count())
    require(below_top % 16 == witnesses[0]["count_with_top_degree_removed"],
            "Explicit lower-cutoff rejection mismatch")
    return witnesses


def binary_rank(rows):
    pivots = {}
    for row in rows:
        while row:
            p = row.bit_length() - 1
            if p not in pivots:
                pivots[p] = row
                break
            row ^= pivots[p]
    return len(pivots)


def check_entropy_family():
    cases = []
    for n in (16, 32, 64):
        k = 3
        log_n = n.bit_length() - 1
        length = log_n if log_n % 2 else log_n - 1
        monomials = [sum(1 << ((i + j) % n) for j in range(k)) for i in range(n)]
        system = tuple(tuple(monomials[(i + j) % n] for j in range(length)) for i in range(n))
        rows = [sum(1 << ((i + j) % n) for j in range(length)) for i in range(n)]
        require(binary_rank(rows) == n, "Circulant rank failure")
        require(all(scope(eq).bit_count() == length + k - 1 for eq in system), "Scope failure")
        loads = [sum(scope(eq) >> v & 1 for eq in system) for v in range(n)]
        require(set(loads) == {length + k - 1}, "Variable load failure")
        for equation in system:
            for term in equation:
                require(coefficient(equation, term) == -1, "Odd singleton-term coefficient failed")
        cases.append({"n": n, "k": k, "terms_per_equation": length,
                      "row_rank": n, "scope_and_variable_load": length + k - 1,
                      "certified_retained_nonzero_coefficients": str(length ** n)})
    return cases


def multiply_linear(poly, constant, slope):
    result = [Fraction(0)] * (len(poly) + 1)
    for i, c in enumerate(poly):
        result[i] += c * constant
        result[i + 1] += c * slope
    return result


def check_shifted_integrality_control():
    # A control for the shortcut supplied in the user discussion. Shifted
    # integrality does not imply global integral coefficients or mod-2 equality.
    length, scale = 4, 8
    nodes = range(-length, length)
    denominator = 1
    for q in nodes:
        if q:
            denominator *= -q
    checked = 0
    witness = {}
    for x, y, t in product(range(length), range(length), nodes):
        poly = [Fraction(1, denominator)]
        for q in nodes:
            if q != y - x:
                poly = multiply_linear(poly, t - q, scale)
        require(all(c.denominator % 2 for c in poly), "Shifted integrality failure")
        if x == y == 0 and t in (0, -2):
            witness[t] = poly[0]
        checked += 1
    require(Fraction(1, denominator).denominator % 2 == 0, "Global coefficient control failed")
    require(witness == {0: Fraction(1), -2: Fraction(0)}, "Parity shortcut counterexample failed")
    return {"L": length, "alpha": scale, "shifted_blocks_checked": checked,
            "W00_at_zero": str(witness[0]), "W00_at_minus_two": str(witness[-2]),
            "global_leading_coefficient": str(Fraction(1, denominator)),
            "conclusion": "Do not infer F(t) = F(0) mod 2 from shifted integrality"}


def check_wire_envelopes():
    cases = []
    for n in (64, 128, 256, 512):
        a, k = 6 * n, 3
        log_n = n.bit_length() - 1
        incidences = n * log_n ** 3
        old = min(incidences, k * (a + 2 * n))
        new = min(incidences, k * (a + n))
        old_bits = bit_ceiling(comb(incidences + old, old))
        new_bits = bit_ceiling(comb(incidences + new, new))
        require(new_bits < old_bits, "Degree-envelope improvement missing")
        cases.append({"n": n, "a": a, "k": k, "N": incidences,
                      "old_degree_envelope": old, "scalar_degree_envelope": new,
                      "old_stars_bars_bit_ceiling": old_bits,
                      "scalar_stars_bars_bit_ceiling": new_bits})
    return cases


def main():
    pins = {
        "main_full_version.tex": "b2e6159d4fb7ea6aa4f89ac15605152b0333a5f7cafe93323492bc20a5c066aa",
        "quantitative-reduction.tex": "0b2b136c4f37ee0583dda40ee0c0d692f4751537d3d18539a389cd467ea8359a",
        "quantitative-contraction.tex": "671642d7b53154d92344e8c4be0240f18929632ebcfdf73b07c3e9939b873860",
    }
    for name, expected in pins.items():
        path = ROOT / "upstream/openai-eth-2026/build" / name
        require(sha256(path.read_bytes()).hexdigest() == expected, "Frozen source drift: " + name)
    model = analyze(json.loads((HERE / "model.json").read_text()))
    require(model["alpha"] == "1/2", "Cost model incorrectly claims a new alpha")
    require(model["dominant_envelope"] == {"n": "1", "log": "-1/2", "loglog": "1"},
            "Cost model incorrectly removes log log")
    report = {
        "schema_version": 1, "result": "PASS_EXACT_SCALAR_PARITY_LIFT",
        "scope": "Finite component and encoding checks; no fast contraction implementation or independent proof review",
        "base_commit": "fd6df02023122badbdd888803146f0bd92002214",
        "upstream_commit": "7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a",
        "upstream_sha256": pins,
        "local_projectors": check_local(), "systems": check_systems(),
        "subset_indexing": check_indexing(), "grouped_networks": check_networks(),
        "high_incidence_branches": check_high_incidence_branches(),
        "sharp_degree_witnesses": check_sharpness(),
        "retained_support_family": check_entropy_family(),
        "shifted_integrality_failure_control": check_shifted_integrality_control(),
        "wire_envelope_comparisons": check_wire_envelopes(),
        "cost_model": model,
    }
    report["artifact_sha256"] = {
        name: sha256((HERE / name).read_bytes()).hexdigest()
        for name in ("scalar_lift.py", "verify.py", "PROOF.md", "model.json")
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
