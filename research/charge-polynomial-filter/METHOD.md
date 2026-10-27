# Exact finite scalar classification

This is an author-checked finite computation, not an all-size SAT improvement.
Fix the predecessor's row/column/output codebooks. Each normal-ordered current
contributes at most one power of q, so Q_s^q has degree at most
length(mu)+length(nu). The polynomial recurrence lifts the pinned integer-
charge recurrence over Z[q], coefficient by coefficient. Vandermonde
interpolation shows that its coefficient tensors span exactly the linear
combinations of all rational charge evaluations at fixed s.

For a requested cutoff T, retain only coefficient tensors with |s|>T. Their
scalar-output linear constraints require every off-diagonal y/u entry to vanish
and every y=u block to equal the first diagonal block. These conditions are
necessary and sufficient for a tensor G(x,v)[y=u]. The exact integer echelon
algorithm computes the complete rational nullspace. Each nullvector yields a
label matrix G. A further exact row selection gives a basis of the entire
resulting label-matrix space.

At N<=4 compute the determinant polynomial of a generic linear combination of
that basis using the full Leibniz expansion. If it vanishes identically, every
scalar pairing in this finite space is singular. If it is nonzero, specialize
its variables one at a time to values in 0,...,N while keeping the remaining
polynomial nonzero. A polynomial of degree at most N cannot vanish on that
entire grid unless it is zero. This constructs an explicit invertible G, and
its inverse on x alone gives an actual crossing. The checker verifies the
combined tensor and normalized crossing at every entry.

A charge coefficient is a linear combination of D+1 evaluations. Each
directional rank is therefore at most D+1 times the source bound for that
shift. Here D=O(h)=poly(lambda), so the extra shared-bit charge is O(log h),
provided a uniform large-capacity interval filter were eventually proved. The
local normalization preserves both ranks. The finite checker caps ranks by N
squared and records the actual finite bound; it does not report a conditional
asymptotic ratio as an achieved algorithm.

## Raw charge results

The original registered raw-charge results were:

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

The later all-cutoff control strengthens this finite boundary: at lambda=2 the
raw space also has invertible pairings at cutoffs 3 and 4, while cutoff 5 is
identically singular. `generalized.py` reproduces the decisive cutoff-4/5
comparison. Positive cases are exact finite crossing constructions. Negative
cases cover every linear combination in the stated finite space.

## Inverse-length contraction deficits

The next registered premise rescales each raw entry by
`q^(-length(mu)-length(nu))` before taking charge combinations, using q!=0.
This is a local diagonal change on x and v, so both ranks are preserved at
each charge. With z=1/q it becomes a polynomial whose coefficient of z^e is
obtained by reindexing the raw coefficient d via
`e=length(mu)+length(nu)-d` separately at each label pair.

`deficit.py` classifies every cutoff. At lambda=2 its invertible cases extend
through cutoff 3, with cutoff 4 singular; at lambda=1 they extend through
cutoff 4, with cutoff 5 singular. Thus this inverse-length space does not
improve the completed raw finite boundary at lambda=2.

## Length-amplified charge: the improved finite witness

`generalized.py` changes the local premise in the opposite direction:

```math
 Q_s^(q)(mu,nu)\longmapsto q^{length(mu)+length(nu)}Q_s^(q)(mu,nu).
```

For q!=0 this is again an invertible diagonal change on each label pair. The
new degree `d+length(mu)+length(nu)` coefficient is just the raw degree-d
coefficient. At lambda=2,h=6, the complete scalar span has:

| Family | Cutoff | Matrix-space dimension | Full-rank pairing |
| --- | --- | --- | --- |
| raw | 4 | 10 | yes |
| raw | 5 | 6 | no |
| length-amplified | 5 | 7 | yes |
| length-amplified | 6 | 5 | no |

The amplified cutoff-5 witness removes every shift `-5,...,5`, two more
shifts than the completed raw boundary. It checks all 256 normalized crossing
entries. Its 25 active coefficient pieces have a recorded finite shared-bit
upper bound of 8, with coefficient-rank inflation at most `2D+1=23`. The
cutoff-6 determinant polynomial is identically zero, covering the whole
amplified scalar matrix space rather than only individual basis matrices.

Neither finite boundary extrapolates to every grade or codebook. A uniform
selector, leading label/output capacity and an all-size existence proof remain
essential. No smaller rho, larger alpha or selected-result change is claimed.
