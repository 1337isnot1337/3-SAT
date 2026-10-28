#!/usr/bin/env python3
"""Exact bounded checks for clause/equality Newton modes; standard library only."""
from fractions import Fraction as F
from itertools import product
from math import factorial, prod
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
ZERO = (0, 0, 0)


def phi(z, k):
    return (prod((z - h for h in range(k)), start=F(1)) / factorial(k)
            / prod((1 - 2*h*z for h in range(k+1)), start=F(1)))


def mul(p, q):
    out = {}
    for a, x in p.items():
        for b, y in q.items():
            key = tuple(i+j for i, j in zip(a, b))
            out[key] = out.get(key, F(0)) + x*y
    return {k: v for k, v in out.items() if v}


def add(p, q, scale=1):
    out = p.copy()
    for k, v in q.items():
        out[k] = out.get(k, F(0)) + scale*v
    return {k: v for k, v in out.items() if v}


def main():
    # One source packet: L=8, i=0, t=1, alpha=16, zeta=1.
    L, T = 8, 17
    slots = (0, 2, 4)
    cT = prod(T-j for j in range(-L, L))
    cp0 = prod(-j for j in range(-L, L) if j != 0)
    common = F(cT, cp0)
    def W(x, y):
        return common / (T-y+x)
    def ck(k):
        return 2**k * factorial(k)**2 * (1-2*k*k)
    coeff = [[common / (T+x) * ck(k) * phi(F(1, T+x), k)
              for k in range(3)] for x in slots]
    basis = [[phi(F(y//2), k) for y in slots] for k in range(3)]
    # The fourth finite Newton mode vanishes at all real source columns.
    assert all(phi(F(y//2), 3) == 0 for y in slots)
    for r, x in enumerate(slots):
        for j, y in enumerate(slots):
            assert sum(coeff[r][k]*basis[k][j] for k in range(3)) == W(x, y)

    affine = []
    for row in coeff:
        affine.append({tuple(int(i == k) for i in range(3)): v
                       for k, v in enumerate(row)})
    one = {ZERO: F(1)}
    # E(z1,z2,z3) and the all-positive clause 1-prod(1-z_i).
    eq = one.copy()
    for a in affine:
        eq = add(eq, a, -1)
    for i, j in ((0, 1), (0, 2), (1, 2)):
        eq = add(eq, mul(affine[i], affine[j]))
    complement = one
    for a in affine:
        complement = mul(complement, add(one, a, -1))
    clause = add(one, complement, -1)

    bit_vectors = list(product((0, 1), repeat=3))
    results = {}
    for name, p in (("equality", eq), ("positive_clause", clause)):
        direct = F(0)
        for X in bit_vectors:
            for Y in bit_vectors:
                table = (int(Y[0] == Y[1] == Y[2]) if name == "equality"
                         else int(any(Y)))
                direct += table * prod((sum(W(x, y)*X[j] for j, y in enumerate(slots))
                                         if Y[i] else
                                         1-sum(W(x, y)*X[j] for j, y in enumerate(slots))
                                         for i, x in enumerate(slots)), start=F(1))
        moments = {}
        for e in p:
            moments[e] = sum((prod((sum(basis[k][j]*X[j] for j in range(3))**e[k]
                                    for k in range(3)), start=F(1))
                              for X in bit_vectors), start=F(0))
        assert all(moments.values())
        assert sum((p[e]*moments[e] for e in p), start=F(0)) == direct
        expected = {e for e in product(range(4), repeat=3)
                    if (sum(e) <= 2 if name == "equality" else 1 <= sum(e) <= 3)}
        assert set(p) == expected
        results[name] = {"nonzero_tuples": len(p),
                         "tuples_by_total_degree": [sum(sum(e) == d for e in p)
                                                    for d in range(4)],
                         "direct_assignment_pairs": 64,
                         "all_source_moments_nonzero": True,
                         "exact_child_sum_equals_direct": True}

    # Actual zero-mode child packet with no local columns: each l_Y(0)=1-Y.
    vals = {y: prod(1-b for b in y) for y in bit_vectors}
    cubic = sum((-1)**(3-sum(y))*vals[y] for y in bit_vectors)
    assert cubic == -1 and sum(vals.values()) == 1
    assert sum(int(y[0] == y[1] == y[2]) for y in bit_vectors) == 2
    # Check all-size displayed degree formula on small arities and all inputs.
    identity_checks = 0
    for d in range(1, 9):
        for y in product((0, 1), repeat=d):
            actual = prod(y) + prod(1-b for b in y)
            assert actual == int(len(set(y)) == 1) if d > 1 else actual == 1
            identity_checks += 1
    paths = [HERE / 'verify.py', HERE / 'PROOF.md',
             ROOT / 'research/cauchy-newton-modes/PROOF.md',
             ROOT / 'upstream/openai-eth-2026/build/quantitative-contraction.tex',
             ROOT / 'upstream/openai-eth-2026/build/quantitative-reduction.tex']
    return {"packet": {"L": L, "i": 0, "t": 1, "zeta": 1, "T": T,
                       "row_and_column_slots": list(slots),
                       "kernel_entry_identities": 9, "inactive_mode": 3},
            "cases": results,
            "zero_mode_child": {"table": "product(1-Y_i)",
                                "nonzero_boolean_entries": 1, "cubic_coefficient": cubic},
            "equality_boolean_identity_checks": identity_checks,
            "sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in paths}}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
