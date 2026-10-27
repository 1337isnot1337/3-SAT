"""Bounded exact checks of the second-moment formula and finite spectra."""
from fractions import Fraction as F
from hashlib import sha256
import json
from math import factorial
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREDECESSOR = ROOT / "research" / "charged-operator-moments"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(PREDECESSOR))
import charged
import predecessor
import second


def require(condition, message):
    if not condition:
        raise ValueError(message)


def matmul(left, right):
    return [[sum((left[i][k] * right[k][j] for k in range(len(right))), F(0))
             for j in range(len(right[0]))] for i in range(len(left))]


def matadd(left, right, scale=F(1)):
    return [[left[i][j] + scale * right[i][j] for j in range(len(left[0]))]
            for i in range(len(left))]


def spectral_cubic(matrix, h):
    n = len(matrix)
    identity = [[F(i == j) for j in range(n)] for i in range(n)]
    square = matmul(matrix, matrix)
    cube = matmul(square, matrix)
    # U(U-1)(U+(h-2)/h) = U^3+(a-1)U^2-aU, a=(h-2)/h.
    a = F(h - 2, h)
    answer = matadd(cube, square, a - 1)
    answer = matadd(answer, matrix, -a)
    return answer


def main():
    source = json.loads((HERE / "SOURCES.json").read_text())
    for name, expected in source["operator_predecessor"]["modules"].items():
        actual = sha256((PREDECESSOR / name).read_bytes()).hexdigest()
        require(actual == expected, f"predecessor integrity: {name}")
    require(sha256((PREDECESSOR / "PROOF.md").read_bytes()).hexdigest()
            == source["operator_predecessor"]["proof_sha256"], "predecessor proof integrity")

    direct_checks = 0
    support_checks = 0
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

    rank_rows = []
    spectral_checks = 0
    for h in range(1, 11):
        states = charged.partitions(h)
        matrix = second.normalized_pairing(states)
        rank = predecessor.exact_rank(matrix)
        expected = len(states) - len(charged.partitions(h - 2))
        require(rank == expected, f"finite rank formula at h={h}")
        require(all(not entry for row in spectral_cubic(matrix, h) for entry in row),
                f"finite spectral cubic at h={h}")
        spectral_checks += 1
        rank_rows.append({"h": h, "dimension": len(states), "rank": rank,
                          "nullity": len(states) - rank,
                          "finite_rank_observation": "p(h)-p(h-2)",
                          "finite_eigenvalues": [0, 1, F(-(h - 2), h)]})
        if h == 2:
            require(second.second_operator({(2,): F(1)}, 2) == {}, "h=2 kernel")
        if h == 3:
            require(second.second_operator({(3,): F(6), (1, 1, 1): F(-1)}, 3) == {},
                    "h=3 kernel")

    result = {
        "result": "PASS",
        "scope": "independent exact operators at h<=6 and polynomial matrices at h<=10; finite ranks/spectra are not all-size claims",
        "independent_second_moment_entries": direct_checks,
        "nonzero_length_filtration_entries": support_checks,
        "finite_rank_and_spectral_rows": rank_rows,
        "spectral_cubic_checks": spectral_checks,
        "uniform_singularity_proof": "PROOF.md section 3",
        "uniform_rank_or_spectral_proof_claimed": False,
        "quadratic_crossing_filter_constructed": False,
        "alpha_improvement_claimed": False,
        "source_sha256": {name: sha256((HERE / name).read_bytes()).hexdigest()
                          for name in ("second.py", "verify.py", "PROOF.md", "SOURCES.json")}
    }
    print(json.dumps(result, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
