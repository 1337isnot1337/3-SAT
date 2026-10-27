"""Bounded exact checks for the Newton mode construction, Python stdlib only.

No accepted subexponential contraction or complete SAT algorithm is implemented.
All checks raise explicitly (also under python -O). Output is deterministic JSON.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from math import factorial, prod
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def v2(x):
    x = F(x)
    if not x:
        return float("inf")
    def integer_v(n):
        n = abs(n)
        return (n & -n).bit_length() - 1
    return integer_v(x.numerator) - integer_v(x.denominator)


@dataclass(frozen=True)
class Q:
    """Exact Q[U]/(U^2+U+1), whose reduction at two is irreducible."""
    a: F = F(0)
    b: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, "a", F(self.a))
        object.__setattr__(self, "b", F(self.b))

    @staticmethod
    def coerce(x):
        return x if isinstance(x, Q) else Q(x)

    def __add__(self, other):
        other = Q.coerce(other)
        return Q(self.a+other.a, self.b+other.b)
    __radd__ = __add__

    def __neg__(self):
        return Q(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-Q.coerce(other))

    def __rsub__(self, other):
        return Q.coerce(other) + (-self)

    def __mul__(self, other):
        other = Q.coerce(other)
        return Q(self.a*other.a-self.b*other.b,
                 self.a*other.b+self.b*other.a-self.b*other.b)
    __rmul__ = __mul__

    def inverse(self):
        norm = self.a*self.a-self.a*self.b+self.b*self.b
        if not norm:
            raise ZeroDivisionError
        return Q((self.a-self.b)/norm, -self.b/norm)

    def __truediv__(self, other):
        return self * Q.coerce(other).inverse()

    def __rtruediv__(self, other):
        return Q.coerce(other) * self.inverse()

    def __pow__(self, n):
        if n < 0:
            return self.inverse() ** (-n)
        answer, power = Q(1), self
        while n:
            if n & 1:
                answer *= power
            power *= power
            n >>= 1
        return answer

    def valuation(self):
        return min(v2(self.a), v2(self.b))

    def residue(self, p):
        require(self.valuation() >= 0, "nonintegral residue")
        modulus = 2**p
        return tuple(int(x.numerator * pow(x.denominator, -1, modulus) % modulus)
                     for x in (self.a, self.b))


ONE = Q(1)
U = Q(0, 1)


def basis(z, k):
    z = Q.coerce(z)
    return prod((z-h for h in range(k)), start=ONE) / factorial(k) / prod(
        (1-2*z*h for h in range(k+1)), start=ONE)


def coefficient(k):
    return 2**k * factorial(k)**2 * (1-2*k*k)


def gain(k):
    return k + 2*int(v2(factorial(k)))


def odd_row_basis(z,k):
    return prod(((z-1)/2-h for h in range(k)),start=ONE)/factorial(k)/prod(
        (1-2*z*h for h in range(k+1)),start=ONE)


def odd_column_basis(j,k):
    return prod((Q(j)-h for h in range(k)),start=ONE)/factorial(k)/prod(
        (1-2*(1+2*h)*j for h in range(k+1)),start=ONE)


def odd_coefficient(k):
    return 2**(2*k)*factorial(k)**2*(1-2*(1+2*k)*k)


def odd_gain(k):
    return 2*k+2*int(v2(factorial(k)))


def prefactor(a, t, zeta):
    L = 2**a
    T = Q(t) + 2**(a+1)*zeta
    grid = range(-L, L)
    derivative = prod((-q for q in grid if q))
    return T, prod((T-q for q in grid), start=ONE)/derivative


def modular_basis(z, k, p, odd=False):
    """Compute via guard bits and integer operations on two coordinates."""
    extra = int(v2(factorial(k)))
    modulus = 2**(p+extra)
    if odd:
        zr0 = z.residue(p+extra+1)
        require(zr0[0]%2 == 1 and zr0[1]%2 == 0, "odd row coordinate")
        zr = ((zr0[0]-1)//2, zr0[1]//2)
    else:
        zr = z.residue(p+extra)
    def mul(x, y):
        return ((x[0]*y[0]-x[1]*y[1]) % modulus,
                (x[0]*y[1]+x[1]*y[0]-x[1]*y[1]) % modulus)
    falling = (1, 0)
    for h in range(k):
        falling = mul(falling, ((zr[0]-h) % modulus, zr[1]))
    require(all(x % 2**extra == 0 for x in falling), "guard division not integral")
    odd = factorial(k)//2**extra
    numerator = Q(*(F(x//2**extra, odd) for x in falling))
    denominator = prod((1-2*z*h for h in range(k+1)), start=ONE)
    return (numerator/denominator).residue(p)


def check_rational_identity():
    checks = 0
    for d in range(1, 11):
        for denominator in (1, 3, 5, 7):
            for numerator in range(-3, 4):
                z = Q(F(numerator, denominator))
                row = [basis(z, k) for k in range(d)]
                for j in range(d):
                    actual = sum((coefficient(k)*row[k]*basis(j, k)
                                  for k in range(d)), start=Q())
                    require(actual == 1/(1-2*z*j), "rational Newton identity")
                    checks += 1
    return {"tile_lengths": [1, 10], "odd_denominators": [1, 3, 5, 7],
            "numerators": [-3, 3], "identities": checks}


def check_source_tiles():
    identities = integrality = guards = 0
    odd_identities = odd_integrality = odd_guards = 0
    for a in range(1, 5):
        L = 2**a
        for i in range(a):
            A, d = a+1-i, L//2**(i+1)
            for t, zeta in product((-2**i, 2**i), (Q(1), U)):
                T, common = prefactor(a, t, zeta)
                for y0 in range(2**(i+1)):
                    column_basis = [[basis(j,k) for k in range(d)] for j in range(d)]
                    for x in range(L):
                        if (x>>i)&1 != (y0>>i)&1:
                            continue
                        b = T-y0+x
                        z = 2**i/b
                        z0 = Q(F(2**i, t-y0+x))
                        require((z-z0).valuation() >= A, "congruence hypothesis")
                        P = common/b
                        require(P.valuation() >= A, "initial row valuation")
                        row = [basis(z,k) for k in range(d)]
                        if i == 0:
                            odd_row = [odd_row_basis(z,k) for k in range(d)]
                        for k in range(d):
                            require(row[k].valuation() >= 0, "extension binomial integrality")
                            require((P*coefficient(k)*row[k]).valuation() >= A+gain(k),
                                    "mode valuation")
                            integrality += 1
                            for p in (2, 5, 11):
                                require(modular_basis(z,k,p) == row[k].residue(p),
                                        "guard precision calculation")
                                guards += 1
                            if i == 0:
                                require(odd_row[k].valuation() >= 0, "odd row integrality")
                                require((P*odd_coefficient(k)*odd_row[k]).valuation()
                                        >= A+odd_gain(k), "odd node mode valuation")
                                odd_integrality += 1
                                for p in (2,5,11):
                                    require(modular_basis(z,k,p,odd=True) == odd_row[k].residue(p),
                                            "odd row guard precision")
                                    odd_guards += 1
                        for j in range(d):
                            H = sum((coefficient(k)*row[k]*column_basis[j][k]
                                     for k in range(d)), start=Q())
                            require(H == 1/(1-2*z*j), "extension Newton identity")
                            y = y0+2**(i+1)*j
                            require(P*H == common/(T-y+x), "source kernel reconstruction")
                            identities += 1
                            if i == 0:
                                odd_H = sum((odd_coefficient(k)*odd_row[k]*odd_column_basis(j,k)
                                             for k in range(d)),start=Q())
                                require(odd_H == H, "odd source kernel identity")
                                odd_identities += 1
    require(basis(U,2).valuation() == -1, "nonrational negative control")
    # Deliberately omit the guard bit when computing binom(2,2) mod 2.
    # The falling product 2 is zero mod 2; dividing that residue gives 0,
    # whereas its integral quotient is 1. Thus ordinary precision is insufficient.
    require(((2*1) % 2)//2 != 1 % 2, "missing guard-bit negative control")
    return {"packet_exponents": [1,4], "nodes": "t=+-2^i for every 0<=i<a",
            "evaluation_points": ["1", "U; U^2+U+1=0"],
            "rows_and_tiles": "all crossing rows and all column tiles",
            "kernel_identities": identities, "coefficient_integrality_checks": integrality,
            "guard_precision_checks": guards,
            "odd_node_kernel_identities": odd_identities,
            "odd_node_coefficient_checks": odd_integrality,
            "odd_node_guard_precision_checks": odd_guards,
            "negative_controls": ["binom(U,2) has valuation -1",
                                  "division by k! requires guard bits"]}


def determinant(matrix):
    matrix = [[F(x) for x in row] for row in matrix]
    answer = F(1)
    for i in range(len(matrix)):
        pivot = next((j for j in range(i,len(matrix)) if matrix[j][i]), None)
        if pivot is None:
            return F(0)
        if pivot != i:
            matrix[i], matrix[pivot] = matrix[pivot], matrix[i]
            answer = -answer
        p = matrix[i][i]
        answer *= p
        for j in range(i+1,len(matrix)):
            ratio = matrix[j][i]/p
            for h in range(i+1,len(matrix)):
                matrix[j][h] -= ratio*matrix[i][h]
    return answer


def check_generic_spectrum():
    """An additional finite check, not a claim about every source tile's spectrum."""
    checks = odd_checks = 0
    for d in range(1,7):
        for k in range(1,d+1):
            minimum = float("inf")
            odd_minimum = float("inf")
            for rows, columns in product(combinations(range(d),k),repeat=2):
                value = determinant([[F(1,1-2*x*y) for y in columns] for x in rows])
                expected = k*(k-1)//2 + sum(v2(y-x) for x,y in combinations(rows,2))
                expected += sum(v2(y-x) for x,y in combinations(columns,2))
                require(v2(value) == expected, "bilinear Cauchy minor valuation")
                minimum = min(minimum,v2(value))
                checks += 1
                odd_value = determinant([[F(1,1-2*(1+2*x)*y) for y in columns] for x in rows])
                require(v2(odd_value) == expected+k*(k-1)//2, "odd row Cauchy minor")
                odd_minimum = min(odd_minimum,v2(odd_value))
                odd_checks += 1
            require(minimum == sum(gain(j) for j in range(k)), "generic Smith divisor")
            require(odd_minimum == sum(odd_gain(j) for j in range(k)), "odd Smith divisor")
    return {"dimensions": [1,6], "minors": checks,
            "smith_valuations": "j+2*v2(j!)=3*j-2*popcount(j)",
            "odd_row_minors":odd_checks,
            "odd_row_smith_valuations":"2*j+2*v2(j!)=4*j-2*popcount(j)"}


def polynomial_product(left, right):
    answer = {}
    for a, ca in left.items():
        for b, cb in right.items():
            key = tuple(x+y for x,y in zip(a,b))
            answer[key] = answer.get(key,Q()) + ca*cb
    return answer


def check_network(odd=False):
    """One complete four-wire deformed network, both groups, all bit assignments."""
    a, i, t = 2, 0, 1
    L, d, A = 4, 2, 3
    rb = odd_row_basis if odd else basis
    cb = odd_column_basis if odd else basis
    ck = odd_coefficient if odd else coefficient
    gk = odd_gain if odd else gain
    T, common = prefactor(a,t,U)
    W = [[common/(T-y+x) for y in range(L)] for x in range(L)]
    rows = {g: [x for x in range(L) if x%2 == g] for g in range(2)}
    cols = {g: [y for y in range(L) if 1-y%2 == g] for g in range(2)}
    def row_tensor(g,bits):
        return 1+(g+1)*bits[0]+2*bits[1]+bits[0]*bits[1]
    def col_tensor(g,bits):
        return 1+2*bits[0]-3*bits[1]+g*bits[0]*bits[1]
    all_bits = list(product((0,1),repeat=L))
    direct = Q()
    for X,Y in product(all_bits,repeat=2):
        value = ONE
        for g in range(2):
            value *= row_tensor(g,[Y[x] for x in rows[g]])
            value *= col_tensor(g,[X[y] for y in cols[g]])
        for x in range(L):
            linear = sum((W[x][y]*X[y] for y in range(L)),start=Q())
            value *= linear if Y[x] else 1-linear
        direct += value

    exponents = [b for b in product(range(3),repeat=d) if sum(b)<=2]
    terms = []
    for target0,target1 in product(exponents,repeat=2):
        beta = [target0,target1]  # tile y0 targets group y0, sources group 1-y0
        child_values = []
        for g in range(2):
            child = Q()
            for Xlocal,Ylocal in product(product((0,1),repeat=2),repeat=2):
                X = dict(zip(cols[g],Xlocal))
                Y = dict(zip(rows[g],Ylocal))
                poly = {(0,0): ONE}
                for x in rows[g]:
                    local = sum((W[x][y]*X[y] for y in cols[g]),start=Q())
                    b = T-g+x
                    z, P = 1/b, common/b
                    factor = {(0,0): local if Y[x] else 1-local}
                    for k in range(d):
                        key = tuple(int(h==k) for h in range(d))
                        factor[key] = P*ck(k)*rb(z,k)*(1 if Y[x] else -1)
                    poly = polynomial_product(poly,factor)
                value = poly.get(beta[g],Q())
                source_tile = 1-g
                for k in range(d):
                    source_form = sum((cb(j,k)*X[source_tile+2*j] for j in range(d)),
                                      start=Q())
                    value *= source_form**beta[source_tile][k]
                value *= row_tensor(g,Ylocal)*col_tensor(g,Xlocal)
                child += value
            child_values.append(child)
        weight = sum((A+gk(k))*beta[h][k] for h in range(2) for k in range(d))
        terms.append((weight,child_values[0]*child_values[1]))
    require(sum((term for _,term in terms),start=Q()) == direct, "whole network identity")
    kept_counts = {}
    for p in range(1,17):
        kept = sum((term for w,term in terms if w<p),start=Q())
        require((direct-kept).valuation() >= p, "whole network precision truncation")
        kept_counts[str(p)] = sum(w<p for w,_ in terms)
    return {"wires":4,"groups":2,"bit_assignment_pairs":256,
            "expansion":"odd_node" if odd else "general",
            "degree_feasible_mode_tuples":len(terms),
            "exact_identity":True,"precision_checks":16,"retained_tuples":kept_counts}


def partition_counts(c,p,d,A):
    def count(weights):
        dp = [1]+[0]*(p-1)
        for _ in range(c):
            for weight in weights:
                for j in range(weight,p):
                    dp[j] += dp[j-weight]
        return sum(dp)
    return {"tiles":c,"precision":p,"indices_per_tile":d,"initial_weight":A,
            "raw_geometric":count(range(1,d+1)),
            "geometric_with_initial_weight":count(range(A,A+d)),
            "newton":count([A+gain(k) for k in range(d)]),
            "newton_odd_node":count([A+odd_gain(k) for k in range(d)])}


def main():
    result = {"scope":"finite exact algebra and enumeration only; no full SAT implementation",
              "rational_identity":check_rational_identity(),
              "source_tiles":check_source_tiles(),
              "generic_bilinear_cauchy_spectrum":check_generic_spectrum(),
              "whole_network":[check_network(),check_network(odd=True)]}
    result["finite_mode_counts"] = [partition_counts(*parameters) for parameters in
                                    [(2,32,16,5),(4,64,16,5),(4,128,32,7)]]
    for case in result["finite_mode_counts"]:
        require(case["newton_odd_node"] < case["newton"]
                < case["geometric_with_initial_weight"] <= case["raw_geometric"],
                "finite enumeration improvement")
    root = Path(__file__).resolve().parents[2]
    source_paths = ["research/cauchy-newton-modes/verify.py",
                    "research/cauchy-newton-modes/PROOF.md",
                    "upstream/openai-eth-2026/build/quantitative-contraction.tex",
                    "certificates/selected-result.json"]
    result["source_sha256"] = {name:sha256((root/name).read_bytes()).hexdigest()
                               for name in source_paths}
    result["result"] = "PASS"
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
