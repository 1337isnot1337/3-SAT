"""Bounded exact field, sampler, bad-prime and signed-recovery controls."""

from fractions import Fraction as F
from hashlib import sha256
import importlib.util
from itertools import product
import json
from math import isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("prime_field", HERE / "field.py")
field = importlib.util.module_from_spec(spec)
spec.loader.exec_module(field)
require = field.require


def small_is_prime(n):
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def rational_rank(matrix):
    rows = [list(map(F, row)) for row in matrix]
    rank = 0
    for j in range(len(rows[0])):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][j]), None)
        if pivot is None:
            continue
        rows[pivot], rows[rank] = rows[rank], rows[pivot]
        for i in range(rank + 1, len(rows)):
            coefficient = rows[i][j] / rows[rank][j]
            rows[i] = [x - coefficient * y for x, y in zip(rows[i], rows[rank])]
        rank += 1
    return rank


def main():
    matrices = skips = signed = 0
    values = [F(-2), F(-1, 2), F(0), F(1, 3), F(2, 5)]
    for entries in product(values, repeat=4):
        matrix = [list(entries[:2]), list(entries[2:])]
        rank = rational_rank(matrix)
        for p in [3, 5, 7, 11, 101]:
            try:
                reduced = [[field.rational_residue(x, p) for x in row] for row in matrix]
            except field.BadPrime:
                skips += 1
                continue
            factors = field.factor(reduced, p)
            require(field.reconstruct(factors) == reduced, "Field factor identity")
            require(factors["inner_dimension"] <= rank, "Good-prime rank specialization")
            matrices += 1
    for p in [3, 5, 7, 11, 17, 101, 257]:
        for bound in range(p // 2 + 1):
            if 2 * bound >= p:
                continue
            for value in range(-bound, bound + 1):
                require(field.recover_signed(value % p, p, bound) == value, "Exact signed recovery")
                signed += 1
    # Full sieve only for the registered small intervals T=8,...,16.
    limit = 1 << 17
    sieve = bytearray(b"\1") * limit
    sieve[:2] = b"\0\0"
    for d in range(2, isqrt(limit - 1) + 1):
        if sieve[d]:
            sieve[d * d:limit:d] = b"\0" * len(range(d * d, limit, d))
    profiles = []
    require(F(16, 9) - F(125506, 100000) > F(1, 2), "Prime interval bound constants")
    for T in range(8, 17):
        count = sum(sieve[1 << T:1 << (T + 1)])
        require(count * 2 * T >= 1 << T, "Registered exact prime density")
        require((1 - F(1, 2 * T)) ** (64 * T) < F(1, 2 ** 32), "Capped sampler bound")
        profiles.append({"T": T, "prime_count": count})
    require(F(1, 2 ** 9) + F(1, 2 ** 32) < F(1, 100), "Combined failure bound")
    calls = []
    def recording_prime(candidate):
        calls.append(candidate)
        return small_is_prime(candidate)
    require(field.bounded_prime_sample(8, [256] * 1000, recording_prime) is None, "Capped all-composite failure")
    require(len(calls) == 512, "Sampler worst-outcome trial count")
    require(field.bounded_prime_sample(8, [256, 258, 257, 263], small_is_prime) == 257, "First-prime selection")
    try:
        field.normalizer_residue(F(7, 3), 7)
    except field.BadPrime:
        pass
    else:
        raise ValueError("Zero normalizer numerator escaped rejection")
    # A final-count bound cannot replace the larger intermediate query bound.
    try:
        field.recover_signed(1000 % 101, 101, 1000)
    except ValueError:
        pass
    else:
        raise ValueError("Undersized query prime escaped negative control")
    require(field.recover_signed(1000 % 4099, 4099, 1000) == 1000, "Intermediate query restoration")
    # Odd-field residue cannot be reduced directly modulo a power of two.
    require((-1 % 101) % 8 != -1 % 8, "Signed boundary negative control")
    require(field.recover_signed(-1 % 101, 101, 1) % 8 == -1 % 8, "Integer boundary preserves outer modulus")
    print(json.dumps({"status": "PASS", "scope": "bounded exact transfer controls; no AKS or SAT implementation",
                      "field_matrix_cases": matrices, "rejected_bad_denominator_cases": skips,
                      "signed_query_cases": signed, "prime_intervals": profiles,
                      "negative_controls": ["capped all-composite trials", "zero normalizer numerator",
                                            "small final-count prime fails for a larger query",
                                            "ordinary prime residues do not preserve signed modulo-two values"],
                      "bindings": {name: sha256((HERE / name).read_bytes()).hexdigest()
                                   for name in ["field.py", "verify.py", "PROOF.md", "REGISTERED.md"]}}, indent=2))


if __name__ == "__main__":
    main()
