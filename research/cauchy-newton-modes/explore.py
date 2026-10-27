"""Small exact scratch calculation; not a contraction implementation."""
from fractions import Fraction as F
from math import factorial, prod


def basis(x, k):
    return prod((x-h for h in range(k)), start=F(1)) / factorial(k) / prod(
        (1-2*x*h for h in range(k+1)), start=F(1))


def valuation(x):
    if not x:
        return float('inf')
    x = F(x)
    def v(n):
        n = abs(n)
        return (n & -n).bit_length()-1
    return v(x.numerator)-v(x.denominator)


for d in range(1, 16):
    for z in [F(j, q) for q in [1, 3, 5, 7] for j in range(-5, 6)]:
        for j in range(d):
            terms = [2**k * factorial(k)**2 * (1-2*k*k) * basis(z,k)*basis(F(j),k)
                     for k in range(d)]
            assert sum(terms) == 1/(1-2*z*j)
            for k in range(d):
                assert valuation(basis(z,k)) >= 0
    print('PASS exact rank decomposition', d)
