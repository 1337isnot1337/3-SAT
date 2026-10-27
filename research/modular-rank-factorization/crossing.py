"""End-to-end crossing expansion, modular compression and nonunit recovery."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


modular = load("crossing_modular", HERE / "modular.py")
predecessor_path = HERE.parent / "three-bit-macro-walsh" / "refined.py"
require = modular.require
require(sha256(predecessor_path.read_bytes()).hexdigest()
        == "5eee33b3ba0e1e701cfe3cd9e67b94bf645399976a559c85410ff1bdacf55afb", "Pinned crossing constructor changed")
refined = load("frozen_crossing_family", predecessor_path)


def main():
    data = refined.construct(1)
    N, D = 8, data["denominator"]
    normalizer = D * N * N
    output_precision = 4  # counts 0..8 are recovered exactly
    cap = output_precision + modular.valuation(normalizer, 100)
    modulus = 1 << cap
    indices = {alpha: j for j, alpha in enumerate(data["types"])}
    scheme = refined.SCHEME["classes"]
    pieces = []
    for piece in data["pieces"]:
        values = [int(D * x) for x in piece["function"]]
        row_matrix = [[0] * (N * N) for _ in range(N * N)]
        col_matrix = [[0] * (N * N) for _ in range(N * N)]
        for x in range(N):
            for y in range(N):
                for u in range(N):
                    for v in range(N):
                        value = 0
                        if x ^ y == u ^ v:
                            value = N * sum(values[indices[tuple(int(j == scheme[x ^ y, b]) for j in range(6))]]
                                            * (-1) ** ((b & (y ^ v)).bit_count() % 2) for b in range(N))
                        row_matrix[x * N + y][u * N + v] = value
                        col_matrix[x * N + u][y * N + v] = value
        row = modular.factor(row_matrix, cap)
        col = modular.factor(col_matrix, cap)
        require(modular.reconstruct(row) == [[x % modulus for x in r] for r in row_matrix], "Crossing row compression")
        require(modular.reconstruct(col) == [[x % modulus for x in r] for r in col_matrix], "Crossing column compression")
        require(row["inner_dimension"] <= piece["row_support"] and col["inner_dimension"] <= piece["col_support"],
                "Both rational rank envelopes")
        # Select the cheaper direction, then contract W_xy=f(x)*[y=rotate(x)]
        # and V_uv=1. The original crossing value is sum_x f(x).
        direction, factors = min([("row", row), ("col", col)], key=lambda pair: pair[1]["inner_dimension"])
        coefficients = []
        for x in range(N):
            y = ((x << 1) & 7) | (x >> 2)
            if direction == "row":
                value = sum(a * sum(r) for a, r in zip(factors["left"][x * N + y], factors["right"]))
            else:
                value = sum(sum(factors["left"][x * N + u][j] for u in range(N))
                            * sum(factors["right"][j][y * N + v] for v in range(N))
                            for j in range(factors["inner_dimension"]))
            coefficients.append(value % modulus)
        pieces.append({"direction": direction, "inner_dimension": factors["inner_dimension"],
                       "coefficients": coefficients})
    for mask in range(256):
        residue = sum(piece["coefficients"][x] for piece in pieces for x in range(N) if (mask >> x) & 1) % modulus
        recovered = modular.exact_division_residue(residue, normalizer, output_precision)
        require(recovered == mask.bit_count(), "All Boolean assignment predicates, exact count recovery")
    print(json.dumps({"status": "PASS", "scope": "one-level integer crossing expansion with modular rank factors",
                      "predicates": 256, "pieces": len(pieces), "normalizer": normalizer,
                      "output_precision": output_precision, "working_precision": cap,
                      "selected_directions_and_dimensions": [{key: p[key] for key in ["direction", "inner_dimension"]}
                                                             for p in pieces],
                      "bindings": {"crossing.py": sha256(Path(__file__).read_bytes()).hexdigest(),
                                   "modular.py": sha256((HERE / "modular.py").read_bytes()).hexdigest(),
                                   "predecessor_refined.py": sha256(predecessor_path.read_bytes()).hexdigest()}}, indent=2))


if __name__ == "__main__":
    main()
