"""Exact six-class three-bit macro family, with a pinned adapted-basis engine."""

from fractions import Fraction as F
import importlib.util
from math import factorial, lcm, prod
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("coarse_macro_reference", HERE / "macro.py")
coarse = importlib.util.module_from_spec(spec)
spec.loader.exec_module(coarse)
scheme_spec = importlib.util.spec_from_file_location("local_macro_scheme", HERE / "schemes.py")
schemes = importlib.util.module_from_spec(scheme_spec)
scheme_spec.loader.exec_module(schemes)
SCHEME = schemes.local_scheme()
require = coarse.require


def compositions(total: int, letters: int):
    if letters == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in compositions(total - first, letters - 1):
                yield (first,) + rest


def orbit_weight(alpha: tuple[int, ...]) -> int:
    answer = factorial(sum(alpha))
    for x in alpha:
        answer //= factorial(x)
    return answer * prod(w ** x for w, x in zip(SCHEME["weights"], alpha))


def construct(R: int) -> dict:
    weights_local, C = SCHEME["weights"], SCHEME["matrix"]
    letters = len(weights_local)
    types = sorted(compositions(R, letters), key=lambda alpha: (orbit_weight(alpha), alpha))
    weights = [orbit_weight(alpha) for alpha in types]
    T = []
    for beta in types:
        polynomial = {(0,) * letters: 1}
        for j, count in enumerate(beta):
            for _ in range(count):
                updated = {}
                for alpha, value in polynomial.items():
                    for k, coefficient in enumerate(C[j]):
                        if not coefficient:
                            continue
                        new = list(alpha)
                        new[k] += 1
                        new = tuple(new)
                        updated[new] = updated.get(new, 0) + value * coefficient
                polynomial = {alpha: value for alpha, value in updated.items() if value}
        T.append([polynomial.get(alpha, 0) for alpha in types])
    vectors, images, pivots = coarse.engine.adapted_basis(T)
    target = [F(prod(sign ** x for sign, x in zip(SCHEME["target"], alpha))) for alpha in types]
    remainder = list(target)
    pieces = []
    for i in reversed(range(len(types))):
        coefficient = remainder[i]
        if not coefficient:
            continue
        function = [coefficient * x for x in vectors[i]]
        transformed = [coefficient * x for x in images[i]]
        for j in range(i + 1):
            remainder[j] -= function[j]
        row_support = sum(w for w, x in zip(weights, function) if x)
        col_support = sum(w for w, x in zip(weights, transformed) if x)
        pieces.append({"basis_index": i, "pivot": pivots[i], "function": function,
                       "transformed": transformed, "row_support": row_support, "col_support": col_support,
                       "shared_bits": (row_support - 1).bit_length() + (col_support - 1).bit_length()})
    require(not any(remainder), "Refined target decomposition")
    denominator = 1
    for piece in pieces:
        for value in piece["function"]:
            denominator = lcm(denominator, value.denominator)
    require(all((denominator * value).denominator == 1 for piece in pieces
                for value in piece["function"] + piece["transformed"]), "Refined integer clearing")
    return {"R": R, "lambda": 3 * R, "types": types, "weights": weights,
            "transform": T, "target": target, "pieces": pieces, "denominator": denominator}
