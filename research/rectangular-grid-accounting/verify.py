#!/usr/bin/env python3
"""Enumerate rectangle incidences and exact rational minimax controls."""
from fractions import Fraction as F
from itertools import combinations


def feasible(t, A, B, P, Q):
    x = max(F(0), (t-A)/P)
    y = max(F(0), (t-B)/Q)
    return x*x + y*y <= 1


def main():
    cases = 0
    for p in range(2, 8):
        for q in range(2, 8):
            nodes = [(i, j) for i in range(p) for j in range(q)]
            edges = list(combinations(nodes, 2))
            straight_row = [e for e in edges if e[0][0] != e[1][0] and e[0][1] == e[1][1]]
            straight_col = [e for e in edges if e[0][1] != e[1][1] and e[0][0] == e[1][0]]
            diagonals = [e for e in edges if e[0][0] != e[1][0] and e[0][1] != e[1][1]]
            rectangles = [(rs, cs) for rs in combinations(range(p), 2)
                          for cs in combinations(range(q), 2)]
            assert 2*len(straight_row) == p*(p-1)*q
            assert 2*len(straight_col) == q*(q-1)*p
            assert len(diagonals) == 2*len(rectangles)
            signatures = [(tuple(sorted((e[0][0],e[1][0]))),
                           tuple(sorted((e[0][1],e[1][1])))) for e in diagonals]
            assert all(signatures.count(rect) == 2 for rect in rectangles)
            # lambda=5 and factor costs 6,8 give circle point (3/5,4/5).
            N = p*q*(p*q-1)*5
            a, c, b = F(p-1,p*q-1), F(q-1,p*q-1), F((p-1)*(q-1),p*q-1)
            assert a+c+b == 1
            assert F(2*len(straight_row)*5+2*len(rectangles)*6,N) == a+b*F(3,5)
            assert F(2*len(straight_col)*5+2*len(rectangles)*8,N) == c+b*F(4,5)
            cases += 1
    comparisons = 0
    for p,q,u,v in [(2,7,F(1),F(1)),(3,3,F(1),F(1)),
                    (3,8,F(1,2),F(2)),(8,3,F(3),F(1,4))]:
        a,c,b=F(p-1,p*q-1),F(q-1,p*q-1),F((p-1)*(q-1),p*q-1)
        A,B,P,Q=u*a,v*c,u*b,v*b
        lo,hi=F(0),max(A+P,B+Q)+1
        for _ in range(50):
            mid=(lo+hi)/2
            if feasible(mid,A,B,P,Q): lo=mid
            else: hi=mid
        assert feasible(lo,A,B,P,Q) and not feasible(hi,A,B,P,Q)
        for i in range(101):
            z=F(i,100)
            x,y=(1-z*z)/(1+z*z),2*z/(1+z*z)
            assert min(A+P*x,B+Q*y) <= hi
            comparisons+=1
    print(f'PASS: {cases} exact rectangular graph ledgers; {comparisons} rational minimax controls; 4 exact bisection brackets')


if __name__ == '__main__':
    main()
