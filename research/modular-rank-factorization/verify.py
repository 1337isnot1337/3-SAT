"""Exact bounded controls for local-ring factors and precision-safe division."""

from fractions import Fraction as F
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("modular_factors", HERE / "modular.py")
modular = importlib.util.module_from_spec(spec)
spec.loader.exec_module(modular)
require = modular.require


def rational_rank(matrix):
    rows = [list(map(F, row)) for row in matrix]
    rank = 0
    for j in range(len(rows[0])):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][j]), None)
        if pivot is None:
            continue
        rows[pivot], rows[rank] = rows[rank], rows[pivot]
        for i in range(rank + 1, len(rows)):
            coefficient = rows[i][j] / rows[rank][j]
            rows[i] = [x - coefficient * y for x, y in zip(rows[i], rows[rank])]
        rank += 1
    return rank


def check_matrix(matrix, precision):
    answer = modular.factor(matrix, precision)
    modulus = 1 << precision
    require(modular.reconstruct(answer) == [[x % modulus for x in row] for row in matrix], "Full modular factorization")
    require(answer["inner_dimension"] <= rational_rank(matrix), "Rational rank bound")
    require(answer["pivot_valuations"] == sorted(answer["pivot_valuations"]), "Smith valuation order")
    require(all(0 <= x < modulus for row in answer["left"] + answer["right"] for x in row), "Bounded factor height")
    return answer


def main():
    counts = {"two_by_two": 0, "binary_three_by_three": 0, "structured_rectangular": 0,
              "division_cases": 0, "nested_division_cases": 0, "inverse_valuation_controls": 0}
    for entries in product(range(-2, 3), repeat=4):
        matrix = [list(entries[:2]), list(entries[2:])]
        for precision in range(1, 9):
            check_matrix(matrix, precision)
            counts["two_by_two"] += 1
    for entries in product(range(2), repeat=9):
        matrix = [list(entries[j:j + 3]) for j in range(0, 9, 3)]
        for precision in range(1, 7):
            check_matrix(matrix, precision)
            counts["binary_three_by_three"] += 1
    # Deterministic rectangular low-rank products at varied valuations.
    for m, n, r in [(3, 5, 1), (5, 3, 2), (6, 7, 3), (9, 8, 4)]:
        for parameter in range(12):
            left = [[((i + 1) ** (j + 1) - parameter) * 2 ** ((i + j + parameter) % 5)
                     for j in range(r)] for i in range(m)]
            right = [[((j + 2) ** (i + 1) + parameter) * 2 ** ((i + 2 * j + parameter) % 4)
                      for j in range(n)] for i in range(r)]
            matrix = [[sum(a * right[k][j] for k, a in enumerate(row)) for j in range(n)] for row in left]
            for precision in [1, 2, 5, 12, 24]:
                answer = check_matrix(matrix, precision)
                require(answer["inner_dimension"] <= r, "Constructed rank ceiling")
                counts["structured_rectangular"] += 1
    for b in range(1, 9):
        for multiplier in range(1, 65):
            v = modular.valuation(multiplier, 100)
            for z in range(-19, 20):
                residue = multiplier * z % (1 << (b + v))
                require(modular.exact_division_residue(residue, multiplier, b) == z % (1 << b), "Precision-safe division")
                counts["division_cases"] += 1
    for b in range(1, 7):
        for multipliers in product([2, 3, 6, 8], repeat=3):
            for z in range(-8, 9):
                precision = b + sum(modular.valuation(d, 100) for d in multipliers)
                value = z
                for d in multipliers:
                    value *= d
                value %= 1 << precision
                for d in reversed(multipliers):
                    precision -= modular.valuation(d, 100)
                    value = modular.exact_division_residue(value, d, precision)
                require(value == z % (1 << b), "Nested division precision")
                counts["nested_division_cases"] += 1
    zero_divisor = check_matrix([[2, 0], [0, 2]], 2)
    require(zero_divisor["inner_dimension"] == 2, "Binary rank is not modular inner rank")
    require(rational_rank([[x % 2 for x in row] for row in [[2, 0], [0, 2]]]) == 0, "Binary-rank negative control")
    require((2 * 0) % 8 == (2 * 4) % 8 and 0 % 8 != 4 % 8, "Missing precision-bit collision")
    # Freezing a factor at its creation precision is essential when lifting.
    created, larger = 3, 6
    left, right = 7, 7
    require((left * right) % (1 << created) == 1, "Creation identity")
    require((left * right) % (1 << larger) != 1, "Creation identity must not be silently promoted")
    for H in range(1, 17):
        inverse = [[F(1, 2 ** (j - i + 1)) if j >= i else F(0) for j in range(H)] for i in range(H)]
        require(all(2 * inverse[i][j] - (inverse[i + 1][j] if i + 1 < H else 0) == int(i == j)
                    for i in range(H) for j in range(H)), "Bidiagonal inverse identity")
        require(inverse[0][-1].denominator == 2 ** H, "Exponential inverse-normalizer valuation")
        counts["inverse_valuation_controls"] += 1
    print(json.dumps({"status": "PASS", "scope": "bounded exact modular matrix and precision controls",
                      "counts": counts,
                      "negative_controls": ["rank over F2 loses nonzero torsion factors",
                                            "division without valuation precision is ambiguous",
                                            "creation identities cannot be promoted to higher precision",
                                            "generic inverse normalization can require exponential precision"],
                      "bindings": {name: sha256((HERE / name).read_bytes()).hexdigest()
                                   for name in ["modular.py", "verify.py", "PROOF.md"]}}, indent=2))


if __name__ == "__main__":
    main()
