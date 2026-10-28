# An entropy-amplified dual for the unfused F8 scheme

This is an author-checked, substantially AI-assisted argument. The finite
certificate has an exact replay; no independent or formal review is claimed.
We use the Pauli support identities and finite-block dual construction of
[the predecessor](../three-bit-macro-walsh/BLOCK-BARRIER.md).

## Statement

Let a three-bit macro label be `(A,B)` in `F_8^2`, using the trace-dual
coordinate for B, and classify it by `(0,0)`, the two nonzero axes, or
one of seven nonzero products `AB`. The class sizes are 1 and nine copies
of 7. Let `q(A,B)=(-1)^Tr(AB)`. On R macros, let `q_R` be the product
of q, and allow any finite decomposition `q_R=sum_i f_i` where each
function is constant on the ten-class macro types. The Walsh transform is
the unnormalized symplectic transform on the `64^R` labels.

For some same summand, both `|supp(f_i)|` and `|supp(hat f_i)|` are at least

```math
 \frac{196036848^{\lfloor R/6\rfloor}}{(R+1)^{10}}.
```

Consequently its combined support-bit cost is at least

```math
 \tfrac R3\log_2(196036848)-O(\log R).
```

In the predecessor's convention `lambda=3R` and
`c_row+c_col <= 4 rho lambda+O(log lambda)`, any such decomposition
requires `rho >= log2(196036848)/36 = 0.76518... > 1/sqrt(2)`. Thus this
family cannot improve the target crossing-piece rate. It remains possible
that a less symmetric or non-Pauli construction succeeds; this is not a
SAT lower bound or an improvement of the selected SAT algorithm.

## Exact seed

For a type `alpha` of four macros write `m_alpha` for the number of actual
label words with that type. Define the weighted polynomial of a type
function h by `P_h(z)=sum_alpha m_alpha h(alpha) z^alpha`. The frozen
[seed](seed.json) gives 48 integer orbit values under simultaneous
Frobenius and axis swap; its expansion P has 140 nonzero types.

The local ten-class character table C is reconstructed by the verifier
from all 4,096 label characters. Under the substitution
`z_i -> sum_j C_ij z_j`, the weighted type polynomial is transformed into
the weighted polynomial of the Walsh transform. The verifier computes

```math
 P(Cz)=8^4 P(z),\qquad P(q)=192.
```

Hence `hat h=8^4 h` and `<h,q_4>=192`. All supporting types have no zero
class and have multiplicity patterns `(1,1,1,1)` or `(2,1,1)`. The
integer P coefficients are weighted values `m_alpha h(alpha)`, not the
values h(alpha); the verifier includes an intentionally incorrect
normalization as a negative control. The seed was found by exact rational
linear algebra after a modular screen; the replay does not run that search.

## Optimal floor for this four-macro seed method

The same verifier checks that the seed's entropy floor is best possible
among positive-eigenvalue four-macro seeds with nonzero target pairing.
A type containing the size-one zero class has `2^(4F) <= 4^4*7^3 = 87808`.
If no zero class occurs, the only pattern with larger entropy than the
seed floor 153664 is four distinct nonzero classes. These 126 types form
33 orbits under Frobenius and axis swap. The verifier constructs their
33 orbit-sum columns of `T-8^4 I` and finds full column rank modulo the
prime 65,521. Thus no nonzero invariant positive-eigenvector is supported
there. Averaging any hypothetical target-pairing seed over the group
preserves its pairing, support condition and eigenidentity, so it would
produce such a nonzero invariant vector. This optimality statement is
specific to four-macro seeds and this minimum-entropy proof; it does not
bound stronger seeds at other block sizes or other proof methods.

## Five-macro comparison

The same minimum-entropy method cannot improve the above floor using a
five-macro target-pairing seed. For a five-type alpha, compare its entropy
to the four-macro floor by the exact rational test

```math
 \left(5^5 7^{5-\alpha_0}/\prod_i\alpha_i^{\alpha_i}\right)^4
 > 153664^5.
```

There are exactly 1,008 qualifying types, forming 245 symmetry orbits.
On their orbit-sum columns of `T-8^5 I`, the target-pairing row is an
explicit rational combination of 225 output rows. The frozen relation
[five-relation.json](five-relation.json) stores these coefficients as
integers over a common positive denominator. [five.py](five.py) constructs
the character polynomials afresh and verifies every one of the 245 exact
integer equations; it does not rely on the modular search used to find the
relation. Thus every invariant eigenvector supported on the qualifying
types has zero target pairing. Averaging rules out any target-pairing
seed with a larger minimum entropy, as above. This comparison covers
five-macro seeds for this method, not other block sizes or methods.

## Entropy tensorization

For a type fraction p on k classes of local sizes `w_i`, define

```math
 F(p)= -\sum_i p_i\log_2 p_i + \sum_i p_i\log_2 w_i,
```

with `0 log 0=0`. F is concave and nonnegative. The number of words of
type `R p` obeys

```math
 |T_{Rp}| \ge (R+1)^{-k} 2^{R F(p)}.                 \tag{1}
```

For completeness, set the multinomial distribution's probabilities to p.
The type Rp is a most likely type: moving one occurrence from a coordinate
above its prescribed count to one below it never reduces its probability.
There are at most `(R+1)^k` types, so its probability is at least that
reciprocal. Divide by its per-word probability and multiply by the local
class sizes to obtain (1). This also handles zero p coordinates.

Write `R=4t+s`, `0<=s<4`. Take h tensor-powered t times with `q_s` on the
remaining macros, and average over all R macro permutations. Call the
result H. As in the predecessor, H has Fourier eigenvalue `8^R` and
nonzero pairing `192^t 64^s` with q_R. Each supporting global type is a
sum of t supporting seed types and a remainder type: symmetrization or
cancellation cannot introduce any other types.

For every seed type alpha, `p=alpha/4` has

```math
 2^{4F(p)}=4^4 7^4 / product_i(alpha_i^alpha_i) >= 153664.
```

By concavity, and using `F>=0` for the remainder, every supporting global
type has `R F(p_global) >= t log2(153664)`. With k=10, (1) gives the
four-macro lower bound `153664^t/(R+1)^10` on its size. Since H is
constant on global types, if f has fewer supporting words it has zero
pairing with H. The same holds
if hat f has fewer, by self-adjointness of the Walsh transform and
`hat H=8^R H`. Some summand must pair nontrivially with H, proving the
simultaneous two-support bound for that same summand.

Finally, `153664 > 2^17` and `17^2>288` imply
`log2(153664)>12 sqrt(2)`, proving a strict gap from the target. This
argument is stronger than simply multiplying the minimum finite-block
type cardinality: the multinomial factor from global averaging is paid
explicitly, with only a polynomial loss.

## Stronger six-macro seed

A second [frozen seed](six-seed.json) strengthens the same argument. It is
an integer weighted type polynomial with 467 nonzero Frobenius/swap orbit
coefficients. Its exact target pairing is `4,601,640,960`, and its Walsh
eigenvalue is `8^6`. Every supporting type alpha satisfies

```math
 2^{6 F(\alpha/6)} = 6^6 7^{6-\alpha_0} / \prod_i \alpha_i^{\alpha_i}
 \ge 196036848.
```

The separate [six.py](six.py) replay constructs the 10-class character
table from the underlying labels, enumerates all 5,005 types, and generates
the integer self-Fourier constraints in 1,234 output orbits. The C++17
builder checks character-table equivariance under the six-element group;
its columns are orbit sums, so one representative per output orbit suffices.
The replay checks every output-orbit equation and the target pairing in
arbitrary-precision Python arithmetic, and compares 20 matrix entries with
a separate target-pruned coefficient recurrence. The six-macro search was
modular followed by an exact rational reconstruction; the certificate replay
does not assume that search.

The builder's intermediate coefficients fit signed 64 bits: every local
row has absolute coefficient sum at most 64, so a six-fold polynomial
coefficient is bounded by `64^6`, and an orbit sum by six times that plus
`8^6`. The seed multiplication is done in Python integers. Substituting
this seed into the same tensorization proof, with `R=6t+s`, gives the
stronger bound in the statement. Strictness follows from
`196036848 > 2^27` and `27^2>648`, so its logarithm exceeds `18 sqrt(2)`.
The floor is optimal among six-macro target-pairing seeds for this
minimum-entropy method. The types with strictly greater entropy form 485
input orbits. The replay checks an explicit exact rational combination of
477 output rows equal to the target-pairing row on every one of those
orbits; see [six-relation.json](six-relation.json). Therefore an invariant
seed supported there must pair to zero, and the group-average argument
extends the conclusion to arbitrary seeds. This is a six-macro statement,
not optimality among other block sizes or other proof methods.

## Extension to separate macro groups

Partition the R macros into K nonempty, labelled groups of sizes
`R_1,...,R_K`. Suppose each piece is constant on ten-class types *within
each group*; different groups may have different type functions. Tensor
one copy of the preceding H construction for each group. The resulting
H is constant on the tuple of group types, has eigenvalue `8^R`, and has
nonzero target pairing. Its supporting group-type tuples have cardinality
at least the product of their respective group bounds. Therefore some
same piece has both supports at least

```math
 B=\frac{196036848^{\sum_j\lfloor R_j/6\rfloor}}
          {\prod_j(R_j+1)^{10}}.
```

The argument again permits arbitrary real coefficients and any finite
number of pieces. Put `L=log2(196036848)`. Since
`sum floor(R_j/6) >= (R-5K)/6` and concavity of log gives
`sum log2(R_j+1) <= K log2(1+R/K)`, the bit-cost lower bound is

```math
 (L/3)R - (5L/3)K - 20K log_2(1+R/K).
```

For any sequence of partitions with `K=o(R)`, its error term is `o(R)`
and the asymptotic bound in the statement holds. It also yields a concrete
linear-group allowance. If `K <= R/340`, then the bit cost is at least
`(17/2)R`, strictly above `6 sqrt(2) R`. Indeed
`2^(55/2) < 196036848 < 2^28` and `log2(341)<9`, so the lower bound is
at least `(55/6 - (140/3+180)/340)R = (17/2)R`. The function
`K log(1+R/K)` increases in K, so this also holds for every smaller K.
The comparisons are exact: `196036848^2 > 2^55` and `17^2 > 288`.
This does not cover arbitrary functions with unrestricted linearly many
independent groups.

## Boundary and next premise

The proof assumes type symmetry inside each of a common partition
into `o(R)` macro groups (or at most `R/340` groups) and constancy on
the ten named local classes, and the Pauli-diagonal coefficient model. The
one-group result is the globally symmetric special case. It allows arbitrary real coefficients, any finite number of summands and
cancellation. It does not restrict general Pauli functions or arbitrary
crossing tensors. A successor must change one of those premises. Any new
construction must still provide uniform pieces, both cut factorizations,
coefficient heights, recursion and all outer costs. Independent proof and
certificate review remain open.
