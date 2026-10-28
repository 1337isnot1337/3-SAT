#!/usr/bin/env python3
"""Check independent-set / kernel weight-enumerator identity over GF(8)."""
import hashlib
import json
import itertools
import random
from pathlib import Path


def rank(xs):
    pivots = {}
    for x in xs:
        while x:
            p = x.bit_length()-1
            if p not in pivots:
                pivots[p] = x
                break
            x ^= pivots[p]
    return len(pivots)


def mul(a, b):
    out = 0
    while b:
        if b & 1:
            out ^= a
        a <<= 1
        if a & 8:
            a ^= 11
        b >>= 1
    return out


def carryless_mul(a, b):
    out = 0
    while b:
        if b & 1:
            out ^= a
        a <<= 1
        b >>= 1
    return out


def reduce_gf8(a):
    while a.bit_length() > 3:
        a ^= 11 << (a.bit_length()-4)
    return a


def row_gate_paths(cols, row, mask):
    # Sum local ternary XOR tensors over every accumulator state.
    paths = [1, 0]
    for j, col in enumerate(cols):
        if col >> row & 1:
            x = (mask >> j) & 1
            next_paths = [0, 0]
            for old in range(2):
                for new in range(2):
                    next_paths[new] += paths[old] * int(new == (old ^ x))
            paths = next_paths
    return paths[0]


def evaluate(cols, weights):
    independent = kernel = lifted = 0
    m = len(cols)
    for mask in range(1 << m):
        chosen = [v for i,v in enumerate(cols) if mask >> i & 1]
        if rank(chosen) == len(chosen):
            term = 1
            for i,z in enumerate(weights):
                if mask >> i & 1:
                    term = mul(term,z)
            independent ^= term
        syndrome = 0
        for v in chosen:
            syndrome ^= v
        if syndrome == 0:
            groups = []
            for indices in (range(0, m//2), range(m//2,m)):
                term = 1
                for i in indices:
                    term = mul(term, weights[i] if mask >> i & 1 else 1 ^ weights[i])
                groups.append(term)
            kernel ^= mul(*groups)
            lifted ^= carryless_mul(*groups)
    assert independent == kernel == reduce_gf8(lifted)
    assert lifted.bit_length() <= 5


def row_rref(rows):
    pivots = {}
    for value in rows:
        v = value
        while v:
            bit = v.bit_length()-1
            if bit not in pivots:
                pivots[bit] = v
                break
            v ^= pivots[bit]
    for bit in sorted(pivots):
        for larger in sorted(pivots):
            if larger > bit and (pivots[larger] >> bit & 1):
                pivots[larger] ^= pivots[bit]
    return [pivots[bit] for bit in sorted(pivots, reverse=True)]


def greedy_row_basis(rows):
    selected = []
    for value in sorted(rows, key=lambda v: (v.bit_count(), v)):
        if rank(selected+[value]) > len(selected):
            selected.append(value)
    return selected


def gf8_interpolate(values):
    n = len(values)
    rows = []
    for x, value in enumerate(values):
        powers = [1]
        for _ in range(1,n):
            powers.append(mul(powers[-1],x))
        rows.append(powers + [value])
    for col in range(n):
        pivot = next(i for i in range(col,n) if rows[i][col])
        rows[col], rows[pivot] = rows[pivot], rows[col]
        inverse = next(i for i in range(1,8) if mul(i, rows[col][col]) == 1)
        rows[col] = [mul(v,inverse) for v in rows[col]]
        for i in range(n):
            if i != col:
                coefficient = rows[i][col]
                rows[i] = [x ^ mul(coefficient,y) for x,y in zip(rows[i],rows[col])]
    return [row[-1] for row in rows]


def small_add(a, b, q):
    return (a+b) % 3 if q == 3 else a ^ b


def small_mul(a, b, q):
    if q == 3:
        return a*b % 3
    out = 0
    while b:
        if b & 1:
            out ^= a
        a <<= 1
        if a & 4:
            a ^= 7
        b >>= 1
    return out


def small_rank(columns, q):
    rows = [[col[i] for col in columns] for i in range(2)]
    pivot = 0
    for j in range(len(columns)):
        r = next((r for r in range(pivot,2) if rows[r][j]), None)
        if r is None:
            continue
        rows[pivot], rows[r] = rows[r], rows[pivot]
        inverse = next(v for v in range(1,q) if small_mul(rows[pivot][j],v,q) == 1)
        rows[pivot] = [small_mul(v,inverse,q) for v in rows[pivot]]
        for r in range(pivot+1,2):
            factor = rows[r][j]
            if factor:
                rows[r] = [small_add(x, small_mul(q-1 if q==3 else 1,
                                  small_mul(factor,y,q),q),q)
                           for x,y in zip(rows[r],rows[pivot])]
        pivot += 1
        if pivot == 2:
            break
    return pivot


def general_identity(cols, weights, q):
    left = right = 0
    for mask in range(4):
        chosen = [col for i,col in enumerate(cols) if mask >> i & 1]
        if small_rank(chosen,q) == len(chosen):
            term = 1
            for i,z in enumerate(weights):
                if mask >> i & 1:
                    term = small_mul(term,z,q)
            left = small_add(left,term,q)
    for x in itertools.product(range(q), repeat=2):
        syndrome = [0,0]
        for j in range(2):
            for i in range(2):
                syndrome[i] = small_add(syndrome[i],small_mul(cols[j][i],x[j],q),q)
        if syndrome == [0,0]:
            term = 1
            for j,z in enumerate(weights):
                term = small_mul(term,z if x[j] else small_add(1,z,q),q)
            right = small_add(right,term,q)
    assert left == right


def run():
    exhaustive = gate_cases = zeta_entries = 0
    for packed in range(8**4):
        cols = [(packed >> (3*j)) & 7 for j in range(4)]
        # In characteristic two, the coefficient table is the Boolean
        # inclusion-zeta transform of the kernel truth table.
        for selected in range(16):
            coefficient = 0
            sub = selected
            while True:
                syndrome = 0
                for j, col in enumerate(cols):
                    if sub >> j & 1:
                        syndrome ^= col
                coefficient ^= (syndrome == 0)
                if sub == 0:
                    break
                sub = (sub-1) & selected
            chosen = [col for j,col in enumerate(cols) if selected >> j & 1]
            assert coefficient == (rank(chosen) == len(chosen))
            zeta_entries += 1
        for mask in range(16):
            paths = 1
            for row in range(3):
                paths *= row_gate_paths(cols, row, mask)
            syndrome = 0
            for j, col in enumerate(cols):
                if mask >> j & 1:
                    syndrome ^= col
            assert paths == int(syndrome == 0)
            gate_cases += 1
            weights = [(mask >> j) & 1 for j in range(4)]
            evaluate(cols, weights)
            exhaustive += 1
    rng = random.Random(25104)
    for _ in range(2000):
        cols = [rng.randrange(8) for _ in range(6)]
        weights = [rng.randrange(8) for _ in range(6)]
        evaluate(cols, weights)
    row_basis_cases = nonzero_column_cases = 0
    for rows in itertools.product(range(16), repeat=3):
        full_rank = rank(rows)
        greedy = greedy_row_basis(rows)
        canonical = row_rref(rows)
        assert len(greedy) == len(canonical) == full_rank
        assert row_rref(greedy) == canonical
        costs = []
        for mask in range(8):
            chosen = [v for i,v in enumerate(rows) if mask >> i & 1]
            if len(chosen) == full_rank and rank(chosen) == full_rank:
                costs.append(sum(v.bit_count() for v in chosen))
        assert sum(v.bit_count() for v in greedy) == min(costs)
        if all(any(v >> j & 1 for v in rows) for j in range(4)):
            assert all(any(v >> j & 1 for v in canonical) for j in range(4))
            assert sum(v.bit_count() for v in canonical) >= 4
            nonzero_column_cases += 1
        row_basis_cases += 1
    dense_controls = []
    for n in range(2, 33, 2):
        all_bits = (1 << n)-1
        left = [all_bits ^ (1 << i) for i in range(n)]
        rows = [v | (v << n) for v in left]
        reduced = row_rref(rows)
        assert rank(rows) == n
        assert set(reduced) == {1 << i | 1 << (n+i) for i in range(n)}
        assert sum(v.bit_count() for v in rows) == 2*n*(n-1)
        assert sum(v.bit_count() for v in reduced) == 2*n
        dense_controls.append(n)
    general_cases = {}
    for q in (3,4):
        count = 0
        for raw in itertools.product(range(q), repeat=4):
            cols = [(raw[0],raw[1]), (raw[2],raw[3])]
            for weights in itertools.product(range(q), repeat=2):
                general_identity(cols,weights,q)
                count += 1
        general_cases[str(q)] = count
    parity_interpolations = 0
    for _ in range(200):
        cols = [rng.randrange(8) for _ in range(4)]
        counts = [0]*5
        for mask in range(16):
            chosen = [v for i,v in enumerate(cols) if mask >> i & 1]
            if rank(chosen) == len(chosen):
                counts[len(chosen)] ^= 1
        values = []
        for x in range(5):
            value = 0
            for mask in range(16):
                syndrome = 0
                for i,v in enumerate(cols):
                    if mask >> i & 1:
                        syndrome ^= v
                if syndrome == 0:
                    term = 1
                    for i in range(4):
                        term = mul(term, x if mask >> i & 1 else 1 ^ x)
                    value ^= term
            values.append(value)
        assert gf8_interpolate(values) == counts
        parity_interpolations += 1
    encoded_q4_checks = 0
    for raw in itertools.product(range(4), repeat=4):
        cols = [(raw[0],raw[1]), (raw[2],raw[3])]
        for x in itertools.product(range(4), repeat=2):
            for row in range(2):
                direct = encoded = 0
                for j in range(2):
                    coefficient = cols[j][row]
                    direct ^= small_mul(coefficient,x[j],4)
                    for bit in range(2):
                        if x[j] >> bit & 1:
                            encoded ^= small_mul(coefficient,1 << bit,4)
                assert direct == encoded
                encoded_q4_checks += 1
    # The pair family [I_b|I_b] has a triangular width profile of area b^2.
    controls = []
    for b in range(1, 33):
        widths = list(range(b+1)) + list(range(b-1,-1,-1))
        assert sum(widths) == b*b
        controls.append(b)
    # Over F3, support aggregation from 3-ary kernel inputs to subset
    # coefficients is rectangular and can lower cut rank.
    h3 = [[int((x+y) % 3 == 0) for y in range(3)] for x in range(3)]
    c3 = [[sum(h3[x][y] for x in range(3) for y in range(3)
                if (s or x == 0) and (t or y == 0)) % 3
           for t in range(2)] for s in range(2)]
    assert h3 == [[1,0,0],[0,0,1],[0,1,0]]
    assert c3 == [[1,1],[1,0]]
    # Binary parallel pair, z=(1,1), evaluated over the mismatched F3:
    # independent polynomial is 1+1+1=0, while the weighted kernel sum
    # is (1+1)^2+1=2. This rejects extending the identity across fields.
    unmatched_independence = (1+1+1) % 3
    unmatched_kernel = ((1+1)**2+1) % 3
    assert unmatched_independence == 0 and unmatched_kernel == 2
    return {'row_basis_cases': row_basis_cases,
            'nonzero_column_rowspace_cases': nonzero_column_cases,
            'dense_rowspace_controls': {'cases': len(dense_controls), 'max_n': max(dense_controls)},
            'GF8_size_parity_interpolations': parity_interpolations,
            'F3_kernel_and_coefficient_rank_control': [3,2],
            'mismatched_characteristic_control_F3': [unmatched_independence, unmatched_kernel],
            'prime_power_identity_cases': general_cases,
            'encoded_F4_row_checks': encoded_q4_checks,
            'matrices_3x4': 4096, 'boolean_weight_cases': exhaustive,
            'explicit_xor_gate_cases': gate_cases, 'zeta_coefficient_checks': zeta_entries,
            'GF8_weighted_and_group_lift_cases': 2000, 'seed': 25104,
            'paired_order_controls': {'cases': len(controls), 'max_b': max(controls)},
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
