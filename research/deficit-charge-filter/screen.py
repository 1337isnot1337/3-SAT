"""Complete registered scalar filtering over all charge-deficit coefficients."""
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

poly = load("deficit_filter_polynomial", HERE.parent / "charge-polynomial-filter" / "polynomial.py")
linear = load("deficit_filter_linear", HERE.parent / "charge-polynomial-filter" / "linear.py")


def build_tensors(data):
    N, h = data["N"], data["h"]
    degree = max(map(len, data["row_labels"])) + max(map(len, data["column_labels"]))
    tensors = {}
    order_checks = 0
    for shift in range(-2 * h, 2 * h + 1):
        columns = [[0] * (N ** 4) for _ in range(degree + 1)]
        for x, mu in enumerate(data["row_labels"]):
            for v, nu in enumerate(data["column_labels"]):
                deficit = len(mu) + len(nu)
                for y, argument in enumerate(data["output_labels"]):
                    vector = poly.piece_vector(mu, nu, argument, shift)
                    if data["bits"] == 1 or x == v == y == 0 or x == v == y == N - 1:
                        assert vector == poly.piece_vector(mu, nu, argument, shift, reverse=True)
                        order_checks += 1
                    values = dict(vector)
                    for u, output in enumerate(data["output_labels"]):
                        index = ((x * N + y) * N + u) * N + v
                        for d, coefficient in enumerate(values.get(output, ())):
                            columns[deficit - d][index] = coefficient
        for e, column in enumerate(columns):
            if any(column):
                tensors[e, shift] = column
        print(f"built deficit lambda={data['bits']}, shift={shift}", file=sys.stderr, flush=True)
    poly.clear_caches()
    return tensors, degree, order_checks


def classify(tensors, N, cutoff):
    names = sorted((e, s) for (e, s) in tensors if abs(s) > cutoff)
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
    pairings = [[sum(weight * column[x * N ** 3 + v] for weight, column in zip(weights, columns))
                 for x in range(N) for v in range(N)] for weights in nullbasis]
    _, _, selected = linear.echelon(pairings, N * N)
    space = [pairings[j] for j in selected]
    representatives = [nullbasis[j] for j in selected]
    determinant = linear.determinant_polynomial(space, N)
    result = {"removed_abs_shift_le": cutoff, "allowed_deficit_columns": len(columns),
              "constraint_rank_over_Q": rank, "scalar_weight_nullity": len(nullbasis),
              "label_matrix_space_dimension": len(space), "full_rank_scalar_pairing_exists": bool(determinant)}
    if not determinant:
        return result
    choices, value = linear.grid_witness(determinant, len(space), N)
    weights = [sum(c * row[j] for c, row in zip(choices, representatives)) for j in range(len(columns))]
    combined = [sum(weight * column[j] for weight, column in zip(weights, columns)) for j in range(N ** 4)]
    matrix = [[combined[x * N ** 3 + v] for v in range(N)] for x in range(N)]
    assert linear.determinant(matrix) == value != 0
    normalization = poly.model.inverse(matrix)
    for x in range(N):
        for y in range(N):
            for u in range(N):
                for v in range(N):
                    index = ((x * N + y) * N + u) * N + v
                    assert combined[index] == (matrix[x][v] if y == u else 0)
                    normalized = sum((normalization[x][a] * combined[((a * N + y) * N + u) * N + v]
                                      for a in range(N)), poly.F(0))
                    assert normalized == int(x == v and y == u)
    active = [(name, weight) for name, weight in zip(names, weights) if weight]
    result["witness"] = {"piece_count": len(active), "grid_choices": choices,
                         "maximum_active_abs_shift": max(abs(s) for (_, s), _ in active),
                         "maximum_active_deficit": max(e for (e, _), _ in active),
                         "normalized_crossing_entries": N ** 4}
    return result


def case(bits):
    data = poly.model.construct(bits)
    tensors, degree, order_checks = build_tensors(data)
    h = data["h"]
    bands = []
    for cutoff in sorted(set([0, 1, h // 2 - 1, h - 1, 2 * h - 1])):
        result = classify(tensors, data["N"], cutoff)
        bands.append(result)
        print(f"classified deficit lambda={bits}, cutoff={cutoff}: {result}", file=sys.stderr, flush=True)
    return {"lambda": bits, "h": h, "N": data["N"], "maximum_deficit": degree,
            "coefficientwise_order_checks": order_checks, "bands": bands}


def main():
    cases = [case(bits) for bits in [1, 2]]
    print(json.dumps({"status": "PASS",
                      "scope": "complete registered finite charge-deficit scalar classification; no all-size gain",
                      "cases": cases,
                      "bindings": {name: sha256((HERE / name).read_bytes()).hexdigest()
                                   for name in ["README.md", "screen.py"]}}, indent=2))


if __name__ == "__main__":
    main()
