"""Exact finite checks for the shift-resistant unary packet construction."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('prior', ROOT / 'research/parity-recovery-precision/explore_boolean_packets.py')
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)


def mismatch(bits, t):
    n = len(bits)
    return sum(bits[x] != (bits[x + t] if 0 <= x + t < n else 0) for x in range(n))


def weight_sum(n, t, fixed):
    # Sum 7^m 8^(n-m) over extensions. Edges form disjoint paths.
    step = abs(t)
    if step == n:
        step = n
    total = 1
    for start in range(step):
        path = list(range(start, n, step))
        state = [1, 1]
        for idx, x in enumerate(path):
            allowed = (0, 1) if fixed[x] is None else (fixed[x],)
            next_state = [0, 0]
            for bit in allowed:
                unary = (7 if bit else 8) if not 0 <= x + t < n else 1
                if idx == 0:
                    next_state[bit] = unary
                else:
                    next_state[bit] = unary * sum(state[old] * (7 if old != bit else 8) for old in (0, 1))
            state = next_state
        total *= sum(state)
    return total


def construct(n):
    fixed = [None] * n
    for pos in range(n):
        scores = []
        for bit in (0, 1):
            fixed[pos] = bit
            scores.append(sum(weight_sum(n, t, fixed) for t in range(-n, n) if t))
        fixed[pos] = min(range(2), key=lambda bit: scores[bit])
    return fixed


def mul(a,b): return prior.multiply(a,b)
def add(a,b,scale=1): return prior.add(a,b,scale)


def main():
    # Independent exhaustive sum checks for DP, including both shift directions.
    cases = 0
    for n in (2, 4, 6):
        for t in range(-n, n):
            if not t: continue
            for fixed in ([None]*n, [0]+[None]*(n-1), [1,None]*(n//2)):
                free = [i for i, b in enumerate(fixed) if b is None]
                brute = 0
                for vals in product((0,1), repeat=len(free)):
                    b = list(fixed)
                    for i,v in zip(free, vals): b[i] = v
                    k = mismatch(b,t)
                    brute += 7**k * 8**(n-k)
                assert weight_sum(n,t,fixed) == brute
                cases += 1
    words = {}
    checked_factors = 0
    for n in (2,4,8,16):
        bits = construct(n)
        words[str(n)] = {'word': ''.join(map(str,bits)), 'minimum_mismatch': min(mismatch(bits,t) for t in range(-n,n) if t)}
        for t in range(-n,n):
            if not t: continue
            for x in range(n):
                form=[F(0)]
                for y in range(n):
                    if bits[y]: form=add(form,prior.kernel_polynomial(n,x,y))
                if not bits[x]: form=add([F(1)],form,-1)
                shifted=prior.shift(form,t,2*n)
                if bits[x] != (bits[x+t] if 0 <= x+t < n else 0):
                    assert all(not c or prior.valuation(c)>=1 for c in shifted)
                    checked_factors += 1
                else:
                    assert all(not c or prior.valuation(c)>=0 for c in shifted)
        # Full product content is checked separately at all shifts for the smaller packets.
        if n <= 8:
            polynomial=[F(1)]
            for x in range(n):
                form=[F(0)]
                for y in range(n):
                    if bits[y]: form=add(form,prior.kernel_polynomial(n,x,y))
                if not bits[x]: form=add([F(1)],form,-1)
                polynomial=mul(polynomial,form)
            assert prior.evaluate(polynomial,0)==1
            for t in range(-n,n):
                if not t: continue
                shifted=prior.shift(polynomial,t,2*n)
                assert all(not c or prior.valuation(c)>=mismatch(bits,t) for c in shifted)
    print(json.dumps({'status':'PASS', 'dp_bruteforce_checks':cases, 'mismatched_row_checks':checked_factors, 'words':words, 'scope':'finite exact checks, not an independent proof review'},indent=2))

if __name__ == '__main__': main()
