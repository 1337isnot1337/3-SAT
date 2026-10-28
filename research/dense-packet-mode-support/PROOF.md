# Full-packet Newton support at the source precision

This is an author-checked argument, not an independent review. The accepted
OpenAI theorem is a premise. PR #4 supplies the general Newton modes and
their integrality; [PR #41](https://github.com/1337isnot1337/3-SAT/pull/41),
head `e0ed968e3deea66ee00d645793a4c32ee0fd2c9f`, supplies the single-packet
common-sign observation. The present construction uses full packets, pinned
columns, many disjoint packets and a uniform two-adic upper valuation bound.

## Statement and limits

For arbitrarily large input-size parameters, there is an explicitly
constructible bounded-degree Boolean tensor network, an explicitly specified
valid root packing, and an allowed interpolation evaluation set containing
`zeta=1`, for which the general Newton expansion at `t=1` has at least

```
exp(Omega(M / (u(a+2)))) = exp(Omega(M/u^2))
```

distinct complete child-product summands which lie within the source's
mode-weight budget and are nonzero modulo its prescribed child precision.
Here `M` is the number of edges, `u=floor(epsilon log2 s)` and `a=2u` at
the root. The `Omega` constant is absolute. These summands are a specific
subset; other terms are not classified.

The construction uses only trivalent equality and unary `(1,1)`, `(1,0)`
and `(0,1)` tables, is disconnected and easily simplified. Its specified
packing satisfies the source's explicit packing guarantees, but need not
be the packing selected by the source's particular conditional-expectation
labeling. Nonzero summands can cancel after addition; a different algorithm
can aggregate or eliminate them. This is neither a lower bound on SAT nor
on all implementations of the accepted contraction. In particular this
does **not** reach the formal `exp(Theta(M/sqrt(u)))` scale. All-size proof
and the implicit constants await independent review.

## 1. Balanced full packets and bounded-degree tensors

Let `s=2^N` with `N` sufficiently large, and use the source's root choices

```
u=floor(epsilon N),  a=2u,  L=2^a,  r=64,
D_arr=r^(2a)=L^12,  B_pad=L floor(s/(L D_arr)).
```

Every ordered pair of labels in `[r]^a` gets exactly `B_pad` real edges;
combine them into full packets by the source orientation rule. The graph
has `M=B_pad D_arr=s-O(L D_arr)` edges. Every label-pair load is exactly
`B_pad`, so the collision variance is zero. Each symbol occurs at exactly
`M/r` real ports on each side and in each coordinate. The packet count is
`M/L`. The source root packing inequalities hold for large `N` because
`L<=s^(2 epsilon)`, `D_arr^2<=s^(48 epsilon)` and `48 epsilon<1/10`;
also `M>H`, `M<=s`, and `2L<=ceil(s^(9/10))`.

A packet is eligible if the unordered symbol pair in coordinate zero is
unequal and at least two of its other `a-1` coordinate pairs are equal.
Counting ordered label pairs gives an eligible packet fraction

```
(1-1/r) Pr[Bin(a-1,1/r)>=2],
```

which tends to `(r-1)/r`. Indeed eligibility depends only on the coordinate
pairs, and every full packet contains the same number `L` of real slots.
Thus the number `P` of eligible packets is `Theta(M/L)`.

In each eligible packet take even slots as the target rows and their
matching even columns as the source tile. The row symbol in coordinate zero
is the smaller symbol and is constant on these rows. If `h>=2` other
coordinate pairs are equal, each complete row label occurs `2^h` times
among the even slots. Group those rows into triples of equal complete label;
use a ternary equality vertex for each triple and leave any remainder unary
`(1,1)`. Since `floor(2^h/3)>=2^h/4`, there are at least `L/8` such
vertices. Odd-slot row vertices are unary `(1,1)`. The maximum degree is 3.

In the same packet pin all odd columns to 0 with unary `(1,0)`. Pin all
but the last even column to 0 and the last even column to 1 using unary
`(1,0)` and `(0,1)`. All vertices of noneligible packets are unary
`(1,1)`. This network and its labels and slots can be constructed in time
polynomial in `s`. The pinned unary tables are permitted tensor inputs;
we do not claim the network is the literal output of the source's
fixed-density SAT-to-network reduction.

## 2. A full family of nonzero local coefficients

Use the general Newton expansion at `i=0`, `t=1`, `zeta=1`, so
`T=2L+1`, and put `K=L/2`. Odd columns in the target group are pinned zero,
so each target row has no local contribution. For mode `k<K`, write
`a_xk` for its row coefficient and `phi_k(j)` for its source coefficient.
The only nonzero source bit is at `j=K-1`. Every `phi_k(K-1)` is a
nonzero two-adic unit: its numerator is `binom(K-1,k)`, odd because
`K` is a power of two, and its denominator is odd.

As in PR #41, `sign(a_xk)=(-1)^(k+1)` for every real target row `x`.
A ternary equality has the exact multilinear extension

```
1-z1-z2-z3+z1z2+z1z3+z2z3.
```

Consequently every term contributing to one mode monomial `beta` has row
coefficient sign `(-1)^(sum k beta_k)`. Since all columns are pinned, no
extra sum can cancel this coefficient. Distributing at most two mode
occurrences to each of the at least `L/8` equality vertices shows that all
monomials of total degree at most `L/4` are nonzero over the rationals.
After multiplying the source factors, each such local summand is nonzero.
All chosen source factors are two-adic units.

## 3. An upper valuation bound

Let `b_x=T+x`. The Newton formula simplifies to

```
a_xk = [C(T)/C'(0)]
       * 2^k k! (1-2k^2) prod_{h<k}(1-h b_x)
       / prod_{h<=k}(b_x-2h).
```

All denominators `b_x-2h` are distinct odd positive integers below `4L`.
Let `D` be the odd denominator of `C(T)/C'(0)` in lowest terms multiplied
by the product of all odd positive integers below `4L`. Then `D` is odd,
`D a_xk` is integral, and elementary factor-size bounds give, uniformly
in `x,k`,

```
log2 D <= 6 L(a+2),       log2 |D a_xk| <= 20 L(a+2).    (1)
```

For example the reduced common denominator divides the odd part of
`L!(L-1)!`; the remaining product has fewer than `2L` factors below
`4L`; and the displayed numerator has at most `K+O(1)` factors of size at
most `4L^2`, plus `k!` and `C(T)`, with at most `2L` factors below `4L`.
The constants in (1) deliberately overestimate these contributions.

Consider a **squarefree** mode monomial of degree `d<=L/4`. Its row
coefficient is a sum of at most `L^d` products of `d` row coefficients:
assign each distinct mode to one of the at most `L` target rows. Over
common odd denominator `D^d`, the numerator is a nonzero integer of
absolute value at most `L^d 2^(20d L(a+2))`; common signs give nonzero.
Therefore its two-adic valuation is at most

```
d [20 L(a+2)+a] <= 30 d L(a+2).                         (2)
```

The source factor is a unit, so (2) also bounds the local summand. Degree
zero gives the value one. Unlike a lower valuation bound, (2) ensures that
these particular nonzero rational terms remain visible at sufficiently
large precision.

### Exact excess for the first mode in one placement

For a packet with all other coordinate pairs equal, group the first
`3q` even-slot rows into consecutive triples, with `K=L/2` and
`q=floor(K/3)`, leaving the remaining zero, one or two rows unary. This
is one permitted placement within the construction, not a claim about
all eligible packets. For `L=2^a` with `a>=3`, the coefficient of the
first Newton mode has **exact** valuation

```
a+1                  if a is odd,
a+3                  if a is even.                       (3)
```

The source factor is one for this mode. To prove (3), set
`G=C(2L+1)/C'(0)`. Since `v2(n!)=n-s_2(n)`, direct evaluation of
`C(2L+1)=(3L+1)!/(L+1)!` and `|C'(0)|=L!(L-1)!` gives
`v2(G)=a+1`. The relevant coefficient is `-G S`, with

```
S = sum_{r=0}^{3q-1} 1/(2L+1+2r).
```

In the sum `S_full` over all `0<=r<K`, pair `r` with `K-1-r`.
The two odd denominators add to `5L`, so every pair is divisible by
`2^a` in `Z_(2)`. If `a` is odd, `K=1 mod 3`: one final reciprocal
is removed from `S_full`, making `S` odd. If `a` is even, `K=2 mod 3`:
the two removed denominators are `3L-3` and `3L-1`, and their reciprocal
sum has numerator `6L-4` of valuation exactly two. Here `a>=4`, so
subtracting it from the multiple of `2^a` leaves valuation exactly two.
This proves (3). The checker verifies `a=3,...,9`. The result bounds only
this one coefficient and does not establish the many-mode precision scale.

### Two more single-mode coefficients by telescoping

In the same placement, write `n=3q`, `T=2L+1`, and let `A_k` be the sum
of row coefficients of mode `k` over `r=0,...,n-1`. The sign from the
equality's linear term does not change its valuation. The next two exact
valuations are

```
v2(A_1) = a+2 + (0 if a is odd, 1 if a is even),
v2(A_2) = a+5.                                           (4)
```

For mode 1, the row summand is
`-2G/[(T+2r)(T+2r-2)]`. Consecutive terms telescope to

```
A_1 = -2G n/[(T-2)(T+2n-2)].
```

Both denominator factors are odd. If `a` is odd then `n=K-1` is odd;
if `a` is even then `n=K-2` has valuation one. This gives the first line.

For mode 2, the row summand is
`56G(b-1)/[b(b-2)(b-4)]`, `b=T+2r`. Partial fractions and telescoping give

```
A_2 = 7G [3/(T-4)+1/(T-2)
          -3/(T+2n-4)-1/(T+2n-2)].
```

Put `v=T-4`. The bracket equals `8n Q` divided by four odd factors, where
`Q=v^2+(2n+3)v+3n+3`. Since `v=1 mod 4`, `Q=3+n mod 4`. When `a` is odd,
`n=3 mod 4`, so `v2(n)=0` and `v2(Q)=1`. When `a` is even, `n=2 mod 4`,
so `v2(n)=1` and `v2(Q)=0`. In both cases the bracket has valuation four,
proving the second line of (4). The checker independently sums the source
Newton coefficients and compares the telescoping expressions for
`a=3,...,9`. These are three separate degree-one mode monomials, not a
bound on arbitrary mixed-mode coefficients.

## 4. Exponent count and the source precision

Choose

```
b=floor(L / (1000 u (a+2))).
```

For sufficiently large `N`, `b>=1` and `b<=L/4`. In each eligible packet
independently select an arbitrary subset of its first `b` modes, with each
selected exponent equal to one. Set all other mode exponents to zero.
The resulting `2^(P b)` tuples are distinct. Sum over the bits of each
packet: each eligible packet contributes its nonzero local summand, while
noneligible packets contribute a power of two from their free unary
columns. Thus each complete summand has valuation at most

```
M + 30 P b L(a+2) <= M + 0.03 M L/u.                    (5)
```

The source's actual precision at `t=1` is
`p_t=p+8 ceil(3M/u)L+8M(a+1)`, hence `p_t>=24ML/u`. For large `N`, the
right side of (5) is strictly below `p_t`. All complete summands are
therefore nonzero modulo `2^p_t`.

The Newton mode weight satisfies `w_k<=a+1+3k`. The total weight of every
chosen tuple is at most

```
P b (a+1+3b) <= (M/L) b (a+1+3b) < p_t,
```

for sufficiently large `N`. Thus every chosen tuple is actually retained
by the source's weighted enumeration. Finally `P=Theta(M/L)` and
`b=Theta(L/[u(a+2)])`, proving the stated count. The exact toy checks do
not establish any of the asymptotic packing or valuation claims on their
own.

## Sources and open question

The upstream `lem:tensor-packets`, `eq:tensor-mode-budget`,
`eq:tensor-recursion-identity`, and `lem:tapered-hermite` are in the frozen
[quantitative contraction](../../upstream/openai-eth-2026/build/quantitative-contraction.tex).
The original source and license hashes are in the root
[SOURCES.json](../../SOURCES.json). PR #4 gives the mode formula and PR #41
is credited above for the local sign mechanism. Work is substantially
OpenAI Codex assisted.

The remaining quantitative gap is from `M/u^2` to `M/sqrt(u)`. Closing it
would require a much sharper upper valuation bound for the summed row
coefficients, while retaining balance, explicit tables and the actual taper.
Even such a result would still need to address simplification, aggregation,
default packing, and all costs before any algorithmic conclusion.
