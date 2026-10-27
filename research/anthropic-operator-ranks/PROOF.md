# A first-moment relation and one fewer operator piece

Status: author-checked, AI-assisted mathematical argument. The finite checker
is separate from this all-size proof. No independent or formal review and no
improvement in alpha is claimed. The source is Anthropic's versioned
[paper](https://hexagonmath.org/2610.00577v1), pinned offline in
[SOURCES.json](SOURCES.json), particularly `eq:two-orders`, the paragraph
"One Laurent polynomial", `eq:Q`, and `thm:halfpieces`.

## 1. The operator relation

Let V_E be the weight-E subspace of Q[t_1,t_2,...], and let the operators
and Q_s(a,b) be exactly those in Appendix B. Here b is homogeneous of
weight h>=1, and a has weight at most h, as required by that construction.
Then as an operator on V_E,

```math
 \sum_{s=-E-h}^{E+h}s\,Q_s(a,b)=0.
 \tag{1}
```

The sum is finite because Q_s=0 outside the stated range. The assertion is
linear in a and b. It therefore suffices to take a=t^mu of weight h'<=h
and b=t^nu of weight h. Put H=h'+h, and fix two partitions sigma,sigma'
of E. Use the matrix coefficient notation
`<X> = [t^sigma] X t^sigma'` from the source.

The basic operators are multiplication by t_k and k*d/dt_k; their
commutator is k when the indices match and zero otherwise. Commuting
annihilations past creations therefore expands a product of the two
vertex operators into partial contractions. This is the source's
`eq:two-orders` calculation, performed coefficientwise at finite energy.
After multiplication by (w_1-w_2)^H, its two expansions define the same
Laurent polynomial F(w_1,w_2). In the notation of that calculation,

```math
 F=\mu!\nu!\sum
   \Gamma_{\mu',\nu'}(w_1-w_2)^r n_{\mu'',\nu''},
 \quad r=|\mu''|+|\nu''|,
 \quad \mu'\sqcup\mu''=\mu,\ \nu'\sqcup\nu''=\nu.
 \tag{2}
```

The uncontracted normal-ordered coefficient n is Laurent polynomial;
each part records the positive weight of an uncontracted field. If
r=0, it is the constant `[sigma=sigma']`, and that summand of F is
constant. If r=1, the uncontracted parts consist of exactly one part
of size one. That coefficient is the matrix element of a single
current J_1^+(w_j)+J_1^-(w_j) for j=1 or 2. Every term of this current
is one creation or annihilation with a nonzero index. It changes
energy, so its matrix coefficient between two weight-E vectors is
identically zero. There is no zero-index operator in this module.

All remaining terms in (2) have r>=2. Consequently, in the Laurent
polynomial ring,

```math
 F(w_1,w_2)-F(1,1)\ \text{is divisible by }(w_1-w_2)^2.
 \tag{3}
```

The source's coefficient reading gives
`F=sum_s <Q_s(a,b)> w_1^s w_2^(-s)`. Apply w_1*d/dw_1 and evaluate
at (1,1). Equation (3) makes that derivative zero; the coefficient
reading makes it `sum_s s <Q_s(a,b)>`. This proves (1) for every
matrix entry on V_E. Finally sum the homogeneous components of a:
the binomial weights in its a^{<i>} are exactly the componentwise
weights used in this argument. No analytic convergence or division
modulo a prime is involved.

## 2. One fewer piece with the same denominator

Use exactly the Appendix-B encoded states at energy h and its tensors
A_s, s=-2h,...,2h. They have integer entries, both integer
factorizations, and
`sum_s A_s = h! [x=v][y=u]`. Equation (1) at E=h gives
`sum_s s A_s=0`. Define

```math
 A'_s=(1-s)A_s,\qquad s\in\{-2h,\ldots,2h\}\setminus\{1\}.
 \tag{4}
```

Then

```math
 \sum_{s\ne1}A'_s=h![x=v][y=u].
 \tag{5}
```

There are 4h pieces instead of 4h+1, and the integer denominator h!
does not change. Negative entries are allowed by the source's piece
contract. Multiplying one factor in each row/column factorization
by (1-s) preserves integrality and the number of shared bits. This
coefficient is nonzero on every retained piece, so each flattening
rank is also unchanged. Its magnitude is at most 2h+1: integer bit
heights increase by only O(log h), and evaluation adds one integer
multiplication. Listing the pieces and their descriptions remains
uniform in lambda with the same asymptotic budgets.

This is a component reduction in the number of pieces. In a step with
R rectangles, the corresponding raw enumeration count changes from
(4h+1)^R to (4h)^R; the bound on every summand is preserved up to
the polynomial bit overhead already allowed. The worst shared-bit
parameter rho=1/sqrt(2), grouping, recursion and arbitrary-density
logarithm remain unchanged. There is no new full asymptotic envelope
or alpha, and the source theorem as a whole is not independently
verified by this consequence of its operator definitions.

## 3. Exact finite ranks and the limit of scalar reweighting

The checker computes every piece at lambda=1,2,3, using the minimal
h and the source's lexicographically first 2^lambda partitions. It
checks the two operator orders as full integer output vectors, the
crossing identity, (1), and (5). The formal intermediate-space counts
are explicit upper bounds; a modular rank is used as an exact
certificate only when it meets such an upper bound. Every unmatched
case is resolved by rational elimination.

For any one finite case where the span of the 4h+1 tensors has rank
4h, relation (1) spans its entire relation space. Every scalar
reweighting with the same sum therefore has coefficients
`c_s=1+t*s` for one rational t. In particular c_0=1, and at most one
coefficient can vanish. Thus (4) is optimal in the number of retained
pieces within scalar reweightings of those fixed tensors, while the
central piece cannot be removed by such a reweighting.

This last optimality conclusion is asserted only for the finite
cases where the checker certifies span rank 4h. It does not prove an
all-h independence result, restrict a change of the pieces, or turn
the finite ranks into an asymptotic lower bound.
