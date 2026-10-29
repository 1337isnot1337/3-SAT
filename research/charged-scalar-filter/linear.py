#!/usr/bin/env python3
"""Exact scalar-output screen for the pinned first-moment codebooks."""
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import sys
from math import gcd, lcm

root = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('asymmetric_model', root / 'research/charged-asymmetric-crossing/model.py')
model = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = model
spec.loader.exec_module(model)


def rref(rows, width):
    rows = [[F(x) for x in row] for row in rows if any(row)]
    pivot = []
    for j in range(width):
        k = next((i for i in range(len(pivot), len(rows)) if rows[i][j]), None)
        if k is None:
            continue
        rank = len(pivot)
        rows[k], rows[rank] = rows[rank], rows[k]
        a = rows[rank][j]
        rows[rank] = [v/a for v in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][j]:
                a = rows[i][j]
                rows[i] = [v-a*w for v,w in zip(rows[i], rows[rank])]
        pivot.append(j)
        if rank + 1 == len(rows):
            break
    return rows[:len(pivot)], pivot


def nullspace(rows, width):
    reduced, pivots = rref(rows, width)
    basis = []
    for free in range(width):
        if free in pivots:
            continue
        v = [F(0)]*width
        v[free] = 1
        for i,j in enumerate(pivots):
            v[j] = -reduced[i][free]
        basis.append(v)
    return basis


def matrix_rank(rows):
    return len(rref(rows, len(rows[0]))[1]) if rows else 0


def integers(vector):
    denominator = lcm(*(v.denominator for v in vector))
    values = [int(v * denominator) for v in vector]
    divisor = gcd(*values)
    return [v // divisor for v in values] if divisor else values


