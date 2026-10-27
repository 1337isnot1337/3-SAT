# A rank-preserving rational stress family

For N=2^lambda, let B=2I-S_N, where S_N is the upper shift matrix.
Its inverse has entries `B^-1(a,b)=2^-(b-a+1)` for b>=a, and zero
otherwise. In particular the top-right denominator is 2 to the power N.
Both B and its inverse can be generated in `2^O(lambda)` bit time;
their exact output bit lengths need not be polynomial in lambda.

Given any rational crossing family, set

```math
 A'_i(x,y,u,v)=\sum_{a,b}B_{x,a} A_i(a,y,u,b)(B^{-1})_{b,v}.
```

The sum over i remains d times the crossing because B B inverse=I
on the x,v pair and the y,u identity is untouched. Each of the two required
flattenings is multiplied by invertible matrices on its separate row and
column axes. Its rational rank is therefore exactly preserved. Uniform
entry evaluation still takes `2^O(lambda)` bit time: at most N squared
terms, each with `2^O(lambda)` bits. This is a change of local basis,
not a new rank bound.

Large dyadic denominators really can occur. For example the crossing
subtensor `P(x,y,u,v)=[x=0][v=0][y=u]` transforms to
`P'(x,y,u,v)=[x=0][y=u] 2^-v`. Its coefficient at v=N-1 has denominator
`2^(N-1)`. Both flattening ranks of P and P' are N. If a stress example
within a given crossing decomposition is desired, add P and -P before
conjugation. This keeps its sum unchanged and adds two pieces with combined
support bits 2 lambda, which meets every rho>=1/2 bound. This cancelling
pair is only a coefficient-height control, not a source of a faster algorithm.
It shows why coefficient height and rank are separate constraints.

The actual bounded checker uses the predecessor's four nontrivial pieces,
not that artificial pair. It computes their original and conjugated exact
crossing sums at N=8, both modular rank factorizations, and all 256 Boolean
assignment-predicate counts. The largest observed denominator is 2^9.
This finite value is reported literally; the all-size inverse and projection
formulas above, rather than extrapolation from nine, show the possible
exponential denominator growth.

This exercise tests the rational interface and normalization. It cannot
improve rho, since invertible local changes preserve both ranks. Existing
symmetry barriers are not invalidated by this representation change.
All text and computations are Codex-assisted and await independent review.
