"""Finite exact checks for one sparse-oscillator extension; Python stdlib only."""
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(condition,message):
    if not condition:
        raise ValueError(message)


def monomials(weight,minimum=1):
    if not weight:
        yield ()
    for part in range(minimum,weight+1):
        for rest in monomials(weight-part,part):
            yield (part,)+rest


def operator(index,polynomial,allowed):
    if not index or abs(index) not in allowed:
        return {}
    answer = {}
    for monomial,coefficient in polynomial.items():
        if index < 0:
            target = tuple(sorted(monomial+(-index,)))
            factor = 1
        else:
            factor = index*monomial.count(index)
            if not factor:
                continue
            target_list = list(monomial)
            target_list.remove(index)
            target = tuple(target_list)
        answer[target] = answer.get(target,0)+coefficient*factor
    return {m:c for m,c in answer.items() if c}


def q_operator(shift,polynomial,allowed,reverse=False):
    answer = {}
    for i,factor in enumerate((1,-2,1)):
        k = shift+i-1
        first,second = (k,-k) if reverse else (-k,k)
        term = operator(first,operator(second,polynomial,allowed),allowed)
        for monomial,coefficient in term.items():
            answer[monomial] = answer.get(monomial,0)+factor*coefficient
    return {m:c for m,c in answer.items() if c}


def subtract(left,right):
    answer = left.copy()
    for m,c in right.items():
        answer[m] = answer.get(m,0)-c
    return {m:c for m,c in answer.items() if c}


def g(index,allowed):
    return index if abs(index) in allowed else 0


def partition_counts(parts,maximum):
    dp = [1]+[0]*maximum
    for part in parts:
        for n in range(part,maximum+1):
            dp[n] += dp[n-part]
    return dp


def main():
    comparisons = 0
    witnesses = []
    all_monomials = [m for E in range(7) for m in monomials(E)]
    for bits in product((False,True),repeat=7):
        allowed = {1}|{k+2 for k,present in enumerate(bits) if present}
        examples = [m for m in all_monomials if set(m)<=allowed]
        for shift in range(-7,8):
            scalar = -(g(shift-1,allowed)-2*g(shift,allowed)+g(shift+1,allowed))
            for monomial in examples:
                left = q_operator(shift,{monomial:1},allowed)
                right = q_operator(shift,{monomial:1},allowed,reverse=True)
                expected = {monomial:scalar} if scalar else {}
                require(subtract(left,right) == expected,"commutator defect identity")
                comparisons += 1
        missing = next((k for k in range(2,9) if k not in allowed),None)
        if missing:
            shift = missing-1
            defect = subtract(q_operator(shift,{():1},allowed),
                              q_operator(shift,{():1},allowed,reverse=True))
            require(defect == {():missing},"first omission witness")
            witnesses.append((missing,shift,missing))
        else:
            for shift in range(-7,8):
                require(g(shift-1,allowed)-2*g(shift,allowed)+g(shift+1,allowed)==0,
                        "full-index control within tested interior")
    squares = {k*k for k in range(1,9)}
    q2 = q_operator(2,{():1},squares)
    rev2 = q_operator(2,{():1},squares,reverse=True)
    require(q2 == {} and rev2 == {():1},"square-only vacuum control")
    unrestricted = partition_counts(range(1,129),128)
    square_counts = partition_counts([k*k for k in range(1,12)],128)
    cube_counts = partition_counts([k*k*k for k in range(1,6)],128)
    require(unrestricted[:6] == [1,1,2,3,5,7],"partition base control")
    require(all(1<=cube_counts[E]<=square_counts[E]<=unrestricted[E] for E in (32,64,128)),
            "selected restricted partition counts")
    rescaling_checks = 0
    for spacing in range(1,9):
        counts = partition_counts(range(spacing,129,spacing),128)
        for E in range(129):
            expected = unrestricted[E//spacing] if E%spacing==0 else 0
            require(counts[E]==expected,"arithmetic energy rescaling")
            rescaling_checks += 1
    unique_witnesses = [dict(zip(("first_missing_index","shift","defect_scalar"),w))
                        for w in sorted(set(witnesses))]
    result = {
        "result":"PASS",
        "scope":"finite exact operators and partition counts; no complete contraction or SAT implementation",
        "index_subsets_containing_one":128,
        "available_index_range":[1,8],
        "shifts":[-7,7],
        "input_grade_range":[0,6],
        "operator_identity_comparisons":comparisons,
        "first_omission_witnesses":len(witnesses),
        "distinct_first_omission_witnesses":unique_witnesses,
        "square_only_vacuum_at_shift_two":{"original":0,"reversed":1},
        "partition_counts":[{"energy":E,"all_parts":unrestricted[E],
                              "square_parts":square_counts[E],"cube_parts":cube_counts[E]}
                             for E in (32,64,128)],
        "arithmetic_rescaling_checks":rescaling_checks,
        "conditional_targets_only":[{"beta":str(b),"alpha_if_all_other_contracts_held":str(1-b)}
                                    for b in (Fraction(1,2),Fraction(1,3),Fraction(1,4))],
        "source_sha256":{name:sha256((HERE/name).read_bytes()).hexdigest()
                         for name in ("verify.py","PROOF.md")}
    }
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
