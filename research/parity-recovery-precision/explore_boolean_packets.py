"""Registered finite screen: all 256 Boolean tensor pairs on one L=2 packet.

Question: how large can the minimum complete shifted content at active odd
nodes be when the original tensors use creation-time canonical 0/1 entries?
Success is a checkable finite classification or a useful actual-network
witness. No conclusion about growing packets or a faster algorithm follows.
No randomness, external dependencies, or unregistered parameter expansion.
"""

from fractions import Fraction as F
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("parity_reference", HERE / "verify.py")
reference = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)
evaluate, multiply = reference.evaluate, reference.multiply
require, valuation = reference.require, reference.valuation


def kernel_polynomial(length: int, x: int, y: int) -> list[F]:
    numerator = [F(1)]
    denominator = 1
    for s in range(-length, length):
        if s != y - x:
            numerator = multiply(numerator, [F(-s), F(1)])
        if s:
            denominator *= -s
    return [c / denominator for c in numerator]


def add(left: list[F], right: list[F], scale: int = 1) -> list[F]:
    answer = list(left) + [F(0)] * max(0, len(right) - len(left))
    for j, c in enumerate(right):
        answer[j] += scale * c
    return answer


def shift(polynomial: list[F], node: int, alpha: int) -> list[F]:
    answer = [F(0)]
    for c in reversed(polynomial):
        answer = add(multiply(answer, [F(node), F(alpha)]), [c])
    return answer


def tensor_polynomial(A: list[int], B: list[int], transfers: list[list[list[F]]]) -> list[F]:
    answer = [F(0)]
    for Y, X in product(range(4), repeat=2):
        answer = add(answer, transfers[Y][X], A[Y] * B[X])
    return answer


def main() -> None:
    length = 2
    kernels = [[kernel_polynomial(length, x, y) for y in range(length)]
               for x in range(length)]
    transfers = [[None] * 4 for _ in range(4)]
    for Y, X in product(range(4), repeat=2):
        polynomial = [F(1)]
        for row in range(length):
            form = [F(0)]
            for column in range(length):
                if X & (1 << column):
                    form = add(form, kernels[row][column])
            if not Y & (1 << row):
                form = add([F(1)], form, -1)
            polynomial = multiply(polynomial, form)
        transfers[Y][X] = polynomial
    histogram = {}
    witnesses = {}
    checked = 0
    all_cases = []
    for Aword, Bword in product(range(16), repeat=2):
        A = [(Aword >> j) & 1 for j in range(4)]
        B = [(Bword >> j) & 1 for j in range(4)]
        polynomial = tensor_polynomial(A, B, transfers)
        origin = sum(a * b for a, b in zip(A, B))
        require(evaluate(polynomial, 0) == origin, "Original contraction")
        shifted = [shift(polynomial, t, 4) for t in [-1, 1]]
        all_cases.append((Aword, Bword, origin % 2, shifted))
        if not origin % 2:
            continue
        contents = [min(valuation(c) for c in polynomial_at_t if c)
                    for polynomial_at_t in shifted]
        require(min(contents) >= 0, "Shifted polynomial is not integral")
        content = min(contents)
        histogram[content] = histogram.get(content, 0) + 1
        if content not in witnesses:
            witnesses[content] = {"A": A, "B": B, "origin_count": origin,
                                  "polynomial": [str(c) for c in polynomial],
                                  "node_contents": contents}
        checked += 1
    # A signed integer realization of H(T)=1-T^2. Replacing its entries
    # by their canonical mod-2 representatives can change higher jets.
    signed_A = [-3, -4, 0, -1]
    signed_B = [1, -1, 1, 0]
    signed = tensor_polynomial(signed_A, signed_B, transfers)
    require(signed == [F(1), F(0), F(-1)] + [F(0)] * (len(signed) - 3),
            "Signed generic taper realization")
    canonical = tensor_polynomial([x % 2 for x in signed_A], [x % 2 for x in signed_B], transfers)
    signed_contents = [min(valuation(c) for c in shift(signed, t, 4) if c) for t in [-1, 1]]
    canonical_contents = [min(valuation(c) for c in shift(canonical, t, 4) if c) for t in [-1, 1]]
    first_A, first_B = [1, 1, 0, 0], [1, 0, 1, 0]
    second_A, second_B = [1, 1, 1, 0], [0, 1, 1, 0]
    first = tensor_polynomial(first_A, first_B, transfers)
    second = tensor_polynomial(second_A, second_B, transfers)
    diagonal = kernels[0][0]
    require(not any(add(first, add([F(2)], diagonal, -1), -1)), "First canonical identity")
    require(not any(add(second, add([F(2)], multiply(diagonal, [F(0), F(0), F(2), F(1)])), -1)),
            "Second canonical identity")
    difference = add(first, second, -1)
    collision_contents = [min(valuation(c) for c in shift(difference, t, 4) if c) for t in [-1, 1]]
    require(collision_contents == [3, 4], "Canonical opposite-parity collision")
    # Second registered question, same complete input universe: at which
    # p in 1..6 do the full active jets uniquely determine origin parity?
    # Compare *all pairs of cases*, not only odd cases against zero data.
    parity_recovery = []
    for p in range(1, 7):
        modulus = 1 << p
        classes = {}
        ambiguous = set()
        example = None
        for Aword, Bword, parity, shifted in all_cases:
            residue = tuple(c.numerator * pow(c.denominator, -1, modulus) % modulus
                            for polynomial_at_t in shifted for c in polynomial_at_t)
            if residue in classes:
                old_A, old_B, old_parity = classes[residue]
                if parity != old_parity:
                    ambiguous.add(residue)
                    if example is None:
                        example = {"first_A_word": old_A, "first_B_word": old_B,
                                   "second_A_word": Aword, "second_B_word": Bword}
            else:
                classes[residue] = (Aword, Bword, parity)
        parity_recovery.append({"p": p, "distinct_local_data": len(classes),
                                "ambiguous_local_data": len(ambiguous),
                                "opposite_origin_parities_example": example})
    report = {"status": "PASS", "scope": "complete L=2 Boolean-table screen; no growing-packet theorem",
              "registered_tensor_pairs": 256, "origin_odd_pairs": checked,
              "min_active_node_content_histogram": histogram,
              "witness_for_each_content": witnesses,
              "complete_local_data_parity_classification": parity_recovery,
              "signed_taper_example": {"A": signed_A, "B": signed_B,
                                        "polynomial": "1-T^2", "signed_node_contents": signed_contents,
                                        "canonical_mod2_node_contents": canonical_contents},
              "canonical_collision": {"first_A": first_A, "first_B": first_B,
                                      "second_A": second_A, "second_B": second_B,
                                      "origin_counts": [int(evaluate(first, 0)), int(evaluate(second, 0))],
                                      "difference_node_contents": collision_contents},
              "bindings": {"script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
                           "reference_sha256": sha256((HERE / "verify.py").read_bytes()).hexdigest(),
                           "proof_sha256": sha256((HERE / "PROOF.md").read_bytes()).hexdigest()}}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
