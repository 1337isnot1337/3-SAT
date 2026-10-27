"""Bounded field rank factors and exact signed-query recovery.

The caller must supply a certified prime. This module does not implement
the polynomial-time primality algorithm used by the all-size argument.
"""


class BadPrime(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rational_residue(value, prime):
    denominator = value.denominator % prime
    if not denominator:
        raise BadPrime("Rational denominator vanishes modulo the selected prime")
    return value.numerator * pow(denominator, -1, prime) % prime


def factor(matrix, prime):
    require(prime >= 3 and matrix and matrix[0], "Odd certified prime and nonempty matrix required")
    m, n = len(matrix), len(matrix[0])
    require(all(len(row) == n for row in matrix), "Ragged matrix")
    residual = [[x % prime for x in row] for row in matrix]
    columns, rows = [], []
    while True:
        pivot = next(((i, j) for i in range(m) for j in range(n) if residual[i][j]), None)
        if pivot is None:
            break
        i, j = pivot
        inverse = pow(residual[i][j], -1, prime)
        column = [row[j] for row in residual]
        row = [x * inverse % prime for x in residual[i]]
        residual = [[(x - a * b) % prime for x, b in zip(old, row)]
                    for old, a in zip(residual, column)]
        columns.append(column)
        rows.append(row)
        require(len(rows) <= min(m, n), "Nonterminating field elimination")
    return {"left": [[column[i] for column in columns] for i in range(m)],
            "right": rows, "inner_dimension": len(rows), "shape": [m, n], "prime": prime}


def normalizer_residue(value, prime):
    residue = rational_residue(value, prime)
    if not residue:
        raise BadPrime("Crossing normalizer vanishes modulo the selected prime")
    return residue


def reconstruct(data):
    return [[sum(a * row[j] for a, row in zip(left, data["right"])) % data["prime"]
             for j in range(data["shape"][1])] for left in data["left"]]


def recover_signed(residue, prime, absolute_bound):
    require(absolute_bound >= 0 and prime > 2 * absolute_bound, "Prime does not cover the integer query range")
    value = residue % prime
    if value > prime // 2:
        value -= prime
    require(abs(value) <= absolute_bound, "Recovered query exceeds its proved bound")
    return value


def bounded_prime_sample(bits, candidates, primality_test):
    """Test at most 64*bits candidates from the specified dyadic interval.

    Production analysis uses independent uniform candidates and a deterministic
    polynomial-time primality test. Bounded checkers supply finite fixtures.
    """
    require(bits >= 8, "Registered sampler range starts at eight bits")
    iterator = iter(candidates)
    for _ in range(64 * bits):
        try:
            candidate = next(iterator)
        except StopIteration:
            return None
        require(1 << bits <= candidate < 1 << (bits + 1), "Candidate outside prime interval")
        if primality_test(candidate):
            return candidate
    return None
