"""Bounded exact checks of scalar moment recovery for the operator pieces.

No all-size rank or SAT bound is inferred from these finite tables. The
quadratic-moment formula is checked against a separate Wick contraction.
"""

import argparse
from hashlib import sha256
from itertools import product
import json
from math import factorial
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from moments import PREDECESSOR, full_pairing, partial_pairing, second_pairing
from operators import (
    binomial, build_pieces, exact_rank, flatten, modular_rank, operator, partitions,
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def general_second_moment():
    checked = 0
    for h in range(1, 4):
        for a_weight in range(h + 1):
            for a, b in product(partitions(a_weight), partitions(h)):
                for energy in range(4):
                    expected = 4 * energy * partial_pairing(((a, 1),), ((b, 1),))
                    for argument in partitions(energy):
                        moment = {}
                        for s in range(-energy - h, energy + h + 1):
                            for i in range(a_weight + h + 1):
                                scale = s * s * (-1) ** i * binomial(a_weight + h, i)
                                for intermediate, c in operator(b, h - s - i, argument):
                                    for output, d in operator(a, s - h + i, intermediate):
                                        moment[output] = moment.get(output, 0) + scale * c * d
                        require(all(c == (expected if output == argument else 0)
                                    for output, c in moment.items()), "General second moment fails")
                        require(moment.get(argument, 0) == expected, "Missing scalar moment entry")
                        checked += 1
    return checked


def scalar_constraints(pieces, dimension):
    rows = []
    for x, y, u, v in product(range(dimension), repeat=4):
        index = ((x * dimension + y) * dimension + u) * dimension + v
        if y != u:
            row = [tensor[index] for tensor in pieces.values()]
        elif y:
            base = x * dimension ** 3 + v
            row = [tensor[index] - tensor[base] for tensor in pieces.values()]
        else:
            continue
        if any(row):
            rows.append(row)
    return rows


def certified_constraint_rank(rows, known_nullity):
    columns = len(rows[0]) if rows else 0
    upper = columns - known_nullity
    lower = {str(p): modular_rank(rows, p) for p in (101, 103, 1009)}
    require(max(lower.values()) <= upper, "Known moment nullvectors fail the rank bound")
    if max(lower.values()) == upper:
        rank = upper
        method = "modular_lower_matches_explicit_nullvector_upper"
    else:
        rank = exact_rank(rows)
        method = "rational_elimination"
    return {"rank_over_Q": rank, "weight_space_dimension": columns - rank,
            "modular_lower_bounds": lower, "proved_upper_bound": upper, "method": method}


def case(bits, predecessor_report):
    h, states, pieces, _ = build_pieces(bits, check_reversed=False)
    dimension = len(states)
    source_case = next(item for item in predecessor_report["cases"] if item["lambda"] == bits)
    for item in source_case["pieces"]:
        actual = sha256(json.dumps(pieces[item["shift"]], separators=(",", ":")).encode()).hexdigest()
        require(actual == item["tensor_sha256"], "Predecessor tensor drift")
    second = [sum(s * s * tensor[i] for s, tensor in pieces.items())
              for i in range(dimension ** 4)]
    pairing = [[second_pairing(mu, nu, h) for nu in states] for mu in states]
    for x, y, u, v in product(range(dimension), repeat=4):
        expected = pairing[x][v] if y == u else 0
        require(second[((x * dimension + y) * dimension + u) * dimension + v] == expected,
                "Wick pairing and actual second-moment tensor disagree")
    rows = scalar_constraints(pieces, dimension)
    shifts = list(pieces)
    for power in (0, 1, 2):
        vector = [s ** power for s in shifts]
        require(all(sum(a * b for a, b in zip(row, vector)) == 0 for row in rows),
                "Known quadratic scalar-recovery weight failed")
    rank = certified_constraint_rank(rows, known_nullity=3)
    moments = []
    crossing_control = None
    for power in range(7):
        tensor = [sum(s ** power * piece[i] for s, piece in pieces.items())
                  for i in range(dimension ** 4)]
        # Third flattening: (x,v) | (y,u), distinct from the source's two cuts.
        matrix = [[tensor[((x * dimension + y) * dimension + u) * dimension + v]
                   for y in range(dimension) for u in range(dimension)]
                  for x in range(dimension) for v in range(dimension)]
        actual_rank = exact_rank(matrix)
        if power >= 2:
            require(actual_rank <= len(partitions(power)) - 1,
                    "Higher-moment rank exceeds the zero-mode dimension bound")
        if power == 0:
            require(actual_rank == 1, "Crossing third-cut control fails")
            required = {direction: modular_rank(flatten(tensor, dimension, direction), 101)
                        for direction in ("row", "column")}
            require(set(required.values()) == {dimension ** 2}, "Crossing required-cut control fails")
            crossing_control = {"third_cut_rank": 1,
                                "row_and_column_rank_over_Q": dimension ** 2,
                                "certification": "mod101 lower bound equals full matrix dimension"}
        moments.append({"power": power, "middle_flattening_rank_over_Q": actual_rank,
                        "nonzero_entries": sum(bool(value) for value in tensor)})
    return {"lambda": bits, "h": h, "binary_dimension": dimension,
            "second_moment_entry_checks": dimension ** 4,
            "second_moment_pairing": pairing,
            "second_moment_pairing_rank_over_Q": exact_rank(pairing),
            "nonzero_scalar_constraints": len(rows), "scalar_weight_space": rank,
            "quadratic_weights_exhaust_scalar_recovery": rank["weight_space_dimension"] == 3,
            "third_cut_is_not_two_direction_gain_control": crossing_control,
            "moments": moments}


def full_state_pairings(max_h):
    cases = []
    for h in range(2, max_h + 1):
        states = partitions(h)
        matrix = [[second_pairing(mu, nu, h) for nu in states] for mu in states]
        cases.append({"h": h, "dimension": len(states), "rank_over_Q": exact_rank(matrix),
                      "dimension_minus_p_h_minus_2": len(states) - len(partitions(h - 2)),
                      "pairing_sha256": sha256(json.dumps(matrix, separators=(",", ":")).encode()).hexdigest()})
    return cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-bits", type=int, choices=(1, 2, 3), default=3)
    parser.add_argument("--max-h", type=int, choices=range(2, 15), default=12)
    args = parser.parse_args()
    predecessor = json.loads((PREDECESSOR / "verification.json").read_text())
    expected = predecessor["artifact_sha256"]["operators.py"]
    require(sha256((PREDECESSOR / "operators.py").read_bytes()).hexdigest() == expected,
            "Frozen predecessor operator module changed")
    report = {"schema_version": 1, "result": "PASS_FINITE_SCALAR_MOMENT_RECOVERY",
              "scope": "Exact finite scalar-recovery weights and Wick second-moment checks; no asymptotic rank or improved SAT bound",
              "predecessor_operator_sha256": expected,
              "general_second_moment_cases": general_second_moment(),
              "coded_cases": [case(bits, predecessor) for bits in range(1, args.max_bits + 1)],
              "full_state_pairings": full_state_pairings(args.max_h),
              "artifact_sha256": {name: sha256((HERE / name).read_bytes()).hexdigest()
                                  for name in ("moments.py", "screen.py", "PROOF.md")}}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
