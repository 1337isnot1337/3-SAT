"""Direct integer crossing factors and exhaustive support-code checks."""

from hashlib import sha256
import importlib.util
from itertools import product
import json
from math import factorial, gcd, prod
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("direct_refined", HERE / "refined.py")
refined = importlib.util.module_from_spec(spec)
spec.loader.exec_module(refined)
require = refined.require
CLASSES = refined.SCHEME["classes"]
LOCAL = [[label for label, j in CLASSES.items() if j == i] for i in range(6)]


def word_type(a, b, R):
    answer = [0] * 6
    for j in range(R):
        answer[CLASSES[(a >> (3 * j)) & 7, (b >> (3 * j)) & 7]] += 1
    return tuple(answer)


def multinomial(alpha):
    answer = factorial(sum(alpha))
    for a in alpha:
        answer //= factorial(a)
    return answer


def unrank_type(alpha, index):
    if index < 0 or index >= refined.orbit_weight(alpha):
        return None
    choices = prod(len(labels) ** a for labels, a in zip(LOCAL, alpha))
    sequence_index, within = divmod(index, choices)
    counts = list(alpha)
    a = b = 0
    for position in range(sum(alpha)):
        for letter, count in enumerate(counts):
            if not count:
                continue
            counts[letter] -= 1
            block = multinomial(counts)
            if sequence_index < block:
                break
            sequence_index -= block
            counts[letter] += 1
        within, local_index = divmod(within, len(LOCAL[letter]))
        x, y = LOCAL[letter][local_index]
        a |= x << (3 * position)
        b |= y << (3 * position)
    require(within == sequence_index == 0, "Support decoder remainder")
    return a, b


def support_decode(data, function, index):
    if index < 0:
        return None
    for alpha, weight, value in zip(data["types"], data["weights"], function):
        if value:
            if index < weight:
                return unrank_type(alpha, index)
            index -= weight
    return None


def rank(matrix):
    matrix = [list(row) for row in matrix]
    result = 0
    for column in range(len(matrix[0])):
        pivot = next((j for j in range(result, len(matrix)) if matrix[j][column]), None)
        if pivot is None:
            continue
        matrix[result], matrix[pivot] = matrix[pivot], matrix[result]
        p = matrix[result][column]
        for j in range(result + 1, len(matrix)):
            a = matrix[j][column]
            if a:
                row = [p * x - a * y for x, y in zip(matrix[j], matrix[result])]
                common = 0
                for x in row:
                    common = gcd(common, x)
                matrix[j] = [x // common for x in row] if common else row
        result += 1
    return result


def direct_factors(data):
    N = 1 << data["lambda"]
    require(N == 8, "Registered direct ranks are only for one macro")
    index = {alpha: j for j, alpha in enumerate(data["types"])}
    D = data["denominator"]
    total = [0] * (N ** 4)
    identities = ranks = 0
    for piece in data["pieces"]:
        f = [int(D * x) for x in piece["function"]]
        hat = [int(D * x) for x in piece["transformed"]]
        row_matrix = [[0] * (N * N) for _ in range(N * N)]
        col_matrix = [[0] * (N * N) for _ in range(N * N)]
        for j, (x, y, u, v) in enumerate(product(range(N), repeat=4)):
            row_value = col_value = 0
            if x ^ y == u ^ v:
                a = x ^ y
                row_value = N * sum(f[index[word_type(a, b, 1)]] * (-1) ** ((b & (y ^ v)).bit_count() % 2)
                                    for b in range(N))
            if x ^ u == y ^ v:
                c = x ^ u
                col_value = sum(hat[index[word_type(c, d, 1)]] * (-1) ** ((d & (x ^ y)).bit_count() % 2)
                                for d in range(N))
            require(row_value == col_value, "Direct cleared row and column factors")
            total[j] += row_value
            row_matrix[x * N + y][u * N + v] = row_value
            col_matrix[x * N + u][y * N + v] = row_value
            identities += 1
        require(rank(row_matrix) == piece["row_support"], "Direct rational row rank")
        require(rank(col_matrix) == piece["col_support"], "Direct rational column rank")
        ranks += 2
    for value, (x, y, u, v) in zip(total, product(range(N), repeat=4)):
        require(value == D * N * N * int(x == v and y == u), "Direct complete crossing")
        identities += 1
    return {"integer_factor_and_crossing_entries": identities, "exact_flattening_ranks": ranks}


def main():
    profiles = []
    for R in [1, 2]:
        data = refined.construct(R)
        N = 1 << (3 * R)
        indices = {alpha: j for j, alpha in enumerate(data["types"])}
        all_words = {(a, b): indices[word_type(a, b, R)] for a, b in product(range(N), repeat=2)}
        codes = 0
        for piece in data["pieces"]:
            for function in [piece["function"], piece["transformed"]]:
                expected = {word for word, j in all_words.items() if function[j]}
                decoded = [support_decode(data, function, j) for j in range(len(expected))]
                require(len(set(decoded)) == len(decoded) and set(decoded) == expected, "Exhaustive support decoder")
                require(support_decode(data, function, -1) is None, "Negative support code")
                for j in range(len(expected), (1 << (len(expected) - 1).bit_length()) + 1):
                    require(support_decode(data, function, j) is None, "Invalid support code")
                codes += len(expected)
        profiles.append({"macros": R, "actual_words": len(all_words), "valid_support_codes": codes,
                         **(direct_factors(data) if R == 1 else {})})
    print(json.dumps({"status": "PASS", "scope": "direct ranks at R=1 and exhaustive support codes at R=1,2",
                      "profiles": profiles,
                      "bindings": {name + "_sha256": sha256((HERE / (name + ".py")).read_bytes()).hexdigest()
                                   for name in ["direct", "refined", "schemes", "macro"]}}, indent=2))


if __name__ == "__main__":
    main()
