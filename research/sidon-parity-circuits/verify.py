#!/usr/bin/env python3
"""Exact bounded checks for the Sidon-row parity circuit construction."""
from itertools import combinations, product
from math import isqrt


def rows(n):
    # This equals floor(log2(n)) - 2 and ensures the wrap separation.
    length = n.bit_length() - 3
    if length < 2:
        raise ValueError('n must be at least 16')
    shifts = [1 << j for j in range(length)]
    return [frozenset((i + shift) % n for shift in shifts) for i in range(n)]


def check_structure(n):
    supports = rows(n)
    length = len(supports[0])
    assert all(len(row) == length for row in supports)
    assert all(len(a & b) <= 1 for a, b in combinations(supports, 2))
    # m_j = x_j x_(j+1); count original variable scopes per row.
    scopes = [{v for j in row for v in (j, (j + 1) % n)} for row in supports]
    loads = [sum(v in scope for scope in scopes) for v in range(n)]
    total = sum(map(len, scopes))
    lam = (n - 1).bit_length()
    root = isqrt(lam)
    threshold = max(1, (total + n - 1) // n) * (root + (root * root != lam))
    assert max(loads) <= threshold
    # Left-associated tree; distinct non-singleton supports certify no
    # shared internal gate in this construction.
    gates = set()
    internal_wires = 0
    for row in supports:
        terms = sorted(row)
        for i in range(2, length + 1):
            gate = frozenset(terms[:i])
            assert gate not in gates
            gates.add(gate)
        internal_wires += max(0, length - 2)
    assert len(gates) == n * (length - 1)
    assert internal_wires == n * (length - 2)
    return n, length, total, max(loads), threshold, len(gates), internal_wires


def check_gate_semantics():
    checks = 0
    # Test equality constraints at each gate using all candidate auxiliary
    # bits, not just a simulation of the intended output.
    for length in range(2, 6):
        for bits in product((0, 1), repeat=length):
            expected = sum(bits) % 2
            for aux in product((0, 1), repeat=length - 1):
                valid = aux[0] == (bits[0] ^ bits[1])
                for j in range(2, length):
                    valid &= aux[j - 1] == (aux[j - 2] ^ bits[j])
                if valid:
                    assert aux[-1] == expected
                checks += 1
            # There is exactly one extension satisfying all local gates.
            extensions = sum(all(
                aux[j - 1] == ((bits[0] ^ bits[1]) if j == 1
                               else (aux[j - 2] ^ bits[j]))
                for j in range(1, length))
                for aux in product((0, 1), repeat=length - 1))
            assert extensions == 1
    return checks


def check_boolean_realization(n):
    supports = rows(n)
    checks = 0
    for row in supports:
        scope = sorted({v for j in row for v in (j, (j + 1) % n)})
        for bits in product((0, 1), repeat=len(scope)):
            value = dict(zip(scope, bits))
            terms = [value[j] & value[(j + 1) % n] for j in sorted(row)]
            accumulator = terms[0]
            for term in terms[1:]:
                accumulator ^= term
            assert accumulator == sum(terms) % 2
            checks += 1
    return checks


def main():
    print('n L incidences max_load threshold gates internal_gate_wires')
    for n in (16, 20, 31, 32, 64, 100, 128, 256, 512):
        print(*check_structure(n))
    print('gate_constraint_assignments', check_gate_semantics())
    print('quadratic_scope_assignments', sum(check_boolean_realization(n) for n in (16, 20, 32, 64)))
    print('All checks passed.')


if __name__ == '__main__':
    main()
