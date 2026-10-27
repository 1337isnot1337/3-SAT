"""Bounded exact checks; not an implementation or verification of a full SAT theorem."""
from fractions import Fraction as F
from hashlib import sha256
import json
from math import factorial
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import charged
import pairing
import predecessor


def require(condition,message):
    if not condition:
        raise ValueError(message)


def main():
    source=json.loads((HERE/"SOURCES.json").read_text())
    require(sha256((HERE/"predecessor.py").read_bytes()).hexdigest()==source["sha256"],
            "predecessor source integrity")
    direct_checks=zero_controls=binomial_checks=0
    for w in range(4):
        for a in charged.partitions(w):
            for E in range(3):
                for f in charged.partitions(E):
                    for r in range(-E,4-E):
                        for q in (-1,0,1,2):
                            actual=charged.operator(a,r,f,q)
                            require(actual==charged.direct_operator(a,r,f,q),"normal-order recurrence")
                            direct_checks+=1
                            if q==0:
                                require(actual==predecessor.operator(a,r,f),"zero-charge predecessor")
                                zero_controls+=1
    for r in range(1,13):
        for m in range(1,13):
            actual=sum((-1)**(r+n)*predecessor.binomial(r,n)
                       *F(factorial(n+m-1),factorial(n-1)*factorial(m-1))
                       for n in range(1,r+1))
            require(actual==m*predecessor.binomial(m-1,r-1),"transformed contraction")
            binomial_checks+=1
    rank_rows=[]
    pairing_checks=0
    for h in range(2,9):
        states=charged.partitions(h)
        matrix=pairing.first_pairing(states)
        for i,x in enumerate(states):
            for j,v in enumerate(states):
                actual=dict(charged.moment(x,v,(),1,1)).get((),0)
                require(actual==matrix[i][j],"independent first-pairing formula")
                require(not actual or len(x)==len(v)+1,"strict length filtration")
                pairing_checks+=1
        exact=predecessor.exact_rank(matrix)
        expected=len(states)-len(charged.partitions(h-1))
        require(exact==expected,"full charged pairing rank")
        rank_rows.append({"h":h,"full_dimension":len(states),"rank":exact,
                          "p_h_minus_p_h_minus_one":expected})
    moment_checks=order_checks=0
    for h in (2,3,4):
        states=charged.partitions(h)
        matrix=pairing.first_pairing(states)
        for i,x in enumerate(states):
            for j,v in enumerate(states):
                for E in range(3):
                    for f in charged.partitions(E):
                        for q in (-1,0,1,2):
                            m0=dict(charged.moment(x,v,f,0,q))
                            m1=dict(charged.moment(x,v,f,1,q))
                            scalar=q*matrix[i][j]
                            require(m0==({f:factorial(h)} if x==v else {}),"charged crossing")
                            require(m1==({f:scalar} if scalar else {}),"energy-independent pairing")
                            moment_checks+=1
                            if q in (-1,1):
                                for shift in range(-E-h,E+h+1):
                                    require(charged.piece_vector(x,v,f,shift,q)==
                                            charged.piece_vector(x,v,f,shift,q,reverse=True),
                                            "two operator orders")
                                    order_checks+=1
    polynomial_checks=right_inverse_checks=0
    for h in range(11):
        for state in charged.partitions(h):
            f={state:F(1)}
            require(pairing.L(pairing.P(f))=={},"L P=0")
            require(pairing.T(pairing.T(f))=={},"T squared=0")
            commutator=pairing.add(pairing.L(pairing.B(f)),pairing.B(pairing.L(f)),-1)
            require(commutator==({state:F(len(state))} if state else {}),"Weyl commutator")
            polynomial_checks+=1
            if state:
                require(pairing.L(pairing.L_right_inverse(f))==f,"L right inverse")
                right_inverse_checks+=1
            if h>=2:
                derivative=pairing.L(f)
                kernel=pairing.add(f,pairing.L_right_inverse(derivative) if derivative else {},-1)
                require(pairing.L(kernel)=={},"kernel projection")
                require(pairing.P(pairing.P_right_inverse_on_invariants(kernel))==kernel,
                        "P right inverse on invariants")
                right_inverse_checks+=1
    larger_rank_rows=[]
    for h in (9,10):
        states=charged.partitions(h)
        matrix=pairing.first_pairing(states)
        rank=predecessor.exact_rank(matrix)
        require(rank==len(states)-len(charged.partitions(h-1)),"polynomial rank formula")
        larger_rank_rows.append({"h":h,"full_dimension":len(states),"rank":rank,
                                "scope":"independent polynomial formula; charged operators not enumerated here"})
    partition_dp=[1]+[0]*128
    for part in range(1,129):
        for n in range(part,129):
            partition_dp[n]+=partition_dp[n-part]
    for h in range(2,129):
        image=partition_dp[h]-partition_dp[h-1]
        require((h-1)*image>=partition_dp[h]-1,"image label-capacity lower bound")
    result={
        "result":"PASS",
        "scope":"finite exact charged operators, moments and polynomial identities; no full SAT algorithm or independent theorem review",
        "charges":[-1,0,1,2],
        "independent_normal_order_checks":direct_checks,
        "zero_charge_predecessor_controls":zero_controls,
        "contraction_binomial_checks":binomial_checks,
        "vacuum_pairing_entry_checks":pairing_checks,
        "operator_pairing_ranks":rank_rows,
        "positive_grade_moment_cases":moment_checks,
        "two_order_output_vector_checks":order_checks,
        "polynomial_identity_inputs":polynomial_checks,
        "right_inverse_checks":right_inverse_checks,
        "larger_polynomial_rank_cases":larger_rank_rows,
        "label_capacity_checks":127,
        "square_zero":True,
        "full_common_label_inverse_exists":False,
        "alpha_improvement_claimed":False,
        "source_sha256":{name:sha256((HERE/name).read_bytes()).hexdigest()
                         for name in ("charged.py","pairing.py","predecessor.py","verify.py","PROOF.md","SOURCES.json")}
    }
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
