"""Bounded exact evidence for rational output compression; offline."""
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
from random import Random
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from compression import affine_groups, compress, sandwich


def require(value, message):
    if not value:
        raise ValueError(message)


def check_compression(matrices, result):
    u, v = result["u"], result["v"]
    k, n, m = len(u), len(matrices[0]), len(matrices)
    require(k * (result["max_degree"]+1) * m*(m+1) >= 2*n,
            "Dimension guarantee failed")
    for a, scalar in zip(matrices, result["scalars"]):
        actual = sandwich(u, a, v)
        require(actual == [[scalar*int(i == j) for j in range(k)]
                           for i in range(k)], "Compression identity failed")


def affine_controls():
    rng = Random(150)
    cases = 0
    ranks_seen = set()
    for m in range(1,7):
        for n in range(1,25):
            points = [tuple([1]+[rng.randrange(-3,4) for _ in range(m-1)])
                      for _ in range(n)]
            groups, weights, c, layers = affine_groups(points)
            require(sum(r*b for r,b in layers.items()) == n, "Lost vectors")
            require(len(groups)*m*(m+1) >= 2*n, "Affine packing bound")
            require(len({i for g in groups for i in g}) == sum(map(len,groups)),
                    "Groups not disjoint")
            for g,w in zip(groups,weights):
                require(sum(w) == 1, "Weights are not affine")
                require(tuple(sum(a*points[i][j] for a,i in zip(w,g))
                              for j in range(m)) == c, "Wrong common vector")
            ranks_seen.update(layers)
            cases += 1
    # A deliberate descent through all three possible ranks.
    points = [(1,0,0)]*12 + [(1,1,0)]*3 + [(1,0,1)]
    groups,weights,c,layers=affine_groups(points)
    require(set(layers)=={1,2,3}, "Rank-descent fixture was ineffective")
    require(sum(r*b for r,b in layers.items())==len(points), "Descent count")
    return {"seeded_cases":cases,"ranks_seen":sorted(ranks_seen),
            "rank_descent_layers":layers}


def matrix_controls():
    rng=Random(151)
    cases=0
    for n in (1,2,5,11,19):
        for m in (1,2,4):
            for trial in range(5):
                matrices=[[{i:1} for i in range(n)]]
                for _ in range(m-1):
                    a=[]
                    for j in range(n):
                        col={j:rng.randrange(-8,9)}
                        for i in range(n):
                            if i != j and rng.randrange(12)==0:
                                col[i]=rng.choice((-2,-1,1,2))
                        a.append({i:x for i,x in col.items() if x})
                    matrices.append(a)
                check_compression(matrices,compress(matrices)); cases+=1
    # Every signature is different, yet the rational code has dimension 16.
    n=32
    matrices=[[{i:1} for i in range(n)], [{i:i} if i else {} for i in range(n)]]
    result=compress(matrices)
    check_compression(matrices,result)
    require(len(result["u"])==16, "Distinct-signature gain missing")
    require(any(x<0 for row in result["u"] for x in row.values()),
            "Signed-weight control was ineffective")
    try:
        compress([[{}]])
    except ValueError:
        pass
    else:
        raise ValueError("Missing identity was accepted")
    bad=[list(a) for a in matrices]
    i=next(iter(result["u"][0]))
    bad[1][i]={i:bad[1][i].get(i,0)+1}
    try:
        check_compression(bad,result)
    except ValueError:
        pass
    else:
        raise ValueError("A changed selected diagonal passed the check")
    return {"seeded_sparse_cases":cases,"distinct_signatures":n,
            "old_signature_class_maximum":1,"new_code_dimension":16,
            "negative_controls":2}


def load_model():
    path=ROOT/'research/charged-asymmetric-crossing/model.py'
    spec=importlib.util.spec_from_file_location('rational_compression_model',path)
    model=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=model
    spec.loader.exec_module(model)
    return model


def charged_controls():
    model=load_model()
    charged=model.charged
    partitions=model.predecessor.partitions
    reports=[]; direct=0; entry_checks=0; nontrivial=0
    for E,d,q,h in ((3,3,1,2),(4,3,0,2),(5,3,2,3),
                    (6,4,1,2),(7,4,1,2),(8,5,1,2),(9,5,1,2),
                    (10,5,1,3),(12,5,1,3)):
        states=partitions(E)
        index={s:i for i,s in enumerate(states)}
        fields=[a for j in range(d+1) for a in partitions(j)]
        matrices=[]
        for a in fields:
            matrix=[]
            for st in states:
                vector=charged.operator(a,0,st,q)
                if E<=4:
                    require(vector==charged.direct_operator(a,0,st,q),
                            "Independent normal ordering disagrees")
                    direct+=1
                matrix.append({index[out]:v for out,v in vector})
            matrices.append(matrix)
        result=compress(matrices)
        check_compression(matrices,result)
        k=len(result['u'])
        nontrivial+=int(k>1)
        # Check the actual filtered operator, including off-diagonal entries.
        used=sorted(set().union(*(set(v) for v in result['v'])))
        r=(d-1)//2
        for mu in partitions(h):
            for nu in partitions(h):
                matrix=[{} for _ in states]
                for j in used:
                    acc={}
                    for s in range(-(E+h),E+h+1):
                        weight=s
                        for z in range(1,r+1): weight*=s*s-z*z
                        if weight:
                            for out,value in charged.piece_vector(mu,nu,states[j],s,q):
                                i=index[out]
                                acc[i]=acc.get(i,0)+weight*value
                    matrix[j]={i:v for i,v in acc.items() if v}
                actual=sandwich(result['u'],matrix,result['v'])
                scalar=actual[0][0]
                require(actual==[[scalar*int(i==j) for j in range(k)]
                                 for i in range(k)],"Actual filter not scalar")
                entry_checks+=k*k
        reports.append({"energy":E,"degree":d,"charge":q,"label_grade":h,
                        "states":len(states),"fields":len(fields),
                        "independent_states":len(result['independent']),
                        "compressed_dimension":k,"rank_layers":result['layers']})
    require(nontrivial>0,"No nontrivial actual output compression checked")
    return {"cases":reports,"independent_operator_comparisons":direct,
            "actual_filter_matrix_entries":entry_checks,
            "cases_with_output_dimension_above_one":nontrivial}


def main():
    report={"affine":affine_controls(),"matrices":matrix_controls(),
            "charged":charged_controls(),"status":"PASS"}
    paths=[HERE/'compression.py',HERE/'verify.py',HERE/'PROOF.md',
           ROOT/'research/charged-operator-moments/charged.py',
           ROOT/'research/charged-asymmetric-crossing/model.py',
           ROOT/'research/anthropic-operator-ranks/operators.py',
           ROOT/'research/partition-transition-codebooks/PROOF.md']
    report['sha256']={str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest()
                      for p in paths}
    print(json.dumps(report,indent=2,sort_keys=True))


if __name__=='__main__':main()
