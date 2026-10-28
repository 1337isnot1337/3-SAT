# Deterministic primes for cyclic-shift crossings

Status: `scoped_checked`; author-checked, substantially Codex-assisted and
not independently reviewed. No improved rho, selected SAT bound, or
polynomial-space result is claimed. This package is stacked on PR #60.

A cyclic conjugation `B=aI-C` at dimension `N=2^lambda` creates exact inverse
coefficients with denominator `a^N-1`, whose bit length is exponential in
lambda. For any fixed finite set of integer bases `a>=2`, every prime in the
progression `-1 mod 8*lcm(a)` avoids all these denominators at every length.
The explicit progression bound used here covers fixed moduli up to 100,000,
and supplies polynomially many primes via a deterministic sieve. Given a compact base-family bad-prime certificate, use
those primes and the PR #60 CRT interface to reconstruct each signed network
query before the outer reduction. The proof does not require factoring or
constructing the large denominator to select primes.

[PROOF.md](PROOF.md) states the uniform family assumptions, good-prime proof,
explicit supply, rank preservation, time and space, and remaining gaps. A long
denominator alone does not show that every compact certificate is impossible.
The arbitrary rational contract of PR #17 is not derandomized. The practical
constant of the explicit prime-supply bound is large; this is an asymptotic
interface, not a practical solver.

Run with Python 3.11+ and the standard library:

```sh
python3 -I -B research/cyclic-shift-prime-transfer/verify.py
make verify
```

[verification.json](verification.json) records 4,004 binary and 6,040 general good-prime/length
checks, three negative controls, the exact 4,096 entries of the actual
six-class R=1 base-3 cyclic-conjugated crossing sum, both flattening factorizations
across five primes, and all 256 predicate counts recovered by CRT. It does not
run the large explicit sieve or implement the full master algorithm. The
all-size proof is not mechanically verified.

Sources, exact paper hash and credit are in [SOURCES.json](SOURCES.json).
The accepted OpenAI theorem is a premise; PRs #14, #15, #17 and #60 supply the
predecessor pieces, rational transfer and deterministic CRT. The progression
estimate is due to Bennett, Martin, O'Bryant and Rechnitzer; elementary CRT,
quadratic reciprocity and Euler's criterion are classical. Contributor: Cinna
Davis with substantial OpenAI Codex assistance; new material is Apache-2.0.

The remaining target is a truly lower-rate crossing family that meets both
rank bounds, uniform generation, and an appropriate prime-supply contract, or
a deterministic selection method for genuinely unrestricted rational
families. Refresh active issues before pursuing either.
