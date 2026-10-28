# Shift-resistant Boolean unary packets

This is an author-checked information obstruction for the source graph-only
packing and a specified local-data interface. It is not an algorithmic lower bound and does not
realize the tapered polynomial in the predecessor's Section 5.

## Claim

There is a deterministic polynomial-time construction, in `L`, of a binary
word `b` of each power-of-two length `L >= 1024` such that, for every
`t in {-L,...,L-1} \ {0}`,

```
N_t = #{x in [0,L): b_x != (b_{x+t} if 0 <= x+t < L else 0)} > L/4.
```

Take `q` full `L`-slot packets, `M=qL` independent edges, and one unary
row and column tensor on each edge, both equal to the indicator of the
corresponding bit of `b`. The canonical entries are 0 or 1, all degrees
are one, and the tensor network's undeformed contraction is 1. At each
nonzero node, the entire shifted deformation polynomial is coefficientwise
divisible by `2^ceil(qL/4)` over the two-adic integers. Thus its complete
local jets at all nonzero nodes modulo that power of two coincide with
those of the zero network, although the origin parities differ. All nodes
and all jet orders are supplied; a recovery rule that sees only these
residues cannot distinguish the two networks.

This full-packet statement does not require a specific balancing choice.
The next section extends the conclusion, with a smaller constant, to every
source graph-only packing satisfying the packet-count bound.

## Word construction

Choose independent uniform bits `B_x`. Extend the word by zero outside its
range. For a fixed nonzero `t`, each of the `L` disagreements has mean
`1/2`, so `E N_t=L/2`. Changing one bit affects at most two comparisons.
The bounded-difference exponential moment estimate gives, for `eta>0`,

```
E exp(-eta N_t) <= exp(-eta L/2 + eta^2 L/2).
```

This follows from the Doob martingale and Hoeffding's lemma applied to
increments with range at most 2. Put `eta=log(8/7)` and

```
Z(b) = sum_{t != 0} (8/7)^(L/4) (7/8)^N_t.
```

There are `2L-1` terms. Since `1/8 < eta < 1/7`,

```
E Z <= 2L exp(-L/32 + L/98) < 1,   L >= 1024.
```

The last inequality holds at 1024 and its left side decreases thereafter.
Assign bits in order, choosing the value with smaller conditional `E Z`.
The final `Z` is below 1, so every summand is below 1 and every `N_t>L/4`.

This is a uniform deterministic polynomial-time construction. For a fixed
`t`, the interactions connect `x` and `x+t`; their graph is a union of
paths. The weight `(7/8)^N_t` factors into binary edge weights and unary
boundary weights. A two-state transfer on each path computes the exact
conditional expectation in polynomial time. Its rational numerators and
denominators have `O(L)` bits. There are `L` choices, two trials per
choice, and fewer than `2L` shifts; a straightforward implementation uses
`O(L^3)` arithmetic operations on `O(L)`-bit integers. This construction
is evidence of uniformity, not a practical performance claim. The checker
compares this transfer with exhaustive enumeration for small paths.

## Arbitrary occupied packets

The full-packet condition can be removed for the source packing. Let `R`
be an arbitrary set of `k` real slots in a packet. There is a bit assignment
supported on `R` whose mismatch count exceeds `k/4` for every nonzero grid
node whenever

```
k >= K = 128 ceil(log_2(2L)).
```

To prove this, independently assign each real slot a uniform bit and set
all other slots to zero. Count mismatches only at real rows. Each of the `k`
terms still has expectation `1/2`; every bit influences at most two terms.
The same exponential-moment bound, now with `k` instead of `L`, yields

```
E Z <= 2L exp(-k/32 + k/98) < 1.
```

The inequality follows from `k>=K`: the exponent is less than
`-2 log(2L)`. Conditional expectation makes the assignments deterministic.
For each `t`, the occupied-slot interaction graph is a disjoint union of
paths (some singletons); use the same two-state transfer, with a boundary
weight for every row whose shifted column is absent. All intermediate
integers have `O(k)` bits and the algorithm is polynomial in `L` and `k`.

Take the source graph of `M` independent unary edges, and fix its graph-only
packing. The source gives at most `3M/L` packets and each real edge has
the same occupied slot on both sides. Set both unary indicators to the
constructed bit on each packet with at least `K` real slots. On each smaller
packet set every bit to zero. The latter packet contributes identically 1
to the deformation and costs no negative valuation. If

```
L >= 6K,
```

then small packets contain at most `(3M/L)K <= M/2` real edges, and the
large packets contain at least `M/2`. The sum of mismatch counts at any
nonzero node exceeds one quarter of the large-packet edge count. Thus the
entire shifted network polynomial is divisible by `2^ceil(M/8)` at every
nonzero node, while its origin contraction is 1. The all-zero network has
origin parity 0 and the same residues at all nonzero nodes. This applies
to every graph-only packing satisfying the source packet-count bound, with
tensor entries assigned after the packing; it does not require all packets
to be full. The source has growing powers of two `L` in its asymptotic
active regime, so the stated numerical condition eventually holds.

The zero comparison is produced on the same graph and packing by replacing
one row unary indicator with the identically zero table. Its deformation is
identically zero. Hence the difference is an information obstruction for
local-data-only recovery, even with arbitrary nonlinear processing and all
jet orders; a tensor-aware algorithm may read the descriptions directly.

## Stronger simultaneous obstruction on retained levels

There is a second Boolean unary family with a larger threshold at every
active node `v_2(t)<u`. It is a separate input family from the all-nonzero-
node witness above. Put `P=2^u`, `h=L/P`, assume `1<=u<=a`, and suppose

```
M/h >= 1280 ln(2P).
```

For any graph-only packing with at most `3M/L` packets, canonical Boolean
unary tensors can be constructed deterministically in polynomial time so
that their undeformed contraction is 1, but every complete shifted
polynomial at an active node is divisible by

```
2^((floor(M/8)+1)*(a+2-u)).
```

The zero network gives identical residues and even origin parity. The
source active parameters satisfy the displayed size condition: its packing
condition `M >= L D_arr` gives `M/h >= P D_arr`, and `D_arr=r^(2a)`
with `r=64` is more than enough for `a>=u>=1`. The degree, tensor entries,
packing and coefficient ring remain those of the frozen source.

For each packet `j`, independently choose a length-`P` binary word
`b_j`. A real column `y` is fixed to `b_j[y mod P]`. A real row `x` is
fixed to 1 if `b_j[x mod P]=1`, and is unrestricted otherwise. Its local
factor is therefore either `sum_y W_xy(T)b_j[y mod P]` or 1. At the
origin the contraction equals 1.

For a residue shift `d` in `{1,...,P-1}`, define `N_d` as the number of
real rows `x` with `b_j[x mod P]=1` and `b_j[(x+d) mod P]=0`. Each row
is counted with probability 1/4, so `E N_d=M/4`. A word bit affects only
rows in two residue classes, at most `2h` rows. There are at most
`Q P <= (3M/L)P` word bits, so the sum of their squared bounded
differences is at most `12 M h`.

Set `eta=-ln(1-1/(64h))`, `q=exp(-eta)`, and `m=floor(M/8)`. Hoeffding's
lemma applied to the bounded-differences martingale gives

```
E sum_{d=1}^{P-1} q^(N_d-m)
  <= P exp(-eta M/8 + (3/2) eta^2 M h)
  <= P exp(-M/(640h)) < 1.
```

For the second inequality use `1/(64h) <= eta <= 1/(63h)`; the final
inequality follows from the displayed size condition. Fix all word bits
by conditional expectation. The final sum is below 1, so `N_d>m` for
every nonzero `d`. This construction is deterministic and polynomial in
the network size. For a given `d`, the weighted interactions on a packet's
residues are `n_r b_r(1-b_{r+d})`, where `n_r` counts real rows of residue
`r`. The directed permutation `r -> r+d` decomposes into cycles. A two-state
transfer computes each cycle's exact conditional expectation; multiply
across cycles and packets. With rational `q=(64h-1)/(64h)`, intermediate
integers have polynomial bit length. The finite cycle checker compares
these expectations with brute force.

Now let `t` be active, so `d=t mod P` is nonzero. For each counted row,
all columns with bit 1 have `y-x` distinct from `t` modulo `P`. Hence
`v_2(t-(y-x))<=u-1`. The Cauchy formula factors as in the next section
and shows that every such `W_xy(t+alpha z)` is coefficientwise divisible
by `2^(a+2-u)`. The whole constrained-row factor has the same divisibility.
The other row factors are integral, so multiplying the more than `m`
counted factors proves the stated bound at every active node at once.

This is `Omega(M(a-u))` precision for the source's active-node recovery
interface, stronger than the prior `Omega(M)` construction when `a-u`
grows. It still does not match the generic `Theta(M D_i/u)` threshold,
which can be exponentially larger in `a-i`, and does not imply any lower
bound against a tensor-aware or different-deformation algorithm.

## An extra cancellation for full packets

For the periodic construction, suppose additionally that every used
packet is full. Then each selected-row polynomial is divisible by
`2^(2(a-u)+3)` at each active node if `a>u`, gaining `a-u+1` bits
beyond the previous bound. If `a=u`, use the earlier two-bit bound. With the same conditional-expectation word construction,
complete active-node data vanish modulo

```
2^((floor(M/8)+1)*(2(a-u)+3))   when a>u.
```

This improvement is specific to full packets; it does not change the
arbitrary-occupancy result. To prove it, fix one selected row, one active
node `t`, and one residue `y_0 mod P` whose word bit is 1. Because the
row is selected, `t+x-y_0` has valuation at most `u-1`. All `h=L/P`
columns `y_0+jP` are present. Write `T=t+alpha z` and
`A=T-(y_0-x)`. In the two-adic formal power-series ring,

```
sum_{j=0}^{h-1} W_{x,y_0+jP}(T)
 = W_{x,y_0}(T) sum_{b>=0} (P/A)^b S_b,
S_b = sum_{j=0}^{h-1} j^b.
```

The series converges coefficientwise because `P/A` has positive
two-adic valuation. If `h=2^k`, every `S_b` is divisible by `2^(k-1)`
for `k>=1`; for `b=0` it is divisible by `2^k`. This follows by induction
on `k`, pairing `j` and `j+2^(k-1)`. Thus the `b=0` term is divisible
by `2^k`, and every term with `b>=1` is also divisible by `2^k` because
`P/A` is even. The conclusion is immediate when `h=1` as well.

The first Cauchy factor has content at least `a+2-u` by the previous
argument, and the parenthesized series has content at least `k=a-u`.
For `k>=1`, there is one more bit: if `P/A` is divisible by four, the
first Cauchy factor has one extra bit because `v_2(t+x-y_0)<=u-2`.
Otherwise `P/A` has valuation exactly one. Modulo `2h` the only terms
that can survive in the parenthesized series are `h` and `(P/A)S_1`;
since `S_1=h(h-1)/2`, these two terms cancel modulo `2h`. The higher
terms are multiples of `2h`. Thus in either case the product has content
at least `2k+3`. Summing over the word's 1-residues preserves that
divisibility. The
selected-row product and the other integral row factors then yield the
claimed bound. The bound `2k+3` is sharp uniformly in the parameters: let `a>=3`,
`u=2`, `P=4`, `x=0`, `t=1-L`, and use the word that is 1 only on residue
0. Here `A(0)=1-L` is odd, so `P/A` is divisible by 4. After dividing
by `h=2^(a-2)`, the parenthesized series has odd constant term: its
`b=0` term is 1 and every other term is even. The linear coefficient of
the diagonal Cauchy factor has valuation `a+1`, so the selected-row
linear coefficient has valuation exactly `a+1+(a-2)=2k+3`.

The full-packet bound fails for a partial packet: take `L=4`, `P=2`,
real slots `{0,2,3}`, word `(0,1)`, selected row `x=3` and node `t=-3`.
The sole 1-column is 3, so the row is the diagonal polynomial `W_33`.
Its shifted content is exactly 3 by the predecessor's diagonal formula,
while the full-packet bound would require 5. Exact finite controls are
included in `verify_periodic.py`; they are examples, not a proof for all
`L`.

## Complete blocks inside partial packets

The cancellation also holds in partial packets when its supporting columns
come in complete blocks. Fix `B=2^b` with `1<=b<=a-u`, so `B<=h=L/P`.
In each packet and residue `r mod P`, divide the `h` slot indices
`j=0,...,h-1` into aligned blocks of `B` consecutive indices. Mark a
block only if every one of its slots `r+jP` is real. Let `N` be the number
of marked slots across the network. Assume

```
N/h >= 360 ln(2P).
```

There is a deterministic polynomial-time Boolean unary construction whose
origin contraction is 1 and whose complete jets at every active node are
divisible by

```
2^((floor(N/8)+1)*(a+2-u+b+1)).
```

To construct it, choose a binary word for each packet as above. Fix a
column to 1 only when its slot is marked and its residue bit is 1; all
other columns are fixed to 0. Fix the corresponding marked rows to 1 and
leave all other rows unrestricted. At the origin this still contracts to
1. A marked row counts for residue shift `d` when its bit is 1 and the
shifted residue bit is 0. The expected count is `N/4`.

If `n_{j,r}` is the number of marked slots in packet `j` and residue `r`,
then `n_{j,r}<=h`, `sum n_{j,r}=N`, and changing one word bit changes
the count by at most `n_{j,r}+n_{j,r-d}`. The sum of squared differences
is therefore at most `4hN`. Set `q=1-1/(16h)`, `eta=-ln(q)` and
`m=floor(N/8)`. Bounded differences and `1/(16h)<=eta<=1/(15h)` yield

```
E sum_{d=1}^{P-1} q^(N_d-m)
 <= P exp(-eta N/8 + eta^2 h N/2)
 <= P exp(-N/(180h)) < 1.
```

The displayed size assumption gives the strict final inequality. The same
cycle-transfer conditional-expectation algorithm fixes all word bits in
polynomial time and yields more than `m` selected rows for every active
residue.

For a selected row and a marked block, the `B` columns form a consecutive
arithmetic progression of step `P`. Apply the preceding power-sum
argument with `h` replaced by `B`, using the first column of that block as
`y_0`. Its Cauchy sum is divisible by `2^(a+2-u+b+1)`; sum over marked
blocks and multiply the selected-row factors. Other row factors are
integral. The comparison zero network again gives identical active-node
data at the stated precision and opposite origin parity.

The bound is deliberately expressed in terms of `N`. A packet can have
occupancy fraction `1-1/B` while containing no marked block: omit one
slot from every aligned block. Thus the source's total packet-count bound
alone does not guarantee `N=Omega(M)`. The checker `verify_blocks.py`
replays selected rows on four bounded occupancy patterns; no generic
packing-density conclusion or SAT bound follows.

## Deformation calculation

Let `C(T)=product_{s=-L}^{L-1}(T-s)` and `alpha=2L`. The source's
`W_xy(T)` is `C(T)/(C'(0)(T-(y-x)))`. For every node `t`,
`C'(t)/C'(0)` is a two-adic unit: the differences from `t` to the other
`2L-1` grid points form all the nonzero residue classes modulo `2L`, as do
the differences from 0. For every `s != t`, `v_2(t-s)<=a` with
`L=2^a`; hence `alpha/(t-s)` is even. Factoring each shifted Cauchy entry
at `t` gives

```
W_xy(t+alpha z) = 1[y-x=t] * unit + 2 Z_2[z],
```

where the displayed unit is the constant `C'(t)/C'(0)` and is odd. When
`y-x != t`, the missing root gives a factor `alpha z/(t-(y-x))`, also
coefficientwise even. This proves the congruence for the entire polynomial,
not only its value at `z=0`.

The column tensors fix `X=b`. The row tensor at `x` fixes `Y_x=b_x`,
so the packet polynomial is

```
P_b(T) = product_x l_{b_x}(sum_y W_xy(T) b_y),
 l_1(z)=z,  l_0(z)=1-z.
```

At a nonzero shifted node, each factor is an integral polynomial; if
`b_x` differs from the zero-extended `b_{x+t}`, its entire polynomial
is even. Thus `P_b(t+alpha z)` is divisible by `2^N_t`. At the origin
`W(0)=I`, so `P_b(0)=1`. The `q` independent packets multiply their
polynomials, giving divisibility by `2^(qN_t)` and hence by
`2^ceil(qL/4)`. A network with one unary tensor identically zero has
identically zero deformation and origin parity zero.

## Cost and limits

The word construction uses polynomial time and space in `L`; writing the
`2M` unary tables uses `O(M)` bits once the word is available. The
construction needs no randomness after derandomization, no dense tensor
entries, and no preprocessing exponential in `L`. Directly enumerating the
`2^M` assignments is unnecessary. These costs describe the witness,
not a proposed faster SAT algorithm. No reduction branches, queries, modes,
recursive calls, or recovery algorithm are replaced or claimed cheaper.

The predecessor's actual-network witness gives about `M/L` times a node
valuation factor; the construction gives at least `M/8` at every nonzero
node for the source graph-only packing. The separate periodic construction
gives `Omega(M(a-u))` simultaneously at active levels. For the accepted
growing parameters and small valuation `i`,
the generic taper witness has `Theta(M D_i/u)` content, potentially much
larger than `M`; this result does not attain that scale. It does not show
that the specific Section 5 polynomial is tensor-realizable, requires the specified packet-count bound and graph-only packing, and does
not rule out tensor-aware recovery or an alternative deformation.

The source is the frozen OpenAI `quantitative-contraction.tex`, labels
`eq:tensor-cauchy`, `eq:tensor-deformed-contraction` and
`lem:tensor-packets`, commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`.
The predecessor is `research/parity-recovery-precision` at base
`630041c9da3a26edb8c8f59d5f8a4132a188c8bd`. The bounded-difference estimate
and conditional expectation are standard; no novelty claim is made for them.

Concurrent [PR 65](https://github.com/1337isnot1337/3-SAT/pull/65)
uses a most-populated residue class to select at least `ceil(M/P)` rows and
gives valuation-dependent divisibility `a+1-i` per row, plus a jet-order
bound. The periodic random-word construction selects more rows under its
size assumption but guarantees only `a+2-u` bits per selected row uniformly
across active levels; its statement makes no corresponding jet-order claim.
The two bounds have different parameter dependence and should be compared
for the particular node. [PR 52](https://github.com/1337isnot1337/3-SAT/pull/52)
realizes the generic tapered polynomial over a broader coefficient ring,
with different port-budget and Boolean-input limitations. Neither concurrent
package has been independently reviewed here.
