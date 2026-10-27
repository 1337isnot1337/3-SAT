"""Exact rational checks of the parity-recovery counterexample and contents."""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from math import factorial, prod
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def valuation(number: F | int) -> int:
    number = F(number)
    require(number != 0, "No finite valuation for zero")
    numerator = abs(number.numerator)
    denominator = number.denominator
    return ((numerator & -numerator).bit_length()
            - (denominator & -denominator).bit_length())


def multiply(left: list[F], right: list[F]) -> list[F]:
    answer = [F(0)] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            answer[i + j] += x * y
    return answer


def evaluate(polynomial: list[F], at: F | int) -> F:
    value = F(0)
    for coefficient in reversed(polynomial):
        value = value * at + coefficient
    return value


def diagonal_shift(a: int, t: int) -> list[F]:
    length = 1 << a
    alpha = 2 * length
    result = [F(1)]
    denominator = 1
    for s in range(-length, length):
        if s:
            result = multiply(result, [F(t - s), F(alpha)])
            denominator *= -s
    return [c / denominator for c in result]


def diagonal_value(length: int, at: F | int) -> F:
    return prod((F(at) - s) / -s for s in range(-length, length) if s)


def cauchy_entry(length: int, x: int, y: int, at: F | int) -> F:
    difference = y - x
    denominator = prod(-s for s in range(-length, length) if s)
    # Cancel the matching numerator factor before evaluation at a grid point.
    return prod(F(at) - s for s in range(-length, length) if s != difference) / denominator


def generalized_binomial(at: F | int, k: int) -> F:
    return prod(F(at) - j for j in range(k)) / factorial(k)


def explicit_packet_sum(length: int, marked: int, at: F) -> F:
    """Sum the source's affine row factors for the specified unary tensors."""
    # B fixes the marked column to 1 and all the other columns to zero.
    row_forms = [cauchy_entry(length, x, marked, at) for x in range(length)]
    answer = F(0)
    for bits in product((0, 1), repeat=length):
        if not bits[marked]:
            continue
        answer += prod(z if bit else 1 - z for z, bit in zip(row_forms, bits))
    return answer


def main() -> None:
    shifted = powers = integers = packet_sums = 0
    fixtures = []
    for a in range(1, 5):
        length = 1 << a
        alpha = 2 * length
        for t in range(-length, length):
            if not t:
                continue
            polynomial = diagonal_shift(a, t)
            expected = a + 1 - valuation(t)
            require(polynomial[0] == 0, "Shifted constant is nonzero")
            require(min(valuation(c) for c in polynomial if c) == expected,
                    "Exact shifted content")
            require(valuation(polynomial[1]) == expected, "Linear coefficient witness")
            for z in [F(0), F(1), F(-1), F(3, 5)]:
                require(evaluate(polynomial, z) == diagonal_value(length, t + alpha * z),
                        "Shift substitution")
            shifted += 1
            powered = [F(1)]
            for q in range(1, 5):
                powered = multiply(powered, polynomial)
                require(all(not c for c in powered[:q]), "Jet order witness")
                require(min(valuation(c) for c in powered if c) == q * expected,
                        "Power content")
                require(valuation(powered[q]) == q * expected, "Power leading witness")
                require(all(not c or valuation(c) >= q for c in powered),
                        "Indistinguishable from zero modulo 2^q")
                powers += 1
        for at in range(-4 * length, 4 * length + 1):
            value = diagonal_value(length, at)
            alternative = ((-1) ** (length - 1) * generalized_binomial(at + length, length)
                           * generalized_binomial(at - 1, length - 1))
            require(value == alternative, "Integer-valued binomial identity")
            require(value.denominator == 1, "Integer-valuedness")
            require(value.numerator % 2 == int(at % alpha == 0), "Integer parity residue class")
            integers += 1
        require(diagonal_value(length, 0) == 1, "Origin value")
        if length <= 8:
            for t in [-length, -2, -1, 0, 1]:
                for z in [F(0), F(1), F(3, 5)]:
                    at = F(t) + alpha * z
                    for marked in range(length):
                        answer = explicit_packet_sum(length, marked, at)
                        require(answer == diagonal_value(length, at), "Actual unary network sum")
                        packet_sums += 1
        global_polynomial = [c / alpha ** j for j, c in enumerate(diagonal_shift(a, 0))]
        global_content = min(valuation(c) for c in global_polynomial if c)
        require(global_content == -valuation(factorial(length) * factorial(length - 1)),
                "Global coefficient denominator")
        require(global_content < 0, "Counterexample accidentally globally integral")
        fixtures.append({"a": a, "L": length, "nonzero_nodes": 2 * length - 1,
                         "min_global_coefficient_valuation": global_content})
    # Explicit regression for the parameters in the failed shortcut.
    example = diagonal_shift(2, -2)
    require(example[1] == F(-20, 3), "L=4 explicit coefficient")
    require(diagonal_value(4, 0) == 1 and diagonal_value(4, -2) == 0,
            "Even-node parity counterexample")
    manifest = json.loads((ROOT / "SOURCES.json").read_text())
    hashes = {}
    for source in manifest["files"]:
        digest = sha256((ROOT / source["path"]).read_bytes()).hexdigest()
        require(digest == source["sha256"], "Frozen source drift")
        hashes[source["path"]] = digest
    report = {"status": "PASS", "scope": "finite exact rational checks of a recovery-data barrier; no SAT improvement",
              "exact_shifted_content_checks": shifted, "exact_power_content_checks": powers,
              "integer_value_and_parity_checks": integers, "explicit_unary_packet_sums": packet_sums,
              "grid_fixtures": fixtures,
              "parameters": {"a": [1, 2, 3, 4], "q": [1, 2, 3, 4],
                             "all_nonzero_grid_nodes": True, "rational_shift_points": ["0", "1", "-1", "3/5"]},
              "counterexample": {"L": 4, "t": -2, "origin": "1", "node_value": "0",
                                  "shifted_linear_coefficient": str(example[1]),
                                  "shifted_content_valuation": 2},
              "source_bindings": {"upstream_commit": manifest["upstream_commit"],
                                  "frozen_source_sha256": hashes,
                                  "proof_sha256": sha256((HERE / "PROOF.md").read_bytes()).hexdigest(),
                                  "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest()}}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
