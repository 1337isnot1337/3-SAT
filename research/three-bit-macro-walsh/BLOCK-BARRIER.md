# A finite-block certificate gives an all-size obstruction

## The certificate

Use the six-class table and weights from
[SCHEME-REFINEMENT.md](SCHEME-REFINEMENT.md). For four macros there are
126 types. The integer type function h listed in
[four-block-dual.json](four-block-dual.json) has 27 nonzero values. Direct
integer multiplication by the four-fold compressed transform gives

```math
 T_4h=8^4h,\qquad
 \langle h,q_4\rangle_m=17\,948\,262\,528\ne0.
```

Every supporting type has at least W=129654 actual Pauli words, and the
minimum is attained. These are weighted word counts, not counts of types.
[certificate.py](certificate.py) checks these identities directly from
the frozen vector, without running the search or adapted-basis algorithm.

## Tensorization lemma

More generally, let a closed finite class scheme on an alphabet of size
N squared have a self-adjoint Fourier transform with square N squared,
positive-eigenvalue target q, and positive local class sizes. Suppose a
class-type-constant function h on b macros satisfies

1. its Fourier transform is N to the power b times h;
2. its pairing with the target is nonzero;
3. every supporting b-macro type has at least W actual words.

For R=bt+s with 0<=s<b, form h tensor-powered t times, tensor q on the
remaining s macros, and average over all R macro permutations. Call the
result H_R. Permutations commute with the Fourier transform, so H_R is
self-Fourier with eigenvalue N to the power R. Its target pairing is
the t-th power of the seed pairing times the positive squared norm of
q_s, so it is nonzero even when coefficients cancel under averaging.

Every type supporting H_R contains a concatenation of t supporting seed
types and one remainder type. The whole R-macro type contains the Cartesian
product of their separate block orbits. Its word cardinality is therefore
at least the product of the block cardinalities, hence at least W to the
power t. Averaging can remove support but cannot introduce a smaller type.

Now take any decomposition q_R=sum_i f_i into functions constant on the
global macro types. If f_i has fewer than W to the power t supporting
words, it vanishes on every type supporting H_R and pairs to zero with it.
If its Fourier transform has fewer than that many supporting words, the
same conclusion follows from self-adjointness and the eigenidentity for
H_R. Some same summand must have nonzero pairing, since their sum does.
That summand consequently has BOTH word supports at least W to the power t.

This permits any finite number of summands, arbitrary characteristic-zero
coefficients, and cancellations. It applies to every macro-type-constant
decomposition, not merely to the adapted basis used in the screen. The
permutation symmetry between all R macros is essential to this lemma.

## Strict separation from the target rate

Here b=4, N=8 and lambda=3R. Thus some piece has combined support-bit cost

```math
 c_{\rm row}+c_{\rm col}
 \ \ge\ 2\lfloor R/4\rfloor\log_2(129654)
 =\tfrac12R\log_2(129654)-O(1).
```

All comparisons needed for strict separation can be certified by integers:
`129654^100 > 2^1698` and `(1698/400)^2 > 18`. Hence
`log2(129654)/4 > 3 sqrt(2)`. The lower rate is strictly above
`6 sqrt(2) R`, by a linear amount that cannot be absorbed by O(log R).
In the convention `c_row+c_col <=4 rho lambda+O(log lambda)`, the necessary
rho is at least `log2(129654)/24`, approximately 0.707679, above
`1/sqrt(2)`, approximately 0.707107.

The six-class, three-bit macro family is therefore closed as a route to
the target crossing-piece rate, including every choice of basis and every
number of pieces within that family. This is an all-size proof from an
exact finite certificate, not a regression on the screen results. It is
not a lower bound for arbitrary Pauli functions, less symmetric functions,
arbitrary crossing tensors, or SAT algorithms.

## Search scope and changed premise

The search checked b=1,...,5. Its maximal minimum-type thresholds were
7, 294, 3087, 129654 and 1512630. Only the four-macro certificate is used
for the theorem above; larger b is unnecessary. It was found by projecting
small-type coordinate vectors into the positive Fourier eigenspace, adding
them in increasing type-cardinality order, and testing when their span
first contains q. An exact annihilating functional at the preceding step
gives the dual. The search output and code are retained for provenance;
the frozen certificate is independently checked by a separate code path.

Do not extend the unchanged six-class screen. A next construction must
change its class invariance, its global macro permutation symmetry, or the
Pauli-diagonal representation. A lower-symmetry candidate still needs the
full polynomial piece count, uniform integer factors and cost composition.

All proof text and checks are substantially AI-assisted and author-checked.
No independent reviewer or formal proof is claimed.
