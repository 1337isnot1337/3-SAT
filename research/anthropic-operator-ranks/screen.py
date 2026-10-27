"""Exact bounded screen of the Hexagon Appendix-B operator pieces.

Default coverage: lambda=1,2,3, with all piece tensors and both operator
orders. Modular ranks certify exactness only when matching a separate
factorization upper bound; every remaining rank is computed over Q.
No network, third-party dependencies or full SAT algorithm is used.
"""

import argparse
from fractions import Fraction
import gzip
from hashlib import sha256
from itertools import product
import json
from math import factorial
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from operators import (
    binomial, build_pieces, direct_operator, dual_polynomial, dual_scale,
    exact_rank, flatten, modular_rank, operator, partitions,
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def operator_checks():
    checks = 0
    for weight in range(4):
        for monomial in partitions(weight):
            for energy in range(4):
                for argument in partitions(energy):
                    for target in range(4):
                        actual = operator(monomial, target - energy, argument)
                        require(actual == direct_operator(monomial, target - energy, argument),
                                "Direct and recursive operators disagree")
                        require(all(sum(output) == target for output, _ in actual),
                                "Wrong homogeneous energy")
                        checks += 1
    binomials = 0
    for n in range(-8, 9):
        for degree in range(1, 10):
            require(binomial(n, degree) == binomial(n - 1, degree)
                    + binomial(n - 1, degree - 1), "Integer binomial Pascal failure")
            binomials += 1
    # A lower modular rank is not an upper rank bound over Q.
    control = [[101, 0], [0, 1]]
    require(exact_rank(control) == 2 and modular_rank(control, 101) == 1
            and modular_rank(control, 103) == 2, "Bad-prime control failure")
    return {"normal_order_vs_recurrence": checks, "integer_binomial_cases": binomials,
            "bad_prime_control": {"rational_rank": 2, "mod101_rank": 1, "mod103_rank": 2}}


def homogeneous_moment_checks():
    checks = 0
    for h in range(1, 4):
        for a_weight in range(h + 1):
            for a, b in product(partitions(a_weight), partitions(h)):
                scalar = dict(operator(a, -h, b)).get((), 0)
                for energy in range(4):
                    for argument in partitions(energy):
                        total, moment = {}, {}
                        for shift in range(-energy - h, energy + h + 1):
                            local = {}
                            for i in range(a_weight + h + 1):
                                weight = (-1) ** i * binomial(a_weight + h, i)
                                for intermediate, c in operator(b, h - shift - i, argument):
                                    for output, d in operator(a, shift - h + i, intermediate):
                                        local[output] = local.get(output, 0) + weight * c * d
                            for output, c in local.items():
                                total[output] = total.get(output, 0) + c
                                moment[output] = moment.get(output, 0) + shift * c
                        require(all(c == (scalar if output == argument else 0)
                                    for output, c in total.items()), "Homogeneous Q sum fails")
                        require(total.get(argument, 0) == scalar, "Homogeneous scalar coefficient missing")
                        require(not any(moment.values()), "Homogeneous first moment fails")
                        checks += 1
    return checks


def dual_checks(h):
    checks = 0
    states = partitions(h)
    for mu, nu in product(states, repeat=2):
        value = 0
        for monomial, scalar in dual_polynomial(mu):
            image = dict(operator(monomial, -h, nu))
            require(set(image) <= {()}, "Dual operator did not land at energy zero")
            value += scalar * image.get((), 0) * dual_scale(nu)
        require(value == (factorial(h) if mu == nu else 0), "Biorthogonality failure")
        checks += 1
    return checks


def ceil_bits(rank):
    return (rank - 1).bit_length() if rank else 0


def certified_rank(matrix, upper, reason="explicit_intermediate_factorization_and_matrix_size"):
    modular = {str(prime): modular_rank(matrix, prime) for prime in (101, 103, 1009)}
    lower = max(modular.values())
    require(lower <= upper, "Modular lower bound exceeds factorization upper bound")
    if lower == upper:
        rank = upper
        method = "modular_lower_bound_matches_proved_upper_bound"
    else:
        rank = exact_rank(matrix)
        method = "rational_elimination"
        require(lower <= rank <= upper, "Rational/factorization/modular rank inconsistency")
    return {"rank_over_Q": rank, "method": method, "modular_lower_bounds": modular,
            "proved_upper_bound": upper, "upper_bound_reason": reason,
            "rank_index_bits": ceil_bits(rank), "upper_bound_index_bits": ceil_bits(upper)}


def screen(bits):
    h, states, pieces, order_checks = build_pieces(bits, check_reversed=True)
    dimension = len(states)
    require(len(partitions(h - 1)) < dimension <= len(partitions(h)),
            "Input energy is not minimal as required by the source")
    crossing = [sum(tensor[index] for tensor in pieces.values())
                for index in range(dimension ** 4)]
    first_moment = [sum(s * tensor[index] for s, tensor in pieces.items())
                    for index in range(dimension ** 4)]
    require(not any(first_moment), "First-moment identity fails")
    require(all(sum((1 - s) * tensor[index] for s, tensor in pieces.items() if s != 1)
                == crossing[index] for index in range(dimension ** 4)),
            "Integer one-piece deletion fails")
    span_rows = list(pieces.values())
    # The proved nonzero relation (s) supplies the upper bound 4h.
    span = certified_rank(span_rows, len(pieces) - 1, reason="nonzero_first_moment_relation")
    cases = []
    for shift, tensor in pieces.items():
        row_terms = sum(len(partitions(shift + i)) for i in range(2 * h + 1))
        col_terms = sum(len(partitions(2 * h - shift - i)) for i in range(2 * h + 1))
        row = certified_rank(flatten(tensor, dimension, "row"), min(dimension ** 2, row_terms))
        column = certified_rank(flatten(tensor, dimension, "column"), min(dimension ** 2, col_terms))
        cases.append({"shift": shift, "row_factorization_terms": row_terms,
                      "column_factorization_terms": col_terms, "row": row, "column": column,
                      "tensor_sha256": sha256(json.dumps(tensor, separators=(",", ":")).encode()).hexdigest(),
                      "largest_integer_coefficient_bits": max(abs(x).bit_length() for x in tensor)})
    return {"lambda": bits, "h": h, "encoded_states": [list(state) for state in states],
            "full_energy_dimension": len(partitions(h)), "matrix_size": dimension ** 2,
            "operator_order_vector_checks": order_checks,
            "crossing_identity_entries": dimension ** 4,
            "first_moment_zero_entries": dimension ** 4,
            "pruned_crossing_identity_entries": dimension ** 4,
            "original_piece_count": len(pieces), "pruned_piece_count": len(pieces) - 1,
            "piece_span_rank": span,
            "fixed_piece_reweighting_is_one_dimensional": span["rank_over_Q"] == len(pieces) - 1,
            "full_state_dual_pairing_checks": dual_checks(h), "pieces": cases,
            "strict_rank_gaps": sum(item[side]["rank_over_Q"]
                < item[side]["proved_upper_bound"]
                for item in cases for side in ("row", "column")),
            "rank_index_bit_savings": sum(item[side]["rank_index_bits"]
                < item[side]["upper_bound_index_bits"]
                for item in cases for side in ("row", "column")),
            "worst_exact_shared_bit_total": max(item["row"]["rank_index_bits"]
                + item["column"]["rank_index_bits"] for item in cases)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-bits", type=int, choices=(1, 2, 3), default=3)
    args = parser.parse_args()
    metadata = json.loads((HERE / "SOURCES.json").read_text())["sources"][0]
    source = gzip.decompress((HERE / "source/anthropic-2610.00577v1.tex.gz").read_bytes())
    require(sha256(source).hexdigest() == metadata["source_file"]["sha256"], "External source drift")
    for label in ("eq:ops", "eq:Q", "lem:dual", "eq:half-row", "eq:half-col"):
        require(("\\label{" + label + "}").encode() in source, "Unresolved source label: " + label)
    report = {"schema_version": 1, "result": "PASS_FINITE_OPERATOR_PIECES",
              "scope": "Exact finite operator identities and characteristic-zero ranks only; no improved rho, SAT algorithm or asymptotic bound",
              "source_sha256": sha256(source).hexdigest(), "operator_checks": operator_checks(),
              "general_homogeneous_first_moment_cases": homogeneous_moment_checks(),
              "cases": [screen(bits) for bits in range(1, args.max_bits + 1)],
              "artifact_sha256": {name: sha256((HERE / name).read_bytes()).hexdigest()
                  for name in ("operators.py", "screen.py", "SOURCES.json", "PROOF.md")}}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
