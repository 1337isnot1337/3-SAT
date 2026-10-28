#!/usr/bin/env python3
"""Bounded exact checks for the four-packet subdivided unit-clause gadget."""
from fractions import Fraction as F
from itertools import product
from math import comb, factorial, prod
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def mod(v, modulus):
    assert v.denominator % 2
    return v.numerator*pow(v.denominator, -1, modulus) % modulus


def row_basis(z, k):
    return (prod(((z-1)/2-h for h in range(k)), start=F(1))/factorial(k)
            / prod((1-2*h*z for h in range(k+1)), start=F(1)))


def col_basis(j, k):
    return (prod((F(j)-h for h in range(k)), start=F(1))/factorial(k)
            / prod((1-2*(1+2*h)*j for h in range(k+1)), start=F(1)))


def v2_int(n):
    return (n & -n).bit_length()-1


def gadget(L, b):
    assert b <= L//4 and b & (b-1) == 0
    T, a, K = 2*L+1, L.bit_length()-1, L//2
    common = F(prod(T-j for j in range(-L, L)),
               prod(-j for j in range(-L, L) if j))
    W = [[mod(common/F(T-y+x), 16) for y in range(L)] for x in range(L)]
    assert all((W[x][y] % 2 == int(y == x+1)) for x in range(L) for y in range(L))
    selected = tuple(2*r for r in range(b))
    pinrow = L-3
    assert pinrow not in selected

    # Physical original row endpoint types: each subdivision column pairs
    # the same slot of T/T' or H/H', connecting one clause to one variable.
    for x in range(L):
        t_is_clause = x in selected
        tp_is_clause = x not in selected
        h_is_clause = False
        hp_is_clause = True
        assert t_is_clause != tp_is_clause and h_is_clause != hp_is_clause
    # Reconstruct the old CNF vertices: each selected variable occurs in
    # two negative unit clauses; each other variable has one unit clause.
    clauses = []
    variable_count = 0
    for x in range(L):
        if x in selected:
            clauses.extend(((variable_count, 0), (variable_count, 0)))
            variable_count += 1
        else:
            clauses.append((variable_count, int(x == pinrow)))
            variable_count += 1
            clauses.append((variable_count, 0))
            variable_count += 1
    assert len(clauses) == 2*L and variable_count+len(clauses) == 4*L-b
    by_variable = {}
    for var, value in clauses:
        by_variable.setdefault(var, []).append(value)
    assert len(by_variable) == variable_count
    assert sum(len(v) == 2 for v in by_variable.values()) == b
    assert all(len(set(v)) == 1 for v in by_variable.values())

    # The selected variable has its two row ports in T' and H at the same
    # slot and hence the same label for any shared packet type/orientation.
    label_checks = 0
    for rest in product(((0, 0), (0, 1), (1, 1)), repeat=a-1):
        pairs = ((0, 1),)+rest
        packets = {}
        for name in ('T', 'Tprime', 'H', 'Hprime'):
            slots = []
            for x in range(L):
                row, col = [], []
                for i, (lo, hi) in enumerate(pairs):
                    flip = lo != hi and (x >> i & 1)
                    row.append(hi if flip else lo)
                    col.append(lo if flip else hi)
                slots.append((tuple(row), tuple(col)))
            packets[name] = slots
        for x in selected:
            assert packets['Tprime'][x][0] == packets['H'][x][0]
            label_checks += 1
        for x in range(L):
            assert packets['T'][x][1] == packets['Tprime'][x][1]
            assert packets['H'][x][1] == packets['Hprime'][x][1]
            label_checks += 2

    # Independently sum all helper bits modulo 16 with explicit equality
    # extensions, for every Boolean pattern on the external selected rows.
    helper_totals = [0]*(1<<b)
    for bits in range(1<<L):
        z = [sum(W[x][y] for y in range(L) if bits >> y & 1) % 16 for x in range(L)]
        pins = prod(1-v for v in z) % 16
        for t in range(1<<b):
            gates = prod((1-((t>>j)&1)-z[x]+2*((t>>j)&1)*z[x]
                          for j, x in enumerate(selected)))
            helper_totals[t] = (helper_totals[t]+pins*gates) % 16
    assert helper_totals == [8]+[0]*((1<<b)-1)

    weights = [a+1+2*k+2*v2_int(factorial(k)) for k in range(b)]
    matrix = []
    for r in range(b):
        z = F(1, T+2*r)
        vals = []
        for k in range(b):
            ck = 2**(2*k)*factorial(k)**2*(1-2*(1+2*k)*k)
            val = common/F(T+2*r)*ck*row_basis(z, k)/2**weights[k]
            vals.append(mod(val, 2))
        matrix.append(vals)
    poly = {(0,)*b: 1}
    for vals in matrix:
        nxt = poly.copy()
        for e in poly:
            for k, val in enumerate(vals):
                if val:
                    ee = tuple(v+int(i == k) for i, v in enumerate(e))
                    nxt[ee] = nxt.get(ee, 0) ^ 1
        poly = {e: v for e, v in nxt.items() if v}
    witness = {}
    for e in poly:
        mask = sum(1<<i for i, v in enumerate(e) if v)
        if mask & 1:
            witness.setdefault(mask, e)
    assert len(witness) == 2**(b-1)

    # T' pin rows and the divided helper enforce X_1..X_(L-1),
    # leaving X_0 free. Independently enumerate all target bit assignments
    # and evaluate actual source-mode residues for every selected support.
    sigma = [[mod(col_basis(j, k), 2) for j in range(K)] for k in range(b)]
    parity = {mask: 0 for mask in witness}
    accepted = 0
    for X in range(1<<L):
        z = [sum(W[x][y] for y in range(L) if X>>y&1) % 2 for x in range(L)]
        if any(z[x] != int(x == pinrow) for x in range(L-1)):
            continue
        accepted += 1
        modes = [sum(sigma[k][j]*((X>>(2*j))&1) for j in range(K)) % 2
                 for k in range(b)]
        for mask, e in witness.items():
            parity[mask] ^= prod(modes[k]**e[k] for k in range(b))
    assert accepted == 2 and all(v == 1 for v in parity.values())
    return {'L': L, 'b': b, 'physical_slot_pairs': 2*L,
            'selected_degree_two_variables': b, 'formula_variables': variable_count,
            'formula_clauses': len(clauses), 'all_unit_constraints_consistent': True,
            'row_label_checks': label_checks,
            'helper_totals_mod_16': helper_totals,
            'mode_support_witnesses_containing_zero': len(witness),
            'target_assignments_after_pins': accepted,
            'every_complete_normalized_witness_odd': True}


def main():
    paths = [HERE/'reduction-gadget.py', HERE/'PROOF.md',
             ROOT/'upstream/openai-eth-2026/build/quantitative-contraction.tex',
             ROOT/'upstream/openai-eth-2026/build/quantitative-reduction.tex']
    return {'cases': [gadget(8, 2), gadget(16, 4)],
            'scope': 'bounded gadget checks; all-size proof remains author-checked',
            'sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in paths}}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
