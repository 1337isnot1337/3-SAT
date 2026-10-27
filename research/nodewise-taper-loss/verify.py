#!/usr/bin/env python3
"""Exact nodewise maximum-principle and primal/dual checks; no SAT solver."""

from fractions import Fraction as F
from itertools import product
from math import ceil, comb
import json


def require(value, message):
    if not value:
        raise ValueError(message)


def v2(n):
    n = abs(n)
    require(n > 0, "valuation of zero")
    return (n & -n).bit_length() - 1


def node_data(a, u):
    L = 2**a
    nodes = [t for t in range(-L, L) if t and v2(t) < u]
    levels = [v2(t) for t in nodes]
    matrix = [[(a + 1 if t == s else v2(t - s)) - levels[j]
               for j, s in enumerate(nodes)] for t in nodes]
    return L, nodes, levels, matrix


def level_matrix(a, u):
    return [[2 - F(1, 2**(a-i)) if i == j else
             -F(j-i, 2**(j-i)) if j > i else F(0)
             for j in range(u)] for i in range(u)]


def exhaustive_maxima():
    checked = 0
    for a, u, alphabet in ((2, 2, range(3)), (3, 3, range(2))):
        L, nodes, levels, matrix = node_data(a, u)
        for q in product(alphabet, repeat=len(nodes)):
            mass = sum(q)
            if not mass:
                continue
            # P_t/D_t multiplied by L: P_t * 2^v2(t).
            scaled = [sum(c*x for c, x in zip(row, q)) * 2**levels[i]
                      for i, row in enumerate(matrix)]
            active = max(value for value, x in zip(scaled, q) if x)
            require(active == max(scaled), "maximum principle failed")
            require(2*u*active >= mass, "normalized loss floor failed")
            checked += 1
    return checked


def certificates():
    samples = []
    lifted_columns = 0
    for a, u in ((1, 1), (2, 1), (2, 2), (3, 2), (3, 3), (4, 4),
                 (16, 8), (32, 16), (64, 32), (128, 64)):
        B = level_matrix(a, u)
        w = [F(1, 2**i) for i in range(u)]
        v = [F(0)] * u
        for i in reversed(range(u)):
            v[i] = (1 - sum((B[i][j]*v[j] for j in range(i+1, u)), F(0))) / B[i][i]
        y = [F(0)] * u
        for i in range(u):
            y[i] = (w[i] - sum((B[j][i]*y[j] for j in range(i)), F(0))) / B[i][i]
        require(all(t > 0 for t in v + y), "nonpositive certificate")
        require(all(sum((B[i][j]*v[j] for j in range(u)), F(0)) == 1 for i in range(u)),
                "primal residual")
        require(all(sum((B[j][i]*y[j] for j in range(u)), F(0)) == w[i] for i in range(u)),
                "dual residual")
        normalizer = sum((w[i]*v[i] for i in range(u)), F(0))
        require(normalizer == sum(y), "objective mismatch")
        require(F(1, 2*u) <= 1/normalizer <= F(9, u), "two-sided envelope failed")
        if a <= 4:
            L, nodes, levels, matrix = node_data(a, u)
            counts = [sum(i == j for j in levels) for i in range(u)]
            for row, i in zip(matrix, levels):
                for j in range(u):
                    average = F(sum(row[k] for k, level in enumerate(levels) if level == j),
                                2**(a-i))
                    require(average == B[i][j], "full-node to level reduction mismatch")
            for col in range(len(nodes)):
                dual = sum((y[i] / counts[i] * F(matrix[t][col], 2**(a-i))
                            for t, i in enumerate(levels)), F(0))
                require(dual == F(1, L), "lifted nodewise dual identity failed")
                lifted_columns += 1
        samples.append({"a": a, "u": u, "u_times_optimum_W1": float(u/normalizer)})
    return {"exact_primal_dual_certificates": len(samples),
            "lifted_nodewise_dual_columns": lifted_columns, "samples": samples}


def top_jet_check():
    checked = 0
    for a, u in ((2, 2), (3, 2)):
        L, nodes, levels, matrix = node_data(a, u)
        q = [1 + j % 3 for j in range(len(nodes))]
        for i, t in enumerate(nodes):
            coefficient = F(1)
            for j, s in enumerate(nodes):
                if j != i:
                    coefficient *= F(-s, t-s)**q[j]
            coefficient *= F(-t, 2**(a+1))**(q[i]-1)
            loss = v2(coefficient.denominator) - v2(coefficient.numerator)
            P = sum(c*x for c, x in zip(matrix[i], q))
            require(loss == P - (a+1-levels[i]), "highest-jet valuation mismatch")
            checked += 1
    return checked


def blind_polynomials():
    witnesses = []
    for a, u, M in ((2, 1, 16), (3, 2, 32)):
        L, nodes, levels, matrix = node_data(a, u)
        B = level_matrix(a, u)
        v = [F(0)] * u
        for i in reversed(range(u)):
            v[i] = (1 - sum((B[i][j]*v[j] for j in range(i+1, u)), F(0))) / B[i][i]
        q = [ceil(F(M, 4*u)*x) for x in v]
        coefficients = [F(1)]
        for s, i in zip(nodes, levels):
            for _ in range(q[i]):
                expanded = coefficients + [F(0)]
                for j, c in enumerate(coefficients):
                    expanded[j+1] -= c/s
                coefficients = expanded
        degree = len(coefficients)-1
        require(coefficients[0] == 1, "blind witness constant is not one")
        require(degree <= M*(2*L-1), "blind witness degree exceeds source cap")
        contents = []
        for t in range(-L, L):
            chart = [sum((c*comb(j, k)*t**(j-k) for j, c in enumerate(coefficients)
                          if j >= k), F(0)) * (2*L)**k for k in range(degree+1)]
            content = min(v2(c.numerator)-v2(c.denominator) for c in chart if c)
            require(content >= 0, "nonintegral witness chart")
            if t in nodes:
                index = nodes.index(t)
                expected = sum(c*q[i] for c, i in zip(matrix[index], levels))
                require(content == expected, "Gauss valuation formula mismatch")
                require(content >= M*2**(a-levels[index]) // (8*u),
                        "retained chart precision floor failed")
            else:
                require(content == 0, "omitted chart should have content zero")
            contents.append({"node": t, "gauss_valuation": content})
        witnesses.append({"a": a, "u": u, "M": M, "level_multiplicities": q,
                          "degree": degree, "charts": contents})
    return witnesses


if __name__ == "__main__":
    print(json.dumps({"status": "PASS", "scope": "finite exact checks of nodewise loss optimization; no improved alpha",
                      "exhaustive_nonzero_multiplicity_vectors": exhaustive_maxima(),
                      "certificates": certificates(), "exact_top_jet_coefficients": top_jet_check(),
                      "generic_joint_recovery_witnesses": blind_polynomials()}, indent=2))
