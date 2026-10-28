# Local mode support and a child-tensor obstruction

This is an author-checked research note, not an independent proof review.
The accepted OpenAI theorem is used as a premise. The predecessor Newton
modes are those in [PR #4](https://github.com/1337isnot1337/3-SAT/pull/4).

## 1. Exact local identities

For a Boolean table `A` on `d` row ports define its multilinear extension

```
F_A(z_1,...,z_d) = sum_{y in {0,1}^d} A(y) prod_i l_{y_i}(z_i),
l_0(z)=1-z,  l_1(z)=z.
```

This identity holds over any commutative ring. For the equality table,

```
F_eq(z) = prod_i (1-z_i) + prod_i z_i.
```

Its coefficient of `prod_{i in S} z_i` is `(-1)^|S|` for proper
subsets, and `1+(-1)^d` for the full set. Thus, for odd `d>=3`, its
total degree is `d-1`; for even `d` its full coefficient is 2. In
particular, for a trivalent equality,

```
F_eq = 1-z_1-z_2-z_3+z_1z_2+z_1z_3+z_2z_3.       (1)
```

This cancellation is exact over the integral coefficient ring, not merely
modulo 2. For a clause with unique falsifying pattern `v`, its extension is
`1-prod_i l_{v_i}(z_i)` and has degree `d` with full coefficient `+1` or
`-1`. A tautology can be removed as in the source reduction.

At a deformed-contraction call, each `z_i` is an affine form in local
column bits and crossing mode variables. Substitution into (1) therefore
has total mode degree at most 2 for this single equality vertex, even if
its ports lie in different packets. This follows because a vertex belongs
to one group, so all its row bits can be summed together. The bound is
local: in a whole group, products of many such vertices can have much
larger total degree, and distinct vertices can share mode variables. It
also does not say which individual coefficients vanish, nor that the group
contraction is cheap to evaluate.

## 2. One exact packet with no additional support holes

Use `L=8`, `i=0`, `t=1`, `alpha=16`, `zeta=1`, so `T=17`. Take a
packet with unequal coordinate-0 symbols. It has real row and column ports
at slots `0,2,4` only; all row ports are in one group and all column
ports in the other. This respects the local slot/orientation rule; we do
not claim that this small packet alone satisfies all global asymptotic
packing side conditions. The three row ports are one trivalent equality
vertex or one positive 3-clause vertex. Each column is attached to a unary
`(1,1)` vertex. Thus every input table is a fixed-density reduction table.
There are no local row-to-column terms in either group.

Use the general Newton modes from PR #4. The tile has `j=0,1,2,3`, but
only `j=0,1,2` are real, hence mode `k=3` has zero source linear form.
For `k=0,1,2`, write `a_{xk}` for the row coefficient and `b_{kj}` for
the column coefficient. The checker verifies the nine identities
`W_xy=sum_k a_xk b_ky` exactly over the rationals. It substitutes the
three row affine forms into (1) and into the clause polynomial, and then
multiplies each mode coefficient by the actual source-side moment obtained
by summing all eight Boolean column assignments. Independently it sums all
64 pairs of assignments in the original deformed contraction.

The equality case has **all 10** tuples of three modes with total degree at
most two, and no others. The positive clause case has **all 19** tuples of
total degree one through three, and no others. Every corresponding source
moment is nonzero and the child sum equals the direct contraction exactly.
The checker determines nonzero values over `Q`, before reducing modulo a
precision; some may vanish at a particular two-adic precision. This is a
bounded illustration of the absence of further support holes in this one
packet, not a claim for every input, interpolation point, or packing.

## 3. A growing rational family with full degree-feasible support

For every `q>=1` and `K>=3q`, choose a power of two `L>=2K`, put
`i=0`, `t=1`, `alpha=2L`, and `T=2L+1` (`zeta=1`). Use one packet
with matched real row and column slots `0,2,...,2(K-1)`. All row ports
belong to one group and all column ports to the other. On the row side
put `q` trivalent equalities on disjoint triples and `K-3q` unary `(1,1)`
vertices. On the column side put `K` unary `(1,1)` vertices. Summing a
row unary vertex produces 1. There are `K` nonzero general-Newton source
modes, indexed by `0,...,K-1`; modes at higher indices vanish on the real
columns. If the `q` equalities are replaced by positive 3-clauses, retain
the same port arrangement.

For the equality family, after summing row and column bits, the rational
summand associated with **every** `beta in N^K` with `|beta|<=2q` is
nonzero; all others are zero. For the clause family, the same holds exactly
for `q<=|beta|<=3q`. Thus the two respective support sizes are

```
  binom(K+2q, 2q),
  binom(K+3q, 3q) - binom(K+q-1, q-1).
```

**Proof.** For `x` a real row slot, set `z=1/(T+x)`. The Newton row
coefficient of mode `k` is

```
a_xk = [C(T)/(C'(0)(T+x))] c_k phi_k(z).
```

Here `C(T)>0`, `C'(0)<0` because even `L` gives `L-1` negative factors,
`0<z<1`, and every factor in the denominator of `phi_k(z)` is positive.
For `k>=1`, the falling factorial in `phi_k(z)` has sign `(-1)^(k-1)`
and `c_k<0`; the formula also covers `k=0`. Consequently
`sign(a_xk)=(-1)^(k+1)` and no such coefficient is zero. This sign is
independent of `x`.

For one equality, the degree-zero, one and two terms in (1) have coefficient
sign `(-1)^(sum k beta_k)`, with every tuple of that degree present. For
one positive clause, the degree-one through degree-three terms have sign
`(-1)^(sum k beta_k+1)`, again with every tuple present. In the product
of `q` vertices, all contributions to a fixed tuple have the same sign;
none cancel. A tuple of size at most `2q` can be distributed among the
`q` equality factors with at most two indices per factor. A tuple of size
between `q` and `3q` can be distributed among clause factors with one to
three indices each. This gives the stated row support and no larger degree.

For a real column `j>=k`, `phi_k(j)` has sign `(-1)^k` and is nonzero;
it is zero for `j<k`. Thus the source form for mode `k` is `(-1)^k` times
a nonnegative sum on Boolean columns, positive when all columns are one.
For any `beta`, every summand in its source moment has the same weak sign
`(-1)^(sum k beta_k)`, and the all-ones column assignment is nonzero.
Every row coefficient therefore remains nonzero after the source sum. This
also handles `beta=0`. The stars-and-bars count proves the displayed sizes.

This is an all-size statement about a specified single-packet rational
contraction and the **general** Newton expansion. In particular `K=3q`
gives exponentially many nonzero tuples as `q` grows. The taper comparison
below first treats a conditional local packet; a subsequent construction
embeds it into a globally admissible root call with a specified valid packing. It does not exclude cancellation
with other terms in the final contraction, establish a lower bound for a
more efficient aggregation algorithm, or improve or refute a SAT bound.
The bounded checker separately tests `(K,q)=(3,1),(4,1),(6,2)` for each
family, including source moments and exact contractions.

### A precision-aware bound for this family

Let `d=|beta|` and write `R=Z_(2)`, the rationals with odd denominator.
The source moment is a sum over all `K` Boolean column assignments of a
product of `d` linear forms with coefficients in `R`. Reduce each power
`X_j^m` to `X_j` on Boolean inputs. The result is a multilinear polynomial
of degree at most `d`, and a monomial on `s` distinct variables sums to
`2^(K-s)` over all assignments. Hence, for `d<=K`, the source moment is
divisible in `R` by `2^(K-d)`.

Put `A=log2(L)+1` and `w_k=A+k+2 v2(k!)`, the general Newton weights.
The accepted-point integrality and row coefficient bound from PR #4 give
`v2(a_xk)>=w_k`. Every term of the row coefficient for `beta` has one
such factor for each mode occurrence. Consequently the full rational
summand has valuation at least

```
K - |beta| + sum_k w_k beta_k.                         (3)
```

For either family the degree range ensures `|beta|<=K`. A summand is zero
modulo `2^p` whenever the right side is at least `p`. This is a bound for
the specified free-unary source group; it cannot be applied to a general
child tensor, where the source bits may have a nonconstant weight. It is
also not an algorithmic pruning gain without a way to establish and use the
bound under the actual recursive packing and recovery costs.

The checker measures actual rational valuations as well as proving the
finite instances satisfy (3). For `K=6, q=2`, 47 of 210 equality terms and
39 of 917 clause terms survive modulo `2^32`; at precision 128 all of
these listed terms survive. These are specified test precisions, not an
assertion that the source's actual taper chooses either value. A surviving
summand does not preclude cancellation in the final sum.

### Comparison with the source taper, conditional on the local packet

For either growing family, every listed local summand is also nonzero
modulo the source-prescribed child precision at an active `t=1` call,
provided the call contains this local packet and the evaluation set
includes the binary-coordinate lift `zeta=1`. Both the equality and clause
families use the general Newton expansion. This statement concerns the
isolated packet summands; the global tensor-network construction below
separately handles the other group tensors.

Here is a deliberately loose uniform bound, included to avoid inferring
modular nonvanishing from rational nonvanishing. Let `a=log2 L` and
`H=20 L(a+2)`. The numerators and denominators, in lowest terms, of every
row coefficient `a_xk` and source coefficient `phi_k(j)` have at most
`H` binary digits. Indeed `T+x<4L`, all factors of `C(T)` and `C'(0)`
have absolute value below `4L`, and the formulas for the falling
factorials, `k!`, and `c_k` have at most `O(L)` factors of magnitude at
most `4L^2`; direct counting gives the stated generous bound. All these
coefficients are in `Z_(2)` by the predecessor's integrality argument.

There are fewer than `L^2` such row and column coefficients. Their odd
lowest-term denominators have a common odd multiple `D` whose binary
logarithm is at most `L^2 H`. Multiplying any coefficient by `D` gives an
integer of absolute value at most `D 2^H`. A term of degree `d<=K` in the
row coefficient and source moment can be expanded using at most
`2^K(4K)^(2K)` products, each containing `2d` such coefficients. Thus
its nonzero numerator over the odd denominator `D^(2d)` has at most

```
K + 2K log2(4K) + 2K(L^2 H + H) + 1
    <= 200 L^4(a+2)                                      (4)
```

bits. Its two-adic valuation is no larger than that bit bound. This also
handles degree zero. The common-sign proof above ensures the numerator is
nonzero; the estimate does not assume its valuation is close to the lower
bound (3).

The source has `r=64`, `D_arr=r^(2a)=L^12`, `u<=a`, and active packing
condition `M>=L D_arr=L^13`. For `t=1`, `D_t=L` and the explicit child
precision is `p_t=p+8hL+8M(a+1)`, where `h=ceil(3M/u)`. Consequently

```
p_t >= 24 M L/u >= 24 L^14/a > 200 L^4(a+2)            (L>=8).
```

Thus every nonzero summand is nonzero modulo `2^p_t`. The usual mode
weight of each degree-`d` tuple is also far below that precision, since
`w_k<=a+1+3k` and `d<=K<=L/2`. The source permits choosing distinct
binary-coordinate lifts for evaluation; the conditional statement chooses
a set containing 1. It does not assert what happens at all other evaluation
points, or when this packet is combined with the rest of a child group.
The finite checker verifies the height bound, weighted-budget comparison,
and actual valuations for its registered cases; the general estimate is
an author-checked argument awaiting independent review.

### An explicitly packed global tensor-network family

The local family can be embedded into an entire active root call using a
**specified valid packing**. This packing is a deterministic alternative;
we do not assert that the source's particular conditional-expectation
labeling returns it. The input is a valid bounded-degree tensor network
using the fixed-density reduction's equality and unary table types. It is
easily simplified and no lower bound on arbitrary SAT algorithms or on an
optimized contraction method follows.

Let `s=2^N`, `lambda=N`, `u=floor(epsilon N)`, `a=2u`, `L=2^a`,
`r=64`, `D_arr=r^(2a)=L^12`, and

```
B = L floor(s/(L D_arr)),  q = floor(L/6),  K = 3q.
```

Take `N` sufficiently large that `u>=1`, `B>=L`, and the inequalities
below hold. For every ordered pair of vertex labels in `[r]^a`, reserve
exactly `B` slots, and combine the slots into packets by the source's
orientation rule. There are `B D_arr/L` packets. Choose the packet whose
coordinate-zero unordered symbol pair is `{0,1}`, all other pairs are
`{0,0}`, and whose packet index is the first. Keep only its slots
`0,2,...,2(K-1)` real. Every slot in every other packet is real.

On each real edge put a distinct unary `(1,1)` vertex on both sides,
except that the `K=3q` row unary vertices of the selected packet are
replaced by `q` ternary equality vertices, each incident to one disjoint
triple. Each triple has one row label, since all its selected slots have
the same coordinate-zero orientation and all other coordinates equal.
The resulting bipartite network has maximum degree three and

```
M = B D_arr - (L-K) = s - O(L D_arr + L).
```

Its label class loads are `B` except that one class loses `L/2-K`
slots and its reversed coordinate-zero class loses `L/2`. Therefore
`max X_gamma=B`, `B` is a multiple of `L`, and
`sum_gamma (X_gamma-M/D_arr)^2 <= L^2 <= 2M Delta`. At most
`B D_arr/r <= 3M/r` row or column ports carry any given symbol in any
coordinate. Packet count is `B D_arr/L <= 3M/L`, and all packet orientation
rules hold by construction. Thus it satisfies the same explicit balance,
collision-load, padding and packet conclusions as the source packing
lemma, with a directly constructible labeling and slot allocation.

For the source's root parameters, `L<=s^(2 epsilon)` and
`D_arr^2<=s^(48 epsilon)`. Since `48 epsilon<1/10`, sufficiently large
`N` gives `M>H`, `M>=2D_arr^2 ceil(s^(9/10))`, `M>=L D_arr`, and
`2L<=ceil(s^(9/10))`. Hence this is an active, globally admissible root
call with `M<=s` and the required degree bound. The graph and labeling
are constructible in polynomial time in `s` by enumerating label classes,
packets and slots. The toy [embedding checker](embedding.py) verifies the
slot arithmetic and balance in a small `r=2` model; it does not pretend
to realize the asymptotic root parameters.

At `t=1` and `zeta=1`, set every mode outside the selected packet's even
source tile to exponent zero. For every selected-tile tuple `beta` with
`|beta|<=2q`, summing each filler row unary bit gives
`l_0(z)+l_1(z)=1`, independently of its local and crossing forms. Each
of the remaining `M-K` filler column unary bits then contributes a factor
2. Consequently the **complete** child-product summand equals `2^(M-K)`
times the specified nonzero local summand, exactly over the rationals.
There are `binom(K+2q,2q)=2^Omega(L)` such distinct tuples. The same
statement holds for the clause replacement and its stated degree interval,
although the displayed all-equality family suffices.

The source precision contains both `8hL` and `8M(a+1)`. The previous
height estimate bounds the local summand's valuation by
`200 L^4(a+2) < 8hL`, while `M-K < 8M(a+1)`. Thus each complete summand
is nonzero modulo the prescribed `2^p_t`. Its mode tuple also lies inside
the source weight budget. The result does not say that the sum of these
summands is nonzero, that the particular default packing produces them,
or that enumerating them is necessary; unary components can be simplified
and the asymptotic support here is only `2^Omega(L)`, not a lower bound of
the form `2^Omega(M/sqrt(u))`.

## 4. A child need not retain the input table family

In the same packet, choose `beta=0` for all crossing modes. By the source
child construction, the packet vertex on the row group is the coefficient
of the mode-free part of the row factors. Since that group has no local
column ports, each row argument's local part is zero, and the packet table is

```
P(Y_1,Y_2,Y_3) = prod_i l_{Y_i}(0) = (1-Y_1)(1-Y_2)(1-Y_3).   (2)
```

Its cubic Boolean multilinear coefficient is `-1`, and it has one nonzero
Boolean entry; a ternary equality table has two and no cubic coefficient.
Thus even a network starting with a trivalent equality and unary tensors
can acquire a non-equality packet tensor in a zero-mode child. This does
not assert that the entire child contraction has a nonzero cubic mode term:
packet tensors and original vertex tensors are both present in the child,
and the child is later repacked and deformed. The statement only refutes
closure of the *individual input table family* under the specified child
construction. A successor may find a broader invariant using their joint
structure.

## 5. Cost and unresolved obligations

No new algorithm, asymptotic mode count, or SAT bound follows from (1) or
(2). The total number of group vertices can grow with the input, and the
formal weighted count includes coupled modes, recursive packet tensors,
precision and recovery. It is not valid to replace that global count by
10 per equality or to infer a smaller alpha from the small example. The
accepted reduction branches, queries, descriptions, entry computations,
recursion, precision, recovery and space bounds remain the baseline; no
changed cost is claimed.

A concrete next question is whether a joint invariant of old vertices and
packet tensors, retained through *repacking*, yields a uniform weighted
support bound. It must cover clauses as well as equalities, cancellation
modulo the actual precision, every child and every group. Alternatively,
construct admissible large packet families with sufficiently many nonzero
low-weight terms modulo the real taper to rule out a named support-only
strategy. The finite rational example does neither.

## Source references

The fixed-density network appears at `subsec:sharp-fixed-density` in the
frozen quantitative reduction. Packet orientation, deformed contraction,
mode budget and child tensors are `lem:tensor-packets`,
`eq:tensor-deformed-contraction`, `eq:tensor-mode-budget` and
`eq:tensor-recursion-identity` in the frozen quantitative contraction.
Hashes and upstream attribution are in the root `SOURCES.json`. The Newton
identity and its integral validity at source points are credited to the
local [predecessor](../cauchy-newton-modes/PROOF.md). The small-packet
support example and the child-table observation are the present scope.
