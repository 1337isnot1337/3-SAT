#!/usr/bin/env python3
"""Exact local checks and small packing controls for dense packet support."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import comb, factorial, prod
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def phi(z, k):
    return (prod((z-h for h in range(k)), start=F(1))/factorial(k)
            / prod((1-2*h*z for h in range(k+1)), start=F(1)))


def mul(p, q):
    out = {}
    for a, x in p.items():
        for b, y in q.items():
            e = tuple(i+j for i, j in zip(a, b))
            out[e] = out.get(e, F(0)) + x*y
    return {e: v for e, v in out.items() if v}


def add(p, q, factor=1):
    out = p.copy()
    for e, v in q.items():
        out[e] = out.get(e, F(0)) + factor*v
    return {e: v for e, v in out.items() if v}


def valuation(v):
    def v2(x):
        x = abs(x)
        assert x
        return (x & -x).bit_length()-1
    return v2(v.numerator)-v2(v.denominator)


def packet(L, q, b):
    K, T = L//2, 2*L+1
    assert 3*q <= K and b <= K
    rows = [2*j for j in range(3*q)]
    x_source = 2*(K-1)
    common = F(prod(T-j for j in range(-L, L)),
               prod(-j for j in range(-L, L) if j))
    def W(x, y):
        return common/(T-y+x)
    forms = []
    for x in rows:
        z = F(1, T+x)
        coeff = [common/(T+x)*2**k*factorial(k)**2*(1-2*k*k)*phi(z, k)
                 for k in range(K)]
        forms.append({tuple(int(j == k) for j in range(K)): coeff[k] for k in range(K)})
    a = L.bit_length()-1
    D = common.denominator * prod(range(1, 4*L, 2))
    assert D.bit_length() <= 6*L*(a+2)
    assert all(D % v.denominator == 0 and abs(D*v.numerator//v.denominator).bit_length()
               <= 20*L*(a+2) for row in forms for v in row.values())
    one = {(0,)*K: F(1)}
    polynomial = one
    for t in range(q):
        f = one.copy()
        for row in forms[3*t:3*t+3]:
            f = add(f, row, -1)
        for i, j in ((0, 1), (0, 2), (1, 2)):
            f = add(f, mul(forms[3*t+i], forms[3*t+j]))
        polynomial = mul(polynomial, f)
    source = [phi(F(K-1), k) for k in range(K)]
    assert all(valuation(v) == 0 for v in source)
    assert all(comb(K-1, k) % 2 == 1 for k in range(K))
    selected = [tuple(int(k < b and (mask >> k) & 1) for k in range(K))
                for mask in range(2**b)]
    values = [polynomial[e]*prod((source[k]**e[k] for k in range(K)), start=F(1))
              for e in selected]
    assert all(x > 0 for x in values)
    for e, value in zip(selected, values):
        assert valuation(value) <= 30*sum(e)*L*(a+2)
    direct = F(0)
    for ys in product((0, 1), repeat=3*q):
        if all(ys[3*t] == ys[3*t+1] == ys[3*t+2] for t in range(q)):
            direct += prod((W(x, x_source) if y else 1-W(x, x_source)
                            for x, y in zip(rows, ys)), start=F(1))
    expanded = sum((v*prod((source[k]**e[k] for k in range(K)), start=F(1))
                    for e, v in polynomial.items()), start=F(0))
    assert direct == expanded
    return {'L': L, 'q': q, 'modes_K': K, 'chosen_modes': b,
            'selected_subsets': len(selected),
            'selected_summand_max_v2': max(map(valuation, values)),
            'all_source_modes_units': True, 'odd_common_denominator_bound': True,
            'direct_row_assignments': 2**(3*q),
            'exact_contraction_identity': True}


def packing():
    # Full packet control: r=2, a=3; not the source's asymptotic schedule.
    r, a, L = 2, 3, 8
    packets = []
    for pairs in product(((0, 0), (0, 1), (1, 1)), repeat=a):
        unequal = sum(x != y for x, y in pairs)
        for _ in range(2**unequal):  # B=L
            slots = []
            for x in range(L):
                row, col = [], []
                for i, (lo, hi) in enumerate(pairs):
                    if lo == hi:
                        row.append(lo); col.append(lo)
                    elif (x >> i) & 1:
                        row.append(hi); col.append(lo)
                    else:
                        row.append(lo); col.append(hi)
                slots.append((tuple(row), tuple(col), x))
            packets.append((pairs, slots))
    loads = Counter((row, col) for _, slots in packets for row, col, _ in slots)
    assert len(loads) == r**(2*a) and set(loads.values()) == {L}
    eligible = [(pairs, slots) for pairs, slots in packets
                if pairs[0][0] != pairs[0][1] and
                sum(lo == hi for lo, hi in pairs[1:]) >= 2]
    for pairs, slots in eligible:
        by_label = Counter(row for row, _, x in slots if x%2 == 0)
        q = sum(n//3 for n in by_label.values())
        assert q >= L//8
        assert all(row[0] < col[0] for row, col, x in slots if x%2 == 0)
    return {'r': r, 'a': a, 'L': L, 'packets': len(packets),
            'all_pair_loads_equal': L, 'eligible_packets': len(eligible),
            'eligible_target_rows_grouped_by_label': True,
            'asymptotic_schedule_claimed_for_toy': False}


def main():
    paths = [HERE/'verify.py', HERE/'PROOF.md',
             ROOT/'research/cauchy-newton-modes/PROOF.md',
             ROOT/'upstream/openai-eth-2026/build/quantitative-contraction.tex']
    return {'packet_cases': [packet(8, 1, 2), packet(16, 2, 3)],
            'toy_packing': packing(),
            'sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in paths}}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
