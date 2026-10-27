# Cauchy modes from a rational Newton expansion

This changes the modes in the accepted contraction, not the accepted theorem.
The all-size arguments are author-checked with substantial AI assistance;
independent review has not occurred.

## 1. An exact separable identity

Put `(z)_k=z(z-1)...(z-k+1)`, with `(z)_0=1`, and define

```math
 \phi_k(z)=\frac{\binom zk}{\prod_{h=0}^k(1-2hz)},\qquad
 c_k=2^k(k!)^2(1-2k^2).
```

For every positive integer `d` and `j in {0,...,d-1}`,

```math
 \frac1{1-2zj}=\sum_{k=0}^{d-1}c_k\phi_k(z)\phi_k(j).       \tag{1}
```

This is an identity of rational functions of `z`. In particular, it holds
in the accepted coefficient field whenever its denominators are defined.

One direct proof uses successive rank-one elimination at the pairs
`(z,j)=(k,k)`. Before eliminating pair `k`, the residual is

```math
 R_k(z,j)=\frac{2^k(z)_k(j)_k}
 {(1-2zj)\prod_{h<k}(1-2hz)\prod_{h<k}(1-2hj)}.
```

The rank-one term `R_k(z,k)R_k(k,j)/R_k(k,k)` is exactly the `k`th
summand of (1). Subtraction gives `R_(k+1)` by cancellation. The initial
residual is `R_0=1/(1-2zj)`, and `R_d(z,j)=0` at every indicated `j`.
Equivalently these residuals follow from the Cauchy determinant identity.
This proves (1) without approximation or an infinite series.

## 2. Integrality at the source's actual evaluation points

Use the source notation `L=2^a`, `alpha=2^(a+1)`, `i=v2(t)<u<=a`,
`D=L/2^i` and `T=t+alpha*zeta`, with `zeta` in its unramified valuation
ring `O`. In a column tile `y=y0+2^(i+1)j`, set `d=D/2`. Thus
`0<=j<d`, even if some of the corresponding ports are unused.

For any crossing row `x`, the source proves `v2(t-y0+x)=v<=i`. Define

```math
 b_x=T-y_0+x,\qquad z_x=2^i/b_x,\qquad
 P_x=\frac{\mathcal C(T)}{\mathcal C'(0)b_x},\qquad A=a+1-i.
```

Then `z_x` is integral. Moreover,

```math
 z_x\equiv\frac{2^i}{t-y_0+x}\pmod {2^A\mathcal O},
```

since the valuation of the difference is at least
`i+a+1-2v>=A`. The rational number on the right belongs to `Z_(2)`.
For each `k<d=2^(A-2)`, this implies `binom(z_x,k)` is integral.
Here is a proof that also applies when `zeta` has nonrational coordinates.
Choose an integer `r` congruent to that rational number modulo `2^A`.
For each `1<=b<=floor(log2 k)`, at least `floor(k/2^b)` of the factors
`z_x-h`, `0<=h<k`, are divisible by `2^b`. Hence

```math
 v_2((z_x)_k)\ge\sum_{b\ge1}\lfloor k/2^b\rfloor=v_2(k!).
```

The case `k=0` is immediate. Every denominator `1-2hz_x` is a unit,
so `phi_k(z_x)` is integral. Also `phi_k(j)` is integral for integer `j`.
An arbitrary integral element of an unramified extension need not have
integral binomial coefficients; the displayed congruence is essential.

The source's proof of `lem:tensor-integrality` gives
`v2(C(T)/C'(0))>=a+1`, so `v2(P_x)>=A`. Applying (1) gives the exact tile
identity

```math
 W_{xy}(T)=P_x\sum_{k=0}^{d-1}c_k\phi_k(z_x)\phi_k(j).    \tag{2}
```

Consequently the row coefficient of the mode
`L_k(X)=sum_(real y in tile) phi_k(j) X_y` is divisible by

```math
 2^{w_k},\qquad
 w_k=A+k+2v_2(k!)=A+3k-2\operatorname{popcount}(k).          \tag{3}
```

The source's geometric modes use the weaker guaranteed weight `k+1`,
or `A+k` when retaining the initial valuation. Equation (2) has one mode
per tile and index, with the same source and target groups. No row-residue
partition or additional tile multiplicity is needed.

## 3. Recursion interface and cost

In each row affine form use (2) for crossings and keep its local form.
Expand in formal mode variables of weights (3). Every coefficient of
`Z^beta` is divisible by `2^(sum w_k beta_k)`, because all the remaining
coefficients are integral. At child precision `p_t` retain only tuples
with `sum w_k beta_k<p_t`. The proof of
`eq:tensor-recursion-identity` now applies verbatim: each mode still has
one source group and one target group, and substitution is a linear form
on bits of the source tile. The identity is exact modulo `2^p_t`.

There are still at most `6M/D` tiles, each of size `d=D/2`. The number of
groups, packets and child wires is unchanged. In particular every child
has fewer than `M/8` wires. At most `O(M)` mode variables are introduced,
each with a polynomial-size description. There are fewer modes than the
untruncated geometric construction, rather than a new exponential family.

To evaluate `phi_k(z_x)` modulo `2^p_t`, compute the falling factorial
with `p_t+v2(k!)` bits of precision, divide its known power of two,
and invert the odd part of `k!`. All its other denominators are units.
Here `k<d<=L` and `v2(k!)<L`; the guard precision and arithmetic remain
polynomial in the source size and working precision. The original
precision passed to recursive calls does not increase. The extra bits
are used only to compute local coefficients from the specified evaluation
point. That point is the same binary-coordinate lift as in the source.

The new source linear forms have integral scalar coefficients with
polynomial-time evaluation. Coefficient extraction in a packet still
expands at most `L` affine row factors, each with polynomially many
terms. Entry work remains `exp(O(L log s))` time and polynomial space.
Creation-time canonical lifts, immutable descriptions, recovery, leaves,
all outer reductions and queries are unchanged. The modified contraction
therefore keeps the accepted complete time and polynomial-space envelopes.

## 4. The improvement in the enumeration bound

Let `c` be any positive integer upper bound on the number of tiles and
`p` the child precision. After dropping `A>=1` and extending the index
range, the number of retained tuples is bounded, for every `theta>0`, by

```math
 N\le\exp\left(\theta p+
 c\sum_{k\ge0}-\ln(1-e^{-\theta(1+3k-2\operatorname{popcount}(k))})\right).
```

As `theta` decreases to zero the sum is
`(pi^2/18+o(1))/theta`. To justify this without exchanging unbounded
errors, for each fixed `eta>0` bracket all sufficiently large weights
between `(3-eta)k` and `(3+eta)k`. The finitely many excluded terms
contribute `O_eta(log(1/theta))`. For any fixed `b>0`, the sum with
weights `bk` is asymptotic to `pi^2/(6b theta)`, by its logarithmic
series or an integrable Riemann sum. Let `eta` tend to zero.

Optimizing gives, whenever `p/c` tends to infinity,

```math
 \log N\le\left(\frac{\pi\sqrt2}{3}+o(1)\right)\sqrt{cp}. \tag{4}
```

For geometric weights `k+1`, the same generating-product argument has
coefficient `pi*sqrt(2/3)` instead. Thus (4) improves the leading
coefficient in this particular mode-count upper envelope by `1/sqrt(3)`.
The source regime has `p/c=Theta(D^2/u)` and `D>=2^u`, so the asymptotic
condition holds at every active call as the root size grows.

This is a positive constant-factor refinement of a component bound, not
a factor-of-sqrt(3) speed measurement or a comparison between unspecified
constants in the accepted big-O theorem. Inserting the unchanged precision
bound still gives `exp(O(M/sqrt(u)))`. The root still has `u=Theta(log s)`;
alpha remains `1/2` and the arbitrary-density `log log n` factor remains.

## 5. Stronger modes at every odd interpolation node

When `i=0`, crossing row and column slots have the same parity. Thus
`t-y0+x` is odd, `z_x=1/(T-y0+x)` is congruent to one modulo two, and
`(z_x-1)/2` is integral. It is congruent to a rational two-adic integer
modulo `2^(A-1)`. Since `k<d=2^(A-2)`, the same counting proof makes
`binom((z_x-1)/2,k)` integral, including at nonrational `zeta`.

Instead eliminate at row points `a_h=1+2h` and column points `h`. Put

```math
 \rho_k(z)=\frac{\binom{(z-1)/2}{k}}{\prod_{h=0}^k(1-2hz)},\qquad
 \sigma_k(j)=\frac{\binom jk}{\prod_{h=0}^k(1-2(1+2h)j)},
```

```math
 c_k^{\rm odd}=2^{2k}(k!)^2\bigl(1-2(1+2k)k\bigr).
```

Then exactly, for every `j in {0,...,d-1}`,

```math
 \frac1{1-2zj}=\sum_{k=0}^{d-1}c_k^{\rm odd}\rho_k(z)\sigma_k(j). \tag{5}
```

To verify this by the same elimination proof, replace `(z)_k` in the
residual by `prod_(h<k)(z-a_h)` and replace the factors `1-2hj` by
`1-2a_hj`. The rank-one term becomes

```math
 \frac{2^k(1-2a_kk)\prod_{h<k}(z-a_h)(j-h)}
 {\prod_{h\le k}(1-2hz)\prod_{h\le k}(1-2a_hj)}.
```

Now `prod_(h<k)(z-a_h)=2^k k! binom((z-1)/2,k)`, proving (5).
All denominators remain units. There is still one mode per tile and index,
now with coefficient valuation at least

```math
 w_k^{\rm odd}=A+2k+2v_2(k!)=A+4k-2\operatorname{popcount}(k). \tag{6}
```

Computing the row binomial variable requires one further local guard bit
to form `(z-1)/2`; no extra precision is passed to a child. All other
entry, recursion and space bounds in Section 3 are unchanged. Using (5)
at odd nodes and (2) at the other active nodes therefore gives one
uniform variant of the accepted contraction. Recovery still uses all
the original nodes and multiplicities. The odd-node mode-count envelope is

```math
 \log N_{\rm odd}\le\left(\frac\pi{\sqrt6}+o(1)\right)\sqrt{cp},
```

a factor `1/2` in the leading coefficient of the geometric envelope.
The uniform all-node guarantee remains (4); a worst-branch estimate cannot
replace it with the odd-node coefficient. Neither version changes alpha.

### Why this change alone still has the square-root scale

For a formal family with `c=Theta(M/D)` occupied tiles and precision
`p=Theta(MD/u)`, take the first `B=floor(delta D/sqrt(u))` modes of each
tile, where `delta>0` is a sufficiently small fixed constant. All the new
weights, including the odd-node weights, are at most `A+4B`. Since
`A=log2(D)+1=O(log s)` and `D>=2^u`, the total weight of these `cB`
variables, each with exponent one, is at most
`cB(A+4B)<p` for that choice of `delta` and sufficiently large source size.
Every squarefree subset is therefore retained, giving
`exp(Omega(M/sqrt(u)))` formal tuples as well. The upper and lower orders
match for this specified full-tile formal family. This does not assert
nonzero realizable coefficients on SAT inputs; it explains exactly why
linear changes to the weights are a constant refinement of this enumeration
strategy. PR #1 is the predecessor for this type of formal counting barrier.

## 6. Generic spectra of the canonical kernels

For the integer-indexed matrix `H_(r,j)=1/(1-2rj)`, `0<=r,j<d`, (1)
gives `H=Phi diag(c_k) Phi^T`, where `Phi_(r,k)=phi_k(r)` is lower
triangular with unit diagonal over `Z_(2)`. All its entries are integral,
so `Phi` and its inverse are integral. Consequently its Smith valuations
are exactly `k+2v2(k!)`, in increasing order. This explains the linear
three-slope weights for this canonical kernel. It is a different matrix
from PR #1's normalized additive Cauchy block, whose spectrum has slope
four.

For the odd-row matrix `1/(1-2(1+2r)j)`, (5) gives two lower triangular
integral basis matrices, each with unit diagonal. Its exact Smith
valuations are `2k+2v2(k!)`. This realizes a four-slope spectrum in the
odd-node recursion without adding a row-residue partition. PR #1 already
proved the corresponding linear spectrum for its normalized local block;
the new contribution here is its usable separable expansion and the
uniform guard/integrality argument. No contradiction or stronger
obstruction for other restricted source-row domains is asserted. Those
restrictions could still improve the constant at even nodes.

## Sources and limits

Frozen OpenAI source commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`:
[quantitative-contraction.tex](../../upstream/openai-eth-2026/build/quantitative-contraction.tex),
labels `lem:tensor-integrality`, `eq:tensor-mode-expansion`,
`eq:tensor-mode-multiplicity`, `eq:tensor-mode-budget`,
`eq:tensor-recursion-identity`, and `subsec:tensor-cost`.
Hashes and Apache-2.0 attribution are in [SOURCES.json](../../SOURCES.json).

[PR #1](https://github.com/1337isnot1337/3-SAT/pull/1), head
`8790b8e14e08ea14f75c2bd6eecfdbc70fe97770`, provides the predecessor
Smith-valuation obstruction for a fixed normalized local Cauchy block and
explicitly leaves constant improvements by basis changes open. It does not
supply this tile identity, the nonrational-point integrality argument, or
the three-slope mode construction. No scientific-priority claim is made.

The finite checker tests its listed domains, not the full contraction
algorithm or the all-size argument. No independent or formal review and
no selected-result change are claimed.
