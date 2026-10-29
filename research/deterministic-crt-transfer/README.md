# Deterministic CRT transfer for compact bad-prime certificates

Status: `scoped_checked`; author-checked, substantially Codex-assisted and
not independently reviewed. This is a conditional algorithm interface, not a
new 3-SAT bound. Selected alpha remains 1/2.

Starting from the rational-rank crossing transfer in PR #17, this package
replaces random selection of one very large prime by a deterministic inventory
of polynomially many small good primes and exact signed CRT at every original
integer network-query boundary. The new hypothesis is a uniformly computable,
polynomial-bit integer whose odd prime divisors cover all possible entry and
normalizer failures through the polynomial call-size cap. It is sufficient,
for example, when dyadic denominators are multiplied by a known polynomial-bit
common denominator per size. PR #17's nilpotent conjugation of the prior
polynomial-height adapted-basis families meets this certificate, though those
families do not provide an improved rate. The more general PR #17 contract
does not necessarily meet the new certificate and remains randomized.

[PROOF.md](PROOF.md) states the all-size result, deterministic prime supply,
complete conditional time/space accounting, example, and open obligations.
The proof is not mechanically verified. Its exponentially large field matrices
lose the accepted theorem's polynomial-space guarantee. The accepted theorem
is a premise, not an audit target. No rank or selected result changes.

Reproduce with Python 3.11+ and the standard library:

```sh
python3 -I -B research/deterministic-crt-transfer/verify.py
make verify
```

[verification.json](verification.json) records 6,400 signed CRT checks,
certificate and ambiguity controls, and the existing actual six-class crossing
after nilpotent conjugation: all 256 predicate counts, both flattening
factorizations on five good primes, four pieces, and denominator exponents up
to 9. The finite checker uses simple trial division and is not the full master
algorithm or the polynomial-time sieve described in the proof. It checks no
asymptotic rank rate, sparse SAT solver or theorem selection.

Sources and credit: base `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`;
OpenAI source `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`, pinned in
[SOURCES.json](../../SOURCES.json); Anthropic master and prime-density source
pins are in [PR #17's manifest](../odd-prime-rank-transfer/SOURCES.json).
The crossing and finite constructor are credited to
[PR #14](../symmetric-walsh-pieces/CONSTRUCTION.md),
[PR #15](../three-bit-macro-walsh/CONSTRUCTION.md), and
[PR #17](../odd-prime-rank-transfer/CONJUGATION.md). The dyadic-prime density
bound is Rosser and Schoenfeld's, as cited in PR #17. No novelty claim is made
for CRT or deterministic sieving. Cinna Davis with substantial OpenAI Codex
assistance; new material is Apache-2.0.

Next: find an actually cheaper crossing family with a proved certificate and
both rank bounds, or a different deterministic selection method covering
families without one. Check live claims and changed premises first.
