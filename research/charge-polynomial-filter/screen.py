"""Complete registered small-codebook scalar filtering over all charge coefficients."""

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


poly = load("charge_filter_polynomial", HERE / "polynomial.py")
linear = load("charge_filter_linear", HERE / "linear.py")
require = poly.require


def digest(value):
    return sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def controls():
    count = 0
    for weight in range(4):
        for monomial in poly.model.predecessor.partitions(weight):
            for energy in range(3):
                for argument in poly.model.predecessor.partitions(energy):
                    for mode in range(-energy, 4 - energy):
                        values = poly.operator(monomial, mode, argument)
                        for charge in [-2, -1, 0, 1, 2]:
                            require(poly.evaluate(values, charge) == poly.model.charged.operator(monomial, mode, argument, charge),
                                    "Polynomial recurrence and fixed-charge reference disagree")
                            count += 1
    basis, rank = linear.nullspace([[1, 2, 3], [2, 4, 6]], 3)
    require(rank == 1 and len(basis) == 2, "Exact nullspace control")
    determinant = linear.determinant_polynomial([[1, 0, 0, 0], [0, 0, 0, 1]], 2)
    require(determinant == {(1, 1): 1}, "Individually singular basis can have an invertible combination")
    witness, value = linear.grid_witness(determinant, 2, 2)
    require(value != 0 and witness == [1, 1], "Deterministic grid selection")
    require(not linear.determinant_polynomial([[1, 0, 0, 0], [0, 1, 0, 0]], 2), "Singular matrix-space control")
    poly.clear_caches()
    return count


def build_tensors(data):
    N, h = data["N"], data["h"]
    degree = max(map(len, data["row_labels"])) + max(map(len, data["column_labels"]))
    tensors = {}
    evaluation_checks = order_checks = 0
    for shift in range(-2 * h, 2 * h + 1):
        columns = [[0] * (N ** 4) for _ in range(degree + 1)]
        for x, mu in enumerate(data["row_labels"]):
            for v, nu in enumerate(data["column_labels"]):
                for y, argument in enumerate(data["output_labels"]):
                    vector = poly.piece_vector(mu, nu, argument, shift)
                    selected = data["bits"] == 1 or x == v == y == 0 or x == v == y == N - 1
                    if selected:
                        require(vector == poly.piece_vector(mu, nu, argument, shift, reverse=True),
                                "Charge-polynomial two-order identity")
                        order_checks += 1
                        for charge in [-1, 0, 1, 2]:
                            require(poly.evaluate(vector, charge)
                                    == poly.model.charged.piece_vector(mu, nu, argument, shift, charge),
                                    "Full polynomial piece and fixed-charge reference disagree")
                            evaluation_checks += 1
                    values = dict(vector)
                    for u, output in enumerate(data["output_labels"]):
                        index = ((x * N + y) * N + u) * N + v
                        for d, coefficient in enumerate(values.get(output, ())):
                            columns[d][index] = coefficient
        for d, column in enumerate(columns):
            if any(column):
                tensors[d, shift] = column
        if shift % 4 == 0:
            print(f"charge polynomials lambda={data['bits']}, shift={shift}", file=sys.stderr, flush=True)
    poly.clear_caches()
    return tensors, degree, evaluation_checks, order_checks


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
    pairings = [[sum(weight * column[x * N ** 3 + v] for weight, column in zip(weights, columns))
                 for x in range(N) for v in range(N)] for weights in nullbasis]
    _, _, selected = linear.echelon(pairings, N * N)
    space = [pairings[j] for j in selected]
    representatives = [nullbasis[j] for j in selected]
    polynomial = linear.determinant_polynomial(space, N)
    # Independent scalar substitutions check the determinant expansion path.
    for offset in [0, 1, 3]:
        values = [(j + offset) % 5 for j in range(len(space))]
        matrix = [[sum(c * row[i * N + j] for c, row in zip(values, space)) for j in range(N)] for i in range(N)]
        require(linear.polynomial_value(polynomial, values) == linear.determinant(matrix), "Determinant polynomial reconstruction")
    result = {"removed_abs_shift_le": cutoff, "smallest_allowed_abs_shift": cutoff + 1,
              "allowed_charge_coefficient_columns": len(columns), "nonzero_scalar_constraints": len(constraints),
              "constraint_rank_over_Q": rank, "scalar_weight_nullity": len(nullbasis),
              "label_matrix_space_dimension": len(space), "label_matrix_space_basis": space,
              "determinant_monomials": len(polynomial),
              "determinant_polynomial_sha256": digest([[list(alpha), value] for alpha, value in sorted(polynomial.items())]),
              "full_rank_scalar_pairing_exists": bool(polynomial)}
    if not polynomial:
        return result
    choices, determinant = linear.grid_witness(polynomial, len(space), N)
    weights = [sum(c * row[j] for c, row in zip(choices, representatives)) for j in range(len(columns))]
    combined = [sum(weight * column[j] for weight, column in zip(weights, columns)) for j in range(N ** 4)]
    matrix = [[combined[x * N ** 3 + v] for v in range(N)] for x in range(N)]
    require(linear.determinant(matrix) == determinant != 0, "Full-rank scalar pairing witness")
    normalization = poly.model.inverse(matrix)
    for x in range(N):
        for y in range(N):
            for u in range(N):
                for v in range(N):
                    index = ((x * N + y) * N + u) * N + v
                    require(combined[index] == (matrix[x][v] if y == u else 0), "Complete scalar-output witness")
                    value = sum((normalization[x][a] * combined[((a * N + y) * N + u) * N + v] for a in range(N)), F(0))
                    require(value == int(x == v and y == u), "Actual filtered crossing after local normalization")
    active = [(name, weight) for name, weight in zip(names, weights) if weight]
    worst_bits = 0
    for (_, shift), _ in active:
        row_bound = min(N * N, (degree + 1) * sum(poly.model.partition_count(shift + i) for i in range(2 * h + 1)))
        col_bound = min(N * N, (degree + 1) * sum(poly.model.partition_count(2 * h - shift - i) for i in range(2 * h + 1)))
        worst_bits = max(worst_bits, (row_bound - 1).bit_length() + (col_bound - 1).bit_length())
    result["witness"] = {"weights": [{"charge_degree": d, "shift": s, "value": value} for (d, s), value in active],
                         "label_matrix": matrix, "determinant": determinant, "grid_choices": choices,
                         "piece_count": len(active), "finite_shared_bit_upper_bound": worst_bits,
                         "normalized_crossing_entries": N ** 4,
                         "coefficient_rank_inflation_bound": degree + 1}
    return result


def case(bits):
    data = poly.model.construct(bits)
    tensors, degree, evaluations, orders = build_tensors(data)
    h, N = data["h"], data["N"]
    bands = []
    for cutoff in sorted(set([0, 1, h // 2 - 1, h - 1, 2 * h - 1])):
        result = classify(tensors, N, h, degree, cutoff)
        bands.append(result)
        print(f"classified lambda={bits}, cutoff={cutoff}, space={result['label_matrix_space_dimension']}, "
              f"invertible={result['full_rank_scalar_pairing_exists']}", file=sys.stderr, flush=True)
    return {"lambda": bits, "h": h, "N": N, "maximum_charge_degree": degree,
            "nonzero_coefficient_tensors": len(tensors), "fixed_charge_evaluation_checks": evaluations,
            "coefficientwise_order_checks": orders,
            "coefficient_tensor_sha256": digest([[list(name), values] for name, values in sorted(tensors.items())]),
            "bands": bands}


def main():
    count = controls()
    cases = [case(bits) for bits in [1, 2]]
    print(json.dumps({"status": "PASS", "scope": "complete registered finite charge-span scalar-filter classification; no all-size gain",
                      "small_operator_evaluations": count, "cases": cases,
                      "bindings": {name: sha256((HERE / name).read_bytes()).hexdigest()
                                   for name in ["polynomial.py", "linear.py", "screen.py", "REGISTERED.md"]},
                      "codebook_sha256": sha256(poly.REFERENCE.read_bytes()).hexdigest()}, indent=2))


if __name__ == "__main__":
    main()
