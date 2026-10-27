"""Independent polynomial formula for the charged first-moment pairing."""
from collections import Counter
from fractions import Fraction as F
from math import factorial


def clean(poly):
    return {m:c for m,c in poly.items() if c}


def add(left,right,scale=1):
    answer=left.copy()
    for m,c in right.items():
        answer[m]=answer.get(m,F(0))+scale*c
    return clean(answer)


def L(poly):
    """Translation derivative: L(u_j)=(j-1)u_(j-1)."""
    answer={}
    for m,c in poly.items():
        for part,multiplicity in Counter(m).items():
            if part>1:
                row=list(m)
                row.remove(part)
                row.append(part-1)
                key=tuple(sorted(row,reverse=True))
                answer[key]=answer.get(key,F(0))+c*(part-1)*multiplicity
    return clean(answer)


def B(poly):
    """Multiplication by the coordinate sum on a fixed-length symmetric space."""
    answer={}
    for m,c in poly.items():
        for part,multiplicity in Counter(m).items():
            row=list(m)
            row.remove(part)
            row.append(part+1)
            key=tuple(sorted(row,reverse=True))
            answer[key]=answer.get(key,F(0))+c*multiplicity
    return clean(answer)


def P(poly):
    answer={}
    current=poly
    degree=0
    while current:
        scale=F((-1)**degree,factorial(degree))
        for m,c in current.items():
            key=tuple(sorted(m+(degree+1,),reverse=True))
            answer[key]=answer.get(key,F(0))+scale*c
        current=L(current)
        degree+=1
    return clean(answer)


def T(poly):
    return P(L(poly))


def L_right_inverse(poly):
    """Finite Weyl-algebra right inverse, split by particle number."""
    by_length={}
    for m,c in poly.items():
        if not m:
            raise ValueError("The vacuum has no preimage under L")
        by_length.setdefault(len(m),{})[m]=c
    answer={}
    for length,component in by_length.items():
        current=component
        degree=0
        while current:
            raised=current
            for _ in range(degree+1):
                raised=B(raised)
            scale=F((-1)**degree,length**(degree+1)*factorial(degree+1))
            answer=add(answer,raised,scale)
            current=L(current)
            degree+=1
    return answer


def P_right_inverse_on_invariants(poly):
    answer={}
    for m,c in poly.items():
        ones=m.count(1)
        if ones:
            row=list(m)
            row.remove(1)
            key=tuple(row)
            answer[key]=answer.get(key,F(0))+F(ones,len(m))*c
    return clean(answer)


def multiplicity_factorial(partition):
    answer=1
    for multiplicity in Counter(partition).values():
        answer*=factorial(multiplicity)
    return answer


def first_pairing(states,charge=1):
    h=sum(states[0])
    columns=[T({v:F(1)}) for v in states]
    return [[charge*factorial(h)*F(multiplicity_factorial(x),multiplicity_factorial(v))
             *columns[j].get(x,F(0)) for j,v in enumerate(states)] for x in states]
