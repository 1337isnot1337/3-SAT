# Certificate floor under unfused F8 classes

## Setup and inherited certificate

Work in the Pauli/Walsh setting of the predecessor, and retain global macro
permutation symmetry. Identify a three-bit macro label with `(A,B)` in
`F_8^2`, using the trace-dual identification for the second coordinate.
The ten classes are `(0,0)`, `(0,B!=0)`, `(A!=0,0)`, and seven classes
`AB=t` for each nonzero t. Their sizes are 1 and nine copies of 7. The
quadratic target is `(-1)^Tr(AB)` and the symplectic Walsh transform closes
on these classes. The checker constructs its character table from all 64^2
characters and checks its square and target eigenvalue 8.

Fusing product classes in Frobenius orbits gives the predecessor's six
classes. Its four-macro dual is constant on the finer types as well; the
function and its Fourier eigenidentity and target pairing are unchanged.
However, a fused type is a union of finer types. Enumerating the lift of
its 27 supported types shows minimum *finer* type cardinality 2,401. Since
`2401=7^4 < 2^12 < 2^(12 sqrt(2))`, the floor supplied by the old seed
cannot meet the strict rate condition. This says nothing about other duals.

## The finite-block criterion

A b-macro self-Fourier dual h with nonzero target pairing and every
supported type of cardinality at least W gives, via the predecessor's
averaging/tensorization lemma, a lower bound `2 floor(R/b) log2 W` on
combined support bits for some same piece. With `lambda=3R`, a strict
obstruction to `2 sqrt(2) lambda + O(log lambda)` requires

```math
 W > 2^{3b\sqrt 2}.
```

We show that no such certificate exists for `1 <= b <= 6`. This is only a
necessary condition for a strict obstruction *using this single-seed floor
argument*; it is not a necessary condition for any other kind of proof.

For a type `alpha`, its cardinality is
`b! / product(alpha_i!) * product(w_i^alpha_i)` with local weights
`w=(1,7,...,7)`. Exact enumeration of all types gives maxima for b=1,...,6:

```
7, 98, 2058, 57624, 2016840, 84707280.
```

For b<=5 each maximum is less than `2^floor(21b/5)`, and `7/5<sqrt(2)`.
Thus no type meets the required floor. At b=6, the only types that can
exceed `2^(18 sqrt(2))` have six distinct nonzero classes: any other type
has cardinality at most `360*7^6`. Indeed
`(360*7^6)^5 < 2^127`, and `127/5 < 18 sqrt(2)`. Each of the 84 distinct
six-class choices has size `720*7^6 > 2^26 > 2^(18 sqrt(2))`.

## Six-macro exact rank

Let C be the ten-class compressed Walsh character table. For a candidate
input type alpha, form the coefficient polynomial
`product_i (sum_j C_ij z_j)^alpha_i`. These 84 polynomials are the columns
of the induced transform in *weighted type-polynomial coordinates*; the
correspondence takes h(alpha) to `size(alpha) h(alpha)`. Subtract `8^6`
on each column's own coordinate. This produces an integer matrix with 84
columns and 5,005 degree-six type rows. The checker computes row rank 84
modulo the prime 1,000,000,007, after generating C directly from the
characters. A nonzero integer minor modulo a prime is nonzero over the
rationals and reals, so the kernel is zero. Therefore there is no nonzero
positive-eigenvalue dual supported only on those 84 types; in particular
none has a nonzero target pairing.

This establishes the stated b<=6 limit, including arbitrary real
coefficients. It neither constrains negative-eigenvalue or asymmetric
certificates, nor certificates without a uniform type floor, nor b>=7.
The computation is a bounded exact rank check, not a proof by extrapolation.

## Next work and cost boundary

Explore b>=7 with a structural or symmetry-reduced exact linear system;
first establish feasible time and memory before materializing all types.
Alternatively change the support-dual method or exhibit actual pieces with
proved two-sided support bounds. A successful finite dual would still need
the tensorization argument and independent review. A constructive route
must separately pay piece count, uniform factor generation, coefficient
heights, both cut ranks, recursion, query encoding and recovery. This screen
provides none of those SAT algorithm costs and makes no alpha claim.
