"""Registered exact asymmetric crossing screen; full tensors only at lambda=1,2."""

from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("asymmetric_model", HERE / "model.py")
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)
field_path = HERE.parent / "odd-prime-rank-transfer" / "field.py"
model.require(sha256(field_path.read_bytes()).hexdigest()
              == "36b63603503a088b03934e0b33f13f888a5881b1f5b9030c94e8a87920defeba", "Pinned field compiler changed")
field = model.load("asymmetric_prime_factors", field_path)
require = model.require


def matrices(tensor, N):
    row = [[tensor[x][y][u][v] for u in range(N) for v in range(N)] for x in range(N) for y in range(N)]
    col = [[tensor[x][y][u][v] for y in range(N) for v in range(N)] for x in range(N) for u in range(N)]
    return row, col


def check(bits):
    data = model.construct(bits)
    N, h, prime = data["N"], data["h"], 65537
    total = [[[[F(0) for _ in range(N)] for _ in range(N)] for _ in range(N)] for _ in range(N)]
    coefficient_sum = [0] * N
    profiles, order_checks, rank_checks = [], 0, 0
    for shift in data["shifts"]:
        raw, normalized, orders = model.piece(data, shift, check_reverse=bits == 1)
        order_checks += orders
        raw_matrices = matrices(raw, N)
        new_matrices = matrices(normalized, N)
        ranks, factors = [], []
        for old, new in zip(raw_matrices, new_matrices):
            old_rank = model.predecessor.exact_rank(old)
            new_rank = model.predecessor.exact_rank(new)
            require(old_rank == new_rank, "Local normalization changed a flattening rank")
            ranks.append(new_rank)
            reduced = [[field.rational_residue(x, prime) for x in row] for row in new]
            factored = field.factor(reduced, prime)
            require(field.reconstruct(factored) == reduced, "Field factor reconstruction")
            require(factored["inner_dimension"] <= new_rank, "Field rank exceeds rational rank")
            factors.append(factored)
            rank_checks += 2
        row_terms = sum(model.partition_count(shift + i) for i in range(2 * h + 1))
        col_terms = sum(model.partition_count(2 * h - shift - i) for i in range(2 * h + 1))
        require(ranks[0] <= row_terms and ranks[1] <= col_terms, "Source directional term bounds")
        direction, chosen = min(enumerate(factors), key=lambda p: p[1]["inner_dimension"])
        for x in range(N):
            y = ((x << 1) & (N - 1)) | (x >> (bits - 1))
            if direction == 0:
                value = sum(a * sum(r) for a, r in zip(chosen["left"][x * N + y], chosen["right"]))
            else:
                value = sum(sum(chosen["left"][x * N + u][j] for u in range(N))
                            * sum(chosen["right"][j][y * N + v] for v in range(N))
                            for j in range(chosen["inner_dimension"]))
            coefficient_sum[x] = (coefficient_sum[x] + value) % prime
            for y in range(N):
                for u in range(N):
                    for v in range(N):
                        total[x][y][u][v] += normalized[x][y][u][v]
        profiles.append({"shift": shift, "row_rank": ranks[0], "col_rank": ranks[1],
                         "source_row_terms": row_terms, "source_col_terms": col_terms})
        if shift % 4 == 0:
            print(f"lambda={bits}, h={h}, shift={shift}", file=sys.stderr, flush=True)
    for x in range(N):
        for y in range(N):
            for u in range(N):
                for v in range(N):
                    require(total[x][y][u][v] == int(x == v and y == u), "Exact normalized crossing sum")
    require(coefficient_sum == [1] * N, "Field query contraction")
    for mask in range(1 << N):
        residue = sum(coefficient_sum[x] for x in range(N) if (mask >> x) & 1) % prime
        require(field.recover_signed(residue, prime, N) == mask.bit_count(), "Recovered predicate count")
    model.charged.operator.cache_clear()
    model.charged.dual_operator.cache_clear()
    return {"lambda": bits, "h": h, "N": N, "full_partition_dimension": len(data["states"]),
            "first_moment_rank": model.partition_count(h) - model.partition_count(h - 1),
            "row_indices": data["row_indices"], "column_indices": data["column_indices"],
            "minor": [[str(x) for x in row] for row in data["minor"]],
            "inverse": [[str(x) for x in row] for row in data["inverse"]],
            "pieces": profiles, "positive_grade_order_checks": order_checks,
            "exact_rational_rank_checks": rank_checks, "crossing_entries": N ** 4,
            "predicate_counts": 1 << N, "prime": prime}


def main():
    minor_profiles = []
    for bits in range(1, 5):
        data = model.construct(bits)
        N, h = data["N"], data["h"]
        require(len(data["states"]) <= h * h * N, "Polynomial label-capacity overhead")
        require(0 not in data["shifts"], "Central shift was not omitted")
        minor_profiles.append({"lambda": bits, "h": h, "N": N,
                               "full_partition_dimension": len(data["states"]),
                               "inverse_max_numerator_bits": max(abs(x.numerator).bit_length() for row in data["inverse"] for x in row),
                               "inverse_max_denominator_bits": max(x.denominator.bit_length() for row in data["inverse"] for x in row)})
    profiles = [check(bits) for bits in [1, 2]]
    report = {"status": "PASS", "scope": "full charged normalized tensors at lambda=1,2; minor-only lambda=1..4",
              "minor_profiles": minor_profiles, "full_profiles": profiles,
              "bindings": {name: sha256((HERE / name).read_bytes()).hexdigest() for name in ["model.py", "verify.py", "REGISTERED.md"]},
              "predecessor_bindings": model.PINS,
              "field_compiler_sha256": sha256(field_path.read_bytes()).hexdigest()}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
