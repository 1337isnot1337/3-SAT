"""Exact bounded checks for the two-scale grid and its local Smith spectrum.

All Cauchy minors in the registered domain are evaluated by a direct
fraction-free determinant after clearing odd row denominators. Complete
shifted kernel polynomials are expanded separately over a common denominator.
No new contraction algorithm or asymptotic improvement is verified here.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from math import factorial, prod
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def v2(number: int) -> int:
    require(number != 0, "No finite zero valuation")
    number = abs(number)
    return (number & -number).bit_length() - 1


def determinant(matrix: list[list[int]]) -> int:
    matrix = [list(row) for row in matrix]
    n = len(matrix)
    if not n:
        return 1
    previous = 1
    sign = 1
    for k in range(n - 1):
        if matrix[k][k] == 0:
            pivot = next((i for i in range(k + 1, n) if matrix[i][k]), None)
            if pivot is None:
                return 0
            matrix[k], matrix[pivot] = matrix[pivot], matrix[k]
            sign *= -1
        pivot = matrix[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = matrix[i][j] * pivot - matrix[i][k] * matrix[k][j]
                value, remainder = divmod(numerator, previous)
                require(remainder == 0, "Nonexact Bareiss division")
                matrix[i][j] = value
            matrix[i][k] = 0
        previous = pivot
    return sign * matrix[-1][-1]


def cauchy_minor_valuation(positions: list[int], rows: tuple[int, ...],
                           columns: tuple[int, ...], c: int) -> int:
    cleared = []
    for row in rows:
        denominators = [c + 2 * (positions[row] - positions[column]) for column in columns]
        require(all(d % 2 for d in denominators), "Nonunit Cauchy denominator")
        common = prod(denominators)
        cleared.append([common // denominator for denominator in denominators])
    det = determinant(cleared)
    require(det != 0, "Unexpected zero Cauchy minor")
    return v2(det)


def check_minors(positions: list[int], r: int, b: int, c: int) -> dict:
    n = len(positions)
    d = 1 << r
    predicted = [4 * j - 2 * j.bit_count() + 2 * (b - r) * (j // d) for j in range(n)]
    minima = [0]
    count = 0
    for k in range(1, n + 1):
        minimum = None
        subsets = list(combinations(range(n), k))
        vandermonde = {subset: sum(v2(positions[j] - positions[i])
                                  for i, j in combinations(subset, 2)) for subset in subsets}
        for rows in subsets:
            for columns in subsets:
                actual = cauchy_minor_valuation(positions, rows, columns, c)
                expected = k * (k - 1) + vandermonde[rows] + vandermonde[columns]
                require(actual == expected, "Cauchy minor valuation formula")
                minimum = actual if minimum is None else min(minimum, actual)
                count += 1
        minima.append(minimum)
        require(minimum == sum(predicted[:k]), "Minimum determinantal divisor")
    smith = [minima[j + 1] - minima[j] for j in range(n)]
    require(smith == predicted, "Exact local Smith spectrum")
    return {"odd_c": c, "direct_minor_determinants": count, "smith_valuations": smith}


def shifted_kernel_numerator(grid: list[int], omitted: int, node: int, alpha: int) -> list[int]:
    polynomial = [1]
    for root in grid:
        if root == omitted:
            continue
        updated = [0] * (len(polynomial) + 1)
        for j, coefficient in enumerate(polynomial):
            updated[j] += (node - root) * coefficient
            updated[j + 1] += alpha * coefficient
        polynomial = updated
    return polynomial


def check_grid(r: int, t: int, b: int) -> dict:
    d, H, B = 1 << r, 1 << t, 1 << b
    positions = [low + B * high for high in range(H) for low in range(d)]
    grid_pairs = [(low, high) for high in range(-H, H) for low in range(-d, d)]
    grid = [low + B * high for low, high in grid_pairs]
    require(len(set(grid)) == 4 * len(positions), "Grid cardinality")
    differences = {y - x for x in positions for y in positions}
    require(differences.issubset(grid), "Missing port difference")
    derivative_at_zero = prod(-s for s in grid if s)
    expected = 2 * H * v2(factorial(2 * d - 1)) + (2 * H - 1) * b + v2(factorial(2 * H - 1))
    require(v2(derivative_at_zero) == expected, "Origin derivative valuation")
    alpha_exp = b + t + 1
    alpha = 1 << alpha_exp
    for node in grid:
        derivative = prod(node - s for s in grid if node != s)
        require(v2(derivative) == expected, "Nonuniform derivative valuation")
        require(Fraction(derivative, derivative_at_zero).numerator % 2 == 1,
                "Nonunit surviving node scalar")
    selected_differences = sorted({-B, -1, 0, 1, B, B + 1} & differences)
    expanded = coefficient_checks = 0
    for node in grid:
        for omitted in selected_differences:
            polynomial = shifted_kernel_numerator(grid, omitted, node, alpha)
            actual = min(v2(c) - expected for c in polynomial if c)
            content = 0 if node == omitted else alpha_exp - v2(node - omitted)
            require(actual == content and actual >= 0, "Shifted kernel content")
            if node == omitted:
                require(polynomial[0] != 0, "Missing matching node value")
            else:
                require(polynomial[0] == 0, "Nonzero offshift node value")
                require(v2(polynomial[1]) - expected == content, "Linear content witness")
            expanded += 1
            coefficient_checks += len(polynomial)
    matching_pairs = dummy_nodes = 0
    for node, (low, high) in zip(grid, grid_pairs):
        matched = [(i, j) for i, x in enumerate(positions) for j, y in enumerate(positions)
                   if y - x == node]
        if low == -d or high == -H:
            require(not matched, "Dummy node has a real port match")
            dummy_nodes += 1
        if node == 0 or not matched:
            continue
        coordinate = v2(low) if low else r + v2(high)
        require(coordinate < r + t, "Localization needs a nonexistent bit")
        require(all(((i >> coordinate) ^ (j >> coordinate)) & 1 for i, j in matched),
                "A real shifted match fails to flip the localization bit")
        matching_pairs += len(matched)
    spectra = [check_minors(positions, r, b, c) for c in [1, 3]]
    return {"d": d, "H": H, "b": b, "slots": len(positions), "grid_nodes": len(grid),
            "alpha_exponent": alpha_exp, "derivative_valuation": expected,
            "expanded_shifted_kernels": expanded, "checked_integer_coefficients": coefficient_checks,
            "selected_real_differences": selected_differences,
            "localized_real_matches": matching_pairs, "zero_matrix_dummy_nodes": dummy_nodes,
            "local_spectra": spectra}


def loss_matrix(r: int, t: int, b: int) -> tuple[list[list[Fraction]], list[Fraction], list[Fraction]]:
    d, H, gap = 1 << r, 1 << t, b - r
    size = r + t + 2
    A = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    K, weights = [], []
    for i in range(r + 1):
        D = d >> i
        A[i][i] = Fraction(2 * H * (2 * D + gap - 1) - 1)
        for k in range(i + 1, r + 1):
            A[i][k] = Fraction(-2 * H * (d >> k) * (k - i))
        for j in range(t + 1):
            A[i][r + 1 + j] = Fraction(-(H >> j) * (b + j - i))
        K.append(Fraction(2 * H * (D + gap)))
        weights.append(Fraction(2, 1 << i))
    for j in range(t + 1):
        row = r + 1 + j
        E = H >> j
        A[row][row] = Fraction(2 * E - 1)
        for k in range(j + 1, t + 1):
            A[row][r + 1 + k] = Fraction(-(H >> k) * (k - j))
        K.append(Fraction(2 * E))
        weights.append(Fraction(1, d * (1 << j)))
    return A, K, weights


def upper_solve(A: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction]:
    answer = [Fraction(0)] * len(rhs)
    for i in reversed(range(len(rhs))):
        answer[i] = (rhs[i] - sum((A[i][j] * answer[j] for j in range(i + 1, len(rhs))),
                                 Fraction(0))) / A[i][i]
    return answer


def transpose_solve(A: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction]:
    answer = [Fraction(0)] * len(rhs)
    for i in range(len(rhs)):
        answer[i] = (rhs[i] - sum((A[j][i] * answer[j] for j in range(i)),
                                 Fraction(0))) / A[i][i]
    return answer


def apply_matrix(A: list[list[Fraction]], x: list[Fraction]) -> list[Fraction]:
    return [sum((a * b for a, b in zip(row, x)), Fraction(0)) for row in A]


def product_grid(r: int, t: int, b: int) -> list[tuple[int, int]]:
    d, H, B = 1 << r, 1 << t, 1 << b
    return [(low + B * high, v2(low) if low else r + 1 + v2(high))
            for high in range(-H, H) for low in range(-d, d) if low or high]


def check_loss_program() -> dict:
    certificates = direct_rows = limit_checks = 0
    profiles = []
    for r in range(1, 11):
        for t in range(1, 11):
            for b in sorted({r + 2, r + 5, r + (1 << r), r + (1 << (2 * r))}):
                d, H, L = 1 << r, 1 << t, 1 << (r + t)
                A, K, weights = loss_matrix(r, t, b)
                v = upper_solve(A, K)
                y = transpose_solve(A, weights)
                require(all(x > 0 for x in v + y), "Nonpositive primal/dual")
                require(apply_matrix(A, v) == K, "Primal residual")
                Z = sum((a * x for a, x in zip(weights, v)), Fraction(0))
                require(Z == sum((a * x for a, x in zip(y, K)), Fraction(0)), "Dual objective")
                require(sum(weights) == Fraction(4 * L - 1, L), "Full-grid mass")
                phi = ([Fraction(2 * (r - i + t + 2)) for i in range(r + 1)]
                       + [Fraction(2 * (t - j + 1)) for j in range(t + 1)])
                require(all(a >= k for a, k in zip(apply_matrix(A, phi), K)), "Gap-independent supersolution")
                require(all(x <= z for x, z in zip(v, phi)), "Inverse comparison")
                require(Z < 10 * (r + t + 2), "Gap-independent normalizer")
                for i, row in enumerate(A):
                    require(-sum(row[i + 1:], Fraction(0)) <= 4 * K[i], "Rounding loss bound")
                    correction = (b + t + 1 - i if i <= r else
                                  t + 1 - (i - r - 1))
                    require(correction <= K[i], "Highest-jet correction")
                At = sum((v[r + 1 + j] / (2 * (1 << j)) for j in range(t + 1)), Fraction(0))
                limiting_v = [1 + At] * (r + 1) + v[r + 1:]
                require(all(2 * H * limiting_v[i] - sum(
                    (Fraction(H >> j) * limiting_v[r + 1 + j] for j in range(t + 1)), Fraction(0))
                            == 2 * H for i in range(r + 1)), "Large-gap leading equations")
                limit_Z = sum((w * x for w, x in zip(weights, limiting_v)), Fraction(0))
                require(limit_Z == 4 - Fraction(2, d) + 4 * At, "Exact large-gap limit")
                limit_checks += 1
                if r == t and r in [1, 2, 4, 8] and b in [r + 2, r + (1 << (2 * r))]:
                    profiles.append({"r": r, "t": t, "b": b,
                                     "exact_normalizer": str(Z), "large_gap_limit": str(limit_Z)})
                if r <= 2 and t <= 2 and b in [r + 2, r + 5]:
                    nodes = product_grid(r, t, b)
                    alpha_val = b + t + 1
                    for node, row in nodes:
                        for column in range(len(A)):
                            direct = sum((alpha_val if node == root else v2(node - root)) - v2(root)
                                         for root, root_class in nodes if root_class == column)
                            require(direct == A[row][column], "Full-node loss matrix count")
                            direct_rows += 1
                certificates += 1
    return {"exact_primal_dual_certificates": certificates,
            "independent_full_node_matrix_entries": direct_rows,
            "large_gap_leading_system_checks": limit_checks, "profiles": profiles,
            "coverage": "r,t=1..10; b in {r+2,r+5,r+2^r,r+2^(2r)}, deduplicated"}


def check_generic_gap_witnesses() -> dict:
    expanded = coefficient_checks = 0
    witnesses = []
    r = t = 1
    for b in [3, 6]:
        d, H, L = 2, 2, 4
        a = r + t
        M = 160 * (a + 2)
        lam = Fraction(M, 20 * (a + 2))
        A, K, weights = loss_matrix(r, t, b)
        v = upper_solve(A, K)
        q = [-(-(lam * x).numerator // (lam * x).denominator) for x in v]
        P = apply_matrix(A, list(map(Fraction, q)))
        require(all(p >= Fraction(M, 40 * (a + 2)) * k for p, k in zip(P, K)),
                "Rounded generic witness precision")
        nodes = product_grid(r, t, b)
        degree = sum(q[cls] for _, cls in nodes)
        require(degree < L * (Fraction(M, 2) + 4) <= M * (4 * L - 1), "Generic witness degree")
        denominator = prod((-root) ** q[cls] for root, cls in nodes)
        alpha = 1 << (b + t + 1)
        for node, cls in nodes + [(0, -1)]:
            polynomial = [1]
            for root, root_class in nodes:
                for _ in range(q[root_class]):
                    updated = [0] * (len(polynomial) + 1)
                    for j, coefficient in enumerate(polynomial):
                        updated[j] += (node - root) * coefficient
                        updated[j + 1] += alpha * coefficient
                    polynomial = updated
            expected = P[cls] if node else Fraction(0)
            actual = min(v2(c) - v2(denominator) for c in polynomial if c)
            require(actual == expected and actual >= 0, "Expanded generic witness chart")
            if node:
                threshold = (M * K[cls].numerator) // (40 * (a + 2) * K[cls].denominator)
                require(all(not c or v2(c) - v2(denominator) >= threshold for c in polynomial),
                        "Complete generic witness jet does not vanish")
            else:
                require(polynomial[0] == denominator, "Generic witness origin value")
            expanded += 1
            coefficient_checks += len(polynomial)
        witnesses.append({"r": r, "t": t, "b": b, "M": M, "degree": degree,
                          "multiplicities": q, "node_class_contents": list(map(str, P))})
    return {"witnesses": witnesses, "complete_chart_expansions": expanded,
            "expanded_integer_coefficients": coefficient_checks}


def main() -> None:
    fixtures = [check_grid(r, t, b) for r, t in [(1, 1), (1, 2), (2, 1)]
                for b in [r + 2, r + 5]]
    manifest = json.loads((ROOT / "SOURCES.json").read_text())
    source_hashes = {}
    for item in manifest["files"]:
        digest = sha256((ROOT / item["path"]).read_bytes()).hexdigest()
        require(digest == item["sha256"], "Frozen source drift")
        source_hashes[item["path"]] = digest
    report = {"status": "PASS", "scope": "exact finite checks of a changed grid and local spectrum; no full algorithm",
              "parameter_fixtures": fixtures,
              "total_direct_minor_determinants": sum(s["direct_minor_determinants"]
                  for fixture in fixtures for s in fixture["local_spectra"]),
              "total_complete_shifted_kernels": sum(f["expanded_shifted_kernels"] for f in fixtures),
              "total_expanded_integer_coefficients": sum(f["checked_integer_coefficients"] for f in fixtures),
              "nodewise_loss_program": check_loss_program(),
              "generic_gap_precision_witnesses": check_generic_gap_witnesses(),
              "bindings": {"base_commit": json.loads((HERE / "CLAIM.json").read_text())["base_commit"],
                           "upstream_commit": manifest["upstream_commit"], "frozen_source_sha256": source_hashes,
                           "proof_sha256": sha256((HERE / "PROOF.md").read_bytes()).hexdigest(),
                           "loss_model_proof_sha256": sha256((HERE / "LOSS-MODEL.md").read_bytes()).hexdigest(),
                           "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest()}}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
