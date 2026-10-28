"""Check the all-shift two-current formula and outer-filter constraints."""
from fractions import Fraction
from hashlib import sha256
import json
from math import comb
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'charged-operator-moments'
sys.path.insert(0, str(SOURCE))
import charged


def weights(degree, target):
    result = []
    for x in range(degree + 1):
        poly = [Fraction(1)]
        for y in range(degree + 1):
            if x == y:
                continue
            new = [Fraction(0)] * (len(poly) + 1)
            for k, value in enumerate(poly):
                new[k] -= value*y/(x-y)
                new[k+1] += value/(x-y)
            poly = new
        result.append(poly[target])
    return result


def binom(n,k):
    return comb(n,k) if 0<=k<=n else 0


def rank(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row,len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row],a[pivot] = a[pivot],a[row]
        for i in range(row+1,len(a)):
            if a[i][col]:
                scale = a[i][col]/a[row][col]
                for j in range(col,len(a[0])):
                    a[i][j] -= scale*a[row][j]
        row += 1
        if row == len(a):
            break
    return row


cases = 0
for h in range(2,5):
    coeff=weights(2*h,2*h-2)
    B=lambda k:binom(2*h,k)
    for E in range(h+1):
        for state in charged.partitions(E):
            for r in range(2*h+1):
                constant=sum((-1)**(r-j)*B(r-j)*j for j in range(1,r+1))
                eig=((-1)**r*B(r)*2*h*(h-1)*E + h*h*(constant + sum(
                    (-1)**(r+j)*(B(r+j)+B(r-j))*j*state.count(j)
                    for j in range(1,E+1))))
                for reverse in (False,True):
                    out={}
                    for q,w in enumerate(coeff):
                        for target,value in charged.piece_vector((1,)*h,(1,)*h,state,h-r,q,reverse):
                            out[target]=out.get(target,Fraction(0))+w*value
                    out={k:v for k,v in out.items() if v}
                    assert out==({state:eig} if eig else {}), (h,E,state,r,reverse,out,eig)
                    cases+=1

rank_cases=[]
for h in range(2,21):
    def kernel(r,j):
        return (-1)**(r+j)*(binom(2*h,r+j)+binom(2*h,r-j))
    matrix=[[kernel(r,j)-kernel(r,1) for r in range(h-1)] for j in range(2,h+1)]
    actual=rank(matrix)
    assert actual == h-1, (h,actual)
    rank_cases.append({'h':h,'rank':actual})
print(json.dumps({'result':'PASS','operator_cases':cases,'operator_grades':[2,4],
                  'constraint_ranks':rank_cases,'source_hashes':{
                      name:sha256((SOURCE/name).read_bytes()).hexdigest()
                      for name in ('charged.py','predecessor.py')},
                  'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest()},
                 indent=2,sort_keys=True))
