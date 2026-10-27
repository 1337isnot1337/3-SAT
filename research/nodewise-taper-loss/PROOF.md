# Arbitrary node multiplicities cannot lower this loss scale

The accepted OpenAI theorem is a premise. The object optimized here is one
explicit Hermite-coefficient loss functional, not the complexity of every
possible contraction or recovery method.

## 1. Definition of the nodewise functional

Let `a>=1`, `1<=u<=a`, `L=2^a`, and let `S={-L,...,L-1}` represent the
residues modulo `2^(a+1)`. Use only nodes
`A={t in S: t!=0, v_2(t)<u}`. Assign arbitrary real multiplicities `q_t>=0`
on `A`, and zero elsewhere. Write

```math
 Q=\sum_{t\in A}q_t,\qquad W(q)=Q/L,\qquad
 i_t=v_2(t),\qquad D_t=L/2^{i_t}.
```

Define `v_*(t-s)=v_2(t-s)` for distinct nodes, and `v_*(0)=a+1`. Put

```math
 P_t(q)=\sum_{s\in A}q_s\bigl(v_*(t-s)-v_2(s)\bigr),\qquad
 R(q)=\max_{t:q_t>0}\frac{P_t(q)}{D_t}.
```

The diagonal term is `(a+1-i_t)q_t`. It is essential: optimizing only the
off-diagonal product loss can conceal the cost of evaluating a high jet.
The actual highest-jet coefficient differs by one copy of this term, as
shown in Section 4.

## 2. Inactive nodes and symmetry

**Lemma 1 (maximum principle).** For `Q>0`, the maximum defining `R(q)` is
unchanged if all nodes in `A`, including nodes of zero multiplicity, are used.

**Proof.** Set `H(t)=sum_s q_s v_*(t-s)` and
`H(0)=sum_s q_s v_2(s)`, so `P_t=H(t)-H(0)`.
Fix an inactive node `t` at level `i`. If there is no active node at this
level, terms below level `i` cancel in the difference and terms above it are
nonpositive. Thus `P_t<=0`.

Otherwise choose an active `s` at level `i` maximizing `v_2(t-s)`, say `j`.
For each active `z`, if `v_2(t-z)<j`, then
`v_2(s-z)=v_2(t-z)`. If it equals `j`, then `v_*(s-z)>=j`.
It cannot be greater than `j`: such a `z` would have the same level as `t`
and contradict the maximal choice. Hence `H(s)>=H(t)`. Since `D_s=D_t`,
the inactive normalized loss is no larger than an active one on that level.
Finally the global active maximum is positive: after the symmetrization
and triangular-matrix calculation below, nonzero mass cannot have all
normalized losses nonpositive. Alternatively that calculation can be applied
to a hypothetical nonpositive full maximum. QED.

For clarity, the last positivity observation is not needed circularly:
the preceding argument already gives
`max_all <= max(0,max_active)`. If `max_active<=0`, every node has loss
at most zero; averaging as below yields `B_+ qbar<=0`, and the nonnegative
inverse forces zero mass, a contradiction. This completes Lemma 1.

Multiplication by an odd residue permutes `S`, fixes zero, preserves levels
and every valuation of a difference, and acts transitively on each nonzero
level. By Lemma 1, `R` is a maximum of fixed linear functionals on the
nonnegative cone, so it is convex. Average `q` under this finite group.
Mass is preserved, `R` cannot increase, and the averaged multiplicity is a
constant `q_i` on level `i`. Thus restricting to level-symmetric assignments
does not change the optimum of the real relaxation.

## 3. Exact optimum and matching-order bounds

There are `L/2^i` nodes on level `i`. For a level-symmetric assignment,
`W(q)=sum_i 2^-i q_i`. Write `w_i=2^-i`. Counting differences within and
above a level gives

```math
 \frac{P_t(q)}{D_t}
 =\sum_{j=1}^{a-i}\frac{j}{2^j}(q_i-q_{i+j})
   +\frac{a+1-i}{2^{a-i}}q_i
 =(B_+q)_i,
```

where `q_j=0` for `j>=u` and

```math
 (B_+)_{ii}=2-2^{-(a-i)},\qquad
 (B_+)_{ij}=-(j-i)2^{-(j-i)}\ (j>i),
```

with lower-triangular entries zero. In the diagonal simplification use
`sum_{j=1}^k j/2^j=2-(k+2)/2^k`.

**Theorem 2.** For `W0>0`,

```math
 \min_{q_t\ge0,\ W(q)\ge W_0}R(q)
 =\frac{W_0}{w^TB_+^{-1}\mathbf1},\qquad
 \frac{W_0}{2u}\le\frac{W_0}{w^TB_+^{-1}\mathbf1}\le\frac{9W_0}{u}.
```

**Proof.** The triangular matrix has a positive diagonal and nonpositive
off-diagonal entries, so back substitution makes its inverse nonnegative.
Put `v=B_+^-1 1>0`. If `lambda=max_i(B_+q)_i`, then `q<=lambda v`, hence
`W0<=lambda w^Tv`. Equality is attained by
`q=W0 v/(w^Tv)`. Symmetrization proves this is also the full nodewise optimum.

For the lower bound, each diagonal is at least one and at least the sum of
the absolute values of the off-diagonal entries in that row. Back substitution
therefore gives `v_i<=u-i` by induction. Thus

```math
 w^Tv\le\sum_{i=0}^{u-1}2^{-i}(u-i)<2u.
```

For an upper bound choose `q_i=t(u-i)`, with `t=W0/u`. Its mass is at least
`W0`. The difference `q_i-q_{i+j}` is at most `tj`, so the off-diagonal-sum
part of the displayed functional is at most `6t`, using
`sum_{j>=1} j^2/2^j=6`. The additional diagonal term is at most `9t/4`:
with `k=a-i`, use `u-i<=k+1` and
`(k+1)^2/2^k<=9/4` for integer `k>=0`. Thus the maximum is below `9t`.
QED.

An exact dual is `y=B_+^-T w>0`. It satisfies
`sum_i y_i=w^Tv`. Giving each node on level `i` weight
`y_i/(L/2^i)` lifts it to a dual on the full node set:

```math
 \sum_{t\in A}\frac{y_{i_t}}{L/2^{i_t}}\frac{P_t(q)}{D_t}=W(q).
```

The checker verifies this identity on every basis column for its small
full-node matrices, independently of the exhaustive multiplicity search.

## 4. What the functional says about the highest jet

Now take integer multiplicities. For an active node `t` the source's ordinary
Hermite formula uses

```math
 E_t(T)=\prod_{s\ne t}\left(\frac{T-s}{t-s}\right)^{q_s},
 \qquad \alpha=2^{a+1}.
```

The coefficient of the highest supplied Taylor coefficient
`[z^(q_t-1)]F(t+alpha z)` in the reconstruction of `F(0)` is exactly

```math
 E_t(0)(-t/\alpha)^{q_t-1}.
```

Indeed, the reciprocal of `E_t(t+alpha z)` has constant term one, so no
other term of that reciprocal multiplies this highest jet in the truncation.
Its negative two-adic valuation is

```math
 P_t(q)-(a+1-i_t).
```

Since `(a+1-i_t)/D_t<=1`, Theorem 2 implies that some active highest-jet
coefficient has normalized negative valuation at least

```math
 W(q)/(2u)-1.
```

The ordinary degree condition for the source polynomial is
`Q>M(2L-1)`, so `W(q)=Omega(M)`. For this individual-coefficient loss
accounting, arbitrary nodewise multiplicities therefore cannot change the
`M/u` order. A further precision floor from inherited precision would only
add to this accounting.

This is not a necessary-precision theorem for every recovery algorithm.
In particular, oversampled jets satisfy relations; a different linear
combination, correlated error analysis or reconstruction identity might
avoid paying the individual coefficient loss. No such improvement is
proved here. The connection to the mode count remains conditional on using
the source-style coefficientwise precision envelope and formal enumeration;
nonzero SAT coefficient support is not lower-bounded.

## 5. A generic obstruction even with every jet

The preceding coefficient argument does not itself exclude joint recovery.
The following separate construction does, for generic polynomials satisfying
the same degree and chart-integrality hypotheses on the retained grid.

**Theorem 3.** Let `M>=16u` be an integer and `N=M(2L-1)`. There is a rational
polynomial `G` of degree at most `N` with `G(0)=1`, such that every chart
`G(t+2^(a+1) z)`, `t in S`, has two-adically integral coefficients, while
every coefficient on each retained chart `t in A` is divisible by

```math
 2^{\lfloor M D_t/(8u)\rfloor}.
```

Thus zero and `G` cannot be distinguished using even *all* Taylor coefficients
on the retained charts at these precisions, although their values at zero
differ modulo two.

**Proof.** With `v=B_+^-1 1` as above, put `lambda=M/(4u)` and
`q_i=ceil(lambda v_i)`. Write `q=lambda v+epsilon` with `0<=epsilon_i<1`.
The sum of the absolute off-diagonal entries in each row of `B_+` is less
than two. Consequently

```math
 (B_+q)_i\ge\lambda-2\ge\lambda/2=M/(8u).
```

Also `w^Tq<2u lambda+2=M/2+2`. Define

```math
 G(T)=\prod_{s\in A}\left(\frac{T-s}{-s}\right)^{q_{i_s}}.
```

Its constant coefficient is one, and its degree is `L w^Tq`, which is less
than `L(M/2+2)<=M(2L-1)` for the stated parameters.

For a nonzero rational polynomial define its Gauss valuation as the minimum
two-adic valuation of its coefficients. Gauss valuations add under products:
after factoring out the minimum power of two, the reductions of the two
primitive factors are nonzero polynomials over `F_2`, whose product is nonzero.
The factor `(t+2^(a+1) z-s)/(-s)` has Gauss valuation
`v_*(t-s)-v_2(s)`. Therefore the chart of `G` at a retained node has Gauss
valuation exactly

```math
 P_t(q)=D_t(B_+q)_{i_t}\ge M D_t/(8u).
```

For zero and for nodes on the omitted levels `i>=u`, every root `s` has
smaller valuation, so `v_2(t-s)=v_2(s)`, and the chart Gauss valuation is
zero. All charts are integral. This proves the claims. QED.

Theorem 3 rules out a *generic* recovery guarantee with uniformly
`o(M D_t/u)` retained-chart precision under only these degree and integrality
hypotheses. Redundant jets, nonlinear decoding and cancellations between
recovery coefficients cannot distinguish this pair of polynomials. The
theorem does **not** show that `G` is a deformation polynomial of an actual
tensor network, much less of a SAT reduction. Extra information about that
class, omitted charts, new nodes or a new kernel can escape this obstruction.

## 6. Stopping boundary

The tested extension was arbitrary nodewise tapering on the same residue grid,
with the same ordinary Hermite coefficient accounting. Its optimized scale
is still `Theta(M/u)`. The all-input SAT bound is unchanged. A new attempt
must exploit structure beyond the generic degree and chart-integrality
hypotheses, change the node/kernel geometry, or aggregate the modes; it must
also pay every outer and recursive cost. The next concrete question is whether
the actual tensor-deformation polynomial lattice admits cheaper joint recovery.
