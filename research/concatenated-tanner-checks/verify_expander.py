#!/usr/bin/env python3
"""Exact small Margulis graph, powering, port and padding controls."""
import itertools
import json
import math


def moves(v, n):
    x, y = v
    return [((x+2*y)%n, y), (x, (y+2*x)%n),
            ((x+2*y+1)%n, y), (x, (y+2*x+1)%n),
            ((x-2*y)%n, y), (x, (y-2*x)%n),
            ((x-2*y-1)%n, y), (x, (y-2*x-1)%n)]


def graph(n):
    vertices = [(x, y) for x in range(n) for y in range(n)]
    index = {v: i for i, v in enumerate(vertices)}
    ports = [[index[w] for w in moves(v, n)] for v in vertices]
    q = len(vertices)
    A = [[sum(w == j for w in ports[i]) for j in range(q)] for i in range(q)]
    assert all(sum(row) == 8 for row in A)
    assert all(A[i][j] == A[j][i] for i in range(q) for j in range(q))
    for port in range(8):
        assert len({ports[v][port] for v in range(q)}) == q
    return A


def product(A, B):
    q = len(A)
    return [[sum(A[i][k]*B[k][j] for k in range(q))
             for j in range(q)] for i in range(q)]


def check_mixing(A, exponent):
    q = len(A)
    degree = 8**exponent
    assert all(sum(row) == degree for row in A)
    weights = [v.bit_count() for v in range(1 << q)]
    cases = 0
    for left in range(1 << q):
        vec = [sum(A[i][j] for i in range(q) if left >> i & 1) for j in range(q)]
        edge = [0]*(1 << q)
        for right in range(1, 1 << q):
            low = right & -right
            edge[right] = edge[right ^ low] + vec[low.bit_length()-1]
        for right, count in enumerate(edge):
            discrepancy = q*count-degree*weights[left]*weights[right]
            assert 100**exponent * discrepancy**2 <= (
                81**exponent * degree**2 * q**2 * weights[left] * weights[right])
            cases += 1
    return cases


def check_port_inverses():
    inverse = (4, 5, 6, 7, 0, 1, 2, 3)
    cases = 0
    for n in (2, 3):
        for k in (1, 2, 3):
            for word in itertools.product(range(8), repeat=k):
                for x in range(n):
                    for y in range(n):
                        v = (x, y)
                        for port in word:
                            v = moves(v, n)[port]
                        for port in reversed(word):
                            v = moves(v, n)[inverse[port]]
                        assert v == (x, y)
                        cases += 1
    return cases


def check_sampler_bias():
    subcodes = 0
    for n in range(2, 5):
        for a in range(1, 1 << n):
            for b in range(a+1, 1 << n):
                assert min(a.bit_count(), b.bit_count(), (a ^ b).bit_count())*3 <= 2*n
                subcodes += 1
    cases = 0
    for w in range(1, 5):
        for k in range(1, 4):
            good = 0
            for samples in itertools.product(range(8), repeat=k):
                parity = 0
                for z in samples:
                    index, coefficient = z//2, z%2
                    parity ^= coefficient * (index < w)
                good += parity == 0
            assert 2*good == 8**k + (2*(4-w))**k
            cases += 1
    return subcodes, cases


def main():
    cases = 0
    for n in (2, 3):
        A = graph(n)
        power = A
        for exponent in (1, 2, 3):
            cases += check_mixing(power, exponent)
            power = product(power, A)
    # Exact integer attenuation and padding/row-count checks, not a source-scale
    # graph construction; the actual theorem uses a very large powered degree.
    assert 2*9**10 < 10**10
    assert 2*25**3 < 32**3
    schedules = 0
    for B in range(1, 101):
        LB = (4*B+1).bit_length()
        K = (1 << 24)*(4*B)**2*LB
        k = 6*((2*K-1).bit_length())
        D = 8**k
        for factor in (1, 2, 3, 4, 5, 16, 100):
            m = D*factor
            n = (m+B-1)//B
            d = min(m, D)
            c = (d+32*B-1)//(32*B)
            if m <= D:
                q = 1
            else:
                need = (m+d-1)//d
                side = math.isqrt(need)
                if side*side < need:
                    side += 1
                q = side*side
            assert m <= q*d < 4*m
            assert 2*q*c <= 3*n
            schedules += 1
    subcodes, sampler_cases = check_sampler_bias()
    print(json.dumps({'result':'pass', 'mixing_subset_pairs':cases,
                      'subcodes_checked':subcodes, 'sampler_bias_cases':sampler_cases,
                      'padding_schedules':schedules, 'base_graph_sides':[2,3],
                      'powers':[1,2,3], 'port_inverse_cases':check_port_inverses()},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
