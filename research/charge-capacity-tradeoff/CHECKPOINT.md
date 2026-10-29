# Continuation checkpoint

This checkpoint closes the current work at the user's request. PR #32 remains
open for review; do not merge it or change the selected result without current
maintainer authorization. The author has not selected a new SAT result or
independently reviewed the proofs. Frozen upstream is unchanged.

PR #32 contains the support-mask rank and capacity estimates, actual one-
and two-label boundary examples, an h=4 finite rank-three scalar pairing,
simple-spectrum arguments for its outer and adjacent shifts, and an
outer-shift scalarity obstruction in OUTER-FILTER.md. The last uses sign
variation and a reflected-walk determinant; it remains author-checked. The
author-checked arguments, exact hypotheses and limitations are in PROOF.md
and ADJACENT.md. Full capacity `exp(kappa sqrt(h)-O(log h))` requires
effective degree `e=O(sqrt(h) log h)`; the converse concerns the structural
mask only. The new truncated recurrence screens bilateral weights at charge
degree `2h-3` for h=2..6: its scalarizing space has dimension two and both
basis pairings have rank four for h=4,5,6. It matches 640 direct
interpolation coefficients through h=4, reproduces the previous h<=4 bases,
and has 16 direct spot comparisons at h=5,6 in both operator orders. This is
finite evidence only, with no all-size formula or SAT improvement. The work
does not relate shift width to effective degree or rule out charge-dependent
normalization, projected compressions, or arbitrary decompositions.

Canonical main `0d38d11` is integrated in merge `ba54676`. The merged tree
passes `make verify`: 7 frozen sources, 5 tasks, 48 research claims, 377 local
links, and all 17 unit tests. The truncated recurrence and spot outputs bind
checker, model and source hashes; hosted CI should be checked against the
final PR head. The baseline selected alpha remains 1/2.

The adjacent-shift h=4 two-output example does not extend by the same
unprojected all-ones scalar-subspace mechanism to h>=5, because its relevant
operator has simple spectrum. A single operator can still have large
two-sided scalar compression; simultaneous label pairing and factor costs
remain open. Issue #108 is investigating projected partition codebooks, and
issues #21/#23 have investigated fixed-charge scalar filters: read their live
updates before claiming related work.

The latest issue #20 update and PR body should identify this finite next-degree
screen as separate from the capacity theorem and the fixed-charge filter work
in issues #21/#23. Main's extreme-shift output-rank argument excludes only
shifts `|s| >= (1+epsilon)h` under its output-dimension condition; this screen
includes `|s|=h` and studies charge degree `2h-3`. A finite search up to h=400 found no case in which the structural
cover optimum beat both the balanced cover and the full-dimension bound. This
is exploratory only, has no saved certificate or general proof, and must not
be treated as a theorem or substituted for the exact minimum formula.
Unimodality alone does not imply that simplification.
