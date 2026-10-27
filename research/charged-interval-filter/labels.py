"""Fixed-length invariant labels and the central polynomial filter."""
from fractions import Fraction as F
from math import factorial

import charged
import left
import pairing
import predecessor


def require(condition, message):
    if not condition:
        raise ValueError(message)


def invariant_basis(weight, length):
    """Deterministic monomial projection basis for ker L at fixed length."""
    states = [state for state in charged.partitions(weight)
              if len(state) == length]
    basis = []
    vectors = []
    for state in states:
        polynomial = {state: F(1)}
        derivative = pairing.L(polynomial)
        kernel = pairing.add(
            polynomial,
            pairing.L_right_inverse(derivative) if derivative else {}, -1)
        require(pairing.L(kernel) == {}, "kernel projection")
        candidate = [kernel.get(other, F(0)) for other in states]
        rank = predecessor.exact_rank(vectors + [candidate])
        if rank > len(vectors):
            basis.append(kernel)
            vectors.append(candidate)
    if weight >= 2:
        lower = [state for state in charged.partitions(weight - 1)
                 if len(state) == length]
        require(len(basis) == len(states) - len(lower), "fixed-length kernel dimension")
    return basis


def choose_labels(dimension):
    """Least grade whose fixed-length first-moment rank fits dimension."""
    h = 3
    while True:
        for length in range(1, h):
            basis = invariant_basis(h - 1, length)
            if len(basis) >= dimension:
                selected = basis[:dimension]
                columns = [pairing.L_right_inverse(kappa) for kappa in selected]
                rows = [pairing.P(kappa) for kappa in selected]
                minor = [[F(factorial(h)) * sum(
                    (rows[a].get(state, F(0))
                     * pairing.T(columns[b]).get(state, F(0))
                     for state in rows[a]), F(0))
                          for b in range(dimension)] for a in range(dimension)]
                require(len(rows[0]) == 0 or all(
                    len(state) == len(next(iter(rows[0]))) for state in rows[0]),
                    "fixed row length")
                left_labels = [left.freeze_label({
                    state: coefficient / pairing.multiplicity_factorial(state)
                    for state, coefficient in row.items()}) for row in rows]
                right_labels = [left.freeze_label({
                    state: coefficient * pairing.multiplicity_factorial(state)
                    for state, coefficient in column.items()}) for column in columns]
                return h, left_labels, right_labels, minor
        h += 1


def filter_coefficients(k):
    """Integer coefficients of w(s)=s prod_(r=1)^(k-1)(s^2-r^2)."""
    require(k >= 1, "positive filter cutoff")
    polynomial = {1: F(1)}
    for r in range(1, k):
        updated = {}
        for degree, coefficient in polynomial.items():
            updated[degree] = updated.get(degree, F(0)) - coefficient * r * r
            updated[degree + 2] = updated.get(degree + 2, F(0)) + coefficient
        polynomial = updated
    return tuple(polynomial.get(j, F(0)) for j in range(2 * k))


def filter_value(coefficients, shift):
    return sum((coefficient * shift ** j
                for j, coefficient in enumerate(coefficients)), F(0))


def recovery_scale(h, coefficients):
    """Nonzero c_1 sum_s s*w(s), with every summand of one sign."""
    k = (len(coefficients)) // 2
    weighted = sum((shift * filter_value(coefficients, shift)
                    for shift in range(-2 * h, 2 * h + 1)), F(0))
    require(weighted > 0, "positive weighted first-moment scale")
    require(coefficients[1] != 0, "nonzero linear filter coefficient")
    return coefficients[1] * weighted


def flatten(states, pieces, shifts, direction):
    """Flatten a sparse tensor on (shift,x,y)|(u,v) or (shift,x,u)|(y,v)."""
    n = len(states)
    if direction == "row":
        rows = [(shift, x, y) for shift in shifts
                for x in range(n) for y in range(n)]
        columns = [(u, v) for u in range(n) for v in range(n)]
    else:
        rows = [(shift, x, u) for shift in shifts
                for x in range(n) for u in range(n)]
        columns = [(y, v) for y in range(n) for v in range(n)]
    matrix = []
    for first, second in columns:
        row = []
        for shift, x, other in rows:
            if direction == "row":
                # columns=(u,v), rows=(shift,x,y)
                key = (shift, x, other, first, second)
            else:
                # columns=(y,v), rows=(shift,x,u)
                key = (shift, x, first, other, second)
            row.append(pieces.get(key, F(0)))
        matrix.append(row)
    return matrix


def source_term_bound(h, shift, direction):
    if direction == "row":
        return sum(len(charged.partitions(shift + i)) for i in range(2 * h + 1))
    return sum(len(charged.partitions(2 * h - shift - i))
               for i in range(2 * h + 1))
