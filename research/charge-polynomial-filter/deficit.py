"""Exact finite screen of charge-dependent contraction-deficit rescaling."""
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


poly = load("charge_deficit_polynomial", HERE / "polynomial.py")
linear = load("charge_deficit_linear", HERE / "linear.py")
require = poly.require


def digest(value):
    return sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def build_tensors(data):
    N, h = data["N"], data["h"]
    degree = max(map(len, data["row_labels"])) + max(map(len, data["column_labels"]))
    tensors = {}
    for shift in range(-2 * h, 2 * h + 1):
        columns = [[0] * (N ** 4) for _ in range(degree + 1)]
        for x, mu in enumerate(data["row_labels"]):
            for v, nu in enumerate(data["column_labels"]):
                pair_degree = len(mu) + len(nu)
                for y, argument in enumerate(data["output_labels"]):
                    vector = poly.piece_vector(mu, nu, argument, shift)
                    values = dict(vector)
                    for u, output in enumerate(data["output_labels"]):
                        index = ((x * N + y) * N + u) * N + v
                        for d, coefficient in enumerate(values.get(output, ())):
                            deficit = pair_degree - d
                            columns[deficit][index] = coefficient
        for deficit, column in enumerate(columns):
            if any(column):
                tensors[deficit, shift] = column
        print(f"deficit lambda={data['bits']}, shift={shift}", file=sys.stderr, flush=True)
    poly.clear_caches()
    return tensors, degree


def classify(tensors, N, h, degree, cutoff):
    names = sorted((d, s) for d, s in tensors if abs(s) > cutoff)
    columns = [tensors[name] for name in names]
    constraints = []
    for x in range(N):
        for v in range(N):
            base = x * N ** 3 + v
            for y in range(N):
                for u in range(N):
                    index = ((x * N + y) * N + u) * N + v
                    if y != u:
                        row = [column[index] for column in columns]
                    elif y:
                        row = [column[index] - column[base] for column in columns]
                    else:
                        continue
                    if any(row):
                        constraints.append(row)
    nullbasis, rank = linear.nullspace(constraints, len(columns))
    pairings = [[sum(weight * column[x * N ** 3 + v]
                     for weight, column in zip(weights, columns))
                 for x in range(N) for v in range(N)] for weights in nullbasis]
    _, _, selected = linear.echelon(pairings, N * N)
    space = [pairings[j] for j in selected]
    representatives = [nullbasis[j] for j in selected]
    polynomial = linear.determinant_polynomial(space, N)
    for offset in (0, 1, 3):
        values = [(j + offset) % 5 for j in range(len(space))]
        matrix = [[sum(c * row[i * N + j] for c, row in zip(values, space))
                   for j in range(N)] for i in range(N)]
        require(linear.polynomial_value(polynomial, values)
                == linear.determinant(matrix), "determinant reconstruction")
    result = {"removed_abs_shift_le": cutoff,
              "allowed_deficit_columns": len(columns),
              "constraint_rank": rank,
              "scalar_weight_nullity": len(nullbasis),
              "label_matrix_space_dimension": len(space),
              "determinant_monomials": len(polynomial),
              "full_rank_scalar_pairing_exists": bool(polynomial)}
    if not polynomial:
        return result
    choices, determinant = linear.grid_witness(polynomial, len(space), N)
    weights = [sum(c * row[j] for c, row in zip(choices, representatives))
               for j in range(len(columns))]
    combined = [sum(weight * column[j] for weight, column in zip(weights, columns))
                for j in range(N ** 4)]
    matrix = [[combined[x * N ** 3 + v] for v in range(N)] for x in range(N)]
    require(linear.determinant(matrix) == determinant != 0, "pairing witness")
    normalization = poly.model.inverse(matrix)
    for x in range(N):
        for y in range(N):
            for u in range(N):
                for v in range(N):
                    index = ((x * N + y) * N + u) * N + v
                    require(combined[index] == (matrix[x][v] if y == u else 0),
                            "complete scalar-output witness")
                    value = sum((normalization[x][a]
                                 * combined[((a * N + y) * N + u) * N + v]
                                 for a in range(N)), F(0))
                    require(value == int(x == v and y == u), "normalized crossing")
    active = [(name, weight) for name, weight in zip(names, weights) if weight]
    result["witness"] = {
        "weights": [{"deficit": d, "shift": s, "value": value}
                    for (d, s), value in active],
        "label_matrix": matrix,
        "determinant": determinant,
        "piece_count": len(active),
        "normalized_crossing_entries": N ** 4}
    return result


def case(bits):
    data = poly.model.construct(bits)
    tensors, degree = build_tensors(data)
    h, N = data["h"], data["N"]
    bands = []
    for cutoff in range(2 * h):
        result = classify(tensors, N, h, degree, cutoff)
        bands.append(result)
        print(f"classified deficit lambda={bits}, cutoff={cutoff}, "
              f"space={result['label_matrix_space_dimension']}, "
              f"invertible={result['full_rank_scalar_pairing_exists']}",
              file=sys.stderr, flush=True)
    return {"lambda": bits, "h": h, "N": N, "maximum_deficit": degree,
            "nonzero_coefficient_tensors": len(tensors),
            "coefficient_tensor_sha256": digest(
                [[list(name), values] for name, values in sorted(tensors.items())]),
            "bands": bands}


def main():
    result = {"status": "PASS",
              "scope": "complete finite contraction-deficit scalar span on registered codebooks; no all-size claim",
              "cases": [case(bits) for bits in (1, 2)],
              "bindings": {name: sha256((HERE / name).read_bytes()).hexdigest()
                           for name in ("polynomial.py", "linear.py", "deficit.py")}}
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
