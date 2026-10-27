"""Uniform asymmetric charged first-moment crossing construction."""

from fractions import Fraction as F
from hashlib import sha256
import importlib.util
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "charged-operator-moments"
PINS = {"charged.py": "1afcd1e6e898a06664ebe7ca930047a607e311ae96fd4511c9d24fcf5a48d509",
        "pairing.py": "949d5e4f07d546cab4e4f995f96a6a2b3d534f21ee0ce98470374120226044df",
        "predecessor.py": "efcdb6468673d240e0f794484874c149ac4f313669f7898248c901b100991b2f"}
for name, expected in PINS.items():
    if sha256((PARENT / name).read_bytes()).hexdigest() != expected:
        raise ValueError("Pinned predecessor changed: " + name)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


predecessor = load("predecessor", PARENT / "predecessor.py")
charged = load("asymmetric_charged", PARENT / "charged.py")
pairing = load("asymmetric_pairing", PARENT / "pairing.py")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def partition_count(h):
    if h < 0:
        return 0
    counts = [1] + [0] * h
    for part in range(1, h + 1):
        for n in range(part, h + 1):
            counts[n] += counts[n - part]
    return counts[h]


def grade(bits):
    require(bits >= 1, "Positive input bit count required")
    h = 2
    while partition_count(h) - partition_count(h - 1) < 1 << bits:
        h += 1
    return h


def inverse(matrix):
    n = len(matrix)
    require(n and all(len(row) == n for row in matrix), "Square inverse required")
    rows = [[F(x) for x in row] + [F(int(i == j)) for j in range(n)] for i, row in enumerate(matrix)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if rows[i][j]), None)
        require(pivot is not None, "Selected minor is singular")
        rows[pivot], rows[j] = rows[j], rows[pivot]
        scale = rows[j][j]
        rows[j] = [x / scale for x in rows[j]]
        for i in range(n):
            if i != j and rows[i][j]:
                scale = rows[i][j]
                rows[i] = [x - scale * y for x, y in zip(rows[i], rows[j])]
    return [row[n:] for row in rows]


def minor_indices(matrix, size):
    rows = [list(map(F, row)) for row in matrix]
    names = list(range(len(rows)))
    selected_rows, selected_columns = [], []
    for j in range(len(rows[0])):
        rank = len(selected_rows)
        pivot = next((i for i in range(rank, len(rows)) if rows[i][j]), None)
        if pivot is None:
            continue
        rows[pivot], rows[rank] = rows[rank], rows[pivot]
        names[pivot], names[rank] = names[rank], names[pivot]
        selected_rows.append(names[rank])
        selected_columns.append(j)
        if len(selected_rows) == size:
            return selected_rows, selected_columns
        for i in range(rank + 1, len(rows)):
            if rows[i][j]:
                scale = rows[i][j] / rows[rank][j]
                rows[i] = [x - scale * y for x, y in zip(rows[i], rows[rank])]
    raise ValueError("Pairing rank below requested label dimension")


def construct(bits):
    N, h = 1 << bits, grade(bits)
    states = predecessor.partitions(h)
    matrix = pairing.first_pairing(states)
    rows, columns = minor_indices(matrix, N)
    minor = [[matrix[i][j] for j in columns] for i in rows]
    normalization = inverse(minor)
    require(all(sum((normalization[i][k] * minor[k][j] for k in range(N)), F(0)) == int(i == j)
                for i in range(N) for j in range(N)), "Pairing inverse identity")
    return {"bits": bits, "N": N, "h": h, "states": states,
            "row_indices": rows, "column_indices": columns,
            "row_labels": [states[i] for i in rows], "column_labels": [states[j] for j in columns],
            "output_labels": states[:N], "minor": minor, "inverse": normalization,
            "shifts": [s for s in range(-2 * h, 2 * h + 1) if s]}


def piece(data, shift, check_reverse=False):
    N = data["N"]
    raw = [[[[F(0) for _ in range(N)] for _ in range(N)] for _ in range(N)] for _ in range(N)]
    orders = 0
    # raw[a][y][u][v] is Q_s(row_a, col_v)[output_u, output_y].
    for a, mu in enumerate(data["row_labels"]):
        for v, nu in enumerate(data["column_labels"]):
            for y, argument in enumerate(data["output_labels"]):
                vector = charged.piece_vector(mu, nu, argument, shift, 1)
                if check_reverse or (a == v == y == 0):
                    require(vector == charged.piece_vector(mu, nu, argument, shift, 1, reverse=True),
                            "Positive-grade two-order identity")
                    orders += 1
                values = dict(vector)
                for u, output in enumerate(data["output_labels"]):
                    raw[a][y][u][v] = F(values.get(output, 0))
    normalized = [[[[shift * sum((data["inverse"][x][a] * raw[a][y][u][v] for a in range(N)), F(0))
                     for v in range(N)] for u in range(N)] for y in range(N)] for x in range(N)]
    return raw, normalized, orders
