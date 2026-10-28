# Newton-mode support of clause and equality packets

Status: `scoped_checked`; written identities are author-checked, not independently
reviewed. No improved SAT bound or selected-result change is claimed.

Task: `weighted-modes`. Base `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`.
Contributor: Cinna Davis, with substantial OpenAI Codex assistance.

## Result

The actual multilinear extension of a ternary equality is quadratic, so
a single row equality vertex has total crossing-mode degree at most two
after its row bits are summed. A three-literal clause can have degree three.
This is a local identity, not a bound on the full group's mode enumeration.

The [proof and limits](PROOF.md) give a growing single-packet family with
`K` active Newton modes and `q` disjoint ternary equalities. Every tuple of
total degree at most `2q` has a nonzero rational summand; for positive
clauses the exact support is degrees `q` through `3q`. This gives
`binom(K+2q, 2q)` equality tuples, with `K>=3q`. The proof uses an explicit
common-sign argument and includes all source-side Boolean moments. It does
not construct a globally admissible packet embedding. A rational-height
argument shows that every listed local summand survives the source
child precision at `t=1`, conditional on such an embedding and an evaluation
set containing `zeta=1`. This does not establish nonvanishing after other
group tensors are included. For this family, a degree-`d` source moment has
at least `K-d` powers of two; the proof combines this with the Newton row
weights to give a precision-aware lower valuation bound. This uses the free
unary column tensors and is not a general child-network invariant.

A three-port example illustrates the result:
all 10 degree-at-most-two Newton tuples occur for equality and all 19
positive-degree-at-most-three tuples occur for a positive clause. Actual
source moments and the direct contraction are checked over the rationals.
The same packet's zero-mode child has a packet vertex with table
`(1-Y1)(1-Y2)(1-Y3)`, which is not an equality table. This exhibits failure
of closure of the individual original table family under child creation;
it does not rule out a broader invariant for the joint child network.
The example obeys the local slot rule but is not itself a complete large
instance satisfying every asymptotic packing condition.

There is no improved complete cost: reductions, tensor descriptions, entry
work, mode enumeration, precision, recursion and recovery remain at their
accepted baseline bounds. At smaller precisions rational terms can vanish.
A future gain requires a uniform invariant
covering clauses, child packet tensors, and repacking, followed by the full
cost analysis. The all-size identities await independent review.

## Reproduce

From the repository root with standard-library Python 3.11 or newer:

```sh
python3 -I -B research/newton-packet-support/verify.py
make verify
```

[verification.json](verification.json) binds the checker, proof and source
files by SHA-256. It checks nine kernel entries, both full 64-assignment
contractions, their exact mode decompositions, six growing-family cases,
510 Boolean equality cases, exact two-adic valuations, and the cubic child
coefficient. These checks do not prove a global support
bound or implement the full contraction. The frozen upstream source and
accepted theorem remain unchanged.

## Provenance

The accepted OpenAI source is pinned by the root [SOURCES.json](../../SOURCES.json).
The Newton expansion and integrality analysis are from
[PR #4](https://github.com/1337isnot1337/3-SAT/pull/4) and its
[local proof](../cauchy-newton-modes/PROOF.md). Issue
[#22](https://github.com/1337isnot1337/3-SAT/issues/22) coordinates this
lane. New material is Apache-2.0; no scientific priority, independent review
or formal verification is claimed.
