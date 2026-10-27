# Moment-recovery handoff

Base: 7561c0836b94d33166fc9e0eff6e15cc160f03ef. Canonical main was
refreshed to 5b81ed7 after PR10 merged. Work stays in its own package;
the predecessor's computational files and external source are frozen.

## Established scope

- An explicit second-moment Wick pairing and an all-size author proof
  that it acts as a scalar on each fixed energy space.
- An all-size author proof that the j-th moment's third-cut rank is
  at most p(j)-1 for j>=2, via translation and zero-mode relations.
- Exact finite scalar recovery weights at lambda=1,2,3: only the
  quadratic span. A central-zero weight leaves a singular pairing.
- Exact formula-pairing ranks for h=2,...,12 agree with p(h)-p(h-2),
  but this rank pattern is not a proved uniform theorem.

None establishes an improved rho or alpha. The three-party grouping,
two required factorization cuts, entries, integer heights, recovery,
dense reduction and uniformity obligations remain. The report binds
the code and proof and checks complete tensors against PR10's hashes.

## Do not repeat unchanged

A higher moment with a small rank in `(x,v)|(y,u)` is not a solution to
the two required cuts. The crossing tensor itself is the counterexample.
The source codebooks' second pairing has no inverse in the tested cases.
Generic inversion would also need a separate bit-height argument even
if arithmetic time were permitted. The finite scalar-weight result
does not close general product recoveries or prove an all-h no-go.

## Next precise questions

1. Classify non-scalar product recoveries `B(x,v)K(y,u)` in the moment
   span. A third-cut rank-one combination with both factors invertible
   could be normalized by individual leg maps. Its coefficient heights
   and required row/column ranks would still need to fit. Initial
   lambda=1,2 probes found no rank-one `M3-c*M2`; a complete polynomial
   classification has not been run or claimed.
2. Determine the algebraic kernel of G on the full weight-h state
   space. The observed nullity p(h-2) could suggest a uniform theorem
   or an explicit different codebook, but needs a proof. Merely
   deleting one or two shifts would not change the asymptotic rho.

Before a new round or submission, fetch main, inspect live overlap,
and check changed STATE/tasks/selected result. Keep the user's earlier
failed kernel, congruence and low-degree parity routes scoped as in
the predecessor handoff. Merge permission exists for the current
campaign; archiving a package does not promote its proof or the
selected result.
