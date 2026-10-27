"""Uniform quadratic normalizer and bounded actual crossing-piece checks."""
from fractions import Fraction as F
from math import factorial

import charged
import second


def identity(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def matmul(left, right):
    return [[sum((left[i][k] * right[k][j] for k in range(len(right))), F(0))
             for j in range(len(right[0]))] for i in range(len(left))]


def matadd(left, right, scale=F(1)):
    return [[left[i][j] + scale * right[i][j] for j in range(len(left[0]))]
            for i in range(len(left))]


def matscale(matrix, scale):
    return [[scale * entry for entry in row] for row in matrix]


def normalizer_inverse(u, h):
    """Inverse of I-4h^2U_h from its proved spectral decomposition."""
    n = len(u)
    eye = identity(n)
    scale = 4 * h * h
    if h == 1:
        return matscale(eye, F(-1, 3))
    if h == 2:
        # U_2^2=U_2 and (I-16U_2)^-1=I-16U_2/15.
        return matadd(eye, u, F(-16, 15))
    a = F(h - 2, h)
    u2 = matmul(u, u)
    p0 = matscale(matadd(matadd(u2, u, a - 1), eye, -a), F(-1, a))
    p1 = matscale(matadd(u2, u, a), F(1, 1 + a))
    pminus = matscale(matadd(u2, u, -1), F(1, a * (a + 1)))
    answer = matadd(p0, p1, F(1, 1 - scale))
    return matadd(answer, pminus, F(1, 1 + scale * a))


def generic_inverse(matrix):
    """Independent exact Gauss-Jordan inverse for bounded controls."""
    n = len(matrix)
    work = [list(row) + list(eye) for row, eye in zip(matrix, identity(n))]
    for column in range(n):
        pivot = next((row for row in range(column, n) if work[row][column]), None)
        if pivot is None:
            raise ValueError("singular matrix")
        work[column], work[pivot] = work[pivot], work[column]
        scale = work[column][column]
        work[column] = [entry / scale for entry in work[column]]
        for row in range(n):
            if row == column:
                continue
            scale = work[row][column]
            if scale:
                work[row] = [work[row][j] - scale * work[column][j]
                             for j in range(2 * n)]
    return [row[n:] for row in work]


def crossing_pieces(h):
    """Build normalized uncharged pieces and the actual quadratic filter."""
    states = charged.partitions(h)
    size = len(states)
    u = second.normalized_pairing(states)
    normalizer = matadd(identity(size), u, -4 * h * h)
    inverse = normalizer_inverse(u, h)
    scale = F(1, factorial(h))
    source = {}
    filtered = {}
    for shift in range(-2 * h, 2 * h + 1):
        if abs(shift) == 1:
            continue
        weight = 1 - shift * shift
        for x in range(size):
            for y, argument in enumerate(states):
                for v in range(size):
                    vector = charged.piece_vector(states[x], states[v], argument,
                                                  shift, 0)
                    for output, coefficient in vector:
                        z = states.index(output)
                        key = (x, y, z, v)
                        source[(shift, key)] = source.get((shift, key), F(0)) + scale * coefficient
        for x in range(size):
            for y in range(size):
                for z in range(size):
                    for v in range(size):
                        value = sum((inverse[x][a] * source.get((shift, (a, y, z, v)), F(0))
                                     for a in range(size)), F(0))
                        value *= weight
                        if value:
                            filtered[(shift, (x, y, z, v))] = value
    return states, source, filtered


def crossing_defect(states, pieces):
    size = len(states)
    defect = {}
    for (shift, (x, y, z, v)), value in pieces.items():
        key = (x, y, z, v)
        defect[key] = defect.get(key, F(0)) + value
    for key, value in defect.items():
        x, y, z, v = key
        expected = int(x == v and y == z)
        if value != expected:
            return False
    for x in range(size):
        for y in range(size):
            if (x, y, y, x) not in defect:
                return False
    return True
