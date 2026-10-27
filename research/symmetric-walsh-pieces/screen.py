"""Registered exact Walsh-piece screen, r=1..8; standard library only."""

from fractions import Fraction as F
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location("walsh_construction", HERE / "walsh.py")
walsh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(walsh)
require = walsh.require
dual_spec = importlib.util.spec_from_file_location("walsh_dual", HERE / "dual.py")
dual = importlib.util.module_from_spec(dual_spec)
dual_spec.loader.exec_module(dual)


def rational_rank(matrix: list[list[F]]) -> int:
    matrix = [list(map(F, row)) for row in matrix]
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next((i for i in range(rank, len(matrix)) if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        for i in range(rank + 1, len(matrix)):
            if not matrix[i][column]:
                continue
            scale = matrix[i][column] / pivot_value
            for j in range(column, len(matrix[0])):
                matrix[i][j] -= scale * matrix[rank][j]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def direct_checks(candidate: dict) -> dict:
    r = candidate["r"]
    N = 1 << r
    types = candidate["types"]
    indices = {alpha: i for i, alpha in enumerate(types)}
    word_indices = {(a, b): indices[walsh.word_type(a, b, r)]
                    for a, b in product(range(N), repeat=2)}
    gamma = {(a, b, x, y): walsh.gamma(a, b, x, y)
             for a, b, x, y in product(range(N), repeat=4)}
    bell = {(a, b, x, y): walsh.bell(a, b, x, y)
            for a, b, x, y in product(range(N), repeat=4)}
    ranks = identities = 0
    crossing = [F(0)] * (N ** 4)
    for piece in candidate["pieces"]:
        function, transformed = piece["function"], piece["transformed"]
        row_matrix = [[F(0)] * (N * N) for _ in range(N * N)]
        col_matrix = [[F(0)] * (N * N) for _ in range(N * N)]
        for index, (x, y, u, v) in enumerate(product(range(N), repeat=4)):
            row_value = sum((function[word_indices[a, b]] * gamma[a, b, x, y] * gamma[a, b, u, v]
                             for a, b in product(range(N), repeat=2)), F(0)) / N
            col_value = sum((transformed[word_indices[a, b]] * bell[a, b, x, u] * bell[a, b, y, v]
                             for a, b in product(range(N), repeat=2)), F(0)) / (N * N)
            require(row_value == col_value, "Two explicit factorizations disagree")
            row_matrix[x * N + y][u * N + v] = row_value
            col_matrix[x * N + u][y * N + v] = row_value
            crossing[index] += row_value
            identities += 1
        require(rational_rank(row_matrix) == piece["row_support"], "Direct row rank")
        require(rational_rank(col_matrix) == piece["col_support"], "Direct column rank")
        ranks += 2
    for value, (x, y, u, v) in zip(crossing, product(range(N), repeat=4)):
        require(value == int(x == v and y == u), "Full crossing identity")
        identities += 1
    return {"direct_rational_flattening_ranks": ranks, "direct_factorization_and_crossing_entries": identities}


def check_candidate(r: int) -> tuple[dict, dict]:
    candidate = walsh.construct(r)
    T, types, pieces = candidate["transform"], candidate["types"], candidate["pieces"]
    size = len(types)
    require(sum(candidate["weights"]) == 4 ** r, "Type multiplicities")
    for i, row in enumerate(T):
        squared = [0] * size
        for k, coefficient in enumerate(row):
            if coefficient:
                for j, value in enumerate(T[k]):
                    squared[j] += coefficient * value
        require(squared == [(4 ** r if i == j else 0) for j in range(size)], "Compressed transform square")
    transformed_target = walsh.multiply_matrix(T, candidate["target"])
    require(transformed_target == [(1 << r) * x for x in candidate["target"]], "Quadratic sign eigenvector")
    for piece in pieces:
        require(walsh.multiply_matrix(T, piece["function"]) == piece["transformed"], "Exact piece transform")
    require(all(sum((piece["function"][j] for piece in pieces), F(0)) == candidate["target"][j]
                for j in range(size)), "Full coefficient target")
    worst = max(pieces, key=lambda p: p["shared_bits"])
    support_product_worst = max(pieces, key=lambda p: p["row_support"] * p["col_support"])
    payload = [[piece["basis_index"], list(map(str, piece["function"])),
                list(map(str, piece["transformed"]))] for piece in pieces]
    profile = {"lambda": r, "type_dimension": size, "retained_pieces": len(pieces),
               "worst_shared_bit_total": worst["shared_bits"],
               "worst_piece": {key: worst[key] for key in ["basis_index", "pivot", "row_support", "col_support"]},
               "max_exact_support_product": support_product_worst["row_support"] * support_product_worst["col_support"],
               "common_denominator_bits": candidate["denominator"].bit_length(),
               "max_coefficient_bits": max(abs(x.numerator).bit_length() + x.denominator.bit_length()
                                           for piece in pieces for x in piece["function"] + piece["transformed"]),
               "piece_data_sha256": sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()}
    direct = direct_checks(candidate) if r <= 2 else {}
    return profile, direct


def main() -> None:
    profiles, direct = [], []
    for r in range(1, 9):
        profile, checks = check_candidate(r)
        profiles.append(profile)
        if checks:
            direct.append({"lambda": r, **checks})
    manifest = json.loads((ROOT / "SOURCES.json").read_text())
    for item in manifest["files"]:
        require(sha256((ROOT / item["path"]).read_bytes()).hexdigest() == item["sha256"], "Frozen source drift")
    report = {"status": "PASS", "scope": "exact bounded crossing-family screen; no asymptotic rate or SAT improvement",
              "registered_lambda": list(range(1, 9)), "profiles": profiles, "direct_checks": direct,
              "global_symmetry_dual": dual.check_dual(walsh),
              "bindings": {"base_commit": json.loads((HERE / "CLAIM.json").read_text())["base_commit"],
                           "accepted_upstream_commit": manifest["upstream_commit"],
                           "construction_sha256": sha256((HERE / "CONSTRUCTION.md").read_bytes()).hexdigest(),
                           "symmetry_barrier_sha256": sha256((HERE / "SYMMETRY-BARRIER.md").read_bytes()).hexdigest(),
                           "module_sha256": sha256((HERE / "walsh.py").read_bytes()).hexdigest(),
                           "dual_checker_sha256": sha256((HERE / "dual.py").read_bytes()).hexdigest(),
                           "screen_sha256": sha256(Path(__file__).read_bytes()).hexdigest()}}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
