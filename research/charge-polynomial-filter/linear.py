"""Small exact matrix-space classification; no randomized determinant test."""

from fractions import Fraction as F
from functools import reduce
from itertools import permutations
from math import gcd, lcm


def require(condition, message):
    if not condition:
        raise ValueError(message)


def primitive(row):
    common = reduce(gcd, row, 0)
    if not common:
        return list(row)
    first = next(x for x in row if x)
    if first < 0:
        common = -common
    return [x // common for x in row]


def echelon(matrix, columns):
    rows = [primitive(row) for row in matrix]
    require(all(len(row) == columns for row in rows), "Echelon width mismatch")
    names = list(range(len(rows)))
    pivots, selected = [], []
    for j in range(columns):
        rank = len(pivots)
        pivot = next((i for i in range(rank, len(rows)) if rows[i][j]), None)
        if pivot is None:
            continue
        rows[pivot], rows[rank] = rows[rank], rows[pivot]
        names[pivot], names[rank] = names[rank], names[pivot]
        selected.append(names[rank])
        pivots.append(j)
        p = rows[rank][j]
        for i in range(rank + 1, len(rows)):
            a = rows[i][j]
            if a:
                common = gcd(p, a)
                rows[i] = primitive([(p // common) * x - (a // common) * y
                                     for x, y in zip(rows[i], rows[rank])])
    return rows[:len(pivots)], pivots, selected


def nullspace(matrix, columns):
    rows, pivots, _ = echelon(matrix, columns)
    basis = []
    for free in range(columns):
        if free in pivots:
            continue
        vector = [F(0)] * columns
        vector[free] = 1
        for row, pivot in reversed(list(zip(rows, pivots))):
            vector[pivot] = -sum((row[j] * vector[j] for j in range(pivot + 1, columns)), F(0)) / row[pivot]
        denominator = lcm(*(x.denominator for x in vector))
        basis.append(primitive([int(x * denominator) for x in vector]))
    require(len(basis) + len(pivots) == columns, "Nullity count")
    require(all(sum(a * b for a, b in zip(row, vector)) == 0 for row in matrix for vector in basis), "Nullspace reconstruction")
    return basis, len(pivots)


def determinant(matrix):
    n = len(matrix)
    result = F(1)
    rows = [list(map(F, row)) for row in matrix]
    for j in range(n):
        pivot = next((i for i in range(j, n) if rows[i][j]), None)
        if pivot is None:
            return F(0)
        if pivot != j:
            rows[pivot], rows[j] = rows[j], rows[pivot]
            result = -result
        result *= rows[j][j]
        for i in range(j + 1, n):
            scale = rows[i][j] / rows[j][j]
            rows[i] = [x - scale * y for x, y in zip(rows[i], rows[j])]
    return result


def determinant_polynomial(basis, n):
    """Leibniz determinant of sum_j t_j basis[j], used only for n<=4."""
    require(n <= 4, "Registered exact symbolic determinant is limited to N<=4")
    d = len(basis)
    if not d:
        return {}
    answer = {}
    zero = (0,) * d
    for perm in permutations(range(n)):
        sign = (-1) ** sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = {zero: sign}
        for i, k in enumerate(perm):
            updated = {}
            for alpha, coefficient in term.items():
                for j, matrix in enumerate(basis):
                    value = matrix[i * n + k]
                    if value:
                        beta = list(alpha)
                        beta[j] += 1
                        beta = tuple(beta)
                        updated[beta] = updated.get(beta, 0) + coefficient * value
            term = {alpha: x for alpha, x in updated.items() if x}
        for alpha, x in term.items():
            answer[alpha] = answer.get(alpha, 0) + x
    return {alpha: x for alpha, x in answer.items() if x}


def polynomial_value(poly, values):
    total = 0
    for alpha, coefficient in poly.items():
        term = coefficient
        for value, exponent in zip(values, alpha):
            term *= value ** exponent
        total += term
    return total


def grid_witness(poly, variables, degree):
    require(bool(poly), "A zero determinant polynomial has no witness")
    choices = []
    for _ in range(variables):
        for value in range(degree + 1):
            reduced = {}
            for alpha, coefficient in poly.items():
                key = alpha[1:]
                reduced[key] = reduced.get(key, 0) + coefficient * value ** alpha[0]
            reduced = {alpha: x for alpha, x in reduced.items() if x}
            if reduced:
                choices.append(value)
                poly = reduced
                break
        else:
            raise ValueError("Nonzero degree-bounded polynomial vanished on a full grid")
    require(set(poly) == {()}, "Grid witness did not finish specialization")
    return choices, poly[()]
