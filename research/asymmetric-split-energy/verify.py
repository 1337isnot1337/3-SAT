#!/usr/bin/env python3
"""Exact rational controls for the ideal inverse-square recurrence."""
from fractions import Fraction
from functools import lru_cache


def combine_capacity(left, right):
    return left + right


@lru_cache(None)
def tree_capacities(leaves):
    if len(leaves) == 1:
        return frozenset(leaves)
    return frozenset(combine_capacity(a, b)
                     for k in range(1, len(leaves))
                     for a in tree_capacities(leaves[:k])
                     for b in tree_capacities(leaves[k:]))


def main():
    trees = 0
    for n in range(1, 13):
        leaves = tuple(Fraction((i % 5) + 1, (i % 3) + 1) for i in range(n))
        assert tree_capacities(leaves) == {sum(leaves)}
        trees += 1
    # Pythagorean circle points make every check exact, including the unique
    # optimizer of eL=5/a,eR=5/b when x=a/5,y=b/5.
    points = [(Fraction(3, 5), Fraction(4, 5)),
              (Fraction(5, 13), Fraction(12, 13)),
              (Fraction(8, 17), Fraction(15, 17))]
    comparisons = 0
    for x_star, y_star in points:
        e_l, e_r = 1 / x_star, 1 / y_star
        assert e_l*x_star == e_r*y_star == 1
        for t in range(101):
            # Rational parameterization covers the closed quarter circle.
            z = Fraction(t, 100)
            x = (1 - z*z) / (1 + z*z)
            y = 2*z / (1 + z*z)
            assert x*x + y*y == 1
            assert min(e_l*x, e_r*y) <= 1
            comparisons += 1
        assert (1 / (e_l*e_l) + 1 / (e_r*e_r)) == 1
    # Invalid recurrence: arithmetic mean depends on tree shape and is not
    # the minimax answer even for equal coefficients.
    arithmetic_mean = (Fraction(1) + Fraction(1)) / 2
    correct_squared = Fraction(1, 2)
    assert arithmetic_mean**2 != correct_squared
    print(f'PASS: {trees} tree-size families; {comparisons} exact circle controls; 3 equality witnesses; invalid-mean control')


if __name__ == '__main__':
    main()
