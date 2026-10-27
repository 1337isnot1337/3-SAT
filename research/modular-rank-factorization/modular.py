"""Deterministic rank factorization over Z/(2^precision), including zero divisors.

This is standard local-ring elimination, exposed as outer-product peeling.
The application to precision-controlled crossing factors is separate.
"""


def require(condition, message):
    if not condition:
        raise ValueError(message)


def valuation(x, precision):
    return (x & -x).bit_length() - 1 if x else precision


def factor(matrix, precision):
    require(precision >= 1 and matrix and matrix[0], "Nonempty matrix and positive precision required")
    m, n = len(matrix), len(matrix[0])
    require(all(len(row) == n for row in matrix), "Ragged matrix")
    modulus = 1 << precision
    residual = [[x % modulus for x in row] for row in matrix]
    columns, rows, valuations = [], [], []
    while True:
        v, i, j = min((valuation(residual[i][j], precision), i, j)
                      for i in range(m) for j in range(n))
        if v == precision:
            break
        odd = residual[i][j] >> v
        inverse = pow(odd, -1, modulus)
        column = [row[j] * inverse % modulus for row in residual]
        row = [x >> v for x in residual[i]]
        require(column[i] == 1 << v, "Normalized pivot")
        residual = [[(x - a * b) % modulus for x, b in zip(old, row)]
                    for old, a in zip(residual, column)]
        require(not any(residual[i]) and not any(line[j] for line in residual), "Pivot row/column elimination")
        columns.append(column)
        rows.append(row)
        valuations.append(v)
        require(len(rows) <= min(m, n), "Nonterminating elimination")
    return {"left": [[column[i] for column in columns] for i in range(m)],
            "right": rows, "inner_dimension": len(rows), "pivot_valuations": valuations,
            "precision": precision, "shape": [m, n]}


def reconstruct(data):
    modulus = 1 << data["precision"]
    n = data["shape"][1]
    return [[sum(a * row[j] for a, row in zip(left, data["right"])) % modulus for j in range(n)]
            for left in data["left"]]


def exact_division_residue(residue, multiplier, output_precision):
    """Recover z mod 2^b from multiplier*z mod 2^(b+v2(multiplier))."""
    require(multiplier > 0 and output_precision >= 1, "Positive multiplier and precision required")
    v = (multiplier & -multiplier).bit_length() - 1
    require(residue % (1 << v) == 0, "Insufficient or inconsistent division residue")
    modulus = 1 << output_precision
    return ((residue >> v) * pow(multiplier >> v, -1, modulus)) % modulus
