#!/usr/bin/env python3
"""Exact checks for clustered Newton denominators, standard library only."""
from fractions import Fraction as F
from itertools import product
from math import factorial, prod
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def phi(z, k):
    return (prod((z-h for h in range(k)), start=F(1))/factorial(k)
            / prod((1-2*h*z for h in range(k+1)), start=F(1)))


def v2(v):
    def integer(n):
        n = abs(n)
        assert n
        return (n & -n).bit_length()-1
    return integer(v.numerator)-integer(v.denominator)


def multiply(p, q):
    out = {}
    for a, x in p.items():
        for b, y in q.items():
            if a & b:
                continue
            out[a|b] = out.get(a|b, F(0)) + x*y
    return {k: v for k, v in out.items() if v}


def add(p, q, sign=1):
    out = p.copy()
    for k, v in q.items():
        out[k] = out.get(k, F(0)) + sign*v
    return {k: v for k, v in out.items() if v}


def case(L, modes):
    K, T = L//2, 2*L+1
    assert 4*modes <= K
    a = L.bit_length()-1
    rows = [4*j+t for j in range(modes) for t in range(3)]
    # x=2r; rows 4j,4j+1,4j+2 share the same complete label
    # whenever the two corresponding low coordinate pairs are equal.
    C = F(prod(T-j for j in range(-L, L)),
          prod(-j for j in range(-L, L) if j))
    assert v2(C) == a+1
    factors = {T+2*(r-h) for r in rows for h in range(modes)}
    assert len(factors) <= 5*modes and min(factors) > 0
    D = prod(factors)
    assert D % 2 == 1 and D.bit_length() <= 5*modes*(a+2)
    forms = []
    for r in rows:
        z = F(1, T+2*r)
        coeff = [C/(T+2*r)*2**k*factorial(k)**2*(1-2*k*k)*phi(z, k)
                 for k in range(modes)]
        for v in coeff:
            normalized = D*v/C
            assert normalized.denominator == 1
            assert abs(normalized.numerator).bit_length() <= 20*modes*(a+2)
        forms.append({1<<k: v for k, v in enumerate(coeff)})
    polynomial = {0: F(1)}
    for j in range(modes):
        chunk = forms[3*j:3*j+3]
        term = {0: F(1)}
        for row in chunk:
            term = add(term, row, -1)
        for p, q in ((0, 1), (0, 2), (1, 2)):
            term = add(term, multiply(chunk[p], chunk[q]))
        polynomial = multiply(polynomial, term)
    assert set(polynomial) == set(range(2**modes))
    source = [phi(F(K-1), k) for k in range(K)]
    assert all(v2(x) == 0 for x in source)
    vals = []
    for mask, value in polynomial.items():
        result = value*prod((source[k] for k in range(modes) if mask>>k&1), start=F(1))
        assert result > 0
        assert v2(result) <= mask.bit_count()*(a+1+25*modes*(a+2))
        vals.append(v2(result))
    # Check the full source kernel for all K modes and the entire local
    # contraction at the one-hot pinned assignment, not just the truncation.
    W = lambda r: C/(T-2*(K-1)+2*r)
    for r in rows:
        z = F(1, T+2*r)
        decomposed = sum((C/(T+2*r)*2**k*factorial(k)**2*(1-2*k*k)
                          *phi(z, k)*source[k] for k in range(K)), start=F(0))
        assert decomposed == W(r)
    direct = prod((prod((W(rows[3*j+t]) for t in range(3)), start=F(1))
                   + prod((1-W(rows[3*j+t]) for t in range(3)), start=F(1))
                   for j in range(modes)), start=F(1))
    explicit = F(0)
    for ys in product((0, 1), repeat=modes):
        explicit += prod((prod((W(rows[3*j+t]) if ys[j] else 1-W(rows[3*j+t])
                                for t in range(3)), start=F(1))
                          for j in range(modes)), start=F(1))
    assert direct == explicit
    return {'L': L, 'modes_and_triples': modes, 'squarefree_summands': len(vals),
            'distinct_denominators': len(factors), 'all_source_units': True,
            'max_summand_v2': max(vals), 'full_kernel_and_contraction_match': True}


def main():
    paths = [HERE/'verify.py', HERE/'PROOF.md', ROOT/'research/cauchy-newton-modes/PROOF.md',
             ROOT/'upstream/openai-eth-2026/build/quantitative-contraction.tex']
    return {'cases': [case(16, 2), case(32, 3), case(64, 4)],
            'sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in paths}}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
