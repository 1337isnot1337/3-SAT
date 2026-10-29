"""Exact finite grouping certificates; this does not run the fast contraction."""
from itertools import product, combinations
from math import comb
from random import Random
from pathlib import Path
from hashlib import sha256
import json


def normalize(terms):
    out = set()
    for term in terms:
        if term in out:
            out.remove(term)
        else:
            out.add(term)
    return frozenset(out)


def value(poly, assignment):
    return sum((assignment & term) == term for term in poly) % 2


def bits(mask):
    return [i for i in range(mask.bit_length()) if mask >> i & 1]


def expand(local, variables):
    return sum(((local >> j) & 1) << v for j, v in enumerate(variables))


def indicator(equations):
    scope = 0
    for equation in equations:
        for monomial in equation:
            scope |= monomial
    variables = bits(scope)
    coefficients = [int(all(value(p, expand(x, variables)) == 0 for p in equations))
                    for x in range(1 << len(variables))]
    for j in range(len(variables)):
        for mask in range(len(coefficients)):
            if mask >> j & 1:
                coefficients[mask] ^= coefficients[mask ^ (1 << j)]
    return frozenset(expand(x, variables) for x, c in enumerate(coefficients) if c)


def gf_mul(a, b):
    c = 0
    while b:
        if b & 1:
            c ^= a
        b >>= 1
        a <<= 1
        if a & 16:
            a ^= 19
    return c


def gf_product(items):
    out = 1
    for item in items:
        out = gf_mul(out, item)
    return out


def direct_count(equations, n, weights):
    out = 0
    for x in range(1 << n):
        if all(value(p, x) == 0 for p in equations):
            out ^= gf_product(weights[i] for i in range(n) if x >> i & 1)
    return out


def partition_function(factors, n, weights):
    out = 0
    for terms in product(*factors):
        selected = 0
        for monomial in terms:
            selected |= monomial
        out ^= gf_product(weights[i] if selected >> i & 1 else 1 ^ weights[i]
                          for i in range(n))
    return out


def partitions(count):
    if count == 0:
        yield ()
        return
    for previous in partitions(count - 1):
        yield previous + ((count - 1,),)
        for j in range(len(previous)):
            yield previous[:j] + (previous[j] + (count - 1,),) + previous[j + 1:]


def certificate(equations, grouping, variable_groups):
    factors = [indicator([equations[i] for i in group]) for group in grouping]
    scopes = []
    for factor in factors:
        scope = 0
        for term in factor:
            scope |= term
        scopes.append(scope)
    profiles = []
    for factor in factors:
        profiles.append(sorted({tuple((term & group).bit_count() for group in variable_groups)
                                for term in factor}))
    total = 1
    for options in profiles:
        total *= len(options)
    max_wires = max_degree = 0
    worst_profile = None
    for profile in product(*profiles):
        wire_counts = [[(comb((scope & group).bit_count(), d) - 1).bit_length()
                        for group, d in zip(variable_groups, degrees)]
                       for scope, degrees in zip(scopes, profile)]
        wires = sum(map(sum, wire_counts))
        degree = max([sum(row) for row in wire_counts] +
                     [sum(row[j] for row in wire_counts) for j in range(len(variable_groups))], default=0)
        if wires > max_wires:
            worst_profile = profile
        max_wires = max(max_wires, wires)
        max_degree = max(max_degree, degree)
    return {
        'grouping': grouping,
        'factor_degrees': [max((term.bit_count() for term in f), default=0) for f in factors],
        'factor_scope_sizes': [scope.bit_count() for scope in scopes],
        'profile_count': total,
        'max_wires': max_wires,
        'max_tensor_degree': max_degree,
        # Discovery is paid on ORIGINAL scopes, before semantic simplification.
        'max_discovery_scope': max((len(bits(sum_scope([equations[i] for i in group])))
                                    for group in grouping), default=0),
        'worst_wire_profile': worst_profile,
    }, factors


def sum_scope(polys):
    scope = 0
    for p in polys:
        for term in p:
            scope |= term
    return scope


def encoded_sum(factors, variable_groups, n, weights):
    """Literal profile/index contraction, including invalid binary indices."""
    scopes = [sum_scope([f]) for f in factors]
    options = [sorted({tuple((t & g).bit_count() for g in variable_groups) for t in f})
               for f in factors]
    out = 0
    invalid = 0
    for profile in product(*options):
        choices = []
        for scope, degrees in zip(scopes, profile):
            for g, degree in zip(variable_groups, degrees):
                subset_masks = [sum(1 << v for v in subset)
                                for subset in combinations(bits(scope & g), degree)]
                width = (len(subset_masks) - 1).bit_length()
                choices.append(subset_masks + [None] * ((1 << width) - len(subset_masks)))
        for local in product(*choices):
            if None in local:
                invalid += 1
                continue
            selected = 0
            ok = True
            for i, f in enumerate(factors):
                term = 0
                for j in range(len(variable_groups)):
                    term |= local[i * len(variable_groups) + j]
                if term not in f:
                    ok = False
                    break
                selected |= term
            if ok:
                out ^= gf_product(weights[i] if selected >> i & 1 else 1 ^ weights[i]
                                  for i in range(n))
    return out, invalid


def main():
    rng = Random(14820261028)
    identity_cases = profile_cases = invalid = 0
    # Independent truth enumeration against coefficient products and encoded indices.
    for n in range(0, 6):
        for trial in range(40):
            possible = [x for x in range(1 << n) if x.bit_count() <= 3]
            equations = [normalize(rng.choices(possible, k=rng.randrange(6)))
                         for _ in range(rng.randrange(5))]
            weights = [rng.randrange(16) for _ in range(n)]
            target = direct_count(equations, n, weights)
            groups = (sum(1 << i for i in range(n) if i % 2 == 0),
                      sum(1 << i for i in range(n) if i % 2 == 1))
            for grouping in partitions(len(equations)):
                cert, factors = certificate(equations, grouping, groups)
                assert partition_function(factors, n, weights) == target
                identity_cases += 1
                got, bad = encoded_sum(factors, groups, n, weights)
                assert got == target
                invalid += bad
                profile_cases += cert['profile_count']
    # All small systems: the degree of a product is not bounded by the group count.
    disjoint = [frozenset([3]), frozenset([12]), frozenset([48])]
    f = indicator(disjoint)
    assert max(t.bit_count() for t in f) == 6  # one group, degree SIX
    # Genuine Boolean cancellation, but nontrivial degree remains.
    cancellation = [frozenset([3]), frozenset([3, 5])]
    cf = indicator(cancellation)
    assert cf == frozenset([0, 3, 5, 7])
    # Finite exhaustive grouping profiles, not a claim about runtime constants.
    fixture = [frozenset([3]), frozenset([3, 5]), frozenset([12]),
               frozenset([12, 20]), frozenset([48]), frozenset([48, 33])]
    groups = (7, 56)
    reports = []
    for grouping in partitions(len(fixture)):
        cert, factors = certificate(fixture, grouping, groups)
        assert partition_function(factors, 6, [2,3,4,5,6,7]) == direct_count(fixture, 6, [2,3,4,5,6,7])
        reports.append(cert)
    def vector(c):
        return (c['profile_count'], c['max_wires'], c['max_tensor_degree'], c['max_discovery_scope'])
    frontier = [c for c in reports if not any(
        all(a <= b for a,b in zip(vector(d),vector(c))) and vector(d) != vector(c)
        for d in reports)]
    result = {'status':'PASS', 'scope':'finite exact grouping and encoding checks; no fast contraction or global improvement',
              'seed':14820261028, 'identity_cases':identity_cases,
              'profiles_checked':profile_cases, 'invalid_index_assignments_checked':invalid,
              'fixture_groupings':len(reports), 'pareto_groupings':frontier,
              'negative_control':{'one_group_degree':6, 'equations':3},
              'cancellation_control':{'ungrouped_degree_sum':4, 'grouped_degree':3},
              'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
