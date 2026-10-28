# Clustered Newton modes surviving the actual taper

This is an author-checked argument, not an independent review. The owner-accepted
OpenAI theorem is a premise. PR #4 supplies the Newton modes and source-point
integrality. [PR #105](https://github.com/1337isnot1337/3-SAT/pull/105)
(head `f5ad028ac97d208ca95369db0f56e2b3b974c2f2`) gives a balanced full-packet construction with
`exp(Omega(M/u^2))` precision-surviving summands. This continuation clusters
the rows, sharing their odd denominators, and obtains `exp(Omega(M/u))` for
a different explicitly packed family. The proof below is self-contained
relative to the accepted source and PR #4; PR #105 need not be merged first.

## Statement and scope

For arbitrarily large input-size parameters, there is an explicitly
constructible bounded-degree Boolean tensor network, a specified valid root
packing, and an allowed interpolation evaluation set containing `zeta=1`
for which the general Newton expansion at `t=1` has at least

```
exp(Omega(M/sqrt(u(a+2)))) = exp(Omega(M/u))
```

distinct complete child-product summands that satisfy the source's weighted
mode budget and are nonzero modulo its prescribed child precision. At the
root `a=2u`. The input uses unary pinned/unpinned and trivalent equality
tables. It is disconnected and easily simplified. The source's particular
default labeling need not choose the specified valid packing, and nonzero
summands may cancel or be aggregated. No SAT lower bound, algorithmic speedup,
or lower bound for all contraction methods follows. This still falls short
of the formal `exp(Theta(M/sqrt(u)))` enumeration scale.

## 1. A constant fraction of full packets

Let `s=2^N`, `u=floor(epsilon N)`, `a=2u`, `L=2^a`, `r=64`,
`D_arr=r^(2a)=L^12`, and `B_pad=L floor(s/(L D_arr))`. Take `N` large.
Put `B_pad` real edges in every ordered pair-label class and allocate them
to packets by the source orientation rule. Then

```
M=B_pad D_arr=s-O(L D_arr),
```

all pair-class loads are equal, the collision variance is zero, every symbol
in every coordinate has exactly `M/r` row ports and column ports, and all
`M/L` packets are full. As `L<=s^(2 epsilon)` and `48 epsilon<1/10`, the
source's root packing inequalities, active-call condition `M>H`, degree
constraint and `M<=s` hold for all sufficiently large `N`.

Select packets whose coordinate-zero pair is unequal and whose pairs in
coordinates one and two are equal. Eligibility is invariant under changing
packet orientations, so counting ordered label classes shows that their
fraction is exactly `(1-1/r)/r^2`; the number `P` is `Theta(M/L)`.

Choose

```
b = floor(L/[1000 sqrt(u(a+2))]).
```

For sufficiently large `N`, `b>=1` and `4b<=L/2`. In each eligible packet
use even slots as target rows. The rows with source indices
`r=4j,4j+1,4j+2`, for each `j=0,...,b-1`, have identical complete vertex
labels: their slot numbers `2r` differ only in bits one and two, whose
coordinate pairs are equal. Replace each such triple by a ternary equality
vertex. Every other row vertex is unary `(1,1)`.

Pin all odd-slot columns to zero. Among even columns, pin all to zero
except the last one, at `j=K-1` with `K=L/2`, which is pinned to one.
Noneligible packets have unary `(1,1)` tensors at every port. All vertices
and labels are explicit, every edge remains in its originally allocated
full slot, and the maximum degree is three. This is a general input tensor
network, not asserted to be the literal output of the fixed-density
SAT-to-network reduction.

## 2. Mode values and common signs

At `i=0`, `t=1`, `zeta=1`, put `T=2L+1` and
`G=C(T)/C'(0)`. For a selected row indexed by `r` and mode `k`, the general
Newton row coefficient is

```
a_rk = G/(T+2r) c_k phi_k(1/(T+2r)).
```

Every selected source mode `0<=k<b` evaluates to the two-adic unit
`phi_k(K-1)`, since `K` is a power of two, all binomial coefficients in
row `K-1` are odd, and the denominators are odd. All local-column bits are
zero. As in PR #105, `sign(a_rk)=(-1)^(k+1)` for every selected row.

A ternary equality's multilinear extension is
`1-z1-z2-z3+z1z2+z1z3+z2z3`. Its degree-`d` contributions to one mode
monomial all have sign `(-1)^(sum k beta_k)`, independently of the chosen
rows. The product of `b` such equalities therefore has no rational
cancellation in any fixed mode coefficient. Every squarefree monomial in
the first `b` modes occurs: assign at most one mode occurrence to each
triple. The pinned source factors are nonzero. This supplies `2^b` nonzero
local summands per selected packet.

## 3. Clustered odd denominators and valuation

Write `B_r=T+2r`. Cancelling the `k!` in `phi_k` gives

```
a_rk/G = 2^k k! (1-2k^2) prod_{h<k}(1-h B_r)
          / prod_{h<=k}(B_r-2h).                         (1)
```

All denominator factors are odd. For the selected rows and `0<=k<b`,
the integer `r-h` lies in `[-(b-1),4b-2]`; hence at most `5b` distinct
odd factors occur across **all** these coefficients. Let `D` be their
product, with each distinct factor taken once. Because `4b<=L/2`, all
factors are positive and below `4L`. Equation (1) implies

```
log2 D <= 5b(a+2),
log2 |D a_rk/G| <= 20b(a+2).                            (2)
```

The second inequality follows by counting at most `b` factors of size at
most `4L^2`, the `k!`, the explicit power of two and the scalar; the stated
constant overestimates each contribution. The odd `D` is common to all
selected row coefficients, not a separate product for every row-mode pair.

For a selected squarefree monomial of degree `d<=b`, its row coefficient
is a sum of at most `(3b)^d` products of `d` row coefficients. Factoring
out `G^d` and using common denominator `D^d`, its numerator is a nonzero
integer by the common-sign argument, with binary logarithm at most
`25 d b(a+2)`. Since `v2(G)=a+1`, proved from factorial valuations in
PR #105 and directly from the frozen definition of `C`, the local summand
has valuation at most

```
d [a+1+25b(a+2)].                                      (3)
```

The source mode factors are units, and degree zero gives one. This is an
upper bound on the actual valuation, not an estimate from numerical
magnitudes or a claim that arbitrary tensor entries have this property.

## 4. Global precision and count

Independently choose an arbitrary subset of the first `b` modes in each
eligible packet; set every other mode exponent to zero. There are `2^(P b)`
distinct tuples. The corresponding complete child-product summand factors
into the selected local summands and powers of two from the free unary
columns of noneligible packets. Thus its valuation is at most

```
M + P b [a+1+25b(a+2)]
 <= M + (M/L)b(a+1) + 25 M b^2(a+2)/L.                 (4)
```

Using the chosen `b`, the last term is at most `0.000025 M L/u`; the
middle term is `o(M L/u)`, as is `M`. The source prescribes
`p_t=p+8 ceil(3M/u)L+8M(a+1)>=24 M L/u`. Hence every selected complete
summand is nonzero modulo `2^p_t` for sufficiently large `N`.

Also `w_k<=a+1+3k`, so the total source weight of each selected tuple is
at most

```
P b(a+1+3b) <= (M/L)b(a+1+3b) < p_t.
```

All these tuples are retained by the actual mode budget. Since
`P=Theta(M/L)` and `b=Theta(L/sqrt(u(a+2)))`, their number is
`exp(Omega(M/sqrt(u(a+2))))`. At the root `a=2u`, giving the claimed
`exp(Omega(M/u))` scale. Nothing here shows that enumeration of these
terms is unavoidable or that their sum cannot be simplified.

## Verification and remaining gap

The [checker](verify.py) verifies exact common-denominator divisibility,
entry-size and selected-summand valuation bounds, all source units, full
Newton kernel identities and the whole local contraction for `(L,b)`
`(16,2),(32,3),(64,4)`. These are deliberately small checks, not the
source asymptotic schedule or an independent review of the proof. Source
labels are `lem:tensor-packets`, `lem:tapered-hermite`,
`eq:tensor-mode-budget`, and `eq:tensor-recursion-identity`; hashes and
licenses are in the root `SOURCES.json` and hash-bound verification output.

The remaining gap to `M/sqrt(u)` is a factor `sqrt(u)`. Closing it by this
route needs a sharper uniform upper bound on valuations of mixed-mode
coefficients, not just on individual modes. Any bound claim would still
need default-packing, aggregation, reduction and full-cost analysis.
