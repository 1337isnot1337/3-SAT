"""Actual rational crossing with large dyadic denominators, compiled over F_p."""

from fractions import Fraction as F
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


field = load("rational_crossing_field", HERE / "field.py")
require = field.require
predecessor_path = HERE.parent / "three-bit-macro-walsh" / "refined.py"
require(sha256(predecessor_path.read_bytes()).hexdigest()
        == "5eee33b3ba0e1e701cfe3cd9e67b94bf645399976a559c85410ff1bdacf55afb", "Pinned crossing constructor changed")
refined = load("rational_crossing_predecessor", predecessor_path)


def main():
    data = refined.construct(1)
    N, prime = 8, 101
    require(field.normalizer_residue(F(1), prime) == 1, "Rational crossing normalizer")
    indices = {alpha: j for j, alpha in enumerate(data["types"])}
    classes = refined.SCHEME["classes"]
    original_sum = [[F(0)] * (N * N) for _ in range(N * N)]
    conjugated_sum = [[F(0)] * (N * N) for _ in range(N * N)]
    profiles, all_coefficients = [], []
    maximum_denominator_exponent = 0
    for piece in data["pieces"]:
        def original(x, y, u, v):
            if x ^ y != u ^ v:
                return F(0)
            return sum((piece["function"][indices[tuple(int(j == classes[x ^ y, b]) for j in range(6))]]
                        * (-1) ** ((b & (y ^ v)).bit_count() % 2) for b in range(N)), F(0)) / N
        row_matrix = [[F(0)] * (N * N) for _ in range(N * N)]
        col_matrix = [[F(0)] * (N * N) for _ in range(N * N)]
        for x in range(N):
            for y in range(N):
                for u in range(N):
                    for v in range(N):
                        original_sum[x * N + y][u * N + v] += original(x, y, u, v)
                        # B=2I-S acts on x; B^-1 acts on v. Its upper-triangular
                        # entries are 2^-(v-b+1), so the two local basis changes
                        # preserve both flattening ranks and the crossing sum.
                        value = F(0)
                        for a, coefficient in [(x, 2), (x + 1, -1)]:
                            if a >= N:
                                continue
                            b = a ^ y ^ u
                            if b <= v:
                                value += coefficient * original(a, y, u, b) / (1 << (v - b + 1))
                        row_matrix[x * N + y][u * N + v] = value
                        col_matrix[x * N + u][y * N + v] = value
                        conjugated_sum[x * N + y][u * N + v] += value
                        denominator = value.denominator
                        require(denominator & (denominator - 1) == 0, "Conjugation denominator should be dyadic")
                        maximum_denominator_exponent = max(maximum_denominator_exponent, denominator.bit_length() - 1)
        row = field.factor([[field.rational_residue(x, prime) for x in line] for line in row_matrix], prime)
        col = field.factor([[field.rational_residue(x, prime) for x in line] for line in col_matrix], prime)
        require(field.reconstruct(row) == [[field.rational_residue(x, prime) for x in line] for line in row_matrix],
                "Rational row factor identity")
        require(field.reconstruct(col) == [[field.rational_residue(x, prime) for x in line] for line in col_matrix],
                "Rational column factor identity")
        require(row["inner_dimension"] <= piece["row_support"] and col["inner_dimension"] <= piece["col_support"],
                "Conjugation preserves both rank envelopes")
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
            coefficients.append(value % prime)
        all_coefficients.append(coefficients)
        profiles.append({"row_rational_rank_bound": piece["row_support"], "col_rational_rank_bound": piece["col_support"],
                         "row_field_rank": row["inner_dimension"], "col_field_rank": col["inner_dimension"],
                         "selected": direction})
    for x in range(N):
        for y in range(N):
            for u in range(N):
                for v in range(N):
                    require(original_sum[x * N + y][u * N + v] == int(x == v and y == u), "Original exact crossing")
                    require(conjugated_sum[x * N + y][u * N + v] == int(x == v and y == u), "Conjugated exact crossing")
    for mask in range(256):
        residue = sum(coefficients[x] for coefficients in all_coefficients for x in range(N) if (mask >> x) & 1) % prime
        require(field.recover_signed(residue, prime, 8) == mask.bit_count(), "All predicate counts after rational conjugation")
    require(maximum_denominator_exponent >= N - 1, "Test did not exercise a large dyadic denominator")
    try:
        field.rational_residue(F(1, 1 << N), 2)
    except field.BadPrime:
        pass
    else:
        raise ValueError("Bad-prime rejection failed")
    print(json.dumps({"status": "PASS", "scope": "exact conjugated rational crossing, field factors and all 256 predicates",
                      "N": N, "prime": prime, "predicates": 256, "exact_crossing_entries": 2 * N ** 4,
                      "max_dyadic_denominator_exponent": maximum_denominator_exponent, "pieces": profiles,
                      "bindings": {"crossing.py": sha256(Path(__file__).read_bytes()).hexdigest(),
                                   "field.py": sha256((HERE / "field.py").read_bytes()).hexdigest(),
                                   "CONJUGATION.md": sha256((HERE / "CONJUGATION.md").read_bytes()).hexdigest(),
                                   "predecessor_refined.py": sha256(predecessor_path.read_bytes()).hexdigest()}}, indent=2))


if __name__ == "__main__":
    main()
