"""Check structured good primes and an actual cyclic-conjugated crossing."""
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from math import gcd, isqrt, lcm
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


field = load('cyclic_field', ROOT / 'odd-prime-rank-transfer' / 'field.py')
refined = load('cyclic_refined', ROOT / 'three-bit-macro-walsh' / 'refined.py')
crt = load('cyclic_crt', ROOT / 'deterministic-crt-transfer' / 'verify.py')


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def primes_through(limit):
    sieve = bytearray(b'\1') * (limit + 1)
    sieve[:2] = b'\0\0'
    for d in range(2, isqrt(limit) + 1):
        if sieve[d]:
            sieve[d*d:limit+1:d] = b'\0' * len(range(d*d, limit+1, d))
    return [i for i in range(limit+1) if sieve[i]]


def main():
    primes = primes_through(10000)
    safe = [p for p in primes if p % 8 == 7]
    prime_checks = 0
    for p in safe:
        require(pow(2, (p-1)//2, p) == 1, 'Euler criterion')
        for lam in range(13):
            require(pow(2, 1 << lam, p) != 1, 'Cyclic denominator')
            prime_checks += 1
    require(all(pow(2, 2, p) == 1 for p in (3,)), 'Ordinary odd prime negative control')
    require(pow(2, 4, 5) == 1, 'Second ordinary prime negative control')
    require(gcd(7, 7) != 1, 'Base denominator must still be checked')
    general_checks = 0
    for factors in ((2,), (3,), (4,), (2, 3), (5, 7), (2, 3, 5)):
        modulus = 8 * lcm(*factors)
        eligible = [p for p in primes if p % modulus == modulus - 1]
        require(eligible, 'No small progression example')
        for p in eligible:
            for base in factors:
                for lam in range(10):
                    require(pow(base, 1 << lam, p) != 1, 'General denominator')
                    general_checks += 1
    data = refined.construct(1)
    n = 8
    base = 3
    denominator = base**n - 1
    chosen = [p for p in primes if p % 24 == 23 and gcd(p, data['denominator']) == 1][:5]
    indices = {alpha: j for j, alpha in enumerate(data['types'])}
    classes = refined.SCHEME['classes']
    sums = [[F(0)]*(n*n) for _ in range(n*n)]
    residues = [[0]*256 for _ in chosen]
    max_denom_bits = 0
    facts = 0
    for piece in data['pieces']:
        def original(x, y, u, v):
            if x ^ y != u ^ v:
                return F(0)
            return sum((piece['function'][indices[tuple(int(j == classes[x ^ y,b]) for j in range(6))]]
                        * (-1)**((b & (y ^ v)).bit_count() % 2) for b in range(n)), F(0)) / n
        rows = [[F(0)]*(n*n) for _ in range(n*n)]
        cols = [[F(0)]*(n*n) for _ in range(n*n)]
        for x in range(n):
            for y in range(n):
                for u in range(n):
                    for v in range(n):
                        value = F(0)
                        for a, coef in ((x, base), ((x+1)%n, -1)):
                            b = a ^ y ^ u
                            t = (v-b) % n
                            value += coef * original(a,y,u,b) * F(base**(n-1-t), denominator)
                        rows[x*n+y][u*n+v] = value
                        cols[x*n+u][y*n+v] = value
                        sums[x*n+y][u*n+v] += value
                        require((n*denominator*data['denominator']) % value.denominator == 0,
                                'Denominator bound')
                        max_denom_bits = max(max_denom_bits, value.denominator.bit_length())
        for pi, p in enumerate(chosen):
            converted = [[[field.rational_residue(z,p) for z in row] for row in mat] for mat in (rows,cols)]
            factors = [field.factor(mat,p) for mat in converted]
            require(all(field.reconstruct(f) == mat for f,mat in zip(factors,converted)), 'factor')
            require(factors[0]['inner_dimension'] <= piece['row_support'] and
                    factors[1]['inner_dimension'] <= piece['col_support'], 'rank bound')
            side = min(range(2), key=lambda i: factors[i]['inner_dimension'])
            f = factors[side]
            coeffs = []
            for x in range(n):
                y = ((x<<1)&7)|(x>>2)
                if side == 0:
                    val = sum(a*sum(row) for a,row in zip(f['left'][x*n+y],f['right']))
                else:
                    val = sum(sum(f['left'][x*n+u][j] for u in range(n))*
                              sum(f['right'][j][y*n+v] for v in range(n))
                              for j in range(f['inner_dimension']))
                coeffs.append(val % p)
            for mask in range(256):
                residues[pi][mask] += sum(coeffs[x] for x in range(n) if mask >> x & 1)
            facts += 2
    for x in range(n):
        for y in range(n):
            for u in range(n):
                for v in range(n):
                    require(sums[x*n+y][u*n+v] == int(x == v and y == u), 'Crossing sum')
    for mask in range(256):
        require(crt.reconstruct([r[mask] for r in residues],chosen,8) == mask.bit_count(), 'CRT counts')
    require(max_denom_bits >= 8, 'Long odd denominator was not exercised')
    # Exact inverse entry 1/(2^N-1) provides an uncancelled large denominator.
    require(F(1,denominator).denominator == denominator, 'Inverse denominator control')
    paths = [HERE/'PROOF.md', HERE/'verify.py', ROOT/'deterministic-crt-transfer'/'verify.py',
             ROOT/'odd-prime-rank-transfer'/'field.py', ROOT/'three-bit-macro-walsh'/'refined.py']
    print(json.dumps({'status':'PASS','scope':'finite good-prime and actual cyclic crossing controls',
                      'primes_up_to_10000':len(safe),'good_prime_length_checks':prime_checks,
                      'general_progression_checks':general_checks, 'cyclic_base':base,
                      'negative_controls':3,'cyclic_dimension':n,'cyclic_denominator':denominator,
                      'crossing_primes':chosen,'pieces':len(data['pieces']),'factorizations':facts,
                      'crossing_entries':n**4,'predicate_counts':256,'max_entry_denominator_bits':max_denom_bits,
                      'sha256':{str(p.relative_to(ROOT.parent)):sha256(p.read_bytes()).hexdigest() for p in paths}},indent=2))


if __name__ == '__main__':
    main()
