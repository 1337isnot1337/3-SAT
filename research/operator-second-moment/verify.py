"""Bounded exact checks of the second-moment spectrum and quadratic filter."""
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREDECESSOR = ROOT / "research" / "charged-operator-moments"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(PREDECESSOR))
import charged
import filter
import pairing
import predecessor
import second


def require(condition, message):
    if not condition:
        raise ValueError(message)


def spectral_cubic(matrix, h):
    n = len(matrix)
    eye = filter.identity(n)
    square = filter.matmul(matrix, matrix)
    cube = filter.matmul(square, matrix)
    a = F(h - 2, h)
    answer = filter.matadd(cube, square, a - 1)
    return filter.matadd(answer, matrix, -a)


def flatten(states, pieces, direction):
    n = len(states)
    shifts = sorted({shift for shift, key in pieces})
    if direction == "row":
        rows = [(shift, x, y) for shift in shifts for x in range(n) for y in range(n)]
        columns = [(u, v) for u in range(n) for v in range(n)]
        def key(shift, row, column):
            x, y = row
            u, v = column
            return shift, (x, y, u, v)
    else:
        rows = [(shift, x, u) for shift in shifts for x in range(n) for u in range(n)]
        columns = [(y, v) for y in range(n) for v in range(n)]
        def key(shift, row, column):
            x, u = row
            y, v = column
            return shift, (x, y, u, v)
    return [[pieces.get(key(shift, row, column), F(0)) for shift, *row in rows]
            for column in columns]


def main():
    source = json.loads((HERE / "SOURCES.json").read_text())
    for name, expected in source["operator_predecessor"]["modules"].items():
        actual = sha256((PREDECESSOR / name).read_bytes()).hexdigest()
        require(actual == expected, f"predecessor integrity: {name}")
    require(sha256((PREDECESSOR / "PROOF.md").read_bytes()).hexdigest()
            == source["operator_predecessor"]["proof_sha256"], "predecessor proof integrity")

    direct_checks = support_checks = 0
    for h in range(1, 7):
        states = charged.partitions(h)
        matrix = second.second_pairing(states)
        energies = range(3) if h <= 5 else range(2)
        for i, x in enumerate(states):
            for j, v in enumerate(states):
                for energy in energies:
                    for argument in charged.partitions(energy):
                        actual = dict(charged.moment(x, v, argument, 2, 0))
                        value = energy * matrix[i][j]
                        expected = {argument: value} if value else {}
                        require(actual == expected,
                                f"independent second moment: h={h}, {x}, {v}, E={energy}")
                        direct_checks += 1
                        if value:
                            require(len(x) in (len(v), len(v) + 2), "length filtration")
                            support_checks += 1

    identity_checks = integrality_checks = 0
    for h in range(1, 15):
        for v in charged.partitions(h):
            polynomial = {v: F(1)}
            image = second.second_operator(polynomial, h)
            require(pairing.L(pairing.L(image)) == {}, f"L^2U at h={h}")
            identity_checks += 1
            derivative = pairing.L(polynomial)
            harmonic = pairing.add(polynomial,
                                   pairing.L_right_inverse(derivative) if derivative else {}, -1)
            require(pairing.L(harmonic) == {}, "harmonic projection")
            require(second.second_operator(harmonic, h) == harmonic,
                    f"harmonic eigenvalue one at h={h}")
            identity_checks += 1
        if h >= 2:
            a = F(h - 2, h)
            for v in charged.partitions(h - 1):
                polynomial = {v: F(1)}
                derivative = pairing.L(polynomial)
                harmonic = pairing.add(polynomial,
                                       pairing.L_right_inverse(derivative) if derivative else {}, -1)
                lifted = pairing.B(harmonic)
                image = second.second_operator(lifted, h)
                defect = pairing.add(image, lifted, a)
                require(pairing.L(defect) == {}, f"triangular complement at h={h}")
                identity_checks += 1
        matrix = second.normalized_pairing(charged.partitions(h))
        for row in matrix:
            for entry in row:
                require((2 * h * entry).denominator == 1, "2hU integrality")
                integrality_checks += 1

    rank_rows = []
    inverse_checks = 0
    for h in range(1, 13):
        states = charged.partitions(h)
        matrix = second.normalized_pairing(states)
        rank = predecessor.exact_rank(matrix)
        expected = len(states) - len(charged.partitions(h - 2))
        require(rank == expected, f"rank formula at h={h}")
        require(all(not entry for row in spectral_cubic(matrix, h) for entry in row),
                f"spectral cubic at h={h}")
        normalizer = filter.matadd(filter.identity(len(states)), matrix, -4 * h * h)
        inverse = filter.normalizer_inverse(matrix, h)
        require(inverse == filter.generic_inverse(normalizer), f"spectral inverse at h={h}")
        require(filter.matmul(normalizer, inverse) == filter.identity(len(states)),
                f"normalizer inverse identity at h={h}")
        inverse_checks += 1
        rank_rows.append({"h": h, "dimension": len(states), "rank": rank,
                          "nullity": len(states) - rank,
                          "rank_formula": "p(h)-p(h-2)",
                          "eigenvalues": [0, 1, F(-(h - 2), h)]})

    crossing_rows = []
    crossing_sum_checks = rank_checks = 0
    for h in range(1, 5):
        states, source_pieces, pieces = filter.crossing_pieces(h)
        require(filter.crossing_defect(states, pieces), f"filtered crossing at h={h}")
        crossing_sum_checks += len(states) ** 4
        ranks = {}
        for direction in ("row", "column"):
            before = predecessor.exact_rank(flatten(states, source_pieces, direction))
            after = predecessor.exact_rank(flatten(states, pieces, direction))
            require(before == after, f"{direction} flattening rank at h={h}")
            ranks[direction] = {"source": before, "filtered": after}
            rank_checks += 1
        crossing_rows.append({"h": h, "labels": len(states),
                              "retained_shifts": 4 * h - 1,
                              "nonzero_filtered_entries": len(pieces),
                              "flattening_ranks": ranks})

    result = {
        "result": "PASS",
        "scope": "independent exact operators at h<=6, spectral identities at h<=14, inverses at h<=12, and actual crossing tensors at h<=4",
        "independent_second_moment_entries": direct_checks,
        "nonzero_length_filtration_entries": support_checks,
        "spectral_operator_identity_inputs": identity_checks,
        "integrality_entries": integrality_checks,
        "finite_rank_and_spectral_rows": rank_rows,
        "spectral_inverse_checks": inverse_checks,
        "actual_quadratic_crossing_cases": crossing_rows,
        "crossing_sum_checks": crossing_sum_checks,
        "directional_rank_checks": rank_checks,
        "uniform_rank_spectral_and_inverse_proof": "PROOF.md sections 2-3",
        "quadratic_crossing_filter_constructed": True,
        "piece_count": "4h-1, omitting s=+1 and s=-1",
        "rho_improvement_claimed": False,
        "alpha_improvement_claimed": False,
        "source_sha256": {name: sha256((HERE / name).read_bytes()).hexdigest()
                          for name in ("second.py", "filter.py", "verify.py", "PROOF.md", "SOURCES.json")}
    }
    print(json.dumps(result, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
