"""Exact finite checks of the scalar lift, cutoff and one-monomial encoding.

Standard library only. This is a reference experiment, not an implementation
of the accepted subexponential tensor contraction algorithm or a formal proof.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))

from satbounds.cnf import CNF, count


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def value(monomials: tuple[int, ...], assignment: int) -> int:
    """Polynomial value in F_2; a support mask 0 denotes the constant one."""
    result = 0
    for mask in monomials:
        result ^= (assignment & mask) == mask
    return int(result)


def mobius_indicator(monomials: tuple[int, ...], n: int) -> list[int]:
    coefficients = [1 - value(monomials, x) for x in range(1 << n)]
    for bit in range(n):
        for mask in range(1 << n):
            if mask & (1 << bit):
                coefficients[mask] -= coefficients[mask ^ (1 << bit)]
    return coefficients


def expansion_indicator(monomials: tuple[int, ...], n: int) -> list[int]:
    """Independently multiply prod(1-2m) in the integer Boolean ring."""
    polynomial = {0: 1}
    for monomial in monomials:
        updated = dict(polynomial)
        for support, coefficient in polynomial.items():
            union = support | monomial
            updated[union] = updated.get(union, 0) - 2 * coefficient
        polynomial = {s: c for s, c in updated.items() if c}
    polynomial[0] = polynomial.get(0, 0) + 1
    require(all(c % 2 == 0 for c in polynomial.values()), "Nonintegral lift")
    return [polynomial.get(s, 0) // 2 for s in range(1 << n)]


def valuation(coefficient: int) -> int:
    require(coefficient != 0, "valuation(0) is not finite")
    coefficient = abs(coefficient)
    return (coefficient & -coefficient).bit_length() - 1


def cover_numbers(monomials: tuple[int, ...], n: int) -> list[int]:
    """Exhaustive finite oracle, not a claimed efficient cover algorithm."""
    cover = [len(monomials) + 1] * (1 << n)
    cover[0] = 0
    for monomial in monomials:
        updated = list(cover)
        for support, needed in enumerate(cover):
            union = support | monomial
            updated[union] = min(updated[union], needed + 1)
        cover = updated
    return cover


def check_all_small_lifts() -> dict:
    n = 4
    universe = tuple(s for s in range(1 << n) if s.bit_count() <= 3)
    coefficient_checks = 0
    cover_checks = 0
    for word in range(1 << len(universe)):
        monomials = tuple(s for j, s in enumerate(universe) if word & (1 << j))
        actual = mobius_indicator(monomials, n)
        require(actual == expansion_indicator(monomials, n), "Scalar identity")
        cover = cover_numbers(monomials, n)
        k = max((s.bit_count() for s in monomials), default=0)
        for support, coefficient in enumerate(actual):
            coefficient_checks += 1
            if not support or not coefficient:
                continue
            v = valuation(coefficient)
            require(cover[support] <= v + 1, "Exact-cover valuation bound")
            require(support.bit_count() <= k * (v + 1), "Degree valuation bound")
            cover_checks += 1
    return {"variables": n, "max_width": 3,
            "all_anf_polynomials": 1 << len(universe),
            "integer_coefficient_comparisons": coefficient_checks,
            "nonzero_nonconstant_valuation_checks": cover_checks}


def incidence_sum(tables: list[list[int]], n: int, k: int, p: int) -> tuple[int, int]:
    """Reference incidence expansion with the *global* scalar cutoff."""
    cutoff = k * (len(tables) + p - 1)
    result = omitted = 0
    nonzero = [[(s, c) for s, c in enumerate(table) if c] for table in tables]
    for terms in product(*nonzero):
        support = degree = 0
        coefficient = 1
        for s, c in terms:
            support |= s
            degree += s.bit_count()
            coefficient *= c
        if degree > cutoff:
            require(coefficient % (1 << p) == 0, "Omitted coefficient survives")
            omitted += 1
            continue
        result += coefficient * (1 << (n - support.bit_count()))
    return result % (1 << p), omitted


def check_small_systems() -> dict:
    checked = omitted = 0
    n = 3
    universe = tuple(s for s in range(1 << n) if s.bit_count() <= 2)
    polynomials = [tuple(s for j, s in enumerate(universe) if word & (1 << j))
                   for word in range(1 << len(universe))]
    tables = [mobius_indicator(poly, n) for poly in polynomials]
    satisfying = [sum((1 - value(poly, x)) << x for x in range(1 << n))
                  for poly in polynomials]
    for i, j in product(range(len(polynomials)), repeat=2):
        expected = (satisfying[i] & satisfying[j]).bit_count()
        for p in range(1, n + 2):
            actual, discarded = incidence_sum([tables[i], tables[j]], n, 2, p)
            require(actual == expected % (1 << p), "System count after cutoff")
            checked += 1
            omitted += discarded
    # Low-width, no-test, contradictory, unused-variable, and three-test cases.
    extra = [([], 0, 1), ([], 5, 1), ([()], 5, 1), ([(0,)], 5, 1),
             ([(1, 2, 4), (1, 4), (2, 4)], 5, 1),
             ([(1, 2, 4, 8), (3, 12), (0, 5, 10)], 4, 2),
             ([(7, 56), (21, 42), (1, 32)], 6, 3)]
    for polys, n, k in extra:
        expected = sum(all(value(poly, x) == 0 for poly in polys)
                       for x in range(1 << n))
        for p in range(1, n + 2):
            actual, discarded = incidence_sum([mobius_indicator(poly, n) for poly in polys],
                                             n, k, p)
            require(actual == expected % (1 << p), "Extra system count")
            checked += 1
            omitted += discarded
    return {"all_ordered_pairs_of_three_variable_width_two_anfs": len(polynomials) ** 2,
            "modular_count_comparisons": checked, "omitted_zero_coefficients": omitted}


def decode_subset(n: int, d: int, rank: int) -> tuple[int, ...] | None:
    if rank >= comb(n, d):
        return None
    remaining = d
    chosen = []
    for position in range(n):
        if not remaining:
            break
        completions = comb(n - position - 1, remaining - 1)
        if rank < completions:
            chosen.append(position)
            remaining -= 1
        else:
            rank -= completions
    require(remaining == 0 and rank == 0, "Unranking failed")
    return tuple(chosen)


def check_decoder() -> dict:
    valid = invalid = no_wire = 0
    for n in range(11):
        for d in range(n + 1):
            subsets = list(combinations(range(n), d))
            bits = (len(subsets) - 1).bit_length()
            no_wire += bits == 0
            for rank in range(1 << bits):
                expected = subsets[rank] if rank < len(subsets) else None
                require(decode_subset(n, d, rank) == expected, "Subset decoder")
                if expected is None:
                    invalid += 1
                else:
                    valid += 1
    return {"max_incidence_universe": 10, "valid_codes": valid,
            "invalid_codes": invalid, "zero_wire_group_pairs": no_wire}


def grouped_network_count(polys: list[tuple[int, ...]], n: int, k: int, p: int) -> tuple[int, dict]:
    """Exhaustively contract the actual tiny binary networks, including bad codes."""
    test_groups = [list(range(0, len(polys), 2)), list(range(1, len(polys), 2))]
    variable_groups = [list(range(0, n, 2)), list(range(1, n, 2))]
    scopes = [0] * len(polys)
    for i, poly in enumerate(polys):
        for monomial in poly:
            scopes[i] |= monomial
    pairs = []
    for tests in test_groups:
        for variables in variable_groups:
            pairs.append([(i, v) for i in tests for v in variables if scopes[i] & (1 << v)])
    tables = [mobius_indicator(poly, n) for poly in polys]
    cutoff = k * (len(polys) + p - 1)
    total = arrays = assignments = invalid = 0
    for degrees in product(*(range(len(pair) + 1) for pair in pairs)):
        if sum(degrees) > cutoff:
            continue
        arrays += 1
        bits = [(comb(len(pair), d) - 1).bit_length() for pair, d in zip(pairs, degrees)]
        for ranks in product(*(range(1 << b) for b in bits)):
            assignments += 1
            decoded = [decode_subset(len(pair), d, rank)
                       for pair, d, rank in zip(pairs, degrees, ranks)]
            if any(subset is None for subset in decoded):
                invalid += 1
                continue
            selected = [0] * len(polys)
            touched = 0
            for pair, subset in zip(pairs, decoded):
                for index in subset:
                    i, v = pair[index]
                    selected[i] |= 1 << v
                    touched |= 1 << v
            # Products over all tests and variables equal the grouped entries.
            term = 1 << (n - touched.bit_count())
            for table, support in zip(tables, selected):
                term *= table[support]
            total += term
    return total % (1 << p), {"degree_arrays": arrays, "wire_assignments": assignments,
                             "invalid_wire_assignments": invalid}


def check_networks() -> dict:
    cases = [([], 3, 1), ([(0,)], 3, 1), ([()], 3, 1),
             ([(1, 2, 4), (0, 3, 6), (1, 6)], 3, 2),
             ([(1, 2, 4, 8), (3, 12), (0, 5, 10)], 4, 2),
             ([(0, 1, 2, 3, 4, 5, 6, 7), (1, 6)], 3, 3)]
    stats = {"modular_network_counts": 0, "degree_arrays": 0,
             "wire_assignments": 0, "invalid_wire_assignments": 0}
    for polys, n, k in cases:
        expected = sum(all(value(poly, x) == 0 for poly in polys)
                       for x in range(1 << n))
        for p in range(1, n + 2):
            actual, local = grouped_network_count(polys, n, k, p)
            require(actual == expected % (1 << p), "Grouped network contraction")
            stats["modular_network_counts"] += 1
            for key, number in local.items():
                stats[key] += number
    return stats


def multiply_mod_two(left: set[int], right: set[int]) -> set[int]:
    result: set[int] = set()
    for x, y in product(left, right):
        union = x | y
        if union in result:
            result.remove(union)
        else:
            result.add(union)
    return result


def violation_polynomial(clause: tuple[int, ...]) -> tuple[int, ...]:
    polynomial = {0}
    for literal in clause:
        variable = 1 << (abs(literal) - 1)
        polynomial = multiply_mod_two(polynomial, {0, variable} if literal > 0 else {variable})
    return tuple(sorted(polynomial))


def check_cnf_bridge() -> dict:
    n = 3
    clauses = [tuple(sign * (v + 1) for v, sign in enumerate(signs) if sign)
               for signs in product((-1, 0, 1), repeat=n)]
    formulas = [CNF(n, (left, right)) for left, right in product(clauses, repeat=2)]
    formulas += [CNF(0, ()), CNF(0, ((),)), CNF(5, ()), CNF(5, ((1, -1),)),
                 CNF(5, ((1, 1, 2), (-2, -2, -2))), CNF(5, ((), (1,)))]
    for formula in formulas:
        polys = [violation_polynomial(clause) for clause in formula.clauses]
        p = formula.nvars + 1
        actual, _ = incidence_sum([mobius_indicator(poly, formula.nvars) for poly in polys],
                                  formula.nvars, 3, p)
        require(actual == count(formula), "DIMACS-reference CNF bridge")
    return {"exact_cnf_count_comparisons": len(formulas),
            "includes_repeats_tautologies_empty_clauses_unused_and_zero_variables": True}


def check_sharpness_and_support() -> dict:
    sharp = support_cases = support_tuples = 0
    for k, a, p in product(range(1, 4), range(1, 5), range(1, 6)):
        rs = [1] * a
        for j in range(p - 1):
            rs[j % a] += 1
        coefficient = 1
        degree = 0
        for r in rs:
            n = k * r
            # Inclusion/exclusion over all subfamilies at full support: only
            # the full family contributes, since the monomials are disjoint.
            monomials = tuple(((1 << k) - 1) << (k * j) for j in range(r))
            full = (1 << n) - 1
            c = 0
            for word in range(1, 1 << r):
                union = 0
                for j, monomial in enumerate(monomials):
                    if word & (1 << j):
                        union |= monomial
                if union == full:
                    c += (-1) ** word.bit_count() * (1 << (word.bit_count() - 1))
            coefficient *= c
            degree += n
        require(degree == k * (a + p - 1), "Sharp degree")
        require(coefficient % (1 << p) == 1 << (p - 1), "Sharp surviving coefficient")
        sharp += 1
    for n, k, t in [(7, 2, 2), (9, 3, 2), (10, 3, 3), (12, 2, 3)]:
        rows = []
        for i in range(n):
            row = []
            for j in range(t):
                monomial = sum(1 << ((i + k * j + u) % n) for u in range(k))
                row.append(monomial)
            require(sum(s.bit_count() for s in row) == (sum(row)).bit_count(),
                    "Listed monomials not disjoint")
            rows.append(tuple(row))
        require(len(set(tuple(sorted(row)) for row in rows)) == n, "Duplicate cyclic equation")
        require(all(sum(any(mask & (1 << v) for mask in row) for row in rows) == k * t
                    for v in range(n)), "Unequal scope loads")
        for row in rows:
            coefficients = mobius_indicator(row, n)
            require(all(coefficients[m] == -1 for m in row), "Nonunit selected coefficient")
        # Exhaust every one-monomial-per-test tuple in these bounded fixtures.
        all_tuples = set(product(*rows))
        require(len(all_tuples) == t ** n, "Incidence support count")
        support_cases += 1
        support_tuples += len(all_tuples)
    return {"sharp_cutoff_certificates": sharp, "cyclic_nonlinear_fixtures": support_cases,
            "exhausted_unit_coefficient_incidence_monomials": support_tuples}


def source_bindings() -> dict:
    manifest = json.loads((ROOT / "SOURCES.json").read_text())
    hashes = {}
    for item in manifest["files"]:
        digest = sha256((ROOT / item["path"]).read_bytes()).hexdigest()
        require(digest == item["sha256"], "Frozen source drift")
        hashes[item["path"]] = digest
    return {"upstream_commit": manifest["upstream_commit"], "frozen_source_sha256": hashes,
            "proof_sha256": sha256((HERE / "PROOF.md").read_bytes()).hexdigest(),
            "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest()}


def main() -> None:
    report = {"status": "PASS", "scope": "exact finite reference checks; no asymptotic algorithm or independent review",
              "source_bindings": source_bindings(),
              "scalar_lifts": check_all_small_lifts(), "sparse_systems": check_small_systems(),
              "subset_decoder": check_decoder(), "grouped_networks": check_networks(),
              "cnf_bridge": check_cnf_bridge(), "sharpness_and_support": check_sharpness_and_support()}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
