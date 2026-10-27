"""Small reference routines for the scalar parity-projector construction.

Polynomials over F_2 are tuples of distinct variable masks. Mask zero is the
constant monomial. These are research oracles, not an implementation of the
accepted subexponential contraction algorithm. The one-coefficient routine
uses polynomial space; full coefficient tables are only for small checks.
"""

from __future__ import annotations

from itertools import combinations, product
from math import comb


def normalize(terms, n):
    """Normalize lists of variable indices, including repeated variables."""
    masks = set()
    for term in terms:
        mask = 0
        for variable in term:
            if not 0 <= variable < n:
                raise ValueError("Variable outside declared range")
            mask |= 1 << variable
        masks.symmetric_difference_update((mask,))
    return tuple(sorted(masks))


def parity(equation, assignment):
    return sum(assignment & term == term for term in equation) % 2


def scope(equation):
    result = 0
    for term in equation:
        result |= term
    return result


def submasks(mask):
    subset = mask
    while True:
        yield subset
        if subset == 0:
            break
        subset = (subset - 1) & mask


def coefficient(equation, support, precision=None):
    """Integer Mobius coefficient of the even-parity indicator.

    Time is 2^|support| times a polynomial in the input length and precision.
    Space is polynomial. No division modulo a power of two is used.
    """
    value = sum(
        (-1 if (support.bit_count() - subset.bit_count()) % 2 else 1)
        * (1 - parity(equation, subset))
        for subset in submasks(support)
    )
    return value if precision is None else value % (1 << precision)


def coefficient_table(equation):
    """Independent symbolic union-product expansion, only for tiny inputs."""
    phase = {0: 1}
    for term in equation:
        updated = dict(phase)
        for support, value in phase.items():
            union = support | term
            updated[union] = updated.get(union, 0) - 2 * value
        phase = {support: value for support, value in updated.items() if value}
    phase[0] = phase.get(0, 0) + 1
    if any(value % 2 for value in phase.values()):
        raise ValueError("Projector numerator is not coefficientwise even")
    return {support: value // 2 for support, value in phase.items() if value}


def direct_count(equations, n):
    return sum(
        all(parity(equation, assignment) == 0 for equation in equations)
        for assignment in range(1 << n)
    )


def incidence_sum(equations, n, k, precision, cutoff=None):
    """Sum scalar incidence monomials; exponential finite reference only."""
    if cutoff is None:
        cutoff = k * (len(equations) + precision - 1)
    tables = [coefficient_table(equation) for equation in equations]
    total = 0
    retained = 0
    discarded = 0
    for terms in product(*(tuple(table.items()) for table in tables)):
        degree = sum(support.bit_count() for support, _ in terms)
        value = 1
        covered = 0
        for support, local in terms:
            covered |= support
            value *= local
        if degree > cutoff:
            if value % (1 << precision):
                raise ValueError("Discarded coefficient survives target modulus")
            discarded += 1
            continue
        retained += 1
        total += value << (n - covered.bit_count())
    return total % (1 << precision), retained, discarded


def bit_ceiling(count):
    return (count - 1).bit_length()


def decode_subset(items, size, code):
    """Lexicographic combinatorial unranking, without a subset table."""
    count = comb(len(items), size)
    if not 0 <= code < count:
        return None
    chosen = []
    start = 0
    remaining = size
    while remaining:
        for position in range(start, len(items)):
            completions = comb(len(items) - position - 1, remaining - 1)
            if code < completions:
                chosen.append(items[position])
                start = position + 1
                remaining -= 1
                break
            code -= completions
    return tuple(chosen)


def grouped_contraction(equations, n, k, precision, groups=2):
    """Explicitly enumerate degree arrays and Boolean wires on tiny networks.

    This checks the actual grouped encoding, including invalid codes and
    zero-wire group pairs. It does not call a fast contraction algorithm.
    """
    a = len(equations)
    cutoff = k * (a + precision - 1)
    pairs = [(g, h) for g in range(groups) for h in range(groups)]
    incidences = {
        pair: tuple(
            (i, v)
            for i, equation in enumerate(equations)
            for v in range(n)
            if i % groups == pair[0]
            and v % groups == pair[1]
            and scope(equation) >> v & 1
        )
        for pair in pairs
    }
    tables = [coefficient_table(equation) for equation in equations]
    result = 0
    stats = {"arrays": 0, "wire_assignments": 0, "invalid_codes": 0,
             "valid_indices": 0, "zero_wire_pairs": 0, "max_wires": 0}
    for degrees in product(*(range(len(incidences[pair]) + 1) for pair in pairs)):
        if sum(degrees) > cutoff:
            continue
        stats["arrays"] += 1
        counts = [comb(len(incidences[pair]), d) for pair, d in zip(pairs, degrees)]
        widths = [bit_ceiling(count) for count in counts]
        stats["zero_wire_pairs"] += widths.count(0)
        stats["max_wires"] = max(stats["max_wires"], sum(widths))
        # Exhaust every binary code, rather than only valid subset indices.
        for codes in product(*(range(1 << width) for width in widths)):
            stats["wire_assignments"] += 1
            selected = []
            for pair, d, code in zip(pairs, degrees, codes):
                subset = decode_subset(incidences[pair], d, code)
                if subset is None:
                    stats["invalid_codes"] += 1
                    break
                selected.extend(subset)
            else:
                stats["valid_indices"] += 1
                supports = [0] * a
                covered = 0
                for i, v in selected:
                    supports[i] |= 1 << v
                    covered |= 1 << v
                entry_product = 1
                for i, support in enumerate(supports):
                    entry_product *= tables[i].get(support, 0)
                result += entry_product << (n - covered.bit_count())
    return result % (1 << precision), stats
