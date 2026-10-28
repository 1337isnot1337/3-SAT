#!/usr/bin/env python3
"""Finite matrix and direct polynomial commutator checks."""
from itertools import product
from fractions import Fraction


def rank(matrix):
    m = [[Fraction(x) for x in row] for row in matrix]
    r = 0
    for col in range(len(m[0])):
        pivot = next((i for i in range(r, len(m)) if m[i][col]), None)
        if pivot is None:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        v = m[r][col]
        m[r] = [x/v for x in m[r]]
        for i in range(r+1, len(m)):
            v = m[i][col]
            m[i] = [x-v*y for x,y in zip(m[i], m[r])]
        r += 1
    return r


def main():
    cases = 0
    for bits in product((0, 1), repeat=12):
        matrices = [bits[4*i:4*i+4] for i in range(3)]
        def g(k, b, a):
            if k == 0:
                return 0
            m = matrices[abs(k)-1]
            return m[2*b+a] if k > 0 else -m[2*a+b]
        identity = all(g(s-1,b,a)-2*g(s,b,a)+g(s+1,b,a) == 0
                       for s in (0, 1, 2) for b in range(2) for a in range(2))
        c1, c2, c3 = matrices
        criterion = (c1[1] == c1[2] and
                     all(c2[i] == 2*c1[i] and c3[i] == 3*c1[i]
                         for i in range(4)))
        assert identity == criterion
        cases += 1
    # Include nonzero positive and nonsymmetric zero-shift controls.
    for c in product(range(-1, 2), repeat=4):
        c2, c3 = tuple(2*x for x in c), tuple(3*x for x in c)
        assert all(c2[i] == 2*c[i] and c3[i] == 3*c[i] for i in range(4))
        zero_shift = all(c[2*b+a] == c[2*a+b] for a in range(2) for b in range(2))
        assert zero_shift == (c[1] == c[2])
    # Independently apply creation and derivation to monomials in 2 variables.
    comparisons = 0
    for A in product((-1, 0, 1), repeat=4):
        for B in product((-1, 0, 1), repeat=4):
            for a, b, p, q in product(range(2), range(2), range(3), range(3)):
                # Coefficient of each resulting monomial in D_b D_-a - D_-a D_b.
                coeffs = {}
                powers = (p, q)
                for i in range(2):
                    for j in range(2):
                        shifted = list(powers)
                        shifted[j] += 1
                        factor = A[2*a+j] * B[2*b+i] * shifted[i]
                        shifted[i] -= 1
                        coeffs[tuple(shifted)] = coeffs.get(tuple(shifted), 0) + factor
                        if powers[i]:
                            shifted = list(powers)
                            shifted[i] -= 1
                            shifted[j] += 1
                            factor = A[2*a+j] * B[2*b+i] * powers[i]
                            coeffs[tuple(shifted)] = coeffs.get(tuple(shifted), 0) - factor
                expected = sum(A[2*a+j] * B[2*b+j] for j in range(2))
                assert all(v == (expected if mon == powers else 0) for mon,v in coeffs.items())
                assert coeffs.get(powers, 0) == expected
                comparisons += 1
    words = ((0, 0), (0, 1), (1, 1))
    for entries in product(range(-1, 2), repeat=4):
        c = [entries[:2], entries[2:]]
        gram = [[c[u[0]][v[0]]*c[u[1]][v[1]] + c[u[0]][v[1]]*c[u[1]][v[0]]
                 for v in words] for u in words]
        r = rank(c)
        assert rank(gram) == r*(r+1)//2
    print(f'PASS: {cases} three-grade binary matrix cases, 81 scaled controls, {comparisons} direct commutators, 81 degree-two pairing ranks')


if __name__ == '__main__':
    main()
