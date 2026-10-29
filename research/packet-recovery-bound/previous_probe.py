#!/usr/bin/env python3
"""Explore exact linear parity recovery for a fixed Boolean packet input."""

from fractions import Fraction as F
from math import comb, prod
import json
import time


def multiply(left, right, modulus=None):
    result = [0] * (len(left)+len(right)-1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            result[i+j] += x*y
    return [x % modulus for x in result] if modulus else result


def valuation(value, precision):
    return (value & -value).bit_length()-1 if value else precision


def kernel_chart(L, t, precision):
    modulus = 2**precision
    denominator = prod(-s for s in range(-L, L) if s)
    charts = {}
    for difference in range(1-L, L):
        coefficients = [1]
        for s in range(-L, L):
            if s != difference:
                coefficients = multiply(coefficients, [t-s, 2*L])
        rationals = [F(c, denominator) for c in coefficients]
        if any(c.denominator % 2 == 0 for c in rationals):
            raise ValueError("nonintegral kernel chart")
        charts[difference] = [c.numerator * pow(c.denominator, -1, modulus) % modulus
                              for c in rationals]
    return charts


def packet_data(L, X, nodes, precision):
    modulus = 2**precision
    degree = L*(2*L-1)
    rows = []
    for t in nodes:
        charts = kernel_chart(L, t, precision)
        row_functions = [[sum(charts[y-x][j] for y in range(L) if X >> y & 1) % modulus
                          for j in range(2*L)] for x in range(L)]
        polynomials = [[1]]
        for mask in range(1, 2**L):
            bit = mask & -mask
            x = bit.bit_length()-1
            polynomials.append(multiply(polynomials[mask-bit], row_functions[x], modulus))
        rows.extend([[f[k] if k < len(f) else 0 for f in polynomials]
                     for k in range(degree+1)])
    target = [int(mask & X == mask) for mask in range(2**L)]
    return rows, target


def threshold(rows, target, precision):
    """Diagonalize over Z/2^precision, retaining target column operations."""
    modulus = 2**precision
    matrix = [row[:] for row in rows]
    transformed = target[:]
    nrows, ncols = len(matrix), len(target)
    pivots = []
    for k in range(min(nrows, ncols)):
        best = precision
        position = None
        for i in range(k, nrows):
            for j in range(k, ncols):
                v = valuation(matrix[i][j], precision)
                if v < best:
                    best, position = v, (i, j)
                    if best == 0:
                        break
            if best == 0:
                break
        if position is None:
            break
        i, j = position
        matrix[k], matrix[i] = matrix[i], matrix[k]
        if j != k:
            for row in matrix:
                row[k], row[j] = row[j], row[k]
            transformed[k], transformed[j] = transformed[j], transformed[k]
        inverse = pow(matrix[k][k] >> best, -1, modulus)
        matrix[k] = [(x*inverse) % modulus for x in matrix[k]]
        pivot = matrix[k]
        for i in range(k+1, nrows):
            if matrix[i][k]:
                factor = matrix[i][k] >> best
                matrix[i] = [(x-factor*y) % modulus for x, y in zip(matrix[i], pivot)]
        # Clear the rest of this pivot row by column operations. Every other
        # entry in the pivot column is zero (including earlier pivot rows).
        for j in range(k+1, ncols):
            factor = pivot[j] >> best
            transformed[j] = (transformed[j]-factor*transformed[k]) % modulus
            pivot[j] = 0
        pivots.append(best)
    required = max([0] + [v for v, b in zip(pivots, transformed) if b & 1]) + 1
    if any(b & 1 for b in transformed[len(pivots):]):
        required = None
    return {"minimum_linear_parity_precision": required,
            "pivot_valuations": pivots, "rank_mod_2_to_precision": len(pivots)}


if __name__ == "__main__":
    for L in (2, 4, 8):
        for X in sorted({1, 2**L-1, sum(1 << i for i in range(0, L, 2))}):
            for nodes in ([1], [-1, 1], list(range(1-L, L, 2))):
                started = time.monotonic()
                rows, target = packet_data(L, X, nodes, 80)
                result = threshold(rows, target, 80)
                print(json.dumps({"L": L, "X": X, "nodes": nodes,
                                  **result, "seconds": round(time.monotonic()-started, 3)}), flush=True)
