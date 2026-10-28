# One packet for the first tapered factor

This construction changes the column support in the two-packet
interpolation of [PR #52](https://github.com/1337isnot1337/3-SAT/pull/52):
allow the all-zero input as well as one-hot inputs. For the first taper
level this permits an exact one-packet realization. It is a prescribed
packet interface result, not a SAT lower bound or alpha improvement.

## Statement

For `L=2^a>=2`, let `S={-L,...,L-1}` and

```math
 H_1(T)=\prod_{\substack{t\in S\\t\text{ odd}}}\frac{T-t}{-t}.
```

One full `L`-port packet has row and column tensor entries in `Z_(2)` whose
source deformed contraction is exactly `H_1(T)`. The row tensor is affine;
the column tensor is supported on zero and the `L` one-hot inputs. Each
vertex has degree `L`. All table entries and their residues modulo `2^p`
are computable in polynomial time and space in `L` and `p`.

For every `p>=1`, replacing each row and column table entry by its canonical
integer residue modulo `2^p` gives a network whose *complete* shifted
polynomial agrees with `H_1(t+2Lz)` modulo `2^p` at every `t in S`, and whose
original contraction is odd. Repeating `h` copies uses `M=hL` real matched
edges and yields complete odd-node jets divisible by `2^{h(2L-1)}`, when
creation precision `p>=h(2L-1)` is used. A zero network on the same graph
has the same shifted residues and even origin count. The inputs use
nonnegative canonical integers, not necessarily Boolean entries.

The packets are prescribed; the result does not show that the source's
balanced graph-only packing chooses these packets. The predecessor's generic
precision scale at `u=1` and actual edge count `M` is order `ML`; this
construction gives `h(2L-1)=Theta(M)`. It does not establish the generic
scale, a source-valid active-call example, or a faster decision algorithm.

## The shift-polynomial factorization

Write `C(T)=product_(t in S)(T-t)`, and
`W_d(T)=C(T)/(C'(0)(T-d))` for `-L+1<=d<=L-1`. Let

```math
 b_* = H_1(-L),\qquad
 b_d=\frac{H_1(d)-b_*}{W_d(d)},\qquad
 P(z)=\sum_{d=-L+1}^{L-1}b_dz^{d+L-1}.
```

The values `H_1(d)` and `b_*` are 2-integral, and each `W_d(d)` is a
2-adic unit, so all `b_d` lie in `Z_(2)`. Lagrange interpolation on the
`2L` grid nodes gives

```math
 H_1(T)=b_*+\sum_d b_d W_d(T). \tag{1}
```

Since `deg H_1=L`, the polynomial `P(z)` is divisible by `(z-1)^(L-1)`.
To see this, for each `0<=k<=L-2`, the coefficient of `w^k` in `P(1+w)` is

```math
 C'(0)\sum_{d\in S}
 \frac{(H_1(d)-H_1(-L))\binom{d+L-1}{k}}{C'(d)}.
```

The omitted node `d=-L` contributes zero. The numerator is a polynomial
in `d` of degree at most `L+k<=2L-2`. In its interpolation on `S`, the
coefficient of degree `2L-1` is the displayed sum without `C'(0)`, hence
zero. This proves the factorization. Put

```math
 R(z)=(z-1)^{L-1},\qquad Q(z)=P(z)/R(z).
```

`deg Q<=L-1`; division by the monic polynomial `R` keeps all its
coefficients in `Z_(2)`. Denote them `Q(z)=sum_(y=0)^(L-1) q_y z^y`,
and write `R(z)=sum_(x=0)^(L-1) r_x z^(L-1-x)`.

## Row and column tables

On the packet's row slots use the affine table

```math
 A(Y)=b_*+\sum_x r_xY_x.
```

For the column table set `B(0)=1-sum_y q_y`, `B(e_y)=q_y`, and
`B(X)=0` on all other Boolean inputs. Thus `sum_X B(X)=1`. The deformed
contraction is

```math
 b_*+\sum_{x,y}r_xq_yW_{y-x}(T).
```

Its coefficient on `W_d` is the coefficient of `z^(d+L-1)` in `RQ=P`.
Equation (1) proves exact equality with `H_1`.

Computing each `b_d` takes polynomially many rational operations on
products of `O(L)` integers of magnitude `O(L)`; their bit lengths are
polynomial in `L`. Synthetic division by the monic `R`, table evaluation,
and odd-denominator inversion modulo `2^p` have polynomial cost and space
in `L,p`. No explicit `2^L` table is needed: the row entry is an affine
sum and the column entry checks whether its input has weight zero or one.

When each table entry is replaced by its integer residue modulo `2^p`, it
changes by an element of `2^p Z_(2)`. All shifted Cauchy entries belong to
`Z_(2)[z]`; the contraction is polynomial in table entries and Cauchy
entries. Thus its complete shifted polynomial agrees with the original
one modulo `2^p`, coefficient by coefficient, at every grid node. At
zero, `H_1(0)=1`, so the canonical integer contraction is odd. Independent
copies multiply shifted polynomials, preserving the congruence. The
zero network changes one table to zero and has the same graph.

## Exact odd-node content

Fix odd `t in S`. In `H_1(t+2Lz)`, the root at `t` contributes `2Lz/(-t)`.
The other `L-1` odd roots have pairwise differences forming the nonzero
residues of a complete `L`-grid multiplied by two. Their product has
valuation `(L-1)+v_2((L-1)!)=2L-a-2`; denominators are odd. Therefore every
coefficient is divisible by `2^(2L-1)` and the linear coefficient has
exactly that valuation. Taking `h` powers gives exact content `h(2L-1)`:
the first nonzero coefficient is the `h`th power of that linear term.

The generic tapered polynomial and its general-node formula are from
[parity-recovery-precision/PROOF.md](../parity-recovery-precision/PROOF.md).
PR #52's two-packet realization is the direct construction predecessor;
this one-packet improvement covers `u=1` only. No independent review or
novelty claim is made, and no selected bound is changed.

At concurrent PR #52 head `c65f8778bc702c2b6dbf05ddbe4295cb7fda53ba`,
a quadratic row construction realizes up to three copies of `H_1` using
two packets. Its `2L ceil(h/3)`-port construction can be better than the
`hL` ports of the independent one-packet copies here. Our one-packet result
improves the packet count for the single factor, and has a different column
support and affine row table; it is not a general improvement on that
quadratic construction for arbitrary powers.
