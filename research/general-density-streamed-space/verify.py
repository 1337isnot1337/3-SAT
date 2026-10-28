"""Finite subsumption-branch and sparse outer-identity controls."""
from hashlib import sha256
import importlib.util
from itertools import combinations, product
from math import comb
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
spec = importlib.util.spec_from_file_location('general_crt',ROOT/'deterministic-crt-transfer'/'verify.py')
crt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(crt)


def require(test, message):
    if not test:
        raise AssertionError(message)


def clauses(n):
    return [frozenset((j+1)*s for j,s in enumerate(pattern) if s)
            for pattern in product((0,1,-1),repeat=n)]


def antichain(items):
    unique = set(items)
    return frozenset(c for c in unique if not any(d < c for d in unique))


def closure(items, universe):
    return frozenset(c for c in universe if any(d <= c for d in items))


def branch_checks():
    universe = clauses(3)
    families = set()
    for size in range(4):
        for seq in combinations(universe,size):
            families.add(antichain(seq))
    cases = 0
    for current in families:
        before = closure(current,universe)
        possible_h = set()
        for c in current:
            for length in range(1,len(c)):
                possible_h.update(frozenset(h) for h in combinations(sorted(c),length))
        for h in possible_h:
            containing = [c for c in current if h < c]
            for fsize in range(1,len(containing)+1):
                for chosen in combinations(containing,fsize):
                    children = (antichain(set(current)|{h}),
                                antichain(set(current)|{e-h for e in chosen}))
                    for child in children:
                        after = closure(child,universe)
                        require(before < after,'Branch does not strictly increase closure')
                        cases += 1
    return len(families),cases


def outer_controls():
    all_clauses = clauses(2)
    formulae = [(a,b) for a in all_clauses for b in all_clauses]
    zero = positive = mismatched = crt_cases = 0
    primes = crt.good_primes(12,15)
    for formula in formulae:
        checks = [frozenset(j for j in range(2) if mask >> j & 1) for mask in range(4)]
        for threshold in (1,2):
            for a in checks:
                for b in checks:
                    x = f = sat = 0
                    for bits in product((0,1),repeat=2):
                        violated = {j for j,c in enumerate(formula)
                                    if not any(bits[abs(lit)-1] == (lit>0) for lit in c)}
                        sat += not violated
                        even = all(len(violated & check)%2 == 0 for check in (a,b))
                        if even:
                            x += comb(len(violated),threshold+1) if len(violated)>threshold else 0
                            f += sum((-1)**j * comb(len(violated),j)
                                     for j in range(min(len(violated),threshold)+1))
                    require(crt.reconstruct([f%p for p in primes],primes,1<<12) == f,'Signed CRT F')
                    crt_cases += 1
                    if x == 0:
                        require(f == sat,'Certificate X=0 does not recover count')
                        zero += 1
                    else:
                        positive += 1
                        mismatched += int(f != sat)
    require(mismatched > 0,'No positive-X failure control')
    return zero,positive,mismatched,crt_cases


def main():
    families,branches = branch_checks()
    zero,positive,mismatched,crt_cases = outer_controls()
    paths = [HERE/'PROOF.md',HERE/'verify.py',ROOT/'deterministic-crt-transfer'/'verify.py']
    print(json.dumps({'status':'PASS','scope':'finite branching and sparse-outer identities, not full source algorithm',
        'three_variable_antichains':families,'strict_branch_checks':branches,
        'certified_zero_X_cases':zero,'positive_X_cases':positive,'positive_X_wrong_F_controls':mismatched,
        'signed_CRT_F_cases':crt_cases,
        'sha256':{str(p.relative_to(ROOT.parent)):sha256(p.read_bytes()).hexdigest() for p in paths}},indent=2))


if __name__ == '__main__':
    main()
