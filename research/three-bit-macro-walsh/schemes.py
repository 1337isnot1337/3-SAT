"""Exact local refinement over F8; complete 64-label character certificate."""

from fractions import Fraction as F


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def multiply(a: int, b: int) -> int:
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 8:
            a ^= 0b1011
    return result


def trace(a: int) -> int:
    a2 = multiply(a, a)
    return a ^ a2 ^ multiply(a2, a2)


def local_scheme() -> dict:
    labels = [(a, b) for a in range(8) for b in range(8)]
    require(all(trace(a) in [0, 1] for a in range(8)), "F8 trace range")
    require(all(any(multiply(a, b) == 1 for b in range(1, 8)) for a in range(1, 8)), "F8 inverses")
    dual = {}
    for b in range(8):
        candidates = [B for B in range(8)
                      if all(trace(multiply(a, B)) == ((a & b).bit_count() % 2) for a in range(8))]
        require(len(candidates) == 1, "Trace-dual basis map")
        dual[b] = candidates[0]
    def class_of(a: int, b: int) -> int:
        A, B = a, dual[b]
        if not A and not B:
            return 0
        if not A:
            return 1
        if not B:
            return 2
        value = multiply(A, B)
        return 3 if value == 1 else 4 if trace(value) == 0 else 5
    classes = {(a, b): class_of(a, b) for a, b in labels}
    weights = [sum(j == i for j in classes.values()) for i in range(6)]
    require(weights == [1, 7, 7, 7, 21, 21], "Refined class sizes")
    signs = [1, 1, 1, -1, 1, -1]
    require(all((-1) ** ((a & b).bit_count() % 2) == signs[classes[a, b]] for a, b in labels),
            "Quadratic target signs")
    matrix = [None] * 6
    for c, d in labels:
        row = [0] * 6
        for a, b in labels:
            row[classes[a, b]] += (-1) ** (((b & c).bit_count() + (a & d).bit_count()) % 2)
        i = classes[c, d]
        if matrix[i] is None:
            matrix[i] = row
        require(row == matrix[i], "Refined character table does not close")
    require([[sum(matrix[i][k] * matrix[k][j] for k in range(6)) for j in range(6)]
             for i in range(6)] == [[64 * int(i == j) for j in range(6)] for i in range(6)],
            "Refined transform square")
    require(all(weights[i] * matrix[i][j] == weights[j] * matrix[j][i]
                for i in range(6) for j in range(6)), "Refined weighted self-adjointness")
    require([sum(x * y for x, y in zip(row, signs)) for row in matrix] == [8 * x for x in signs],
            "Refined target eigenvector")
    coarse_h = [F(0), F(1, 35), F(1, 35), F(-1, 28), F(1, 35), F(-1, 28)]
    require([sum((F(x) * y for x, y in zip(row, coarse_h)), F(0)) for row in matrix]
            == [8 * x for x in coarse_h], "Inherited support-seven dual")
    require(sum((F(w) * h * q for w, h, q in zip(weights, coarse_h, signs)), F(0)) == 2,
            "Inherited dual target pairing")
    require(matrix[0][4:] == [21, 21] and matrix[3][4:] == [-3, 9],
            "Support-21 dual obstruction rows")
    require(21 * 9 - 21 * -3 != 0, "Support-21 exclusion determinant")
    return {"weights": weights, "matrix": matrix, "target": signs, "classes": classes,
            "trace_dual_map": dual, "all_local_characters": len(labels) ** 2,
            "largest_local_dual_threshold": 7}


if __name__ == "__main__":
    import json
    data = local_scheme()
    print(json.dumps({key: value for key, value in data.items() if key != "classes"}, indent=2))
