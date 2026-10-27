"""Exact permutation-symmetric Walsh crossing construction; no rate claim."""

from fractions import Fraction as F
from math import factorial, lcm

HADAMARD = ((1, 1, 1, 1), (1, 1, -1, -1), (1, -1, 1, -1), (1, -1, -1, 1))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def all_types(r: int) -> list[tuple[int, int, int, int]]:
    return [(a, b, c, r - a - b - c) for a in range(r + 1)
            for b in range(r - a + 1) for c in range(r - a - b + 1)]


def multiplicity(alpha: tuple[int, ...]) -> int:
    answer = factorial(sum(alpha))
    for a in alpha:
        answer //= factorial(a)
    return answer


def ordered_types(r: int) -> list[tuple[int, int, int, int]]:
    return sorted(all_types(r), key=lambda alpha: (multiplicity(alpha), alpha))


def compressed_transform(types: list[tuple[int, int, int, int]]) -> list[list[int]]:
    result = []
    for beta in types:
        polynomial = {(0, 0, 0, 0): 1}
        for letter, times in enumerate(beta):
            for _ in range(times):
                updated = {}
                for alpha, coefficient in polynomial.items():
                    for k, sign in enumerate(HADAMARD[letter]):
                        new_alpha = list(alpha)
                        new_alpha[k] += 1
                        new_alpha = tuple(new_alpha)
                        updated[new_alpha] = updated.get(new_alpha, 0) + sign * coefficient
                polynomial = {alpha: c for alpha, c in updated.items() if c}
        result.append([polynomial.get(alpha, 0) for alpha in types])
    return result


def multiply_matrix(T: list[list[int]], x: list[F]) -> list[F]:
    return [sum((F(a) * b for a, b in zip(row, x) if a and b), F(0)) for row in T]


def adapted_basis(T: list[list[int]]) -> tuple[list[list[F]], list[list[F]], list[int]]:
    size = len(T)
    vectors, images, pivots = [], [], []
    by_pivot = {}
    for i in range(size):
        vector = [F(0)] * size
        vector[i] = F(1)
        image = [F(row[i]) for row in T]
        while True:
            pivot = next((j for j in reversed(range(size)) if image[j]), None)
            require(pivot is not None, "Compressed Walsh transform is singular")
            if pivot not in by_pivot:
                break
            old = by_pivot[pivot]
            scale = image[pivot] / images[old][pivot]
            for j in range(pivot + 1):
                image[j] -= scale * images[old][j]
            for j in range(i):
                vector[j] -= scale * vectors[old][j]
        require(vector[i] == 1 and not any(vector[i + 1:]), "Nontriangular adapted basis")
        by_pivot[pivot] = i
        vectors.append(vector)
        images.append(image)
        pivots.append(pivot)
    return vectors, images, pivots


def construct(r: int) -> dict:
    types = ordered_types(r)
    weights = [multiplicity(alpha) for alpha in types]
    T = compressed_transform(types)
    vectors, images, pivots = adapted_basis(T)
    target = [F((-1) ** alpha[3]) for alpha in types]
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
        row_support = sum(w for w, value in zip(weights, function) if value)
        col_support = sum(w for w, value in zip(weights, transformed) if value)
        require(row_support > 0 and col_support > 0, "Zero retained piece")
        pieces.append({"basis_index": i, "pivot": pivots[i], "coefficient": coefficient,
                       "function": function, "transformed": transformed,
                       "row_support": row_support, "col_support": col_support,
                       "shared_bits": (row_support - 1).bit_length() + (col_support - 1).bit_length()})
    require(not any(remainder), "Crossing coefficient decomposition")
    denominator = 1
    for piece in pieces:
        for value in piece["function"]:
            denominator = lcm(denominator, value.denominator)
    require(all((denominator * value).denominator == 1 for piece in pieces
                for value in piece["function"] + piece["transformed"]), "Integer factor clearing")
    return {"r": r, "types": types, "weights": weights, "transform": T,
            "target": target, "pieces": pieces, "denominator": denominator}


def word_type(a: int, b: int, r: int) -> tuple[int, int, int, int]:
    counts = [0, 0, 0, 0]
    for i in range(r):
        counts[((a >> i) & 1) + 2 * ((b >> i) & 1)] += 1
    return tuple(counts)


def gamma(a: int, b: int, x: int, y: int) -> int:
    return (1 if (b & y).bit_count() % 2 == 0 else -1) if x == y ^ a else 0


def bell(a: int, b: int, x: int, u: int) -> int:
    return (1 if (b & x).bit_count() % 2 == 0 else -1) if u == x ^ a else 0
