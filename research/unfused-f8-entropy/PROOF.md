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
 \frac{153664^{\lfloor R/4\rfloor}}{(R+1)^{10}}.
```

Consequently its combined support-bit cost is at least

```math
 \tfrac R2\log_2(153664)-O(\log R).
```

In the predecessor's convention `lambda=3R` and
`c_row+c_col <= 4 rho lambda+O(log lambda)`, any such decomposition
requires `rho >= log2(153664)/24 = 0.71789... > 1/sqrt(2)`. Thus this
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
claimed lower bound on its size. Since H is constant on global types, if
f has fewer supporting words it has zero pairing with H. The same holds
if hat f has fewer, by self-adjointness of the Walsh transform and
`hat H=8^R H`. Some summand must pair nontrivially with H, proving the
simultaneous two-support bound for that same summand.

Finally, `153664 > 2^17` and `17^2>288` imply
`log2(153664)>12 sqrt(2)`, proving a strict gap from the target. This
argument is stronger than simply multiplying the minimum finite-block
type cardinality: the multinomial factor from global averaging is paid
explicitly, with only a polynomial loss.

## Boundary and next premise

The proof assumes global macro permutation symmetry and constancy on the
ten named local classes, and the Pauli-diagonal coefficient model. It
allows arbitrary real coefficients, any finite number of summands and
cancellation. It does not restrict general Pauli functions or arbitrary
crossing tensors. A successor must change one of those premises. Any new
construction must still provide uniform pieces, both cut factorizations,
coefficient heights, recursion and all outer costs. Independent proof and
certificate review remain open.
