"""Finite depth-first grouping and exact CRT controls, not the master algorithm."""
from contextlib import contextmanager
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
spec = importlib.util.spec_from_file_location('streamed_crt',ROOT/'deterministic-crt-transfer'/'verify.py')
crt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(crt)


def require(test, message):
    if not test:
        raise AssertionError(message)


class Frames:
    def __init__(self):
        self.depth = 0
        self.max_depth = 0
        self.calls = 0

    @contextmanager
    def frame(self):
        self.depth += 1
        self.calls += 1
        self.max_depth = max(self.max_depth,self.depth)
        try:
            yield
        finally:
            self.depth -= 1


def entry(seed, index, x, y):
    # Nonuniform signed table values; no table is materialized by the evaluator.
    return ((seed*(index+3) + 7*index + 3*x + 5*y + 11*x*y) % 5) - 2


def stream(seed, prime, frames):
    def inner_first(a,b):
        with frames.frame():
            total = 0
            for e in range(2):
                total = (total + entry(seed,0,a,e)*entry(seed,1,e,b)) % prime
            return total
    def inner_second(c,d):
        with frames.frame():
            total = 0
            for f in range(2):
                total = (total + entry(seed,3,c,f)*entry(seed,4,f,d)) % prime
            return total
    def left(a,c):
        with frames.frame():
            total = 0
            for b in range(2):
                total = (total + inner_first(a,b)*entry(seed,2,b,c)) % prime
            return total
    def right(c,a):
        with frames.frame():
            total = 0
            for d in range(2):
                total = (total + inner_second(c,d)*entry(seed,5,d,a)) % prime
            return total
    with frames.frame():
        result = 0
        for a,c in product(range(2),repeat=2):
            result = (result + left(a,c)*right(c,a)) % prime
        return result


def direct(seed):
    total = 0
    for a,b,c,d,e,f in product(range(2),repeat=6):
        total += (entry(seed,0,a,e)*entry(seed,1,e,b)*entry(seed,2,b,c)
                  *entry(seed,3,c,f)*entry(seed,4,f,d)*entry(seed,5,d,a))
    return total


def main():
    primes = [101,103,107]
    cases = 0
    negatives = 0
    max_depth = max_calls = 0
    # 6 factors, each bounded by 2, and 2^6 assignments.
    bound = (1 << 6) * 2**6
    for seed in range(256):
        expected = direct(seed)
        residues = []
        for p in primes:
            frames = Frames()
            value = stream(seed,p,frames)
            require(value == expected % p,'Streamed grouping differs from exhaustive contraction')
            require(frames.depth == 0 and frames.max_depth == 3,'Frame lifecycle')
            max_depth = max(max_depth,frames.max_depth)
            max_calls = max(max_calls,frames.calls)
            residues.append(value)
            cases += 1
        value = crt.reconstruct(residues,primes,bound)
        require(value == expected,'Signed CRT after entire query')
        negatives += int(value < 0)
    require(negatives > 0,'Signed-query control not exercised')
    try:
        crt.reconstruct([0],[3],bound)
    except AssertionError:
        pass
    else:
        raise AssertionError('Insufficient CRT range accepted')
    paths = [HERE/'PROOF.md',HERE/'verify.py',ROOT/'deterministic-crt-transfer'/'verify.py']
    print(json.dumps({'status':'PASS','scope':'bounded lazy grouping/CRT, not full master recursion',
        'instances':256,'field_query_comparisons':cases,'signed_negative_queries':negatives,
        'primes':primes,'maximum_nested_frames':max_depth,'maximum_frame_calls_per_query':max_calls,
        'sha256':{str(p.relative_to(ROOT.parent)):sha256(p.read_bytes()).hexdigest() for p in paths}},indent=2))


if __name__ == '__main__':
    main()
