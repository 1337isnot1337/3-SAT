"""Exact polynomial formula for the uncharged second operator moment.

This is a scoped research artifact, not a SAT algorithm or a full theorem
implementation.  Polynomials are dictionaries mapping sorted integer
partitions to rational coefficients.
"""
from collections import Counter
from fractions import Fraction as F
from math import comb, factorial

from pairing import add, multiplicity_factorial


def clean(poly):
    return {monomial: coefficient for monomial, coefficient in poly.items()
            if coefficient}


def multiply(left, right):
    answer = {}
    for a, c in left.items():
        for b, d in right.items():
            key = tuple(sorted(a + b, reverse=True))
            answer[key] = answer.get(key, F(0)) + c * d
    return clean(answer)


def contraction(poly):
    """Apply A=exp(L), where A(u_j)=sum_n binom(j-1,n-1)u_n."""
    answer = {}
    for monomial, coefficient in poly.items():
        image = {(): F(coefficient)}
        for part in monomial:
            factor = {(n,): F(comb(part - 1, n - 1))
                      for n in range(1, part + 1)}
            image = multiply(image, factor)
        answer = add(answer, image)
    return answer


def f_multiply(poly, max_weight):
    """Multiply by F=sum_(r>=1)(-1)^(r-1)r u_r through max_weight."""
    answer = {}
    for monomial, coefficient in poly.items():
        for r in range(1, max_weight - sum(monomial) + 1):
            key = tuple(sorted(monomial + (r,), reverse=True))
            answer[key] = answer.get(key, F(0)) + coefficient * (-1) ** (r - 1) * r
    return clean(answer)


def derivative(poly, part):
    answer = {}
    for monomial, coefficient in poly.items():
        multiplicity = monomial.count(part)
        if multiplicity:
            reduced = list(monomial)
            reduced.remove(part)
            key = tuple(reduced)
            answer[key] = answer.get(key, F(0)) + coefficient * multiplicity
    return clean(answer)


def second_operator(poly, h):
    """Return U_h=(1/(2h))F(FA+2A d/d(u_1)) in exact weight h."""
    if h < 1 or any(sum(monomial) != h for monomial in poly):
        raise ValueError("second_operator expects a fixed positive weight h")
    contracted = contraction(poly)
    mixed = add(f_multiply(contracted, h), contraction(derivative(poly, 1)), 2)
    image = f_multiply(mixed, h)
    return {monomial: coefficient / (2 * h)
            for monomial, coefficient in image.items()
            if sum(monomial) == h and coefficient}


def normalized_pairing(states):
    """The matrix U_h in the source's partition-label normalization."""
    if not states:
        raise ValueError("empty label set")
    h = sum(states[0])
    images = [second_operator({state: F(1)}, h) for state in states]
    return [[F(multiplicity_factorial(x), multiplicity_factorial(v))
             * images[j].get(x, F(0))
             for j, v in enumerate(states)] for x in states]


def second_pairing(states):
    """Second moment at output energy one, before multiplying by E."""
    h = sum(states[0])
    scale = 4 * h * factorial(h)
    return [[scale * entry for entry in row] for row in normalized_pairing(states)]


def integer_matrix(matrix):
    for row in matrix:
        for entry in row:
            if entry.denominator != 1:
                raise ValueError("nonintegral partition pairing")
    return [[int(entry) for entry in row] for row in matrix]
