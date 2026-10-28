# Alternative output codebooks for a charged cubic filter

Status: `scoped_checked` for the finite classification described below.
No asymptotic filter, improved SAT bound, or selected-result change is
claimed. Contributor: Cinna Davis, with substantial OpenAI Codex assistance.
The accepted OpenAI baseline is unchanged.

## Question and finite result

[PR #19](https://github.com/1337isnot1337/3-SAT/pull/19) constructs charged
crossing pieces and asks for a scalar filter that removes a central interval
without losing leading label and output capacity. At grade h=6 it chooses four
asymmetric input rows and four input columns, and four output partition states.
[Issue #23](https://github.com/1337isnot1337/3-SAT/issues/23) independently
classifies those *specific* output states: their scalar weight space is
quadratic, so excluding shifts -1, 0, 1 leaves only zero. Issue #21 also
observed this obstruction and the different grade-4 behavior in parallel.

We keep PR #19's four row and column labels and change the output codebook.
There are 11 partitions of 6; for every one of their 330 four-element subsets,
use the same subset for the input and output sides of the output axis. For
charge one, let Q_s(a,v) be the grade-6 operator from the predecessor, and
let W be the span of a selected set of four partition states. We seek rational
weights w_s, with w_s=0 for s=-1,0,1, for which the restriction **and
projection** of the weighted operator to W is scalar for every one of the
16 chosen input-label pairs:

    [t^u] sum_s w_s Q_s(a,v) t^y = G(a,v) [u=y]  (u,y in W).

The projection matters: we do not assert that W is invariant or that the
weighted operator is scalar on the entire grade-6 space. The exact search
finds:

* 296 codebooks have only the zero scalar-output weight vector. Full column
  rank modulo 1,000,003 certifies this also over the rationals.
* The remaining 34 have a one-dimensional rational weight space. Every one
  is spanned by the same cubic sequence `w_s=(s^3-s)/6`; every resulting
  4-by-4 matrix G is invertible over the rationals.
* Since that cubic is nonzero at s=±2, none of the 330 has a nonzero
  scalar-output weight vector when all five shifts -2,-1,0,1,2 are excluded.

The active shifts range from -12 through 12, except -1,0,1. The 34
codebooks, their explicit weight vectors and exact pairing matrices are in
[verification.json](verification.json). One example uses
`(1,1,1,1,1,1)`, `(2,2,1,1)`, `(3,1,1,1)` and `(3,3)` as output states.
For these, G in the predecessor's deterministic row/column order is

```text
 1598400    532800        0        0
  -53280     -1440   112320  -319680
       0     28080    -8640 -1123200
       0         0        0    57600
```

As in PR #19, multiplying the raw pieces by the cubic and a local inverse
of G on the first label axis yields a valid *finite* four-label crossing
on this output codebook. A local invertible axis change preserves both
flattening ranks; this finite fact does not show improved asymptotic ranks.

## Reproduction and evidence

From repository root, offline with Python 3.11+ and only the standard library:

```sh
python3 -I -B research/charged-scalar-filter/codebooks.py > /tmp/charged-codebooks.json
cmp /tmp/charged-codebooks.json research/charged-scalar-filter/verification.json
make verify
```

The script constructs all output matrix entries from the pinned charged
operator implementation. For every label pair it enforces every off-diagonal
entry and every diagonal difference; checking a trace alone would be
insufficient. For the 296 modular certificates, denominators are inverted
only when nonzero modulo the prime, and full modular column rank implies full
rational column rank. For the other 34, rational elimination finds the
complete kernel, checks each exact scalar constraint and each full-rank pairing,
and checks that all primitive weights equal the stated cubic. It also compares
both operator orders on all 1,408 vectors for the first surviving codebook.
The saved report binds the code and predecessor modules by SHA-256. These are
finite, author-run computational checks, not an independent review or formal
verification. The predecessor code is a shared dependency, not a separately
implemented operator oracle.

## Cost and remaining gap

The output set is a hand-verified small codebook, not a uniform construction.
A fixed positive interval relative to h, exponential-in-sqrt(h) capacity on
both axes, all-size scalarity and invertible pairing, uniform entry generation,
and both directional factorization bounds must all be proved together.
Coefficients, normalizer heights and rational-to-finite-field compilation must
be charged. The source's reductions, branches, queries, modes, recursion,
precision, exact recovery, amplification, time and space remain unchanged and
unverified for any new all-size family. The tested h=6 exclusion is not an
asymptotic ratio or an alpha improvement; no complete SAT solver was run.
The fixed-codebook grade-6 obstruction does not apply to every possible output
codebook, but this search makes no claim about arbitrary linear combinations,
different input labels, other charges, or other grades.

A concrete continuation is to characterize the off-diagonal third-moment
operator and search for uniformly large coordinate subspaces on which
`sum_s (s^3-s)Q_s` has scalar compressions with full-rank label pairing.
Small examples alone cannot establish their capacity.

## Provenance

Base main `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`; PR #19 supplies
the selected asymmetric input labels, normalizer framework and source pins.
The charged operators and first moment are from PR #11; the earlier uncharged
moment screen is branch `research/operator-moment-recovery`, commit
`8191d2e2813615e4941216c012b151c96c5d7ce5`. Issue #23 and
[PR #46](https://github.com/1337isnot1337/3-SAT/pull/46) cover the original
fixed output codebook, independently and in parallel. See predecessor
[SOURCES.json](../charged-asymmetric-crossing/SOURCES.json) for Anthropic's
source, license and exact hashes. This package changes no upstream material.
