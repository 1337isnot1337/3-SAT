"""Exact three-class macro construction, reusing the pinned two-flag engine."""

from fractions import Fraction as F
from hashlib import sha256
import importlib.util
from math import factorial, lcm
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREDECESSOR = HERE.parent / "symmetric-walsh-pieces" / "walsh.py"
PREDECESSOR_SHA256 = "a26c763362252f1efac1d7763d7df55f54e28c1e2c8c9c7ffb414962c699db63"
if sha256(PREDECESSOR.read_bytes()).hexdigest() != PREDECESSOR_SHA256:
    raise ValueError("Pinned predecessor engine changed")
spec = importlib.util.spec_from_file_location("two_flag_engine", PREDECESSOR)
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
require = engine.require

CLASS_WEIGHTS = (1, 35, 28)
CLASS_WALSH = ((1, 35, 28), (1, 3, -4), (1, -5, 4))


def class_of(a: int, b: int) -> int:
    return 0 if a == b == 0 else 1 + ((a & b).bit_count() % 2)


def type_of(a: int, b: int, R: int) -> tuple[int, int, int]:
    answer = [0, 0, 0]
    for i in range(R):
        answer[class_of((a >> (3 * i)) & 7, (b >> (3 * i)) & 7)] += 1
    return tuple(answer)


def orbit_weight(alpha: tuple[int, int, int]) -> int:
    answer = factorial(sum(alpha))
    for a in alpha:
        answer //= factorial(a)
    return answer * 35 ** alpha[1] * 28 ** alpha[2]


def types_of(R: int) -> list[tuple[int, int, int]]:
    return sorted(((a, b, R - a - b) for a in range(R + 1) for b in range(R - a + 1)),
                  key=lambda alpha: (orbit_weight(alpha), alpha))


def transform(types: list[tuple[int, int, int]]) -> list[list[int]]:
    result = []
    for beta in types:
        polynomial = {(0, 0, 0): 1}
        for j, count in enumerate(beta):
            for _ in range(count):
                updated = {}
                for alpha, value in polynomial.items():
                    for k, coefficient in enumerate(CLASS_WALSH[j]):
                        if not coefficient:
                            continue
                        new_alpha = list(alpha)
                        new_alpha[k] += 1
                        new_alpha = tuple(new_alpha)
                        updated[new_alpha] = updated.get(new_alpha, 0) + value * coefficient
                polynomial = {alpha: value for alpha, value in updated.items() if value}
        result.append([polynomial.get(alpha, 0) for alpha in types])
    return result


def construct(R: int) -> dict:
    types = types_of(R)
    weights = [orbit_weight(alpha) for alpha in types]
    T = transform(types)
    vectors, images, pivots = engine.adapted_basis(T)
    target = [F((-1) ** alpha[2]) for alpha in types]
    remainder = list(target)
    pieces = []
    for i in reversed(range(len(types))):
        coefficient = remainder[i]
        if not coefficient:
            continue
        function = [coefficient * value for value in vectors[i]]
        transformed = [coefficient * value for value in images[i]]
        for j in range(i + 1):
            remainder[j] -= function[j]
        row = sum(w for w, value in zip(weights, function) if value)
        col = sum(w for w, value in zip(weights, transformed) if value)
        require(row > 0 and col > 0, "Zero retained macro piece")
        pieces.append({"basis_index": i, "pivot": pivots[i], "function": function,
                       "transformed": transformed, "row_support": row, "col_support": col,
                       "shared_bits": (row - 1).bit_length() + (col - 1).bit_length()})
    require(not any(remainder), "Macro crossing coefficient identity")
    denominator = 1
    for piece in pieces:
        for value in piece["function"]:
            denominator = lcm(denominator, value.denominator)
    require(all((denominator * value).denominator == 1 for piece in pieces
                for value in piece["function"] + piece["transformed"]), "Macro integer clearing")
    return {"R": R, "lambda": 3 * R, "types": types, "weights": weights,
            "transform": T, "target": target, "pieces": pieces, "denominator": denominator}
