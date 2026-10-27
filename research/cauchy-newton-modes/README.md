# cauchy-newton-modes

Status: `scoped_checked` for the stated finite checks. All-size arguments are
author-checked with substantial AI assistance; independent review pending.

Task: `weighted-modes`. Base commit: `fd6df02023122badbdd888803146f0bd92002214`.

Contributor: 1337isnot1337; substantial OpenAI Codex assistance. Disclose substantial AI assistance.

## Question and changed premise

Replace geometric Cauchy modes by the finite rational Newton identity in
[PROOF.md](PROOF.md). The OpenAI theorem is accepted as true.

## Statement and scope

The constructed row coefficients have valuation at least
`a+1-i+3k-2 popcount(k)`, using one mode per tile and index. The formal
enumeration envelope improves by `1/sqrt(3)` in its leading coefficient.
The full asymptotic exponent and alpha do not change. The derivation and
the integration into the accepted recursion are written out. The checker
tests source kernels at nonrational extension points, guard precision and a
complete small child-network identity.

## Complete cost

The proof accounts for the unchanged child size, precision, entry evaluation,
descriptions, recovery and outer costs. No complete SAT implementation or
larger-alpha claim is made.

## Evidence and reproduction

Run from the repository root with standard-library Python 3.11+:

```sh
python3 -I -B research/cauchy-newton-modes/verify.py
make verify
```

[Saved output](verification.json) records 1,540 rational identities; 2,504
source-kernel identities and coefficient-integrality checks in the unramified
quadratic extension; 7,512 guard-precision checks; 1,268 exact generic Cauchy
minors; and a four-wire network with all 256 pairs of assignments, all 36
degree-feasible mode tuples and 16 precision truncations. Negative controls
show why arbitrary extension points and division without guard bits fail.

Finite formal enumeration also improves after retaining the source's initial
valuation: with four tiles, 16 indices per tile, precision 64 and initial
weight 5, the count drops from 114,115,475 to 3,581,459. These are exact
tuple counts, not observed contraction or SAT runtimes. The other two saved
parameter cases also improve.

The checker takes under a minute on the authoring machine. It is not a
contraction implementation and does not verify the all-size proof.

## Limits and open next questions

The root `M/sqrt(u)` scale is unchanged; a larger alpha needs another idea.
First review the congruence needed for integer-valued binomial factors and
the local guard-precision calculation. Next exploit additional restrictions
on realizable source rows or coefficients, or change recovery together with
the kernel. Reoptimizing the same linear-weight partition envelope can only
change its constant. See the [proof](PROOF.md) for all cost boundaries.

## Sources and credit

Source labels and predecessor credit to PR #1 are given in the proof. Frozen
upstream commit: `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`; see
[SOURCES.json](../../SOURCES.json). No scientific-priority claim is made.
