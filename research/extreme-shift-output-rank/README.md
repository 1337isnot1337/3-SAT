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

The proof also charges sums of multiple raw pieces. Polynomially many mixed
pieces retain the quantitative shift requirement; a stated exponential-rate
condition suffices for the fixed-epsilon exclusion. Conversely, any nonzero
scalar entry on those extreme shifts needs at least
`N^(1-sqrt(1-epsilon)-o(1))` raw summands at the predecessor's selected
dimension N. Generic exponential-size label normalization is not
automatically covered, and a summand bound is not a general runtime bound.
The proof also states a shift-location condition for unequal output energy E
and label grade h, with the mixture size charged explicitly.

Run the finite checks with:

```sh
python3 -I -B research/extreme-shift-output-rank/verify.py > /tmp/extreme-shift.json
cmp /tmp/extreme-shift.json research/extreme-shift-output-rank/verification.json
python3 -I -B research/extreme-shift-output-rank/thresholds.py > /tmp/extreme-thresholds.json
cmp /tmp/extreme-thresholds.json research/extreme-shift-output-rank/thresholds.json
make verify
```

The finite checks cover both operator orders and compressed operator ranks
for four label pairs at each of grades 4 and 6, plus bounded endpoint scalar
controls. Additional full-space checks cover grade 4 at output energies
0, 1, 3 and 5 and charges 1 and 2. They do not independently verify the
all-size proof. The proof states the exact support and dimension conditions,
the multiple-label-mixing limit, the partition asymptotics and the remaining
obligations.

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
