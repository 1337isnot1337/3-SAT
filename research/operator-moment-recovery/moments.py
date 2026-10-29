"""Wick contractions for a possible higher-moment recovery interface.

Original AI-assisted reference code. The predecessor operators and the
external source definitions are separately pinned by the experiment.
"""

from collections import Counter
from functools import lru_cache
from math import factorial
from pathlib import Path
import sys

PREDECESSOR = Path(__file__).resolve().parents[1] / "anthropic-operator-ranks"
sys.path.insert(0, str(PREDECESSOR))
from operators import dual_polynomial, dual_scale


@lru_cache(None)
def wick_pair(left, right):
    """Full scalar contraction, as a permanent with repeated parts labeled."""
    if len(left) != len(right):
        return 0
    if not left:
        return 1
    j = left[0]
    result = 0
    for n, multiplicity in Counter(right).items():
        remaining = list(right)
        remaining.remove(n)
        contraction = (-1) ** (j - 1) * factorial(j + n - 1) // (
            factorial(j - 1) * factorial(n - 1))
        result += multiplicity * contraction * wick_pair(left[1:], tuple(remaining))
    return result


def derivative(poly, order=1):
    result = {}
    for monomial, coefficient in poly:
        ones = monomial.count(1)
        if ones < order:
            continue
        scale = 1
        for i in range(order):
            scale *= ones - i
        output = monomial[:len(monomial) - order] if order else monomial
        result[output] = result.get(output, 0) + coefficient * scale
    return tuple(sorted((monomial, c) for monomial, c in result.items() if c))


def full_pairing(left, right):
    return sum(a * b * wick_pair(mu, nu) for mu, a in left for nu, b in right)


def partial_pairing(left, right):
    """Coefficient for two uncontracted unit-weight currents, before 2E."""
    numerator = (full_pairing(derivative(left, 2), right)
                 + 2 * full_pairing(derivative(left), derivative(right))
                 + full_pairing(left, derivative(right, 2)))
    if numerator % 2:
        raise ValueError("Second partial contraction is not integral")
    return numerator // 2


def second_pairing(mu, nu, energy):
    """Candidate sum_s s^2 A_s = B2(x,v) delta(y,u)."""
    left = dual_polynomial(mu)
    right = ((nu, dual_scale(nu)),)
    return 4 * energy * partial_pairing(left, right)
