"""Exact finite Appendix-B operators from Hexagon 2610.00577v1.

Original reference implementation, Apache-2.0; AI-assisted. The mathematical
definitions come from Anthropic's CC BY 4.0 paper, pinned in SOURCES.json.
These small-input routines do not implement its SAT or clique algorithm.
"""

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import comb, factorial


@lru_cache(None)
def partitions(weight, largest=None):
    if weight < 0:
        return ()
    if weight == 0:
        return ((),)
    if largest is None:
        largest = weight
    result = []
    for first in range(1, min(largest, weight) + 1):
        result.extend((first,) + tail for tail in partitions(weight - first, first))
    return tuple(sorted(result))


def binomial(integer, degree):
    if degree < 0:
        return 0
    if integer >= 0:
        return comb(integer, degree) if degree <= integer else 0
    return (-1) ** degree * comb(degree - integer - 1, degree)


def add_scaled(result, terms, scale):
    if scale:
        for monomial, value in terms:
            result[monomial] = result.get(monomial, 0) + scale * value


def freeze(poly):
    return tuple(sorted((monomial, value) for monomial, value in poly.items() if value))


@lru_cache(maxsize=300_000)
def operator(monomial, mode, argument):
    """a[mode] t^argument, by the paper's independent-of-energy O2 recurrence."""
    target = sum(argument) + mode
    if target < 0:
        return ()
    if not monomial:
        return ((argument, 1),) if mode == 0 else ()
    n, tail = monomial[0], monomial[1:]
    result = {}
    for created in range(n, target + 1):
        scale = comb(created - 1, n - 1)
        for output, value in operator(tail, mode - created, argument):
            output = tuple(sorted(output + (created,), reverse=True))
            result[output] = result.get(output, 0) + scale * value
    for destroyed, multiplicity in Counter(argument).items():
        reduced = list(argument)
        reduced.remove(destroyed)
        scale = binomial(-destroyed - 1, n - 1) * destroyed * multiplicity
        add_scaled(result, operator(tail, mode + destroyed, tuple(reduced)), scale)
    return freeze(result)


def direct_operator(monomial, mode, argument):
    """Independent normal-ordered definition (eq:ops), for tiny checks only."""
    energy = sum(argument)
    target = energy + mode
    if target < 0:
        return ()
    if not monomial:
        return ((argument, 1),) if mode == 0 else ()
    choices = tuple(range(-target, 0)) + tuple(range(1, energy + 1))
    result = {}
    for indices in product(choices, repeat=len(monomial)):
        if sum(indices) != -mode:
            continue
        scale = 1
        output = list(argument)
        for n, index in zip(monomial, indices):
            scale *= binomial(-index - 1, n - 1)
        if not scale:
            continue
        # Normal ordering: perform every differentiation before multiplication.
        for index in indices:
            if index > 0:
                multiplicity = output.count(index)
                if not multiplicity:
                    scale = 0
                    break
                scale *= index * multiplicity
                output.remove(index)
        if scale:
            output.extend(-index for index in indices if index < 0)
            output = tuple(sorted(output, reverse=True))
            result[output] = result.get(output, 0) + scale
    return freeze(result)


@lru_cache(None)
def dual_polynomial(partition):
    """a^mu = product_n (-1)^(n-1) y_n, y_n=sum_j binom(n,j)t_j."""
    poly = {(): 1}
    for n in partition:
        updated = {}
        for monomial, value in poly.items():
            for j in range(1, n + 1):
                output = tuple(sorted(monomial + (j,), reverse=True))
                updated[output] = updated.get(output, 0) + value * (-1) ** (n - 1) * comb(n, j)
        poly = updated
    return freeze(poly)


def dual_scale(partition):
    denominator = 1
    for part, multiplicity in Counter(partition).items():
        denominator *= part ** multiplicity * factorial(multiplicity)
    return factorial(sum(partition)) // denominator


@lru_cache(maxsize=100_000)
def dual_operator(partition, taper, mode, argument):
    h = sum(partition)
    result = {}
    for monomial, value in dual_polynomial(partition):
        scale = value * binomial(sum(monomial) + h, taper)
        add_scaled(result, operator(monomial, mode, argument), scale)
    return freeze(result)


def piece_vector(x, v, y, shift, reverse=False):
    """Q_shift(a^x,b^v)t^y, in either of the two operator orders."""
    h = sum(x)
    if sum(v) != h or sum(y) != h:
        raise ValueError("Inconsistent input energies")
    result = {}
    for i in range(2 * h + 1):
        scale = (-1) ** i * dual_scale(v)
        if reverse:
            first = dual_operator(x, i, shift - h + i, y)
            for intermediate, value in first:
                add_scaled(result, operator(v, h - shift - i, intermediate), scale * value)
        else:
            first = operator(v, h - shift - i, y)
            for intermediate, value in first:
                add_scaled(result, dual_operator(x, i, shift - h + i, intermediate), scale * value)
    return freeze(result)


def exact_rank(matrix):
    """Rational Gaussian elimination; intended for small matrices."""
    rows = [[Fraction(value) for value in row] for row in matrix]
    rank = 0
    for column in range(len(rows[0]) if rows else 0):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        base = rows[rank]
        for i in range(rank + 1, len(rows)):
            if rows[i][column]:
                scale = rows[i][column] / base[column]
                for j in range(column + 1, len(base)):
                    rows[i][j] -= scale * base[j]
                rows[i][column] = Fraction(0)
        rank += 1
        if rank == len(rows):
            break
    return rank


def modular_rank(matrix, prime):
    """A lower bound on rational rank; an upper bound must be proved separately."""
    rows = [[value % prime for value in row] for row in matrix]
    rank = 0
    for column in range(len(rows[0]) if rows else 0):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        base = rows[rank]
        inverse = pow(base[column], -1, prime)
        for i in range(rank + 1, len(rows)):
            if rows[i][column]:
                scale = rows[i][column] * inverse % prime
                for j in range(column + 1, len(base)):
                    rows[i][j] = (rows[i][j] - scale * base[j]) % prime
                rows[i][column] = 0
        rank += 1
        if rank == len(rows):
            break
    return rank


def build_pieces(bits, check_reversed=False):
    dimension = 1 << bits
    h = 2
    while len(partitions(h)) < dimension:
        h += 1
    states = partitions(h)[:dimension]
    output_index = {state: i for i, state in enumerate(states)}
    pieces = {s: [0] * dimension ** 4 for s in range(-2 * h, 2 * h + 1)}
    order_checks = 0
    for x, y, v in product(range(dimension), repeat=3):
        for s, tensor in pieces.items():
            vector = piece_vector(states[x], states[v], states[y], s)
            if check_reversed:
                if vector != piece_vector(states[x], states[v], states[y], s, reverse=True):
                    raise ValueError("Two operator orders disagree")
                order_checks += 1
            for state, value in vector:
                if state in output_index:
                    u = output_index[state]
                    tensor[((x * dimension + y) * dimension + u) * dimension + v] = value
    for x, y, u, v in product(range(dimension), repeat=4):
        index = ((x * dimension + y) * dimension + u) * dimension + v
        expected = factorial(h) if x == v and y == u else 0
        if sum(tensor[index] for tensor in pieces.values()) != expected:
            raise ValueError("Sum of pieces fails the crossing identity")
    return h, states, pieces, order_checks


def flatten(tensor, dimension, direction):
    if direction == "row":
        width = dimension ** 2
        return [tensor[i:i + width] for i in range(0, len(tensor), width)]
    if direction == "column":
        return [[tensor[((x * dimension + y) * dimension + u) * dimension + v]
                 for y in range(dimension) for v in range(dimension)]
                for x in range(dimension) for u in range(dimension)]
    raise ValueError("Unknown flattening direction")
