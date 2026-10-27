# Charging the gap in a complete nodewise recovery model

This continues [PROOF.md](PROOF.md). Its grid and local spectrum are exact.
The normalization below is an explicitly stated model of the local spectral
benefit, not a proved complete mode algorithm. We then solve the recovery
functional exactly, allowing every nonzero grid node and arbitrary nodewise
multiplicities. Thus no missing dummy nodes explain the conclusion.

## 1. Node classes and the charged scales

Retain `d=2^r`, `H=2^t`, `B=2^b`, `g=b-r>=2`, `L=dH`, and
`alpha=2^(b+t+1)`. All nonzero nodes lie in the following classes:

- `L_i`, `0<=i<=r`: nodes whose low coordinate has valuation `i`.
  There are `2L/2^i` such nodes. Class `L_r` has low coordinate `-d`.
- `U_j`, `0<=j<=t`: nodes with low coordinate zero and high coordinate
  of valuation `j`. There are `H/2^j` such nodes. Class `U_t` is the
  singleton high coordinate `-H`.

Write `D_i=d/2^i`, `E_j=H/2^j`. Assign positive normalizers

```math
 K_{L_i}=2H(D_i+g),\qquad K_{U_j}=2E_j.                 \tag{1}
```

For a real low-bit tile (`i<r`), its low width is `D_i/2`, its high width
is `H`, and the local Smith spectrum has asymptotic slope
`4+4g/D_i`. Multiplying tile size by that slope gives precisely `K_L_i`.
For a high-bit tile the ordinary slope-four model gives `K_U_j`.
For the two dummy classes (1) deliberately grants a favorable scale of
the same order as the corresponding geometric expansion: `O(gH)` for
the low dummy and `O(1)` for the high dummy. A full implementation of
all source/target mode factorizations is not supplied.

Consequently conclusions about (1) are conclusions about this stated
loss/slope comparison. An algorithm with a different aggregate mode
cost need not obey it. The generic precision witness in Section 5 is a
separate exact polynomial statement at the explicitly defined scales (1).

## 2. Arbitrary nodewise multiplicities symmetrize

Give every nonzero node a real multiplicity `q_s>=0`. For distinct nodes
use the usual `v_2(s-s')`; set `v_*(0)=b+t+1`. Define

```math
 P_s(q)=\sum_{s'\ne0}q_{s'}(v_*(s-s')-v_2(s')),\qquad
 W(q)=\frac1L\sum_{s\ne0}q_s,\qquad
 R(q)=\max_{s:q_s>0}\frac{P_s(q)}{K_s}.                \tag{2}
```

These are the Hermite product/diagonal losses including the top jet,
before subtracting its one-copy correction. The maximum is positive and
unchanged if nodes with zero multiplicity are included. Here is the
maximum principle, as in the predecessor nodewise analysis but for this
new grid. If a zero-multiplicity node has no active node of its valuation,
its loss is nonpositive. Otherwise choose a closest active node of that
valuation. The ultrametric inequality makes the potential at that active
node at least as large: every other active node is either equally distant
or closer to the selected active node. Its normalizer is the same.
If the active maximum were nonpositive, averaging as below and using the
nonnegative inverse in Section 3 would force all mass to be zero.

The finite product grid has a group of valuation-preserving permutations
fixing zero and transitive on every class `L_i,U_j`. To see this, multiply
the low coordinate by an odd residue modulo `2d`; independently translate
the high coordinate modulo `2H` in any nonzero-low-coordinate cluster;
and multiply high coordinates by an odd residue in the zero-low cluster.
Use centered interval representatives afterwards. For different low
coordinates their valuation difference depends only on those coordinates;
within a cluster it is `b` plus the preserved high-coordinate difference.
These permutations preserve `P`, `K`, and mass. Convexity of the full-node
maximum allows averaging, so an optimum exists with multiplicities
constant on each listed class. No monotonicity premise is imposed.

## 3. Exact triangular program

List low classes first, then high classes. For their common multiplicities
`q=(q^L_0,...,q^L_r,q^U_0,...,q^U_t)`, write `P=Aq`. Direct counting gives

```math
 A^{LL}_{ii}=2H(2D_i+g-1)-1,\quad
 A^{LL}_{ik}=-2H D_k(k-i)\quad(k>i),
```

```math
 A^{LU}_{ij}=-E_j(b+j-i),\quad
 A^{UU}_{jj}=2E_j-1,\quad
 A^{UU}_{jk}=-E_k(k-j)\quad(k>j),                       \tag{3}
```

with every other entry zero. For clarity, the low part is `2H` times the
ordinary full `2d` residue-grid matrix, plus `(2Hg-1)q^L_i` on its diagonal.
The upper-cluster contribution is `-sum_j E_j(b+j-i)q^U_j`. The high part
is exactly the ordinary full `2H` residue-grid matrix; all low-root
contributions cancel there.

The mass weights are

```math
 w^L_i=2^{1-i},\qquad w^U_j=d^{-1}2^{-j},\qquad W=w^Tq.
```

The diagonal of `A` is positive, its off-diagonal entries are nonpositive,
and it is upper triangular. Its inverse is therefore nonnegative by back
substitution. With the vector `K` from (1), put `v=A^-1 K>0`. For `W0>0`,

```math
 \min_{q\ge0,\,w^Tq\ge W_0}R(q)=\frac{W_0}{Z},\qquad
 Z=w^TA^{-1}K.                                         \tag{4}
```

Indeed `Aq<=lambda K` implies `q<=lambda v`, so mass is at most `lambda Z`.
Equality is attained by `q=W0 v/Z`. This also proves the positivity used
above. An exact dual is `y=A^-T w>=0`, with `y^TK=Z`.

## 4. The normalizer cannot grow with the numerical gap

For all permitted parameters,

```math
 Z<10(r+t+2).                                          \tag{5}
```

A short explicit supersolution proves this without approximating `b`.
Put `n=r-i`, `m=t-j`, and

```math
 \phi^L_i=2(n+t+2),\qquad \phi^U_j=2(m+1).
```

For an ordinary full residue grid, let its unnormalized matrix be
`C_ii=2D_i-1`, `C_ik=-D_k(k-i)`. Direct finite sums give

```math
 (C\mathbf1)_i=n+1,\qquad
 (C(n+1))_i=D_i\left(6-\frac{2n+5}{2^n}\right)\ge D_i.
```

The last parenthesis is at least one for `n>=0`. Hence the high rows obey
`(A phi)^U_j>=2E_j=K_U_j`. Also the high mass and high valuation moment
of `phi^U` obey

```math
 \sum_j E_j\phi^U_j\le4H(t+1),\qquad
 \sum_j jE_j\phi^U_j\le4H(t+1).
```

Using (3) and these bounds, a low row satisfies

```math
 (A\phi)^L_i\ge4H D_i+4Hg(n+1)-2(n+t+2)
              \ge H(2D_i+2g)=K_{L_i}.
```

The last inequality holds at `n=0` from `H=2^t>=t+1`, `g>=2`, and
only strengthens at larger `n` (or subtract the right side explicitly).
Thus `v<=phi`. Finally `sum_i w^L_i<4` and
`sum_j w^U_j phi^U_j<4(t+1)/d<=2(t+1)`, giving (5).

The ordinary Hermite highest-jet coefficient has negative valuation
`P_s(q)-(b+t+1-v_2(s))`. For both class types its one-copy correction
divided by `K_s` is at most one. Thus at least one active highest-jet
coefficient has normalized loss at least

```math
 \frac{W(q)}{10(r+t+2)}-1.
```

The interpolation degree condition requires `W=Omega(M)`. Within this
spectral-slope / separate-coefficient comparison, the best loss remains
at least order `M/(log L)`: increasing the gap to a power of `log M`
does not change that denominator to `b`. This is not a runtime lower
bound, nor an exact census of nonzero modes.

There is an additional exact limit. Let `B_t` have diagonal
`2-2^{-(t-j)}` and upper entries `-(k-j)/2^(k-j)`, on `j=0,...,t`, and
put `A_t=sum_j 2^-j (B_t^-1 1)_j`. With `r,t` fixed,

```math
 \lim_{b\to\infty}Z=4-\frac2d+4A_t.                   \tag{6}
```

The high part of `v` is independent of `b` and equals `2B_t^-1 1`.
Divide a low row of `Av=K` by `b`: its limit gives
`v^L_i=1+(sum_j E_j v^U_j)/(2H)=1+A_t`. Sum the class weights to obtain
(6). Thus an arbitrarily wide gap ultimately retains only the upper
block's depth in this comparison, rather than creating new levels.

## 5. A generic all-node, all-jet witness

The same program yields an actual indistinguishability witness for the
new interpolation grid, even when every nonzero node is available.
Let `a=r+t`, `M>=160(a+2)`, `lambda=M/(20(a+2))`, and round

```math
 q_i=\lceil\lambda v_i\rceil,\qquad
 F(T)=\prod_{s\in S\setminus\{0\}}
                      \left(\frac{T-s}{-s}\right)^{q_{\mathrm{class}(s)}}.
```

Then `F(0)=1`, and

```math
 \deg F< L(M/2+4)\le M(4L-1).
```

Every row's absolute off-diagonal sum divided by `K_i` is at most four.
For a high row it is at most one. For a low row, the two parts are at most
`4HD_i` and `2H(g+n+2)`, and `n+2<=2D_i` proves the bound. Rounding
therefore gives

```math
 (Aq)_i\ge(\lambda-4)K_i\ge\frac{M K_i}{40(a+2)}.
```

The exact Gauss valuation of `F(s+alpha z)` is `P_s(q)=(Aq)_i`, by
multiplying the normalized linear factors; at the origin it is zero.
All these charts are integral. Consequently `F` and zero have identical
complete jets modulo `2^floor(M K_i/(40(a+2)))` at **every nonzero node**,
but different origin parity. Arbitrary processing of all supplied jets
cannot distinguish them under only the generic degree and chart-integrality
hypotheses.

This is an all-size statement about actual rational polynomials. Its
realization as a tensor deformation is not established. The implication
for a proposed mode algorithm remains conditional on its charged scales
being those in (1). A different representation or a theorem special to
actual tensor polynomials remains an escape.

## Scope and predecessor credit

The grid and exact Smith spectrum are positive component changes. The full
recovery model shows why numerical valuation range alone is not an exponent
gain. This stops the unchanged gap-plus-spectrum proposal, while preserving
the coordinate family for a genuinely different recovery or mode mechanism.
No complete new contraction or SAT bound is claimed.

The maximum principle, symmetrization and triangular primal/dual method are
adapted with credit to [PR 8](https://github.com/1337isnot1337/3-SAT/pull/8),
head `2ce8a90058765b2409ff656b70e3cbf995b4ad9b`, which studies the original
contiguous grid. The generic witness method overlaps [PR 6](https://github.com/1337isnot1337/3-SAT/pull/6).
The new objects here are the two-scale full-node classes, spectral scales,
matrix (3), gap-independent supersolution, limit (6), and their full-grid
witness. All written reasoning is author-checked, AI assisted, and awaits
independent review.
