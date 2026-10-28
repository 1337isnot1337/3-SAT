#!/usr/bin/env python3
"""Finite controls for concatenated local codes and Tanner parameters."""
import itertools
import json
import math
import random


def params(m, B):
    mu = m.bit_length()
    L = (B+1).bit_length()  # ceil(log2(B+2))
    denom = (1 << 24)*B*B*L
    D = (1 << 54)*B**4*L*L*mu
    d = min(m, D)
    q = 1 << ((m+d-1)//d-1).bit_length()
    c = (d+8*B-1)//(8*B)
    return mu, L, denom, D, d, q, c


def local_params(d, B):
    s = max(1, (d-1).bit_length())
    t = s//(64*B)
    ell = s+t
    N = d//ell
    u = N//(64*B)
    if t:
        ratio_ceil = (2*t+ell+t-1)//t
        Linner = (ratio_ceil-1).bit_length()
        h = t//(64*Linner)
    else:
        h = 0
    return s, t, ell, N, u, h


def make_check(ell, t, h):
    """Exact conditional expectation for a tiny test, scaled by 2**t."""
    bad = [v for v in range(1, 1 << ell) if v.bit_count() <= h]
    assert len(bad) < 1 << t
    rows = [0]*t
    known = [0]*t
    def potential():
        total = 0
        for v in bad:
            uncertain = 0
            for row, mask in zip(rows, known):
                if v & ~mask:
                    uncertain += 1
                elif (v & row).bit_count() & 1:
                    break
            else:
                total += 1 << (t-uncertain)
        return total
    before = potential()
    for j in range(t):
        for i in range(ell):
            known[j] |= 1 << i
            zero = potential()
            rows[j] |= 1 << i
            one = potential()
            if zero <= one:
                rows[j] ^= 1 << i
                after = zero
            else:
                after = one
            assert after <= before
            before = after
    assert before == 0
    assert all(any((v & row).bit_count() & 1 for row in rows) for v in bad)
    return len(bad), rows


def mul8(a, b):
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 8:
            a ^= 0b1011
    return out


def toy_concatenation(inner_rows):
    # Outer GF(8) polynomial code N=7,k=5. The inner encoder is selected
    # from the kernel of the conditional-expectation check matrix above.
    basis = {}
    chosen = []
    for candidate in range(1, 256):
        if any((candidate & row).bit_count() & 1 for row in inner_rows):
            continue
        v = candidate
        while v:
            pivot = v.bit_length()-1
            if pivot not in basis:
                basis[pivot] = v
                chosen.append(candidate)
                break
            v ^= basis[pivot]
        if len(chosen) == 3:
            break
    assert len(chosen) == 3
    inner = [0]*8
    for a in range(8):
        for i in range(3):
            if a >> i & 1:
                inner[a] ^= chosen[i]
    assert all(inner[a].bit_count() >= 2 for a in range(1, 8))
    minimum = 56
    count = 0
    for coeff in itertools.product(range(8), repeat=5):
        if not any(coeff):
            continue
        weight = 0
        for x in range(7):
            value = 0
            for a in reversed(coeff):
                value = mul8(value, x) ^ a
            weight += inner[value].bit_count()
        minimum = min(minimum, weight)
        assert weight >= 6
        count += 1
    return count, minimum


def check_shift_span():
    cases = 0
    for q in (2, 4, 8):
        for degree in (1, 2, 3):
            for shifts in itertools.product(range(q), repeat=degree):
                signs = [abs(sum(1 if (v & b).bit_count() % 2 == 0 else -1
                                 for v in shifts)) for b in range(1, q)]
                if max(signs) < degree:
                    assert degree >= q.bit_length()-1
                cases += 1
    return cases


def main():
    rng = random.Random(834211)
    regimes = {'q1': 0, 'q_gt_1': 0, 'local_fallback': 0, 'local_construct': 0,
               'positive_h': 0}
    for _ in range(20000):
        bits = rng.randint(1, 10000)
        m = rng.randrange(1 << (bits-1), 1 << bits)
        B = rng.randint(1, 1000) if rng.randrange(2) else rng.randint(1, 4)
        n = (m+B-1)//B
        mu, L, denom, D, d, q, c = params(m, B)
        assert m <= q*d < 2*m and 2*q*c <= 3*n
        if q > 1:
            assert d == D and d >= (1 << 53)*B**4*L*L*mu
            regimes['q_gt_1'] += 1
        else:
            regimes['q1'] += 1
        if d < denom:
            regimes['local_fallback'] += 1
            continue
        regimes['local_construct'] += 1
        s,t,ell,N,u,h = local_params(d, B)
        assert 16*B*ell <= d
        assert 4*N*s >= d
        assert N*t + u*s + d-N*ell <= c
        assert (h+1)*40960*B*L >= s
        if h:
            regimes['positive_h'] += 1
    # Exercise the asymptotic positive-h branch directly without allocating
    # any graph: d itself is an integer with 65,537 bits.
    huge_d = 1 << 65536
    s, t, ell, N, u, h = local_params(huge_d, 1)
    assert h > 0 and 16*ell <= huge_d and 4*N*s >= huge_d
    assert N*t + u*s + huge_d-N*ell <= (huge_d+7)//8
    assert (h+1)*40960*2 >= s
    entropy_checks = positive_entropy = 0
    for _ in range(2000):
        s0 = rng.randint(1, 500000)
        B0 = rng.randint(1, 12)
        t0 = s0//(64*B0)
        ell0 = s0+t0
        if t0:
            ratio = (2*t0+ell0+t0-1)//t0
            L0 = (ratio-1).bit_length()
            h0 = t0//(64*L0)
            if h0:
                assert sum(math.comb(ell0, i) for i in range(1, h0+1)) < 1 << t0
                positive_entropy += 1
        else:
            h0 = 0
        assert (h0+1)*40960*B0*(B0+1).bit_length() >= s0
        entropy_checks += 1
    bad1, inner_rows = make_check(8, 4, 1)
    bad2, _ = make_check(8, 7, 2)
    bad_words = bad1 + bad2
    codewords, minimum = toy_concatenation(inner_rows)
    print(json.dumps({'seed': 834211, 'parameter_cases': 20000, 'regimes': regimes,
                      'direct_positive_h': h, 'entropy_checks': entropy_checks,
                      'positive_entropy_cases': positive_entropy,
                      'shift_list_cases': check_shift_span(),
                      'toy_low_weight_words': bad_words, 'toy_codewords': codewords,
                      'toy_min_distance': minimum, 'result': 'pass'}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
