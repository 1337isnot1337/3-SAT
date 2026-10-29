#!/usr/bin/env python3
"""Exact checks for odd-node precision-surviving tensor-mode support."""
from fractions import Fraction as F
from itertools import product
from math import comb, factorial, prod
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def v2(x):
    def integer(n):
        n = abs(n)
        assert n
        return (n & -n).bit_length()-1
    return integer(x.numerator)-integer(x.denominator)


def row_basis(z, k):
    return (prod(((z-1)/2-h for h in range(k)), start=F(1))/factorial(k)
            / prod((1-2*h*z for h in range(k+1)), start=F(1)))


def column_basis(j, k):
    return (prod((F(j)-h for h in range(k)), start=F(1))/factorial(k)
            / prod((1-2*(1+2*h)*j for h in range(k+1)), start=F(1)))


def rank2(rows, n):
    rows = rows.copy()
    rank = 0
    for col in range(n):
        pivot = next((i for i in range(rank, len(rows)) if rows[i] >> col & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and rows[i] >> col & 1:
                rows[i] ^= rows[rank]
        rank += 1
    return rank


def case(L, b):
    K, T, a = L//2, 2*L+1, L.bit_length()-1
    assert b <= K and b & (b-1) == 0
    common = F(prod(T-j for j in range(-L, L)),
               prod(-j for j in range(-L, L) if j))
    assert v2(common) == a+1
    weights = [a+1+2*k+2*v2(F(factorial(k))) for k in range(b)]
    coeff = []
    residues = []
    for r in range(b):
        z = F(1, T+2*r)
        t = (z-1)/2
        assert t.denominator % 2 == 1
        residues.append((t.numerator*pow(t.denominator, -1, b)) % b)
        row = []
        for k in range(b):
            ck = 2**(2*k)*factorial(k)**2*(1-2*(1+2*k)*k)
            normalized = common/(T+2*r)*ck*row_basis(z, k)/2**weights[k]
            assert normalized.denominator % 2 == 1
            assert normalized.numerator % 2 == comb(residues[-1], k) % 2
            row.append(normalized)
        coeff.append(row)
    assert len(set(residues)) == b
    matrix = [sum((v.numerator % 2)<<k for k, v in enumerate(row)) for row in coeff]
    assert rank2(matrix, b) == b
    source = [column_basis(K-1, k) for k in range(K)]
    assert all(v2(s) == 0 for s in source)

    # Polynomial coefficients modulo 2, retaining actual exponent tuples.
    zero = (0,)*b
    poly = {zero: 1}
    for row in matrix:
        nxt = poly.copy()
        for exp in poly:
            for k in range(b):
                if row>>k&1:
                    key = tuple(e+int(i == k) for i, e in enumerate(exp))
                    nxt[key] = nxt.get(key, 0) ^ 1
        poly = {e: v for e, v in nxt.items() if v}
    witnesses = {}
    for exp in poly:
        support = sum((1<<k) for k, e in enumerate(exp) if e)
        witnesses.setdefault(support, exp)
    assert len(witnesses) == 2**b
    assert all(sum(e) <= b for e in witnesses.values())

    # For small cases independently compute exact rational normalized
    # coefficients of the chosen monomials, not merely their parity DP.
    exact_checks = 0
    if b <= 4:
        exact = {zero: F(1)}
        for row in coeff:
            nxt = exact.copy()
            for exp, value in exact.items():
                for k in range(b):
                    key = tuple(e+int(i == k) for i, e in enumerate(exp))
                    nxt[key] = nxt.get(key, F(0))+value*row[k]
            exact = nxt
        for exp in witnesses.values():
            assert v2(exact[exp]) == 0
            assert v2(exact[exp]*prod((source[k]**exp[k] for k in range(b)), start=F(1))) == 0
            exact_checks += 1

    # A clause y OR NOT a, paired with a local auxiliary Cauchy block.
    # Modulo two that block is the identity for b<=L/2.
    aux = [[common/(T+2*r-(2*t+1)) for t in range(b)] for r in range(b)]
    assert all((v2(aux[r][t]) == 0 if r == t else v2(aux[r][t]) >= 1)
               for r in range(b) for t in range(b))
    clause_exact = 0
    if b <= 4:
        collected = {}
        for bits in product((0, 1), repeat=b):
            av = [sum((aux[r][t]*bits[t] for t in range(b)), start=F(0))
                  for r in range(b)]
            part = {zero: F(1)}
            for r in range(b):
                nxt = {e: value*(1-av[r]) for e, value in part.items()}
                for exp, value in part.items():
                    for k in range(b):
                        key = tuple(e+int(i == k) for i, e in enumerate(exp))
                        nxt[key] = nxt.get(key, F(0))+value*av[r]*coeff[r][k]
                part = nxt
            for exp, value in part.items():
                collected[exp] = collected.get(exp, F(0))+value
        for exp in witnesses.values():
            assert v2(collected[exp]) == 0
            clause_exact += 1

    # Local subdivision/pin gate: two deformed inputs to a binary
    # equality row, followed by a pin row through a third local block.
    # This checks the scalar gate only, not a globally packed reduction.
    subdivision_checks = 0
    if b <= 4:
        pin = tuple(int(i == b-1) for i in range(b))
        for target in product((0, 1), repeat=b):
            total = F(0)
            u = [sum((aux[i][j]*target[j] for j in range(b)), start=F(0))
                 for i in range(b)]
            for internal in product((0, 1), repeat=b):
                v = [sum((aux[i][j]*internal[j] for j in range(b)), start=F(0))
                     for i in range(b)]
                total += prod(((1-u[i]-v[i]+2*u[i]*v[i])
                               *(v[i] if pin[i] else 1-v[i])
                               for i in range(b)), start=F(1))
            assert total.denominator % 2 == 1
            assert total.numerator % 2 == int(target == pin)
            subdivision_checks += 1

    # Full K-mode kernel identity and full local tensor contraction.
    W = lambda r: common/(T-2*(K-1)+2*r)
    for r in range(b):
        z = F(1, T+2*r)
        actual = sum((common/(T+2*r)*2**(2*k)*factorial(k)**2
                      *(1-2*(1+2*k)*k)*row_basis(z,k)*source[k]
                      for k in range(K)), start=F(0))
        assert actual == W(r)
    if b <= 4:
        for bits in product((0, 1), repeat=b):
            for r in range(b):
                av = sum((aux[r][t]*bits[t] for t in range(b)), start=F(0))
                yv = W(r)
                summed = sum((int(y or not u)*(yv if y else 1-yv)
                              *(av if u else 1-av)
                              for y, u in product((0, 1), repeat=2)), start=F(0))
                assert summed == 1-av+av*yv
    direct = prod((1+W(r) for r in range(b)), start=F(1))
    assignments = sum((prod((2*W(r) if bits[r] else 1-W(r) for r in range(b)),
                            start=F(1)) for bits in product((0, 1), repeat=b)), start=F(0))
    assert direct == assignments
    return {'L': L, 'b': b, 'binary_matrix_rank': rank2(matrix, b),
            'distinct_support_witnesses': len(witnesses),
            'max_witness_degree': max(map(sum, witnesses.values())),
            'exact_rational_witness_checks': exact_checks,
            'source_units': True, 'full_kernel_and_contraction_match': True,
            'auxiliary_block_identity_mod_2': True,
            'clause_exact_witness_checks': clause_exact,
            'local_subdivision_pin_checks': subdivision_checks}


def filler_case(L):
    # Exact mod-16 expansion of a pair of fully occupied packets tied
    # by subdivision equalities, with unit clauses in the first packet.
    T = 2*L+1
    common = F(prod(T-j for j in range(-L, L)),
               prod(-j for j in range(-L, L) if j))
    W = [[(common/F(T-y+x)).numerator *
          pow((common/F(T-y+x)).denominator, -1, 16) % 16
          for y in range(L)] for x in range(L)]
    diag = [W[x][x+1] for x in range(L-1)]
    assert len(set(diag)) == 1
    U = diag[0]
    assert U % 8 == 3
    assert comb(3*L+1, L+1) % 8 == 7
    assert (comb(2*L, L)//2) % 8 == 3
    edges = [[(y, W[x][y]) for y in range(L)
              if y != x+1 and W[x][y] % 16] for x in range(L)]
    result = 0
    contributing = []
    def evaluate(chosen, ys, weight):
        nonlocal result
        value = weight * (-1)**len(chosen)
        for y in range(L):
            baseline = y > 0 and y-1 not in chosen
            if ys >> y & 1:
                if baseline:
                    value *= 1-diag[y-1]
            else:
                value *= 2-diag[y-1] if baseline else 2
            value %= 16
            if not value:
                return
        result = (result+value) % 16
        contributing.append((chosen, ys))
    def visit(start, chosen, ys, weight):
        evaluate(chosen, ys, weight)
        if len(chosen) == 3:
            return
        for x in range(start, L):
            for y, w in edges[x]:
                new_weight = weight*w % 16
                if new_weight:
                    visit(x+1, chosen+(x,), ys | (1<<y), new_weight)
    visit(0, (), 0, 1)
    assert result == 8
    assert set(contributing) == {((), 0), ((L//2-1,), 1), ((L-1,), 1)}
    return {'L': L, 'scalar_mod_16': result, 'valuation': 3,
            'unit_diagonal_mod_8': U % 8, 'surviving_expansion_terms': len(contributing)}


def toy_pairing():
    # Exact packet count and paired-row labels for r=2, a=3, B_pad=L.
    # This is a packing control, not the source asymptotic schedule.
    r, a = 2, 3
    L, b = 2**a, 2
    pairs = 0
    comparisons = 0
    for rest in product(((0, 0), (0, 1), (1, 1)), repeat=a-1):
        unequal = sum(lo != hi for lo, hi in rest)
        auxiliary_packets = 2**unequal
        target_packets = 2**(unequal+1)
        assert target_packets == 2*auxiliary_packets
        for _ in range(auxiliary_packets):
            pairs += 1
            for j in range(b):
                slot = 2*j
                def row_label(first):
                    return tuple(lo if lo == hi or not (slot >> i & 1) else hi
                                 for i, (lo, hi) in enumerate((first,) + rest))
                assert row_label((0, 0)) == row_label((0, 1))
                comparisons += 1
    assert pairs == r**(2*a-2)
    return {'r': r, 'a': a, 'L': L, 'packet_pairs': pairs,
            'paired_row_label_checks': comparisons,
            'asymptotic_schedule_claimed_for_toy': False}


def main():
    paths = [HERE/'verify.py', HERE/'PROOF.md', ROOT/'research/cauchy-newton-modes/PROOF.md',
             ROOT/'upstream/openai-eth-2026/build/quantitative-contraction.tex']
    return {'cases': [case(16, 2), case(32, 4), case(64, 8)],
            'toy_packet_pairing': toy_pairing(),
            'subdivided_filler_cases': [filler_case(L) for L in (4,8,16,32,64)],
            'sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in paths}}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
