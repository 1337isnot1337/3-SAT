# Row-basis-resistant sparse-query support

Status: `scoped_checked` for the bounded checks below. The all-size proof is
author-checked with substantial OpenAI Codex assistance and has no independent
review. The selected SAT bound remains unchanged.

Task: `dense-encoding`. Base: `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`.
Contributor: Cinna Davis, with substantial OpenAI Codex assistance.

## Question and result

The [scalar parity lift handoff](../scalar-parity-lift/HANDOFF.md) asks whether
changing the equation row basis can avoid its coefficientwise support witness;
the earlier witness has a sparse equivalent basis. This package gives a
different, explicit low-load quadratic family in which **every invertible F2
row basis** retains at least `2^Omega(n log log n)` surviving scalar-lift
incidence coefficients before branching. The same order survives on the
all-zero branch of one source high-incidence step, even with row-basis
changes before and after it. In the predecessor's degree-array scheme,
some array on that branch requires `Omega(n log log n)` bits for an injective
index of its nonzero valid assignments. The [proof](PROOF.md) states all
parameters and the exact scope.

This is an obstruction to the specific coefficientwise indexing interface,
not a SAT lower bound or a new algorithm. The family has a trivial satisfying
assignment, and neither aggregation nor non-invertible preprocessing is
excluded. A dense basis may trigger high-incidence branching; the new branch statement
is confined to the all-zero branch of one step, and does not exclude
structure-aware simplification or repeated branching. There is no improvement to the selected
alpha or its general-density logarithmic factor.

## Evidence

From the repository root with standard-library Python:

```sh
python3 -I -B research/row-basis-support/verify.py > /tmp/row-basis-support.json
cmp /tmp/row-basis-support.json research/row-basis-support/verification.json
make verify
```

The [saved output](verification.json) records all 1,009 nonzero row
combinations for n=3,...,9, with L=min(floor(log2 n), floor((n-1)/2));
11,468 exact Mobius coefficient checks; all 20,160 invertible 4-by-4 binary
matrices; 700 seeded invertible bases; all 504 zero-substitution masks for n=3,...,8
with one generated residual basis each; and a duplicate-support cancellation
control. It hash-binds the proof and checker. These finite controls do not
mechanically prove the all-size pigeonhole argument, replay the accepted
algorithm, or establish a full complexity bound.

## Remaining work and credit

A meaningful continuation needs a changed interface: aggregation of the
incidence coefficients, a basis combined with repeated high-incidence branching, or a
construction whose complete post-branch behaviour can be accounted for. Such
work must charge all reduction queries, branches, entry computation, modes,
recursion, precision, recovery and space; this package supplies no such cost
improvement. Issue #28 separately studies transfer aggregation for a different
cyclic witness.

The accepted OpenAI source is pinned at
`7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a` by the repository
[SOURCES.json](../../SOURCES.json); relevant labels are
`lem:tensor-sparse-query`, `eq:sharp-incidence-degree` and
`eq:sharp-wire-budget`. The predecessor scalar-lift support example and its
row-basis caveat are credited in the linked handoff. An independent commenter
on [issue #29](https://github.com/1337isnot1337/3-SAT/issues/29) suggested a
related graph-cut witness; our private-edge construction and proof are distinct.
No priority, human review,
formal verification or selected-result change is claimed.
