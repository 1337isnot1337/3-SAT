# A frontier representation for shared sparse-hash independence

Status: `scoped_checked` for finite controls; the all-size argument is
author-checked and awaits independent review. No SAT speedup or new selected
result is claimed. Task `decision-only`; base
`630041c9da3a26edb8c8f59d5f8a4132a188c8bd`. Contributor: Cinna Davis, with
substantial OpenAI Codex assistance. Apache-2.0.

[PROOF.md](PROOF.md) distributes the shared binary-matroid independence
predicate from [the predecessor](../characteristic-two-decision/FOLLOWUPS.md)
using a deterministic ordered frontier. For an a-by-m binary matrix and a
specified column ordering of maximum prefix/suffix intersection dimension b,
the construction has at most `2^(floor(b²/4)+b)` states per cut, with
polynomial-time transition evaluation. An equivalent succinct tensor network
has `O(m b²)` state-bit incidences and transition arity at most `2b²+1`.
It is exact for every selection, including zero columns and dependent prefixes.

The paired-column family `[I_b | I_b]` has one nonzero per column and exact
cut rank `2^b` at the separated ordering, showing why width and ordering
matter; the interleaved ordering has width at most one. This is a lower bound
for that fixed cut, not for all orders or for SAT.

## Reproduction and evidence

```sh
python3 -I -B research/matroid-frontier/verify.py
make verify
```

The standard-library checker exhausts all 4,096 binary 3-by-4 matrices and
all 16 selected subsets, tests every live frontier transition and independently
checks the shared kernel identity on 65,536 inputs. It enumerates subspaces
through dimension four and verifies the paired cut ranks through b=8. Its
[hash-bound output](verification.json) records exact counts. Finite controls
are not an independent review or an implementation of the accepted solver.

## Remaining work and costs

A useful SAT application requires an efficient ordering with small b for the
actual sparse hash matrices, integration of violation polynomials and selection
bits, and full accounting of all query, wire, precision, recursion and recovery
costs. The characteristic-two network must be embedded into the intended
contraction ring with the correct semantics. Descriptions, transition entries,
state multiplicity, and potentially large auxiliary wiring are explicitly
charged in the proof; no small-width or improved exponent assumption is made.
The accepted theorem and [selected result](../../certificates/selected-result.json)
remain unchanged. A concrete next question is whether the hash distribution
used in the predecessor admits constructible low-width orderings at parameters
that survive the whole reduction; the sparse paired example alone says nothing
about its typical or optimal width.

The predecessor identity is from PR #2, `research/characteristic-two-decision`;
the accepted OpenAI source is pinned in [SOURCES.json](../../SOURCES.json) at
commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`. Standard binary linear algebra,
frontier-state techniques and tensor cut-rank bounds are used; no priority for
these methods is claimed.
