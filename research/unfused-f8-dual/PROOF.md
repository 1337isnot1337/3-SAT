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

We show that no such target-pairing certificate exists for `1 <= b <= 8`. This is only a
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

## Seven-macro symmetry reduction

For b=7, exact enumeration gives 1,800 eligible types. The largest
ineligible and smallest eligible type sizes are respectively `840*7^7`
and `1260*7^7`. The checker compares these with the threshold using
`(840*7^7)^2 < 2^59`, `59/2 < 21 sqrt(2) < 149/5`, and
`(1260*7^7)^5 > 2^149`. Thus no type is ambiguously classified.

Frobenius `(A,B) -> (A^2,B^2)` and swap `(A,B) -> (B,A)` preserve the
trace symplectic form, the target and the cardinality of every type. They
commute and generate a six-element group. Therefore if a real
self-Fourier seed supported on eligible types has nonzero target pairing,
its group average is another such seed and has the same nonzero pairing.
It suffices to rule out group-invariant seeds. The eligible types form 399
group orbits. The checker constructs the 399 orbit-sum polynomial columns
and `T-8^7 I`, checks that the output rows agree on each orbit, and keeps
one representative of each of 2,714 output orbits. The resulting integer
matrix has column rank 399 modulo the prime 65,521. Thus no nonzero
invariant seed exists over the reals, and averaging excludes any seed with
nonzero target pairing, even without an invariance assumption. NumPy is used
only for exact signed 64-bit modular arithmetic, whose products stay below
`2^63`; the script checks this bound and primality.

## Eight-macro frozen minor

At b=8 there are 24,310 types, of which exactly 6,345 exceed the strict
threshold. The neighboring type sizes are 14,527,298,520 and
16,602,626,880; the checker certifies their classification with
`1697/50 < 24 sqrt(2) < 679/20`, together with
`14527298520^50 < 2^1697` and `16602626880^20 > 2^679`.

The same six-element group reduces the eligible types to 1,382 input
orbits, and all types to 5,594 output orbits. The replay constructs the
integer `T-8^8 I` orbit-sum columns modulo 65,521. The saved list of 1,382
output rows identifies a square minor; exact modular elimination gives a
nonzero pivot in each column, proving full column rank. It follows by the
same averaging argument that no eligible positive-eigenvalue seed has a
nonzero target pairing. Twenty entries of the constructed matrix are also
compared with a separate direct, target-pruned coefficient recurrence.

The C++ builder stores coefficients in signed 64-bit integers: the sum of
absolute coefficients of each local transformed row is at most 64, so any
individual degree-eight coefficient has absolute value at most `64^8`, and
an orbit sum is at most six times that, safely below `2^63`. The NumPy
elimination reduces modulo the prime at each step, with products below
`2^63`. This computation checks a specified finite minor; the 20 controls
are not a complete independent implementation of the whole matrix.

This establishes the stated b<=8 limit, including arbitrary real
coefficients. It neither constrains negative-eigenvalue or asymmetric
certificates, nor certificates without a uniform type floor, nor b>=9.
The computation is a bounded exact rank check, not a proof by extrapolation.

## Next work and cost boundary

Explore b>=9 with a structural or symmetry-reduced exact linear system;
first establish feasible time and memory before materializing all types.
Alternatively change the support-dual method or exhibit actual pieces with
proved two-sided support bounds. A successful finite dual would still need
the tensorization argument and independent review. A constructive route
must separately pay piece count, uniform factor generation, coefficient
heights, both cut ranks, recursion, query encoding and recovery. This screen
provides none of those SAT algorithm costs and makes no alpha claim.
