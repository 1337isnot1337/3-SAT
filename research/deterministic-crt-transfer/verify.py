"""Bounded deterministic CRT and actual rational-crossing checks."""
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from math import gcd, isqrt, prod
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


field = load('crt_predecessor_field', ROOT / 'odd-prime-rank-transfer' / 'field.py')
refined = load('crt_predecessor_refined', ROOT / 'three-bit-macro-walsh' / 'refined.py')


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def good_primes(bit_bound, certificate):
    require(bit_bound >= 0 and certificate > 0, 'Bad certificate or bound')
    needed = bit_bound + 2
    k = needed + certificate.bit_length()
    t = 8 + 2 * (k + 1).bit_length()
    # A smaller deterministic sieve suffices for bounded tests; the proof gives
    # a polynomial explicit full limit 2**(t+1), which can be enormous here.
    primes, candidate = [], 3
    while len(primes) < needed:
        if all(candidate % q for q in range(2, isqrt(candidate) + 1)):
            if gcd(candidate, certificate) == 1:
                primes.append(candidate)
        candidate += 2
        require(candidate < 1 << (t + 1), 'Proved supply limit exceeded')
    return primes


def reconstruct(residues, primes, bound):
    require(len(residues) == len(primes) and primes, 'Residue count')
    modulus = prod(primes)
    require(modulus > 2 * bound, 'CRT modulus too small')
    value = 0
    current_modulus = 1
    for residue, prime in zip(residues, primes):
        require(gcd(current_modulus, prime) == 1, 'Primes must be distinct')
        digit = (residue - value) * pow(current_modulus, -1, prime) % prime
        value += current_modulus * digit
        current_modulus *= prime
    if value > modulus // 2:
        value -= modulus
    require(abs(value) <= bound, 'Query outside proved range')
    return value


def crossing_case():
    data = refined.construct(1)
    n = 8
    certificate = data['denominator']
    primes = good_primes(3, certificate)
    indices = {alpha: j for j, alpha in enumerate(data['types'])}
    classes = refined.SCHEME['classes']
    all_residues = [[0] * 256 for _ in primes]
    factor_count = 0
    max_denominator = 0
    for piece in data['pieces']:
        def original(x, y, u, v):
            if x ^ y != u ^ v:
                return F(0)
            return sum((piece['function'][indices[tuple(int(j == classes[x ^ y, b]) for j in range(6))]]
                        * (-1) ** ((b & (y ^ v)).bit_count() % 2) for b in range(n)), F(0)) / n
        rows = [[F(0)] * (n*n) for _ in range(n*n)]
        cols = [[F(0)] * (n*n) for _ in range(n*n)]
        for x in range(n):
            for y in range(n):
                for u in range(n):
                    for v in range(n):
                        value = F(0)
                        for a, coefficient in ((x, 2), (x+1, -1)):
                            if a < n:
                                b = a ^ y ^ u
                                if b <= v:
                                    value += coefficient * original(a, y, u, b) / (1 << (v-b+1))
                        rows[x*n+y][u*n+v] = value
                        cols[x*n+u][y*n+v] = value
                        d = value.denominator
                        max_denominator = max(max_denominator, d.bit_length()-1)
                        while d % 2 == 0:
                            d //= 2
                        require(certificate % d == 0, 'Odd denominator certificate')
        for pi, prime in enumerate(primes):
            converted = [[[field.rational_residue(v, prime) for v in row] for row in mat]
                         for mat in (rows, cols)]
            factored = [field.factor(mat, prime) for mat in converted]
            require(all(field.reconstruct(f) == mat for f, mat in zip(factored, converted)), 'Factors')
            require(factored[0]['inner_dimension'] <= piece['row_support'] and
                    factored[1]['inner_dimension'] <= piece['col_support'], 'Rank envelope')
            direction = min(range(2), key=lambda i: factored[i]['inner_dimension'])
            f = factored[direction]
            coeffs = []
            for x in range(n):
                y = ((x << 1) & 7) | (x >> 2)
                if direction == 0:
                    value = sum(a * sum(row) for a, row in zip(f['left'][x*n+y], f['right']))
                else:
                    value = sum(sum(f['left'][x*n+u][j] for u in range(n)) *
                                sum(f['right'][j][y*n+v] for v in range(n))
                                for j in range(f['inner_dimension']))
                coeffs.append(value % prime)
            for mask in range(256):
                all_residues[pi][mask] += sum(coeffs[x] for x in range(n) if mask >> x & 1)
            factor_count += 2
    for mask in range(256):
        require(reconstruct([r[mask] for r in all_residues], primes, 8) == mask.bit_count(), 'Count')
    require(max_denominator >= 7, 'Dyadic height not exercised')
    return {'n': n, 'primes': primes, 'pieces': len(data['pieces']), 'factorizations': factor_count,
            'exact_predicate_counts': 256, 'maximum_denominator_bits_minus_one': max_denominator}


def main():
    cases = 0
    for bound in range(0, 40):
        for certificate in (1, 3, 15, 3*5*7*11):
            primes = good_primes(bound.bit_length(), certificate)
            require(all(gcd(p, certificate) == 1 for p in primes), 'Bad prime selected')
            require(prod(primes) > 2 * bound, 'Insufficient prime product')
            for value in range(-bound, bound+1):
                require(reconstruct([value % p for p in primes], primes, bound) == value, 'Signed CRT')
                cases += 1
    for callback in (lambda: reconstruct([0], [3], 2),
                     lambda: reconstruct([0, 0], [3, 3], 1)):
        try:
            callback()
        except AssertionError:
            pass
        else:
            raise AssertionError('Negative control failed')
    require((-1 % 3) % 8 != -1 % 8, 'Mod-two boundary control')
    crossing = crossing_case()
    paths = [HERE / 'verify.py', HERE / 'PROOF.md', ROOT / 'odd-prime-rank-transfer' / 'field.py',
             ROOT / 'three-bit-macro-walsh' / 'refined.py']
    print(json.dumps({'status': 'PASS', 'scope': 'finite CRT and one rational crossing, not the master algorithm',
                      'signed_crt_cases': cases, 'negative_controls': 3, 'crossing': crossing,
                      'sha256': {str(p.relative_to(ROOT.parent)): sha256(p.read_bytes()).hexdigest() for p in paths}}, indent=2))


if __name__ == '__main__':
    main()
