#!/usr/bin/env python3
"""Bounded exact modulo-16 screen for moments of the subdivided filler pair."""
from fractions import Fraction as F
from itertools import combinations
from math import prod
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def checker(L):
    T = 2*L+1
    common = F(prod(T-j for j in range(-L, L)),
               prod(-j for j in range(-L, L) if j))
    W = []
    for x in range(L):
        row = []
        for y in range(L):
            value = common/F(T-y+x)
            assert value.denominator % 2
            row.append(value.numerator*pow(value.denominator, -1, 16) % 16)
        W.append(row)
    diag = [W[x][x+1] for x in range(L-1)]
    edges = [[(y, w) for y, w in enumerate(W[x]) if y != x+1 and w]
             for x in range(L)]

    def moment(S):
        result = 0
        def evaluate(chosen, ys, weight):
            nonlocal result
            value = weight*(-1)**len(chosen)
            for y in range(L):
                baseline = y>0 and y-1 not in chosen
                if ys >> y & 1:
                    if baseline:
                        value *= 1-diag[y-1]
                else:
                    value *= 2-diag[y-1] if baseline else 2
                value %= 16
                if not value:
                    return
            result = (result+value) % 16
        def visit(start, chosen, ys, weight):
            evaluate(chosen, ys, weight)
            if len(chosen) == 3:
                return
            for x in range(start, L):
                for y, w in edges[x]:
                    new_weight = weight*w % 16
                    if new_weight:
                        visit(x+1, chosen+(x,), ys | (1<<y), new_weight)
        def insert(i, ys, weight):
            if i == len(S):
                visit(0, (), ys, weight)
                return
            for y, w in enumerate(W[S[i]]):
                new_weight = weight*w % 16
                if new_weight:
                    insert(i+1, ys | (1<<y), new_weight)
        insert(0, 0, 1)
        return result

    # Independent exhaustive bit-sum comparison for every row subset of
    # size at most three when L=8.
    brute_checks = 0
    if L == 8:
        for q in range(4):
            for S in combinations(range(L), q):
                direct = 0
                for x in range(1<<L):
                    z = [sum(row[y] for y in range(L) if x>>y&1) % 16 for row in W]
                    direct += prod(1-v for v in z)*prod(z[j] for j in S)
                assert moment(S) == direct % 16
                brute_checks += 1
    upper = L-1 if L <= 16 else 4
    checks = 0
    for q in range(1, 4):
        for S in combinations(range(upper), q):
            assert moment(S) == 0
            checks += 1
    assert moment((L-1,)) != 0
    return {'L': L, 'nonboundary_zero_moments': checks,
            'last_row_singleton_mod_16': moment((L-1,)),
            'independent_bit_sum_checks': brute_checks}


def main():
    paths = [HERE/'filler-moments.py', HERE/'PROOF.md',
             ROOT/'upstream/openai-eth-2026/build/quantitative-contraction.tex']
    return {'cases': [checker(L) for L in (8, 16, 32, 64)],
            'scope': 'finite modulo-16 screen; nonboundary generalization unproved',
            'sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in paths}}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
