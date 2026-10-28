# Continuation checkpoint

The user's research goal remains active. Coordinate through issue #20 and
refresh live issues, PRs, main and project instructions before a new lane or
submission. The author has not selected a new SAT result or independently
reviewed the proofs. Do not merge this or anyone else's work without current
maintainer authorization. Frozen upstream is unchanged.

PR #32 contains the support-mask rank and capacity estimates, actual one-
and two-label boundary examples, an h=4 finite rank-three scalar pairing,
and simple-spectrum arguments for its outer and adjacent shifts. The
author-checked arguments, exact hypotheses and limitations are in PROOF.md
and ADJACENT.md. Full capacity `exp(kappa sqrt(h)-O(log h))` requires
effective degree `e=O(sqrt(h) log h)`; the converse concerns the structural
mask only. This does not relate shift width to e or rule out charge-dependent
normalization, projected compressions, or arbitrary decompositions.

`make verify` passed after integrating main at `ec45f184710a6adcd74e1aea31f29d7d1c44d0e2`.
All seven operator and spectrum checks replayed byte-for-byte against their
saved output, and the threshold checker replays separately. The final source
hashes are in the verification artifacts; hosted CI should be checked against
the current PR head. The baseline selected alpha remains 1/2.

The adjacent-shift h=4 two-output example does not extend by the same
unprojected all-ones scalar-subspace mechanism to h>=5, because its relevant
operator has simple spectrum. A single operator can still have large
two-sided scalar compression; simultaneous label pairing and factor costs
remain open. Issue #108 is investigating projected partition codebooks, and
issues #21/#23 have investigated fixed-charge scalar filters: read their live
updates before claiming related work.

GitHub temporarily rejected issue comments as too frequent while many agents
were active. The latest pushed PR commits remain available; retry an issue
checkpoint after the service permits it. A finite search up to h=400 found no
case in which the structural cover optimum beat both the balanced cover and
the full-dimension bound. This is exploratory only, has no saved certificate
or general proof, and must not be treated as a theorem or substituted for
the exact minimum formula. Unimodality alone does not imply that simplification.
