#!/usr/bin/env python3
"""Exhaustive bounded checks of affine index sampling and row rejection."""
import json


def mul(a, b, modulus, q):
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & q:
            a ^= modulus
    return out


def parity(x):
    return x.bit_count() & 1


def trace(value, q, modulus):
    acc = 0
    term = value
    for _ in range(q.bit_length() - 1):
        acc ^= term
        term = mul(term, term, modulus, q)
    assert acc in (0, 1)
    return acc


def check_trace_coefficients():
    total = 0
    for length, q, modulus in [(1, 16, 0b10011), (2, 32, 0b100101),
                                (3, 64, 0b1000011), (4, 64, 0b1000011),
                                (5, 128, 0b10000011), (6, 128, 0b10000011),
                                (7, 128, 0b10000011), (8, 128, 0b10000011)]:
        assert q >= 16 * length
        # For each nonzero field multiplier, check that the trace functional
        # takes each bit value exactly q/2 times over all seeds a.
        for value in range(1, q):
            assert sum(trace(mul(a, value, modulus, q), q, modulus)
                       for a in range(q)) == q // 2
        powers = []
        for x in range(q):
            row = [1]
            for _ in range(1, length):
                row.append(mul(row[-1], x, modulus, q))
            powers.append(row)
        for hit in range(1, 1 << length):
            nonzero = 0
            for row in powers:
                value = 0
                for i in range(length):
                    if hit >> i & 1:
                        value ^= row[i]
                nonzero += value != 0
            assert 16 * nonzero >= 15 * q, (length, hit, nonzero)
            total += 1
    return total


def main():
    # A hit pattern describes the positions, including repeated indices, whose
    # violation bits are one. Exhaust all coefficient strings independently.
    coefficient_patterns = 0
    for length in range(1, 9):
        for hit in range(1 << length):
            rejected = sum(parity(hit & bits) for bits in range(1 << length))
            assert rejected == (0 if hit == 0 else 1 << (length - 1))
            coefficient_patterns += 1

    cases = supports = seed_supports = 0
    for q, modulus in [(2, 3), (4, 7), (8, 11)]:
        for m in sorted({q // 2 + 1, q}):
            if m > q:
                continue
            for p in (1, 2, 3, 4, 5):
                length = 2 * p
                if length <= q:
                    rows = [tuple(mul(a, i, modulus, q) ^ b for i in range(length))
                            for a in range(q) for b in range(q)]
                    # Verify uniformity of all pairs of positions directly.
                    for i in range(length):
                        for j in range(i + 1, length):
                            pairs = {(row[i], row[j]) for row in rows}
                            assert len(pairs) == q*q
                else:
                    rows = [tuple(range(q))]
                for support in range(1, 1 << m):
                    weight = support.bit_count()
                    if weight * p < m:
                        continue
                    hits = sum(any((support >> x) & 1 for x in row) for row in rows)
                    assert 2 * hits >= len(rows), (q, m, p, support, hits)
                    # Conditional on a hit, independent coefficients reject half
                    # the time; the preceding exhaustive check covers lengths<=8.
                    supports += 1
                    seed_supports += len(rows)
                cases += 1
    print(json.dumps({"parameter_cases": cases, "qualifying_supports": supports,
                      "seed_support_pairs": seed_supports,
                      "coefficient_hit_patterns": coefficient_patterns,
                      "fields": [2, 4, 8],
                      "trace_hit_patterns": check_trace_coefficients(),
                      "result": "pass"}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
