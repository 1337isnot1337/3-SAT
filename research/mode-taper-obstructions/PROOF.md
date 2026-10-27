# Three scoped lemmas for changing Appendix D

These lemmas analyze proposed improvements to the accepted OpenAI construction.
They do not audit its truth or assert a new SAT algorithm. Source labels refer
to the frozen contraction file identified in the [README](README.md).

## 1. Squarefree modes survive stronger elementary restrictions

Fix integers `u>=1`, `a>=u`, `0<=i<u`, `P>=1`, and set

\[
 L=2^a,\quad D=L/2^i,\quad h=a+1-i,\quad
 v=\lceil\sqrt u\rceil,\quad M=PL.
\]

Consider `P` full packets with differing symbols in coordinate `i`. Each has
`2^{i+1}` column tiles, each containing `D/2` columns. For every tile and
`b>=0`, take the formal mode in `eq:tensor-mode-expansion`. Its coefficient
has uniform divisibility weight at least `h+b`: the first fraction contributes
at least `h`, and the geometric ratio at least one per power. This strengthens
the source's simpler weight `b+1`.

**Proposition 1.** If `D>=max(16v,8vh)`, there are at least `2^{M/(8v)}`
squarefree exponent tuples with total strengthened weight at most `MD/(16u)`,
total degree at most `M`, and degree at most `L` in each packet. Every selected
moment index is below the number of columns in its tile.

**Proof.** Put `q=floor(D/(8v))`. Then

\[
 D/(16v)\le q\le D/(8v),\qquad h\le D/(8v),\qquad q<D/2.
\]

In each tile select the `q` modes with indices `b=0,...,q-1`. Their total is

\[
 N=P2^{i+1}q=(2M/D)q,
 \qquad M/(8v)\le N\le M/(4v).
\]

Independently choose their exponents to be zero or one. Every choice has
weight bounded by that of the all-one choice, hence at most

\[
 N(h+q)\le\frac{M}{4v}\frac{D}{4v}
 =\frac{MD}{16v^2}\le\frac{MD}{16u}.
\]

Total degree is at most `N<=M`, and degree in a packet is at most
`2^{i+1}q<=L/(4v)<=L`. There are `2^N` choices. QED.

The construction even meets a separate `L/2` row cap for each target group:
half the tiles target each group, giving at most `L/(8v)` selected modes there.
The source precision includes `8 ceil(3M/u) D`, so every tuple lies inside
its weight budget. Since `v<=2 sqrt(u)`, the family has
`exp(Omega(M/sqrt(u)))` members. In the source regime `a>=2u`, `i<u`, the
side condition holds for all sufficiently large `u`. If only a constant
fraction of full packets have unequal coordinate symbols, use those packets;
only the entropy constant changes and the total budget is no smaller.

The subfamily's exact generating function, marking degree by `y`, is

\[
 \prod_{b=0}^{q-1}(1+yx^{h+b})^{P2^{i+1}}.
\]

Every term, with multiplicity counting distinct exponent choices, meets the
bounds above. This is a statement about formal tuples with packet/tile
structure. It does not show their coefficients are nonzero, that a hard SAT
instance realizes them, or that an algorithm must enumerate them. Coefficient
support or aggregation may escape this obstruction.

## 2. Exact optimization of the level-dependent product loss

Fix integers `a>=u>=1`. Let `q_i>=0` for `0<=i<u`, extending by zero for
`i>=u`. Allow real multiplicities as a relaxation, so a lower bound also
applies to integer multiplicities. Define

\[
 w_i=2^{-i},\qquad W(q)=\sum_{i=0}^{u-1}w_iq_i,\qquad
 \ell_i(q)=\sum_{j=1}^{a-i}\frac{j}{2^j}(q_i-q_{i+j}).
\]

The identity `eq:tensor-hermite-loss` says
`v_2(E_t(0))=-D_i ell_i(q)`, where `D_i=L/2^i`. There are `L/2^i`
nonzero nodes of valuation `i`. Thus total multiplicity is `L W(q)`, and
interpolating an arbitrary polynomial of the source's degree bound requires

\[
 LW(q)>M(2L-1),
\]

in particular `W(q)>M`. Define the upper triangular matrix

\[
 B_{ii}=\sum_{j=1}^{a-i}\frac{j}{2^j},\quad
 B_{ik}=-\frac{k-i}{2^{k-i}}\ (k>i),\quad B_{ik}=0\ (k<i).
\]

Then `Bq=ell(q)`. Its diagonal is positive and its off-diagonal entries are
nonpositive. Back substitution makes `B^-1` entrywise nonnegative. Put
`v=B^-1 1`, which is strictly positive.

**Proposition 2.** For any `W0>0`,

\[
 \min_{q\ge0,\ w^Tq\ge W_0}\max_i\ell_i(q)
 =\frac{W_0}{w^TB^{-1}\mathbf1}\ge\frac{W_0}{4u}.
\]

**Proof.** Set `lambda=max_i ell_i(q)`. From `Bq<=lambda 1` follows
`q<=lambda v`. Hence `W0<=w^Tq<=lambda w^Tv`. Equality is attained by
`q=W0 v/(w^Tv)`, whose losses all equal `W0/(w^Tv)`.

Let `A_i=B_ii>=1/2`, since `a-i>=1`. The recurrence is

\[
 A_i v_i=1+\sum_{j=1}^{u-1-i}\frac{j}{2^j}v_{i+j}.
\]

Backward induction gives `v_i<=2(u-i)`: the last entry is at most 2;
at each earlier step all successors are at most `2(u-i-1)`, and their
coefficient sum is at most `A_i`. Consequently

\[
 w^Tv\le2\sum_{i=0}^{u-1}2^{-i}(u-i)<4u.
\]

This proves the stated weaker non-strict bound. QED.

No monotonicity of `q` was assumed. A positive maximum loss occurs at an
active level, because `q_i=0` implies `ell_i<=0`. An exact dual certificate
is `y=B^-T w>0`, with `w^Tq=y^T Bq<=lambda sum(y)` and `sum(y)=w^Tv`.
The checker verifies both systems and objective equality.

A linear taper `q_i=t(u-i)` satisfies `ell_i<=6t` and `W(q)>=tu`.
Choosing `t=W0/u` gives an upper bound `6W0/u`. Thus the optimized scale
is exactly `Theta(W0/u)`.

### Closed form in the infinite-grid relaxation

When the upper valuation cutoff tends to infinity, `A_i=2`. With `k=u-i`,

\[
 2v_k-\sum_{j=1}^{k-1}\frac{j}{2^j}v_{k-j}=1,\qquad
 v_k=\frac{k}{6}+\frac5{18}+\frac{2}{9\,4^k}\quad(k\ge1).
\]

Substitution proves the formula; equivalently its generating function is

\[
 \sum_{k\ge1}v_kz^k=\frac{z(2-z)^2}{2(1-z)^2(4-z)}.
\]

Its normalizer is

\[
 \sum_{i=0}^{u-1}2^{-i}v_{u-i}
 =\frac u3+\frac29-\frac{2}{9\,4^u}.
\]

Hence this relaxed optimum is asymptotic to `3W0/u`. This quantifies slack
in conservative taper constants, not an end-to-end speedup or larger alpha.

**Scope.** This prevents the particular maximum normalized `E_t(0)` loss
from becoming `o(M/u)` under the degree and level-support conditions. It
does not prove necessary working precision for every recovery algorithm:
combined Hermite coefficients, jet relations, or another identity could
cancel losses. Within the source's separate product-loss envelope and
partition estimate, it leaves `sqrt(M*(M/u))=M/sqrt(u)` intact. This is not
a runtime lower bound for every taper-based contraction.

## 3. Exact local Cauchy valuation spectrum

Work in the source's two-adic valuation ring, or `Z_(2)`, with `v_2(2)=1`.
For any unit `c` and `0<=j,k<d`, put

\[
 H_{jk}=1/(c+2(j-k)).
\]

All denominators are units. This is the normalized denominator block for
fixed row and column residue classes whose crossing denominator has valuation
exactly `i`, after removing its common power of two. A uniform nonzero scalar
factor shifts all the valuations below equally.

**Proposition 3.** The Smith valuations of `H` are

\[
 e_j=2j+2v_2(j!)=4j-2\operatorname{popcount}(j),\qquad 0\le j<d.
\]

**Proof.** For row and column sets `I,J` of size `k`, the Cauchy determinant
identity and unit denominators give

\[
 v_2(\det H_{I,J})=k(k-1)+v_2(\Delta(I))+v_2(\Delta(J)),
\]

where `Delta` is the product of pairwise differences of the ordered indices.
For distinct nonnegative integers `x_0,...,x_{k-1}`, the integral matrix
`binom(x_i,j)` has determinant

\[
 \frac{\prod_{i<j}(x_j-x_i)}{\prod_{j=0}^{k-1}j!}.
\]

Therefore each Vandermonde valuation is at least
`sum_{j=0}^{k-1}v_2(j!)`. Consecutive indices attain equality on both sides.
The minimum valuation of the `k`-minors is exactly

\[
 \delta_k=k(k-1)+2\sum_{j=0}^{k-1}v_2(j!).
\]

Determinantal divisors make this the sum of the first `k` Smith valuations.
Subtract successive values to obtain `e_j=2j+2v_2(j!)`. Counting multiples
of powers of two gives `v_2(j!)=j-popcount(j)`. QED.

For `j>=1`, `2j<=e_j<=4j`, and in fact `e_j=4j-O(log(j+1))`.
Invertible row and column operations over the valuation ring preserve these
numbers. A basis change alone cannot turn this block's linear spectrum into
quadratic or other superlinear growth, though it may improve constants over
the raw geometric expansion. Sparse restrictions, a different kernel,
nonlinear representations, Boolean identities and joint contraction are
outside this statement.

## Research consequence

These lemmas remove three specific elementary routes to a better exponent:
uniform initial valuation plus degree caps, optimizing the same taper loss
functional, and changing basis in this Cauchy block. They do not prove the
accepted theorem optimal. A larger alpha remains open and requires a new
constraint or mechanism, followed by complete outer and recursive cost bounds.
