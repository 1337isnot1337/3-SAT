#!/usr/bin/env python3
"""Actual packet recovery screen; all conclusions are finite."""
import argparse
import itertools
import json
from pathlib import Path
import random
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from previous_probe import packet_data, valuation


def diagonalize(rows, target, precision, certificates=True):
    modulus = 1 << precision
    matrix = [[x % modulus for x in row] for row in rows]
    m, n = len(matrix), len(target)
    transformed = [x % modulus for x in target]
    U = [[int(i == j) for j in range(m)] for i in range(m)] if certificates else None
    V = [[int(i == j) for j in range(n)] for i in range(n)] if certificates else None
    valuations = []
    for k in range(min(m, n)):
        best, where = precision, None
        for i in range(k, m):
            for j in range(k, n):
                v = valuation(matrix[i][j], precision)
                if v < best:
                    best, where = v, (i, j)
                    if best == 0:
                        break
            if best == 0:
                break
        if where is None:
            break
        i, j = where
        matrix[k], matrix[i] = matrix[i], matrix[k]
        if certificates:
            U[k], U[i] = U[i], U[k]
        if j != k:
            for row in matrix:
                row[k], row[j] = row[j], row[k]
            transformed[k], transformed[j] = transformed[j], transformed[k]
            if certificates:
                for row in V:
                    row[k], row[j] = row[j], row[k]
        inverse = pow(matrix[k][k] >> best, -1, modulus)
        matrix[k] = [x * inverse % modulus for x in matrix[k]]
        if certificates:
            U[k] = [x * inverse % modulus for x in U[k]]
        for i in range(k + 1, m):
            factor = matrix[i][k] >> best
            if not factor:
                continue
            matrix[i] = [(x - factor * y) % modulus for x, y in zip(matrix[i], matrix[k])]
            if certificates:
                U[i] = [(x - factor * y) % modulus for x, y in zip(U[i], U[k])]
        for j in range(k + 1, n):
            factor = matrix[k][j] >> best
            if not factor:
                continue
            transformed[j] = (transformed[j] - factor * transformed[k]) % modulus
            if certificates:
                for row in V:
                    row[j] = (row[j] - factor * row[k]) % modulus
            matrix[k][j] = 0
        valuations.append(best)
    rank = len(valuations)
    unresolved = [j for j in range(rank, n) if transformed[j] & 1]
    required = None if unresolved else 1 + max([-1] + [v for j, v in enumerate(valuations) if transformed[j] & 1])
    result = dict(required_precision=required, cutoff=precision,
                  status='cutoff_unresolved' if unresolved else 'finite_exact_threshold',
                  pivot_valuations=valuations, shape=[m, n])
    if not certificates:
        return result
    if required is not None and required > 0:
        q = 1 << required
        dual = [0] * m
        for j, v in enumerate(valuations):
            if transformed[j] & 1:
                factor = 1 << (required - 1 - v)
                dual = [(x + factor * y) % q for x, y in zip(dual, U[j])]
        # Independently substitute into the original matrix, no diagonalizer used.
        assert all(sum(dual[i] * rows[i][j] for i in range(m)) % q == ((1 << (required - 1)) * target[j]) % q for j in range(n))
        result['upper_certificate_verified'] = True
        # At one less bit, a kernel vector changes the target parity.
        bad = next(j for j, v in enumerate(valuations) if v == required - 1 and transformed[j] & 1)
        witness = [V[i][bad] for i in range(n)]
        lower_modulus = 1 << (required - 1)
        assert all(sum(a * x for a, x in zip(row, witness)) % lower_modulus == 0 for row in rows)
        assert sum(a * x for a, x in zip(target, witness)) % 2 == 1
        result['lower_certificate_verified'] = True
    elif unresolved:
        witness = [V[i][unresolved[0]] for i in range(n)]
        assert all(sum(a * x for a, x in zip(row, witness)) % modulus == 0 for row in rows)
        assert sum(a * x for a, x in zip(target, witness)) % 2 == 1
        result['cutoff_kernel_certificate_verified'] = True
    else:
        assert not any(x & 1 for x in target)
    return result


def brute_threshold(rows, target, cutoff):
    if not any(x & 1 for x in target):
        return 0
    for p in range(1, cutoff + 1):
        modulus = 1 << p
        bad = any(sum(t * z for t, z in zip(target, x)) % 2 and
                  all(sum(a * z for a, z in zip(row, x)) % modulus == 0 for row in rows)
                  for x in itertools.product(range(modulus), repeat=len(target)))
        if not bad:
            return p
    return None


def validate():
    count = 0
    for entries in itertools.product(range(4), repeat=4):
        rows = [entries[:2], entries[2:]]
        for target in itertools.product(range(2), repeat=2):
            actual = diagonalize(rows, target, 2)
            assert actual['required_precision'] == brute_threshold(rows, target, 2)
            count += 1
    rng = random.Random(15520261029)
    for _ in range(100):
        rows = [[rng.randrange(8) for _ in range(3)] for _ in range(rng.randrange(1, 5))]
        target = [rng.randrange(2) for _ in range(3)]
        actual = diagonalize(rows, target, 3)
        assert actual['required_precision'] == brute_threshold(rows, target, 3)
        count += 1
    return dict(solver_cases=count, status='pass', method='exhaustive kernel enumeration plus direct dual/kernel certificate substitution')


def joint_data(L, nodes, precision, xs):
    result, target = None, []
    for X in xs:
        rows, goal = packet_data(L, X, nodes, precision)
        if result is None:
            result = rows
        else:
            for accumulated, row in zip(result, rows):
                accumulated.extend(row)
        target.extend(goal)
    return result, target


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--L', type=int, choices=[2, 4, 8], default=4)
    parser.add_argument('--precision', type=int, default=80)
    parser.add_argument('--validate-only', action='store_true')
    args = parser.parse_args()
    if args.validate_only:
        print(json.dumps(validate(), sort_keys=True))
        return
    L = args.L
    for u in range(1, L.bit_length()):
        nodes = [t for t in range(1-L, L) if t and valuation(abs(t), args.precision) < u]
        started = time.monotonic()
        rows, target = joint_data(L, nodes, args.precision, range(1 << L))
        report = diagonalize(rows, target, args.precision, certificates=(L <= 4))
        report.update(L=L, u=u, nodes=nodes, seconds=round(time.monotonic()-started, 3),
                      column_inputs=1 << L, scope='one COMMON recovery functional for every Boolean column input and multilinear row coefficient')
        print(json.dumps(report, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
