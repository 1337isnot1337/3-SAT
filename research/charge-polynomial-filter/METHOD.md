# Exact finite scalar classification

This is an author/Codex checked finite computation, not an all-size SAT
improvement. Fix the predecessor's row/column/output codebooks. Each
normal-ordered current contributes at most one power of q, so Q_s^q has
degree at most length(mu)+length(nu). The polynomial recurrence lifts the
pinned integer-charge recurrence over Z[q], coefficient by coefficient.
Vandermonde interpolation shows that its coefficient tensors span exactly
the linear combinations of all rational charge evaluations at fixed s.

For a requested cutoff T, retain only coefficient tensors with |s|>T.
Their scalar-output linear constraints require every off-diagonal y,u
entry to vanish and every y=u block to equal the first diagonal block.
These conditions are necessary and sufficient for a tensor G(x,v)[y=u].
The exact integer echelon algorithm computes the complete rational
nullspace. Each nullvector yields a label matrix G. A further exact row
selection gives a basis of the entire resulting label-matrix space.

At N<=4 compute the determinant polynomial of a generic linear combination
of that basis using the full Leibniz expansion. If it vanishes identically,
every scalar pairing in this finite space is singular. If it is nonzero,
specialize its variables one at a time to values in 0,...,N while keeping
the remaining polynomial nonzero. A polynomial of degree at most N cannot
vanish on that entire grid unless it is zero. This constructs an explicit
invertible G, and its inverse on x alone gives an actual crossing. The
checker verifies the combined tensor and normalized crossing at every entry.

This test concerns the whole matrix space, not just its individual basis
matrices. A control has two singular diagonal basis matrices with an
invertible sum; another space is identically singular. Additional scalar
substitutions compare the symbolic determinant with rational elimination.
No randomized determinant oracle is used by this bounded classification.

A charge coefficient is a linear combination of D+1 evaluations. Each
directional rank is therefore at most D+1 times the source bound for that
shift. Here D<=2h=poly(lambda), so the extra shared-bit charge is O(log h),
provided a uniform large-capacity interval filter were eventually proved.
The local normalization preserves both ranks. The finite checker caps ranks
by N squared and records the actual finite bound; it does not report a
conditional asymptotic ratio as an achieved algorithm.

The first registered raw-charge results are:

| lambda | h | Removed shifts | Label matrix-space dimension | Invertible pairing |
| --- | --- | --- | --- | --- |
| 1 | 4 | abs(s)<=0 | 4 | yes |
| 1 | 4 | abs(s)<=1 | 4 | yes |
| 1 | 4 | abs(s)<=3 | 4 | yes |
| 1 | 4 | abs(s)<=7 | 0 | no |
| 2 | 6 | abs(s)<=0 | 16 | yes |
| 2 | 6 | abs(s)<=1 | 16 | yes |
| 2 | 6 | abs(s)<=2 | 15 | yes |
| 2 | 6 | abs(s)<=5 | 6 | no |
| 2 | 6 | abs(s)<=11 | 0 | no |

Unlisted cutoffs are not classified by this report. Positive cases are
exact finite crossing constructions. Negative cases cover every linear
combination of charge values on that particular finite codebook and cutoff.
Neither is extrapolated to every grade, every codebook or every SAT algorithm.

Uniform scalar interval filters remain open. Symbolic determinant expansion
is not claimed to take 2^O(lambda) for arbitrary N. A future uniform selector
needs an explicit identity or a separately paid randomized construction.
Sources and all predecessor credit are in SOURCES.json and REGISTERED.md.
