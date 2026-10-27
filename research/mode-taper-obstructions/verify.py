#!/usr/bin/env python3
"""Exact checks for the scoped Appendix D bottleneck analysis; standard library only."""

from fractions import Fraction as F
from itertools import combinations
from math import ceil, isqrt
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def valuation(x):
    x = F(x)
    require(x != 0, "valuation of zero")
    def integer_v2(n):
        n = abs(n)
        return (n & -n).bit_length() - 1
    return integer_v2(x.numerator) - integer_v2(x.denominator)


def determinant(matrix):
    a = [[F(x) for x in row] for row in matrix]
    result = F(1)
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return F(0)
        if pivot != j:
            a[pivot], a[j] = a[j], a[pivot]
            result = -result
        entry = a[j][j]
        result *= entry
        for i in range(j + 1, len(a)):
            ratio = a[i][j] / entry
            for k in range(j + 1, len(a)):
                a[i][k] -= ratio * a[j][k]
            a[i][j] = F(0)
    return result


def check_cauchy():
    checked = 0
    for d in range(1, 8):
        expected = [4 * j - 2 * j.bit_count() for j in range(d)]
        for c in (1, 3, 7):
            a = [[F(1, c + 2 * (i - j)) for j in range(d)] for i in range(d)]
            previous = 0
            for k in range(1, d + 1):
                minimum = None
                for rows in combinations(range(d), k):
                    for columns in combinations(range(d), k):
                        minor = determinant([[a[i][j] for j in columns] for i in rows])
                        require(minor != 0, "Cauchy minor vanished")
                        v = valuation(minor)
                        minimum = v if minimum is None else min(minimum, v)
                        checked += 1
                require(minimum - previous == expected[k - 1], "Smith valuation mismatch")
                previous = minimum
    require(4 * 4 - 2 * (4).bit_count() < 4**2,
            "control: a putative quadratic valuation bound must fail")
    return {"all_minors_checked": checked, "dimensions": [1, 7], "odd_shifts": [1, 3, 7]}


def taper_matrix(u, a):
    return [[sum((F(j, 2**j) for j in range(1, a - i + 1)), F(0))
             if i == k else -F(k - i, 2**(k - i)) if k > i else F(0)
             for k in range(u)] for i in range(u)]


def check_taper():
    rows = []
    for u in (1, 2, 3, 4, 8, 16, 32, 64):
        b = taper_matrix(u, 2 * u)
        w = [F(1, 2**i) for i in range(u)]
        v = [F(0)] * u
        for i in reversed(range(u)):
            v[i] = (1 - sum((b[i][j] * v[j] for j in range(i + 1, u)), F(0))) / b[i][i]
        y = [F(0)] * u
        for i in range(u):
            y[i] = (w[i] - sum((b[j][i] * y[j] for j in range(i)), F(0))) / b[i][i]
        require(all(x > 0 for x in v + y), "nonpositive primal/dual certificate")
        require(all(sum((b[i][j] * v[j] for j in range(u)), F(0)) == 1
                    for i in range(u)), "primal residual")
        require(all(sum((b[j][i] * y[j] for j in range(u)), F(0)) == w[i]
                    for i in range(u)), "dual residual")
        normalizer = sum((w[i] * v[i] for i in range(u)), F(0))
        require(normalizer == sum(y), "primal/dual objective mismatch")
        optimum = 1 / normalizer
        require(optimum >= F(1, 4 * u), "proved taper floor violated")
        rows.append({"u": u, "a": 2 * u, "u_times_optimum_W1": float(u * optimum)})
        # Independently check the infinite-grid closed form by convolution.
        vinf = [F(k, 6) + F(5, 18) + F(2, 9 * 4**k) for k in range(1, u + 1)]
        for k in range(1, u + 1):
            require(2 * vinf[k - 1] - sum((F(j, 2**j) * vinf[k - j - 1]
                    for j in range(1, k)), F(0)) == 1, "infinite-grid residual")
        require(sum((F(1, 2**i) * vinf[u - i - 1] for i in range(u)), F(0))
                == F(u, 3) + F(2, 9) - F(2, 9 * 4**u), "closed normalizer mismatch")
    return {"exact_primal_dual_certificates": len(rows), "samples": rows}


def check_modes():
    checks = 0
    smallest = None
    for u in (1, 2, 4, 8, 16, 32, 64, 128):
        a = max(16, 2 * u)
        L = 2**a
        v = isqrt(u) + (isqrt(u)**2 != u)
        for i in range(u):
            D = L // 2**i
            h = a + 1 - i
            require(D >= max(16 * v, 8 * v * h), "mode lemma side condition")
            q = D // (8 * v)
            for packets in (1, 3):
                M = packets * L
                tiles = packets * 2**(i + 1)
                count = tiles * q
                # Exact sum of the strengthened weights h, ..., h+q-1.
                total_weight = tiles * (q * h + q * (q - 1) // 2)
                require(count >= F(M, 8 * v), "entropy lower bound failed")
                require(total_weight <= F(M * D, 16 * u), "weight budget failed")
                require(count <= M and 2**(i + 1) * q <= L, "degree cap failed")
                require(2**i * q <= L // 2, "per-target row cap failed")
                require(q <= D // 2, "more moments than columns")
                source_precision_increment = 8 * ceil(F(3 * M, u)) * D + 8 * M * (a + 1)
                require(total_weight < source_precision_increment, "not admitted by source budget")
                checks += 1
                if smallest is None:
                    smallest = {"u": u, "a": a, "i": i, "packets": packets,
                                "M": M, "independent_binary_choices": count,
                                "maximum_total_weight": total_weight,
                                "admitted_tuples": f"2^{count}"}
    # Explicitly enumerate a small subfamily, separately from the all-on bound.
    u, a, i = 1, 8, 0
    L, D, h = 2**a, 2**a, a + 1 - i
    # A smaller eight-variable subfamily makes complete enumeration practical.
    weights = [h + b for tile in range(2) for b in range(4)]
    explicit = 0
    for mask in range(1 << len(weights)):
        weight = sum(w for j, w in enumerate(weights) if mask >> j & 1)
        require(weight < 8 * ceil(F(3 * L, u)) * D,
                "explicit tuple rejected")
        require(mask.bit_count() <= L, "explicit degree cap failed")
        explicit += 1
    return {"parameter_cases": checks, "explicit_tuples": explicit, "smallest_witness": smallest}


if __name__ == "__main__":
    result = {"status": "PASS", "scope": "finite exact checks of three scoped lemmas; no improved SAT exponent",
              "cauchy": check_cauchy(), "taper": check_taper(), "modes": check_modes()}
    print(json.dumps(result, indent=2))
