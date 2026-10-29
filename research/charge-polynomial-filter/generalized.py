"""Complete finite scalar filtering after length-weighted charge rescaling.

The new premise multiplies each raw (mu,nu) entry by q^(len(mu)+len(nu)).
This is an invertible local diagonal change for nonzero q and is different
from both the raw span and the registered inverse-length deficit span.
"""
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


screen = load("generalized_deficit_screen", HERE / "deficit.py")
poly = screen.poly
require = poly.require


def digest(value):
    return sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def build_raw(data):
    N, h = data["N"], data["h"]
    degree = max(map(len, data["row_labels"])) + max(map(len, data["column_labels"]))
    pair_degrees = [0] * (N ** 4)
    for x, mu in enumerate(data["row_labels"]):
        for v, nu in enumerate(data["column_labels"]):
            for y in range(N):
                for u in range(N):
                    pair_degrees[((x * N + y) * N + u) * N + v] = len(mu) + len(nu)
    tensors = {}
    evaluation_checks = 0
    for shift in range(-2 * h, 2 * h + 1):
        columns = [[0] * (N ** 4) for _ in range(degree + 1)]
        for x, mu in enumerate(data["row_labels"]):
            for v, nu in enumerate(data["column_labels"]):
                for y, argument in enumerate(data["output_labels"]):
                    vector = poly.piece_vector(mu, nu, argument, shift)
                    values = dict(vector)
                    for u, output in enumerate(data["output_labels"]):
                        index = ((x * N + y) * N + u) * N + v
                        for d, coefficient in enumerate(values.get(output, ())):
                            columns[d][index] = coefficient
                    if x == v == y == 0:
                        for charge in (-2, 2):
                            direct = poly.evaluate(vector, charge)
                            for output, raw_value in direct:
                                pair_degree = len(mu) + len(nu)
                                amplified = sum(
                                    coefficient * charge ** (d + pair_degree)
                                    for d, coefficient in enumerate(values.get(output, ())))
                                require(amplified == charge ** pair_degree * raw_value,
                                        "length-weighted charge evaluation")
                                evaluation_checks += 1
        for d, column in enumerate(columns):
            if any(column):
                tensors[d, shift] = column
        print(f"raw base lambda={data['bits']}, shift={shift}", file=sys.stderr, flush=True)
    poly.clear_caches()
    return tensors, pair_degrees, degree, evaluation_checks


def amplify(raw, pair_degrees, size):
    """Coefficient e=d+len(mu)+len(nu) of q^pair_degree Q_s^(q)."""
    answer = {}
    for (degree, shift), column in raw.items():
        for index, value in enumerate(column):
            if value:
                key = (degree + pair_degrees[index], shift)
                if key not in answer:
                    answer[key] = [0] * size
                answer[key][index] = value
    return answer


def finite_rank_bits(result, h, N, degree):
    if "witness" not in result:
        return None
    worst = 0
    for entry in result["witness"]["weights"]:
        shift = entry["shift"]
        row = min(N * N, (2 * degree + 1) * sum(
            poly.model.partition_count(shift + i) for i in range(2 * h + 1)))
        column = min(N * N, (2 * degree + 1) * sum(
            poly.model.partition_count(2 * h - shift - i)
            for i in range(2 * h + 1)))
        worst = max(worst, (row - 1).bit_length() + (column - 1).bit_length())
    result["witness"]["finite_shared_bit_upper_bound"] = worst
    result["witness"]["coefficient_rank_inflation_bound"] = 2 * degree + 1
    return worst


def main():
    data = poly.model.construct(2)
    N, h = data["N"], data["h"]
    raw, pair_degrees, degree, evaluations = build_raw(data)
    amplified = amplify(raw, pair_degrees, N ** 4)
    bands = []
    for family, tensors, cutoffs in (
            ("raw", raw, (4, 5)),
            ("length_amplified", amplified, (5, 6))):
        for cutoff in cutoffs:
            result = screen.classify(tensors, N, h, degree, cutoff)
            result["family"] = family
            finite_rank_bits(result, h, N, degree)
            bands.append(result)
            print(f"classified {family}, cutoff={cutoff}, "
                  f"space={result['label_matrix_space_dimension']}, "
                  f"invertible={result['full_rank_scalar_pairing_exists']}",
                  file=sys.stderr, flush=True)
    raw_positive = bands[0]
    raw_negative = bands[1]
    new_positive = bands[2]
    new_negative = bands[3]
    require(raw_positive["full_rank_scalar_pairing_exists"], "raw cutoff-four control")
    require(not raw_negative["full_rank_scalar_pairing_exists"], "raw cutoff-five boundary")
    require(new_positive["full_rank_scalar_pairing_exists"], "amplified cutoff-five witness")
    require(not new_negative["full_rank_scalar_pairing_exists"], "amplified cutoff-six boundary")
    result = {
        "status": "PASS",
        "scope": "complete finite scalar spans at lambda=2,h=6; no all-size or asymptotic claim",
        "lambda": 2,
        "h": h,
        "N": N,
        "maximum_raw_charge_degree": degree,
        "maximum_amplified_degree": 2 * degree,
        "fixed_charge_rescaling_checks": evaluations,
        "raw_coefficient_tensor_sha256": digest(
            [[list(name), values] for name, values in sorted(raw.items())]),
        "amplified_coefficient_tensor_sha256": digest(
            [[list(name), values] for name, values in sorted(amplified.items())]),
        "pair_degree_sha256": digest(pair_degrees),
        "bands": bands,
        "bindings": {name: sha256((HERE / name).read_bytes()).hexdigest()
                     for name in ("polynomial.py", "linear.py", "deficit.py",
                                  "generalized.py", "REGISTERED.md")}
    }
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
