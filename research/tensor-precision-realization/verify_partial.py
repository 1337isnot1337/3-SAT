"""Exact finite checks for occupied-subset shift-resistant packet extension."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import importlib.util
import json

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('full', HERE / 'verify.py')
full = importlib.util.module_from_spec(spec)
spec.loader.exec_module(full)


def mismatch(real, bits, t):
    return sum(bits[x] != bits.get(x+t, 0) for x in real)


def weight_sum(real, t, fixed):
    # Each occupied x has one comparison, either an edge or a boundary unary.
    step = abs(t)
    paths = []
    for x in sorted(real):
        if x-step not in real:
            path = []
            while x in real:
                path.append(x)
                x += step
            paths.append(path)
    total = 1
    for path in paths:
        state = [1, 1]
        for pos, x in enumerate(path):
            choices = (0,1) if fixed[x] is None else (fixed[x],)
            new = [0,0]
            for bit in choices:
                unary = (7 if bit else 8) if x+t not in real else 1
                if not pos:
                    new[bit] = unary
                else:
                    new[bit] = unary * sum(state[b] * (7 if b != bit else 8) for b in (0,1))
            state = new
        total *= sum(state)
    return total


def construct(n, real):
    fixed = {x: None for x in real}
    for x in sorted(real):
        scores = []
        for bit in (0,1):
            fixed[x] = bit
            scores.append(sum(weight_sum(real,t,fixed) for t in range(-n,n) if t))
        fixed[x] = min(range(2), key=lambda bit: scores[bit])
    return fixed


def main():
    transfer_checks = polynomial_checks = factor_checks = 0
    for n in (2,4):
        for mask in range(1, 1<<n):
            real = {x for x in range(n) if mask>>x&1}
            fixed = {x: (0 if x == min(real) else None) for x in real}
            free = [x for x in sorted(real) if fixed[x] is None]
            for t in range(-n,n):
                if not t: continue
                brute = 0
                for values in product((0,1), repeat=len(free)):
                    bits = dict(fixed)
                    bits.update(zip(free, values))
                    k = mismatch(real,bits,t)
                    brute += 7**k * 8**(len(real)-k)
                assert weight_sum(real,t,fixed)==brute
                transfer_checks += 1
            bits = construct(n,real)
            polynomial=[F(1)]
            forms={}
            for x in sorted(real):
                form=[F(0)]
                for y in sorted(real):
                    if bits[y]: form=full.add(form,full.prior.kernel_polynomial(n,x,y))
                if not bits[x]: form=full.add([F(1)],form,-1)
                forms[x]=form
                polynomial=full.mul(polynomial,form)
            assert full.prior.evaluate(polynomial,0)==1
            for t in range(-n,n):
                if not t: continue
                for x in real:
                    shifted=full.prior.shift(forms[x],t,2*n)
                    if bits[x] != bits.get(x+t,0):
                        assert all(not c or full.prior.valuation(c)>=1 for c in shifted)
                        factor_checks+=1
                shifted=full.prior.shift(polynomial,t,2*n)
                assert all(not c or full.prior.valuation(c)>=mismatch(real,bits,t) for c in shifted)
                polynomial_checks+=1
    print(json.dumps({'status':'PASS','transfer_bruteforce_checks':transfer_checks,
                      'partial_packet_product_checks':polynomial_checks,
                      'mismatched_row_checks':factor_checks,
                      'scope':'all nonempty occupancy sets for L=2,4; finite checks only'},indent=2))

if __name__ == '__main__': main()
