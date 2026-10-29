"""Finite clause/equality networks and CRT, not the master SAT algorithm."""
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
spec = importlib.util.spec_from_file_location('fixed_density_crt',ROOT/'deterministic-crt-transfer'/'verify.py')
crt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(crt)


def require(test, message):
    if not test:
        raise AssertionError(message)


def network_count(n, clauses, groups):
    m = len(clauses)
    width = max(1,(m+groups-1)//groups)
    occurrence = []
    nodes = [[] for _ in range(groups)]
    clause_occurrences = []
    for ci,clause in enumerate(clauses):
        owner = min(ci//width,groups-1)
        indices = []
        for literal in clause:
            require(1 <= abs(literal) <= n,'Variable outside declared set')
            idx = len(occurrence)
            occurrence.append((abs(literal),literal > 0,owner))
            nodes[owner].append(idx)
            indices.append(idx)
        clause_occurrences.append(indices)
    by_variable = [[] for _ in range(n+1)]
    for i,(var,_,_) in enumerate(occurrence):
        by_variable[var].append(i)
    equalities = [(a,b) for ids in by_variable for a,b in zip(ids,ids[1:])]
    cross = [(a,b) for a,b in equalities if occurrence[a][2] != occurrence[b][2]]
    internal = [(a,b) for a,b in equalities if occurrence[a][2] == occurrence[b][2]]
    require(len(equalities) <= len(occurrence),'Occurrence-chain bound')
    per_node = [0] * groups
    for a,b in cross:
        per_node[occurrence[a][2]] += 1
        per_node[occurrence[b][2]] += 1
    require(max(per_node,default=0) <= 2*width*3,'Port bound for width-3 clauses')
    count = 0
    for bits in product((0,1),repeat=len(occurrence)):
        if any(bits[a] != bits[b] for a,b in internal):
            continue
        if any(not any(bits[i] == occurrence[i][1] for i in ids) for ids in clause_occurrences):
            continue
        if any(bits[a] != bits[b] for a,b in cross):
            continue
        count += 1
    used = sum(bool(x) for x in by_variable)
    return count, len(occurrence), n-used


def brute(n, clauses):
    total = 0
    for assignment in product((0,1),repeat=n):
        if all(any(assignment[abs(lit)-1] == (lit > 0) for lit in clause) for clause in clauses):
            total += 1
    return total


def main():
    # Every signed subset of three variables, including the empty clause,
    # plus repeated literals and a tautology as explicit controls.
    clauses = [tuple((j+1)*sign for j,sign in enumerate(pattern) if sign)
               for pattern in product((0,1,-1),repeat=3)]
    clauses += [(1,1),(1,-1)]
    formulas = [()] + [(c,) for c in clauses] + list(product(clauses,repeat=2))
    comparisons = empty_controls = unused_controls = 0
    for formula in formulas:
        expected = brute(3,formula)
        for groups in (1,2,3):
            value, occurrences, unused = network_count(3,formula,groups)
            require(value <= (1 << occurrences),'Original query range')
            primes = crt.good_primes(occurrences,15)
            restored = crt.reconstruct([value % p for p in primes],primes,1 << occurrences)
            require(restored << unused == expected,'Network, CRT or unused-variable count')
            comparisons += 1
            empty_controls += int(any(not c for c in formula))
            unused_controls += int(unused > 0)
    paths = [HERE/'PROOF.md',HERE/'verify.py',ROOT/'deterministic-crt-transfer'/'verify.py']
    print(json.dumps({'status':'PASS','scope':'finite direct occurrence networks and CRT, not master recursion',
      'formulas':len(formulas),'network_grouping_comparisons':comparisons,'empty_clause_controls':empty_controls,
      'unused_variable_controls':unused_controls,'sha256':{str(p.relative_to(ROOT.parent)):sha256(p.read_bytes()).hexdigest() for p in paths}},indent=2))


if __name__ == '__main__':
    main()
