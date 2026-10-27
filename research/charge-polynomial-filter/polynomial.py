"""Exact charge-polynomial lift of the pinned normal-order recurrence."""

from collections import Counter
from functools import lru_cache
from hashlib import sha256
import importlib.util
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFERENCE = HERE.parent / "charged-asymmetric-crossing" / "model.py"
if sha256(REFERENCE.read_bytes()).hexdigest() != "7f495836772409f6c705642040f6b5a4307532539037c7d28bed1bdf66fd6fef":
    raise ValueError("Pinned asymmetric codebook changed")
spec = importlib.util.spec_from_file_location("filter_codebook", REFERENCE)
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)
require = model.require


def trim(poly):
    values = list(poly)
    while values and not values[-1]:
        values.pop()
    return tuple(values)


def product(left, right):
    if not left or not right:
        return ()
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return trim(result)


def accumulate(result, monomial, poly, scale=1, shift=0):
    if not poly or not scale:
        return
    old = result.get(monomial, [])
    old.extend([0] * max(0, len(poly) + shift - len(old)))
    for i, coefficient in enumerate(poly):
        old[i + shift] += scale * coefficient
    result[monomial] = old


def add_scaled(result, values, scale=1, shift=0):
    for monomial, poly in values:
        accumulate(result, monomial, poly, scale, shift)


def freeze(result):
    return tuple(sorted((m, p) for m, values in result.items() if (p := trim(values))))


def evaluate(values, charge):
    return tuple((monomial, value) for monomial, poly in values
                 if (value := sum(coefficient * charge ** j for j, coefficient in enumerate(poly))))


@lru_cache(maxsize=200_000)
def operator(monomial, mode, argument):
    target = sum(argument) + mode
    if target < 0:
        return ()
    if not monomial:
        return ((argument, (1,)),) if mode == 0 else ()
    n, tail = monomial[0], monomial[1:]
    result = {}
    for created in range(n, target + 1):
        scale = comb(created - 1, n - 1)
        for output, poly in operator(tail, mode - created, argument):
            output = tuple(sorted(output + (created,), reverse=True))
            accumulate(result, output, poly, scale)
    add_scaled(result, operator(tail, mode, argument), (-1) ** (n - 1), shift=1)
    for destroyed, multiplicity in Counter(argument).items():
        reduced = list(argument)
        reduced.remove(destroyed)
        scale = model.predecessor.binomial(-destroyed - 1, n - 1) * destroyed * multiplicity
        add_scaled(result, operator(tail, mode + destroyed, tuple(reduced)), scale)
    return freeze(result)


@lru_cache(maxsize=80_000)
def dual_operator(partition, taper, mode, argument):
    h = sum(partition)
    result = {}
    for monomial, value in model.predecessor.dual_polynomial(partition):
        scale = value * model.predecessor.binomial(sum(monomial) + h, taper)
        add_scaled(result, operator(monomial, mode, argument), scale)
    return freeze(result)


def piece_vector(mu, nu, argument, shift, reverse=False):
    h = sum(mu)
    require(sum(nu) == h, "Inconsistent label grades")
    result = {}
    for i in range(2 * h + 1):
        scale = (-1) ** i * model.predecessor.dual_scale(nu)
        if reverse:
            first = dual_operator(mu, i, shift - h + i, argument)
            for intermediate, a in first:
                for output, b in operator(nu, h - shift - i, intermediate):
                    accumulate(result, output, product(a, b), scale)
        else:
            first = operator(nu, h - shift - i, argument)
            for intermediate, a in first:
                for output, b in dual_operator(mu, i, shift - h + i, intermediate):
                    accumulate(result, output, product(a, b), scale)
    answer = freeze(result)
    require(all(len(poly) <= len(mu) + len(nu) + 1 for _, poly in answer), "Charge degree exceeded current count")
    return answer


def clear_caches():
    operator.cache_clear()
    dual_operator.cache_clear()
    model.charged.operator.cache_clear()
    model.charged.dual_operator.cache_clear()
