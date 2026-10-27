"""Exact global-symmetry-dual reference checks, independent of basis pruning."""

from fractions import Fraction as F
from math import factorial, lcm, prod


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def multiply(left: dict, right: dict) -> dict:
    result = {}
    for alpha, x in left.items():
        for beta, y in right.items():
            total = tuple(a + b for a, b in zip(alpha, beta))
            result[total] = result.get(total, 0) + x * y
    return {alpha: x for alpha, x in result.items() if x}


def power(polynomial: dict, n: int) -> dict:
    result = {(0, 0, 0, 0): 1}
    for _ in range(n):
        result = multiply(result, polynomial)
    return result


def linear(row: tuple[int, ...]) -> dict:
    return {tuple(int(j == k) for j in range(4)): value for k, value in enumerate(row) if value}


def substitute(polynomial: dict, matrix: tuple) -> dict:
    forms = [linear(row) for row in matrix]
    result = {}
    for alpha, value in polynomial.items():
        term = {(0, 0, 0, 0): value}
        for form, exponent in zip(forms, alpha):
            term = multiply(term, power(form, exponent))
        for beta, coefficient in term.items():
            result[beta] = result.get(beta, 0) + coefficient
    return {alpha: value for alpha, value in result.items() if value}


def evaluate(polynomial: dict, at: tuple[int, ...]) -> int:
    return sum(coefficient * prod(z ** exponent for z, exponent in zip(at, alpha))
               for alpha, coefficient in polynomial.items())


def fast_walsh(values: list[int]) -> list[int]:
    answer = list(values)
    half = 1
    while half < len(answer):
        for start in range(0, len(answer), 2 * half):
            for j in range(start, start + half):
                x, y = answer[j], answer[j + half]
                answer[j], answer[j + half] = x + y, x - y
        half *= 2
    return answer


def check_dual(walsh_module) -> dict:
    H = walsh_module.HADAMARD
    J = {(1, 1, 1, 1): 1}
    for row in H:
        J = multiply(J, linear(row))
    # Independent closed expansion of the product of the four Walsh forms.
    quartic = {}
    for j in range(4):
        alpha = [0] * 4
        alpha[j] = 4
        quartic[tuple(alpha)] = 1
    for i in range(4):
        for j in range(i + 1, 4):
            alpha = [0] * 4
            alpha[i] = alpha[j] = 2
            quartic[tuple(alpha)] = -2
    quartic[(1, 1, 1, 1)] = 8
    require(J == multiply({(1, 1, 1, 1): 1}, quartic), "Base dual expansion")
    L = linear((1, 1, 0, 0))
    require(substitute(J, H) == {alpha: (1 << 8) * c for alpha, c in J.items()},
            "Degree-eight dual eigenidentity")
    require(substitute(L, H) == {alpha: 2 * c for alpha, c in L.items()}, "Linear dual eigenidentity")
    require(5 ** 5 < 2 ** 12 and 3 ** 2 > 8, "Strict entropy-rate separation")
    log17_upper = F(408747, 100000)
    require(17 ** 100000 < 2 ** 408747, "Certified log2(17) upper bound")
    macro_two_lower = (5 - F(17, 32) * log17_upper) / 4
    require(macro_two_lower ** 2 > F(1, 2), "Two-bit macro barrier")
    require(F(253, 384) ** 2 < F(1, 2), "Three-bit macro dual is below target")
    macro_three = [[1, 35, 28], [1, 3, -4], [1, -5, 4]]
    require([[sum(macro_three[i][k] * macro_three[k][j] for k in range(3))
              for j in range(3)] for i in range(3)] == [[64, 0, 0], [0, 64, 0], [0, 0, 64]],
            "Three-class macro Walsh square")
    require([sum(x * y for x, y in zip(row, [1, 1, -1])) for row in macro_three] == [8, 8, -8],
            "Three-class macro quadratic eigenvector")
    macro_labels = [(a, b) for a in range(8) for b in range(8)]
    def macro_class(a: int, b: int) -> int:
        return 0 if a == b == 0 else 1 + ((a & b).bit_count() % 2)
    require([sum(macro_class(a, b) == j for a, b in macro_labels) for j in range(3)] == [1, 35, 28],
            "Macro character-class multiplicities")
    macro_characters = 0
    for c, d in macro_labels:
        row = [0, 0, 0]
        for a, b in macro_labels:
            row[macro_class(a, b)] += (-1) ** (((b & c).bit_count() + (a & d).bit_count()) % 2)
            macro_characters += 1
        require(row == macro_three[macro_class(c, d)], "Direct macro Walsh character sums")
    symbolic = []
    polynomials = {}
    for r in range(8, 33):
        k, s = divmod(r, 8)
        P = multiply(power(J, k), power(L, s))
        minimum_orbit = factorial(r) // (factorial(r - 3 * k) * factorial(k) ** 3)
        require(all(sum(alpha) == r and min(alpha) >= k for alpha in P), "Dual support constraint")
        require(all(walsh_module.multiplicity(alpha) >= minimum_orbit for alpha in P),
                "Dual orbit-size bound")
        require(evaluate(P, (1, 1, 1, -1)) == 16 ** k * 2 ** s, "Nonzero weighted target pairing")
        symbolic.append({"r": r, "nonzero_dual_types": len(P),
                         "minimum_orbit_bound": minimum_orbit})
        if r in [8, 9]:
            polynomials[r] = P
    full = []
    for r, P in polynomials.items():
        k, s = divmod(r, 8)
        rational_values = {alpha: F(coefficient, walsh_module.multiplicity(alpha))
                           for alpha, coefficient in P.items()}
        denominator = 1
        for value in rational_values.values():
            denominator = lcm(denominator, value.denominator)
        values_by_type = {alpha: int(denominator * value) for alpha, value in rational_values.items()}
        values, wrong = [], []
        target_pairing = 0
        first_nonzero = None
        for word in range(4 ** r):
            counts = [0, 0, 0, 0]
            for j in range(r):
                counts[(word >> (2 * j)) & 3] += 1
            alpha = tuple(counts)
            value = values_by_type.get(alpha, 0)
            values.append(value)
            wrong.append(P.get(alpha, 0))
            target_pairing += value * (-1) ** counts[3]
            if value and first_nonzero is None:
                first_nonzero = (word, value, alpha)
        spectrum = fast_walsh(values)
        even_mask = sum(1 << (2 * j) for j in range(r))
        odd_mask = even_mask << 1
        for word, value in enumerate(values):
            swapped = ((word & even_mask) << 1) | ((word & odd_mask) >> 1)
            require(spectrum[swapped] == (1 << r) * value, "Full-word symplectic Walsh eigenidentity")
        require(target_pairing == denominator * 16 ** k * 2 ** s, "Full-word weighted target pairing")
        bad_control = None
        if r == 8:
            wrong_spectrum = fast_walsh(wrong)
            bad_control = any(wrong_spectrum[((word & even_mask) << 1) | ((word & odd_mask) >> 1)]
                              != (1 << r) * value for word, value in enumerate(wrong))
            require(bad_control, "Missing-orbit-normalization control did not fail")
        minimum_orbit = factorial(r) // (factorial(r - 3 * k) * factorial(k) ** 3)
        require(first_nonzero is not None and minimum_orbit > 1, "Nonsymmetric control unavailable")
        word, value, alpha = first_nonzero
        # A delta at this *one word* has support one and nonzero dual pairing.
        # It is not permutation symmetric, demonstrating the scope boundary.
        require(value != 0 and 1 < minimum_orbit, "Nonsymmetric singleton control")
        full.append({"r": r, "all_word_eigenidentities": 4 ** r,
                     "weighted_pairing": str(F(target_pairing, denominator)),
                     "wrong_orbit_normalization_rejected": bad_control,
                     "nonsymmetric_singleton": {"word": word, "type": alpha,
                         "row_support": 1, "col_support": 4 ** r,
                         "nonzero_dual_pairing": str(F(value, denominator))}})
    bound_table = []
    for r in [8, 16, 32, 64, 128, 256]:
        k = r // 8
        m = factorial(r) // (factorial(r - 3 * k) * factorial(k) ** 3)
        bound_table.append({"r": r, "minimum_orbit": str(m),
                            "shared_bit_lower_bound": (m * m - 1).bit_length()})
    return {"base_polynomial_terms": len(J), "symbolic_duals": symbolic,
            "full_word_checks": full, "exact_bound_table": bound_table,
            "macro_alphabet_controls": {"two_bit_rho_rational_lower": str(macro_two_lower),
                "two_bit_lower_square_exceeds_half": True,
                "three_bit_dual_upper": "253/384", "three_bit_upper_square_below_half": True,
                "three_class_transform_square": "64 I", "direct_macro_character_checks": macro_characters},
            "scope": "all-size proof is in SYMMETRY-BARRIER.md; finite checks verify the listed domains"}
