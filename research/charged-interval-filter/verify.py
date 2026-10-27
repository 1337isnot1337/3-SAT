"""Exact controls for the registered charged interval-filter proposal.

PASS means that the valid highest-charge controls and the recorded explicit
counterexamples were reproduced.  It does not validate a central filter.
"""
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
import labels
import left
from predecessor import add_scaled


def require(condition, message):
    if not condition:
        raise ValueError(message)


def vector_sum(vectors):
    result = {}
    for vector in vectors:
        add_scaled(result, vector, 1)
    return {state: value for state, value in result.items() if value}


def main():
    source = json.loads((HERE / "SOURCES.json").read_text())
    for name, expected in source["operator_predecessor"]["modules"].items():
        actual = sha256((PREDECESSOR / name).read_bytes()).hexdigest()
        require(actual == expected, f"predecessor integrity: {name}")
    require(sha256((PREDECESSOR / "PROOF.md").read_bytes()).hexdigest()
            == source["operator_predecessor"]["proof_sha256"], "proof integrity")

    order_checks = scalar_checks = 0
    for h in range(1, 4):
        states = charged.partitions(h)
        for x in states:
            for v in states:
                for energy in range(3):
                    for argument in charged.partitions(energy):
                        for shift in range(-energy - h, energy + h + 1):
                            require(left.piece_vector(x, v, argument, shift, 1)
                                    == left.piece_vector(x, v, argument, shift, 1,
                                                         reverse=True),
                                    "left-charged operator orders")
                            order_checks += 1
                        for degree in range(4):
                            vector = dict(left.highest_charge_moment(
                                x, v, argument, degree))
                            require(set(vector) <= {argument},
                                    "highest-charge moment is not scalar")
                            if vector:
                                require(len(x) == len(v) + degree,
                                        "highest-charge length rule")
                            scalar_checks += 1

    h, left_labels, right_labels, minor = labels.choose_labels(1)
    output = charged.partitions(h)[0]
    coefficients = labels.filter_coefficients(2)
    pieces = {shift: left.projected_piece(
        left_labels[0], right_labels[0], output, shift, coefficients)
              for shift in range(-2 * h, 2 * h + 1)}
    full = vector_sum(pieces.values())
    retained = vector_sum(vector for shift, vector in pieces.items()
                          if abs(shift) >= 2)
    central = vector_sum(vector for shift, vector in pieces.items()
                         if abs(shift) < 2)
    require(full == {output: coefficients[1] * minor[0][0]},
            "corrected full projected crossing")
    require(retained != full, "central omission counterexample")
    require(any(state != output and value for state, value in retained.items()),
            "counterexample must include a non-scalar output")
    require(any(pieces[shift] for shift in (-1, 0, 1)),
            "a central projected piece must be nonzero")

    weighted = vector_sum(tuple((state, labels.filter_value(coefficients, shift) * value)
                                for state, value in vector)
                          for shift, vector in pieces.items() if abs(shift) >= 2)
    predicted_scale = labels.recovery_scale(h, coefficients)
    predicted = {output: predicted_scale * minor[0][0]}
    require(weighted != predicted, "extra-polynomial repair must also fail")

    result = {
        "result": "PASS",
        "meaning": "valid controls and explicit counterexamples reproduced; no interval filter",
        "scope": "left-charged two-order and highest-charge checks at h<=3; full h=3 projected tensors",
        "two_order_checks": order_checks,
        "scalar_highest_charge_checks": scalar_checks,
        "counterexample": {
            "h": h,
            "output": output,
            "cutoff": 2,
            "filter": "w(s)=s(s^2-1)",
            "full_projected_sum": {str(state): str(value)
                                   for state, value in full.items()},
            "retained_sum_after_central_omission": {
                str(state): str(value) for state, value in retained.items()},
            "omitted_central_sum": {str(state): str(value)
                                    for state, value in central.items()},
            "extra_weight_repair_retained_sum": {
                str(state): str(value) for state, value in weighted.items()},
            "extra_weight_repair_predicted_sum": {
                str(state): str(value) for state, value in predicted.items()}
        },
        "uniform_interval_filter_constructed": False,
        "rho_improvement_claimed": False,
        "alpha_improvement_claimed": False,
        "source_sha256": {name: sha256((HERE / name).read_bytes()).hexdigest()
                          for name in ("left.py", "labels.py", "verify.py",
                                       "PROOF.md", "SOURCES.json")}
    }
    print(json.dumps(result, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
