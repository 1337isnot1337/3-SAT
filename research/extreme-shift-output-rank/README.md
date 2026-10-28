# Extreme-shift output-rank obstruction

For the charged crossing interface, every fixed-label raw piece factors
through small intermediate partition spaces near the ends of the shift range.
The [proof](PROOF.md) gives an exact rank-sum bound on its compression to any
output space. If that rank budget is below the output dimension, a scalar
output pairing must be zero.

For output energy `h` and dimension at least `p(h)/poly(h)`, this excludes
nonzero scalar pairings supported *only* on shifts
`|s| >= (1+epsilon)h`, for each fixed `0<epsilon<1` and all sufficiently
large h. More sharply, any nonzero scalar pairing must use a shift with
`|s| <= h+O(sqrt(h) log h)`. The result is independent of the label-pairing
rank and applies to non-coordinate output spaces. It is a scoped,
author-checked all-size argument, substantially AI-assisted and not
independently or formally reviewed. It does not rule out the open central-gap
target, improve a SAT bound, or change the selected result.

Each input label may be an arbitrary linear combination, so the local inverse
normalization of PR #19 preserves the obstruction without paying for its
individual coordinate terms. The proof also charges sums of multiple
separable label-pair pieces. Polynomially many retain the quantitative
shift requirement; a stated exponential-rate condition suffices for the
fixed-epsilon exclusion. Conversely, any nonzero
scalar entry on those extreme shifts needs at least
`N^(1-sqrt(1-epsilon)-o(1))` separable label-pair summands at the predecessor's
selected dimension N. Arbitrary nonseparable joint label mixing must be
charged, and a summand bound is not a general runtime bound.
For a fixed charge, the same lower bound applies to the sum of the ranks of
the shiftwise coefficient matrices in any chosen input-label bases.
The proof also states a shift-location condition for unequal output energy E
and label grade h, with the mixture size charged explicitly.

An output-rate tradeoff covers codebooks whose partition exponent is only a
fixed fraction theta of the full one. Under an explicitly conditional use of
the predecessor's unchanged term-count envelope, losing that output rate does
not lower the support-only envelope threshold, even after the trivial `N^2`
rank cap. This is not an actual-rank or SAT-time lower bound.

The rank-budget criterion is sharp in a relaxed model with independent
intermediate-channel maps: once their total dimension reaches the output
dimension, such maps can sum to the identity. The actual charged modes are
coupled, so this relaxation does not establish a realizable crossing.

Run the finite checks with:

```sh
python3 -I -B research/extreme-shift-output-rank/verify.py > /tmp/extreme-shift.json
cmp /tmp/extreme-shift.json research/extreme-shift-output-rank/verification.json
python3 -I -B research/extreme-shift-output-rank/thresholds.py > /tmp/extreme-thresholds.json
cmp /tmp/extreme-thresholds.json research/extreme-shift-output-rank/thresholds.json
python3 -I -B research/extreme-shift-output-rank/central.py > /tmp/extreme-central.json
cmp /tmp/extreme-central.json research/extreme-shift-output-rank/central.json
python3 -I -B research/extreme-shift-output-rank/triangular.py > /tmp/extreme-triangular.json
cmp /tmp/extreme-triangular.json research/extreme-shift-output-rank/triangular.json
python3 -I -B research/extreme-shift-output-rank/charge_control.py > /tmp/extreme-charge.json
cmp /tmp/extreme-charge.json research/extreme-shift-output-rank/charge_control.json
make verify
```

The finite checks cover both operator orders and compressed operator ranks
for four label pairs at each of grades 4 and 6, separable mixtures of those
labels, and bounded endpoint scalar controls. Additional full-space checks
cover grade 4 at output energies
0, 1, 3 and 5 and charges 1 and 2, plus a non-coordinate output embedding
with a non-orthogonal left inverse. They do not independently verify the
all-size proof. The proof states the exact support and dimension conditions,
the multiple-label-mixing limit, the partition asymptotics and the remaining
obligations.

At grades 4, 6, 9 and 12, a separate finite replay finds that the last
selected row/column label pair gives a full-rank output operator for every
shift `|s|<=h`. These controls show why a uniform per-piece rank reduction
cannot dispose of those finite central shifts; they do not establish
scalarity or an all-size result. The grade-12 control is intentionally kept
out of default CI.

The same sampled piece at shift `-h` is triangular in the original output
order at grades 4, 6 and 9. At grade 12 it has a nonzero two-cycle, so no
common permutation of input and output basis vectors makes it triangular.
This rules out a simple permutation-based proof of the observed full ranks;
it does not rule out a non-permutation basis or another proof.
The sampled `s=-h` matrices also lose rank at charge zero in grades 4, 6
and 9, so their full rank at charge one does not extend uniformly to all
charges.

An exact scan of the predecessor's selected grades through `h=2000` finds
the first passing rank-budget inequalities at `(h, lambda)=(887,93)`,
`(92,23)` and `(14,5)` for epsilon `1/4`, `1/2` and `3/4`, respectively.
All later selected grades within that finite scan also pass. This records
the conservative sufficient bound, not a sharp threshold or a proof of
monotonicity beyond the scan; [thresholds.json](thresholds.json) gives the
coverage.

The source construction is [PR #11](../charged-operator-moments/PROOF.md),
with the scalar-filter target and leading-capacity grade choice in
[PR #19](../charged-asymmetric-crossing/NEXT.md). The finite fixed-codebook
screens in [PR #46](../asymmetric-scalar-filter/README.md) and
[PR #97](../grade-nine-filter/README.md) motivated this separate rank
question; those finite screens are not used as an all-size proof. The base
commit is `1dfac844cbb1e570c99579ecf48c1007d72da7c9`.
