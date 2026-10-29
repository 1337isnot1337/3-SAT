"""Exact left-charged operators and polynomial shift projection.

Only the dual/a side receives the zero-mode charge.  The operator/b side
is the original zero-charge module.  All arithmetic is exact.
"""
from functools import lru_cache
from fractions import Fraction as F

import charged
from predecessor import add_scaled, dual_scale, freeze


@lru_cache(maxsize=200_000)
def piece_vector(x, v, argument, shift, charge, reverse=False):
    """Q_shift^(q)(a_x,b_v)t^argument with charge only on the a side."""
    h = sum(x)
    if sum(v) != h:
        raise ValueError("inconsistent label grades")
    result = {}
    for i in range(2 * h + 1):
        scale = (-1) ** i * dual_scale(v)
        if reverse:
            first = charged.dual_operator(x, i, shift - h + i, argument, charge)
            for intermediate, value in first:
                add_scaled(result,
                           charged.operator(v, h - shift - i, intermediate, 0),
                           scale * value)
        else:
            first = charged.operator(v, h - shift - i, argument, charge=0)
            for intermediate, value in first:
                add_scaled(result,
                           charged.dual_operator(x, i, shift - h + i,
                                                 intermediate, charge),
                           scale * value)
    return freeze(result)


def moment(x, v, argument, degree, charge):
    bound = sum(argument) + sum(x)
    result = {}
    for shift in range(-bound, bound + 1):
        add_scaled(result, piece_vector(x, v, argument, shift, charge),
                   shift ** degree)
    return freeze(result)


def inverse(matrix):
    """Small exact Gauss-Jordan inverse used for Vandermonde controls."""
    n = len(matrix)
    work = [[F(matrix[i][j]) for j in range(n)]
            + [F(i == j) for j in range(n)] for i in range(n)]
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


@lru_cache(maxsize=100)
def vandermonde_inverse(degree):
    return tuple(tuple(row) for row in inverse(
        [[F(q) ** j for j in range(degree + 1)] for q in range(degree + 1)]))


def charge_coefficients(evaluate, degree):
    """Return q^0,...,q^degree coefficients of an integer-charge vector."""
    samples = [dict(evaluate(q)) for q in range(degree + 1)]
    transform = vandermonde_inverse(degree)
    answer = [{} for _ in range(degree + 1)]
    for j in range(degree + 1):
        for q in range(degree + 1):
            scale = transform[j][q]
            if scale:
                add_scaled(answer[j], tuple(samples[q].items()), scale)
    return tuple(freeze(poly) for poly in answer)


def highest_charge_moment(x, v, argument, degree):
    """The coefficient [q^degree] of the degree-th shift moment."""
    coefficients = charge_coefficients(
        lambda q: moment(x, v, argument, degree, q), max(degree, len(x)))
    return coefficients[degree]


def freeze_label(label):
    return tuple(sorted((partition, F(coefficient))
                        for partition, coefficient in label.items() if coefficient))


@lru_cache(maxsize=200_000)
def label_piece_vector(left, right, argument, shift, charge):
    """Bilinear extension to frozen partition-label linear combinations."""
    result = {}
    for x, left_scale in left:
        for v, right_scale in right:
            add_scaled(result, piece_vector(x, v, argument, shift, charge),
                       left_scale * right_scale)
    return freeze(result)


@lru_cache(maxsize=200_000)
def projected_piece(left, right, argument, shift, coefficients):
    """sum_j coefficients[j] shift^j [q^j] Q_shift^(q)."""
    degree = len(coefficients) - 1
    charge_degree = max([degree] + [len(x) for x, scale in left])
    samples = charge_coefficients(
        lambda q: label_piece_vector(left, right, argument, shift, q),
        charge_degree)
    result = {}
    for j, coefficient in enumerate(coefficients):
        scale = F(coefficient) * shift ** j
        if scale:
            add_scaled(result, samples[j], scale)
    return freeze(result)
