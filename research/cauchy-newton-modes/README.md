# Exact Newton modes for Cauchy tiles

Status: `scoped_checked` for the stated finite checks. All-size arguments are
author-checked with substantial AI assistance; independent review pending.

Task: `weighted-modes`. Base commit: `fd6df02023122badbdd888803146f0bd92002214`.

Contributor: 1337isnot1337, with substantial OpenAI Codex assistance. Apache-2.0.

## Question and changed premise

Replace geometric Cauchy modes by the finite rational Newton identity in
[PROOF.md](PROOF.md). The OpenAI theorem is accepted as true.

## Statement and scope

The constructed row coefficients have valuation at least
`a+1-i+3k-2 popcount(k)`, using one mode per tile and index. At every odd
interpolation node, the stronger construction gives
`a+1-i+4k-2 popcount(k)`. The leading coefficient of the stated formal
enumeration envelope improves by `1/sqrt(3)` uniformly and by `1/2` at odd
nodes, compared with the geometric envelope.
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
quadratic extension, plus 680 odd-node specializations; 9,552 guard-precision
checks; 2,536 exact Cauchy minors across the two canonical kernels; and both
versions of a four-wire network, each with all 256 pairs of assignments, all
36 degree-feasible mode tuples and 16 precision truncations. Negative controls
show why arbitrary extension points and division without guard bits fail.
The output binds the proof, checker, frozen contraction source and selected
result by SHA-256.

Finite formal enumeration also improves after retaining the source's initial
valuation: with four tiles, 16 indices per tile, precision 64 and initial
weight 5, the count drops from 114,115,475 to 3,581,459, or 694,143 at an
odd node. These are exact tuple counts, not observed contraction or SAT
runtimes. The other two saved parameter cases also improve.

The checker takes under a minute on the authoring machine. It is not a
contraction implementation and does not verify the all-size proof.

## Limits and open next questions

The root `M/sqrt(u)` scale is unchanged; a larger alpha needs another idea.
First review the congruence needed for integer-valued binomial factors and
the local guard-precision calculation. A full-tile formal counting argument
shows the new linear weights still retain `exp(Theta(M/sqrt(u)))` tuples
in that family, without asserting nonzero SAT coefficients. Reoptimizing
these same unrestricted weights can only change the constant.

The next concrete experiment is to extract mode coefficients for actual
clause/equality packet tensors, compare their nonzero support with the formal
envelope, and identify a support identity preserved by the child construction.
An initial-packet numerical reduction without a preserved recursion invariant
would remain a finite observation. Another route is a joint change to recovery
and kernel. See the [proof](PROOF.md) for all cost boundaries.

## Sources and credit

Source labels and predecessor credit to PR #1 are given in the proof. Frozen
upstream commit: `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`; see
[SOURCES.json](../../SOURCES.json). No scientific-priority claim is made.
