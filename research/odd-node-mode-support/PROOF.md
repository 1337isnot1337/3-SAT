# Odd-node modes realize the formal support scale

This is an author-checked argument awaiting independent review. The accepted
OpenAI theorem is a premise. PR #4 supplies the odd-node Newton expansion
and its source-point integrality. The earlier [PR #105](https://github.com/1337isnot1337/3-SAT/pull/105)
and clustered follow-up study equality tensors with the general Newton
expansion; this argument instead changes to a weighted unary tensor and the
odd-node basis. It is self-contained relative to the accepted source and
PR #4.

## Statement and limitations

For arbitrarily large input-size parameters, there is an explicitly
constructible bounded-degree Boolean tensor network, a specified valid root
packing, and an allowed evaluation set containing `zeta=1`, for which the
odd-node Newton expansion at `t=1` has

```
exp(Omega(M/sqrt(u)))
```

distinct complete child-product summands that both satisfy the source's
weighted mode budget and are nonzero modulo its prescribed child precision.
This matches the order of the formal mode-enumeration upper envelope for
this specified representation and call.

The first construction uses a unary tensor `(1,2)`. Section 5 replaces it
with Boolean two-literal clauses and auxiliary bits while retaining the
same support scale. Neither construction is claimed to be the literal
subdivided SAT-to-network reduction. The source's default deterministic
labeling need not choose the specified valid packing. The network is
disconnected and easily simplified; nonzero summands may be aggregated or
cancel after addition. The result is **not** a SAT lower bound, an
algorithmic time lower bound, or a claim that enumeration is unavoidable.
No improved SAT bound is claimed. All-size claims await independent review.

## 1. Explicit full-packet network

For `s=2^N`, use the source root parameters

```
u=floor(epsilon N), a=2u, L=2^a, r=64,
D_arr=r^(2a)=L^12, B_pad=L floor(s/(L D_arr)).
```

For sufficiently large `N`, put `B_pad` real edges into every ordered
pair-label class and allocate them to full packets by the source orientation
rule. Then `M=B_pad D_arr=s-O(L D_arr)`, every pair-class load is equal,
the collision variance is zero, each symbol in each coordinate has exactly
`M/r` row and column ports, and there are `M/L` packets. The source root
packing inequalities and `M>H` hold for large `N` because
`L<=s^(2 epsilon)`, `D_arr^2<=s^(48 epsilon)` and `48 epsilon<1/10`.

Select every packet whose coordinate-zero symbol pair is unequal. Its
fraction of all packets is exactly `(r-1)/r`, since eligibility is
invariant under swapping packet orientations. Let `P=(r-1)M/(rL)`.
Choose `b` as the largest power of two not exceeding `L/(100 sqrt(u))`.
For sufficiently large `N`, `1<=b<=L/2` and `b | L`.

For each selected packet, even row slots are in one target group. Put a
unary tensor `(1,2)` on rows `x=2r`, `r=0,...,b-1`; put `(1,1)` on all
other row ports. Pin every odd column to 0. Among even columns, pin all to
0 except the last one, indexed `j=K-1` with `K=L/2`, pinned to 1. On
nonselected packets use `(1,1)` on both ends of every edge. All vertices
are unary, all inputs are explicit, and the graph and valid label/slot
allocation are constructible in polynomial time in `s`. Input precision
can be chosen at least two so that the entry 2 is represented exactly.

At `i=0`, `t=1`, `zeta=1`, every selected row has zero local term, and
summing its row bit against `(1,2)` gives `1+z`. Its source modes evaluate
at the one pinned even column. All other selected-packet row tensors sum
to one; each free nonselected column contributes a factor two.

## 2. The binary odd-node mode matrix

Use the odd-node identity of PR #4. Let `T=2L+1`, `A=a+1`, and
`G=C(T)/C'(0)`. As in the predecessor, `v2(G)=A`. For row `r`, set

```
z_r=1/(T+2r),       s_r=(z_r-1)/2=-(L+r)/(2L+1+2r).
```

The coefficient of mode `k` has valuation at least

```
w_k=A+2k+2 v2(k!) <= A+4k.
```

Divide the row coefficient by `2^w_k` and reduce modulo 2. All factors
other than `binom(s_r,k)` become units with residue one, so the resulting
binary matrix is

```
V[r,k] = binom(s_r,k) mod 2,       0<=r,k<b.             (1)
```

The generalized binomial is integral by PR #4. Modulo `b`, because `b|L`,

```
s_r = -r/(1+2r).
```

This fractional-linear map is an involution on `Z/bZ`, hence permutes the
`b` residues. For `k<b`, `binom(s_r,k) mod 2` depends only on `s_r mod b`:
write `s_r` as the limit of nonnegative integer representatives and use
`(1+X)^b=1+X^b` modulo 2 for the power-of-two `b`, truncated below degree
`b`. Therefore `V` is a row permutation of the Pascal matrix
`binom(j,k) mod 2`, `0<=j,k<b`, which is lower triangular with unit diagonal.
It is invertible over `F_2`.

The source coefficient of odd-node mode `k<b` at the pinned column is

```
sigma_k(K-1)=binom(K-1,k) / prod_{h<=k}(1-2(1+2h)(K-1)).
```

It is a two-adic unit: `K` is a power of two, so every binomial
`binom(K-1,k)` is odd, and all denominator factors are odd.

## 3. One odd coefficient for every mode support

Set every mode with index at least `b` to exponent zero and formally replace
mode `Z_k` by `2^w_k Z_k` for `k<b`. After reducing modulo 2, the target-row
product is

```
F(Z)=prod_{r=0}^{b-1} (1+sum_{k<b} V[r,k] Z_k).          (2)
```

Work in the Boolean quotient `F_2[Z]/(Z_k^2-Z_k)`. For any Boolean input
`z`, (2) equals one exactly when `Vz=0`; invertibility of `V` makes that
condition `z=0`. Every Boolean function has a unique multilinear
representative, so in the quotient

```
F(Z)=prod_{k<b}(1+Z_k).                                  (3)
```

For every subset `S` of the `b` modes, the coefficient of its squarefree
monomial on the right of (3) is one. On the left it is the sum modulo 2 of
all original coefficients whose exponent tuple has support exactly `S`.
Consequently at least one such original coefficient is odd. The polynomial
(2) has total degree at most `b`, so each chosen exponent tuple `beta(S)`
has `|beta(S)|<=b`. Distinct supports give distinct tuples, producing at
least `2^b` local tuples.

Crucially, (3) does **not** assert that the squarefree coefficient in the
original polynomial is odd: higher powers fold in the Boolean quotient.
It only selects at least one odd original coefficient for each support.
Because the divided coefficient is odd, the corresponding actual row
coefficient has **exact** valuation `sum_k w_k beta_k`. The pinned source
mode values are units, so the local child-product summand has that same
valuation.

## 4. The actual budget and precision

Choose one such tuple independently in each selected packet and set all
other exponents to zero. Each resulting complete child-product summand is
the product of the selected local summands and powers of two from the free
columns in nonselected packets. Its valuation is at most

```
M + P b(A+4b),
```

and its weighted mode sum is at most `P b(A+4b)`. Since `P<=M/L` and
`b<=L/(100 sqrt(u))`, the second term is

```
<= M A/(100 sqrt(u)) + M L/(2500 u) = o(M L/u) + M L/(2500 u).
```

The source's exact prescribed child precision at `t=1` satisfies
`p_t=p+8 ceil(3M/u)L+8M(a+1)>=24 M L/u`. Thus every selected tuple is
inside the weighted budget and its complete summand is nonzero modulo
`2^p_t` for sufficiently large `N`. The number of tuples is at least

```
2^(P b) = exp(Omega(M/sqrt(u))),
```

because `P=Theta(M/L)` and the largest-power-of-two choice gives
`b=Theta(L/sqrt(u))`. This proves only the scoped statement above.

## 5. Replacing the weighted unary tensors by Boolean clauses

There is a second explicit balanced full-packet family with the same
`exp(Omega(M/sqrt(u)))` conclusion, using only Boolean two-literal clause
tables, unary pins and `(1,1)` tables. It uses **two** paired packets per
selected gadget. It is not asserted to be the precise subdivided network
produced by the source's fixed-density SAT reduction.

Use the same parameters and equal pair-class loads as in Section 1. For each
fixed vector of unordered coordinate pairs in coordinates `1,...,a-1`,
pair an auxiliary packet whose coordinate-zero pair is `{0,0}` with a
distinct target packet whose coordinate-zero pair is `{0,1}`. For each
such vector, the source orientation allocation gives twice as many target
packets as auxiliary packets: an unequal coordinate adds one orientation
bit. Pair every auxiliary packet with one target and leave the remaining
targets unselected. All packets remain full. The number of pairs is
`P=M/(r^2 L)`, since exactly a `1/r^2` fraction of full packet slots have
coordinate-zero ordered pair `(0,0)`.

For each pair and each `0<=r<b`, put a binary clause vertex with one row
port at even target slot `2r` and its other row port at even auxiliary slot
`2r`. These two ports have the same complete row label: their coordinate-zero
symbols are both 0, the other unordered pairs and slot bits are identical,
and the packet orientation convention is shared. The clause table is

```
A(y,a)=1-a+ya,  the satisfaction table for y OR NOT a.
```

All other row ports have unary `(1,1)` tables. In the target packet pin
all odd columns to zero and pin all even columns to zero except the last,
which is one. In the auxiliary packet leave the odd columns at slots
`2r+1`, `0<=r<b`, free with unary `(1,1)` tables, and pin all remaining
columns to zero. All other packets have `(1,1)` on every port. This is an
explicit bounded-degree input network with unchanged pair-class loads and
packet balance.

Let `X_s` be the free auxiliary column bits and `U_r` the deformed auxiliary
row form. At `T=2L+1`, its local Cauchy matrix is

```
J_rs=G/[T+2r-(2s+1)]=G/[2(L+r-s)].
```

When `r=s`, `v2(J_rr)=v2(G)-v2(2L)=0`, so it is one modulo two. If
`r!=s`, then `0<|r-s|<b<=L/2`, so
`v2(L+r-s)=v2(r-s)<a`; hence `v2(J_rs)>=1`. Therefore
`U_r=sum_s J_rs X_s = X_r mod 2`. This auxiliary packet has an equal
coordinate-zero symbol pair, so all these entries are local and no auxiliary
crossing modes are introduced.

Summing the two row bits of each clause gives
`1-U_r+U_r z_r`, where `z_r` is the target row form. Set target modes with
index `>=b` to zero and divide the first `b` mode coefficients by their
weights as in Section 2. Reducing modulo two and summing all auxiliary
column assignments yields the **formal** polynomial

```
sum_{X in F_2^b} prod_r (1-X_r+X_r sum_k V[r,k] Z_k)
 = prod_r (1+sum_k V[r,k] Z_k).                          (4)
```

The right side is exactly (2), before taking the Boolean quotient in the
mode variables. Thus the witnesses `beta(S)` of Section 3 are also odd
normalized coefficients for the Boolean-clause gadget. The target source
mode values remain units. The per-packet weighted budget and exact
valuation are unchanged; the other free columns contribute at most `M`
powers of two. Since `P=M/(r^2 L)=Theta(M/L)`, the count and precision
comparison in Section 4 hold with a different absolute constant.

The checker constructs the actual auxiliary `J` for all three finite cases
and verifies its modulo-two identity. For `b<=4`, it also sums the actual
rational clause-gadget coefficients over all auxiliary assignments and
checks each selected original exponent tuple has odd normalized coefficient;
it separately checks the clause table identity. These checks do not replace
independent review of the all-size pairing or establish that the source's
specific subdivision and default packing select this instance.

## 6. A local gate for subdivision wires

A conditional local calculation supports, but does not complete, a bridge
to the source's subdivided SAT network. Suppose three local packet blocks
transmit the same `b` Boolean column bits to their selected row ports by
integral matrices congruent to the identity modulo 2; all other columns
are fixed to zero or have no modulo-two effect on those rows. Join the first
two row ports at each index by an original binary equality vertex and put a
unit clause pin on the third. Suppose subdivision equality tensors tie the
second and third column-bit vectors, while the first is the external vector
`X`. Let the required pin pattern be `c`.

The binary equality table has multilinear extension
`E(z,w)=(1-z)(1-w)+zw=1-z-w+2zw`. Modulo two on Boolean arguments this is
`1+z+w`, the indicator that the arguments agree. The unit clause has
extension `z` for a one pin or `1-z` for a zero pin. Summing the shared
internal Boolean vector `V` therefore gives, modulo two,

```
sum_V prod_i (1+X_i+V_i) pin_{c_i}(V_i) = [X=c].
```

The selected Cauchy blocks constructed in Section 5 have the required
identity reduction. Thus, **if** a globally valid arrangement supplies the
three blocks and the specified equality connections without additional
interference, the extra equality and pin chain can transmit the pinned
column pattern needed in Section 5 modulo two. The checker uses the actual
rational Cauchy block to check every external vector for `b=2,4` and a
one-hot pin pattern. This calculation is only a local gate: it does not
construct the needed packets and filler vertices as an exact output of the
source reduction, prove its global balance, or establish an end-to-end
summand count for that output.

## 7. A complete pair of subdivided filler packets

The following all-size filler is compatible with the *local vertex types*
of the source's subdivision. Take two full packets of the same unordered
pair-label type and pair their corresponding column ports into binary
equality vertices. On every row port of the first packet put the unit clause
`(1,0)`; on every row port of the second put the free variable table
`(1,1)`. Thus each subdivision equality connects one unit-clause endpoint
and one degree-one variable endpoint. Pairing corresponding slots also
matches each column vertex's complete label.

At `t=1,zeta=1`, summing the second packet's row bits gives one, and the
column equality vertices tie the two packets' column vectors. The scalar
contribution of this isolated pair is

```
S_L = sum_{X in {0,1}^L} prod_{x=0}^{L-1}(1-sum_y W_xy X_y).
```

For every power of two `L>=4`, this scalar has **exact valuation three**.
In particular each such pair contributes `2^3` times a two-adic unit; an
arbitrary number of disjoint pairs does not unexpectedly annihilate a
summand at the source precision.

To prove this, put `U=G/(2L)`, an odd two-adic rational. In `W`, the
entries `(x,x+1)` for `0<=x<L-1` equal `U`; every other entry is even.
The only off-diagonal entry of valuation one is
`W_(L-1,0)=2U/3`; every other off-diagonal entry has valuation at least two.
To see this, write the denominator as `2L+(x+1-y)`. For the bounded slot
range, valuation `a` occurs only for `x=L-1,y=0`; all other nonzero
shifts have valuation at most `a-1`.

Expand `S_L` modulo 16 around the `L-1` diagonal row factors
`1-U X_(x+1)`. Four off-diagonal selections vanish automatically. Two or
three selections also vanish: without the unique valuation-one entry their
product is divisible by 16; with it, a second selection has valuation at
least two and its removed diagonal leaves an unselected Boolean variable,
whose sum contributes another factor two. For one selection, the Boolean
sums vanish modulo 16 unless its column is 0 and its row is either
`L/2-1` or `L-1`. Indeed any other selected column leaves the unselected
column 0 free, and either removes another free diagonal variable or gives
an even factor `1-U` at the selected column. The only valuation-two entry
in column 0 before the last row is `W_(L/2-1,0)=4U/5`.

The three surviving contributions are therefore

```
2(2-U)^(L-1)
- 2(4U/5)(2-U)^(L-2)
- (2U/3)(2-U)^(L-1).                                  (5)
```

It remains to show `U=3 mod 8`. From the definition of `C`,

```
U = - 1/2 * binom(3L+1,L+1) * binom(2L,L).
```

For `L>=8`, let `O(n)` be the product modulo 8 of all odd integers at
most `n`, and let `F(n)` be the odd part of `n!` modulo 8. The recursion
`F(n)=O(n)F(floor(n/2))`, together with `O(8m)=1`, gives
`F(L)=F(L+1)=F(2L)=3` and `F(3L+1)=7`. Thus
`binom(3L+1,L+1)=7 mod 8` and `binom(2L,L)/2=3 mod 8`, proving
`U=-7*3=3 mod 8`. The case `L=4` is a direct calculation. In (5) the first
and last terms combine to a multiple of 16, while the middle term is 8
modulo 16. Hence `S_L=8 mod 16`, as claimed.

The checker independently expands modulo 16, recording the three surviving
terms, for `L=4,8,16,32,64`. This is a complete filler-pair lemma, not a
complete embedding of Section 5's selected clause gadgets into the exact
subdivided reduction. One must still allocate the selected gadgets and all
remaining filler pairs simultaneously with consistent row and column labels.

### Finite screen for filler pin moments

The filler-pair calculation does not by itself show that attaching a
subdivision pin gate preserves the leading unit after dividing by `2^3`.
A relevant moment is

```
N_S = sum_X prod_x(1-z_x(X)) prod_{j in S} z_j(X),
```

where `z_x(X)=sum_y W_xy X_y`. For `|S|>=4`, `N_S=0 mod 16` follows
pointwise: each of the distinct factors `z_j(1-z_j)` is even. The remaining
cases `1<=|S|<=3` need another argument.

An exact [finite screen](filler-moments.py) finds `N_S=0 mod 16` for all
nonempty subsets of non-last rows of size at most three at `L=8,16`, and
for all such subsets of the first four rows at `L=32,64`. The screen uses
a complete modulo-16 expansion with at most three off-diagonal selections;
for `L=8` it independently compares all 93 subsets, including the empty
and boundary cases, with direct Boolean summation. **The last row is an
essential exception:** its singleton moment equals 2 modulo 16 in each
listed case. The broad non-last-row assertion is an unproved conjectural
continuation, not part of the filler lemma or an end-to-end subdivision
construction. A proof must handle the nonboundary sets uniformly, the
selected pin pattern and the simultaneous label/slot allocation.

### An all-size even-row pinning lemma

For every power of two `L>=8` and every nonempty set `S` of even row
indices, the moment `N_S` above is divisible by 16. Thus, for arbitrary integral external forms `t_j` independent of the
filler bits `X`, attaching an equality row gate at each
`j in S` gives the modulo-16 identity

```
sum_X prod_x(1-z_x) prod_{j in S} E(t_j,z_j)
    = 8 prod_{j in S}(1-t_j) mod 16.                      (6)
```

Indeed `E(t,z)=(1-t)+(2t-1)z`: expand in subsets and use `N_empty=8`
and the stated moment divisibility. After division by 8, (6) supplies
simultaneous zero pins modulo two. The restriction to even rows is essential
to the proof and is sufficient for the selected slots in Section 5.

To prove the moment statement, write `d=|S|` and split the sum by `X_0`.
For fixed remaining bits, let

```
H(X_0)=prod_{x<L-1}(1-z_x) prod_{j in S} z_j.
```

Each `z_j(1-z_j)` is even, so `H(X_0)` is divisible by `2^d`. The only
valuation-one off-diagonal entry is `W_(L-1,0)=2U/3`; hence with `X_0=0`
the last-row form is divisible by four. Using `U=3 mod 8`, the combined
contribution for `X_0=0,1` is

```
H(0)[2-2 z_(L-1)(0)-W_(L-1,0)]
 + [H(1)-H(0)] [1-z_(L-1)(0)-W_(L-1,0)].
```

The bracket in the first line is divisible by eight, so that line vanishes
modulo 16 for `d>=1`. For the second line, every selected even row `j` has
`W_j0` divisible by `2^(a+1)`, hence by 16. Among the other non-last rows,
only `m=L/2-1` has `v2(W_m0)=2`; all others have valuation at least three.
Changes at selected rows or at rows other than `m` therefore vanish modulo
16, and the `m` contribution vanishes when `d>=2` because of the `d` even
factors.

It remains to consider `d=1`, say `S={j}`. Since `j` is even, `j!=m`.
Divide the `m` contribution by eight and reduce modulo two. For any
non-last row, its only odd Cauchy entry is its shifted diagonal. Thus
`z_j(1-z_j)/2 mod 2` depends only on `X_(j+1)` (because all off-diagonal
entries in that row are divisible by four), and every remaining
`(1-z_x) mod 2` depends only on `X_(x+1)`. The factor at row `m` was
removed by the change, so this reduced summand is independent of
`X_(m+1)`. Summing over that free bit gives zero modulo two. This proves
`N_S=0 mod 16` for all nonempty even `S`.

The finite moment checker includes all even-row subsets up to size three
at `L=8,16` and selected subsets at `L=32,64`; four or more vanish
pointwise. The proof does not claim the stronger non-last-row statement
suggested by the screen, and the last-row exception remains real. It also
does not supply the complete global arrangement of subdivision and pin
packets.

### Arbitrary even-row pin patterns

The preceding argument extends to simultaneous **arbitrary** pin values.
For disjoint sets `R,S` of even rows, with `R union S` nonempty, define

```
B_(R,S)=sum_X prod_{x notin R}(1-z_x) prod_{j in S} z_j.
```

Then `B_(R,S)=0 mod 16` for all powers of two `L>=8`. In particular `R`
may remove pin factors while `S` inserts moments at different rows.

The proof uses the same split by `X_0` as the even-row moment lemma. Put
`d=|S|` and let `H` omit the pin rows in `R` while retaining the `d`
factors `z_j(1-z_j)`. If `d>=1`, the first line of the split is divisible
by `2^(d+3)` as before. If `d=0`, `R` is nonempty: modulo 16, the bracket
in that line is a multiple of `8 X_(L/2)`. Every `j in R` is even, so its
omitted row leaves the distinct odd-indexed bit `X_(j+1)` free; the other
row factors modulo two do not depend on it. Summing that bit gives an
additional factor two.

For the difference `H(1)-H(0)`, even rows contribute no change modulo 16;
the exceptional odd row `m=L/2-1` has column-zero valuation two and all
other non-last rows have valuation at least three. With `d>=1`, changes
outside `m` vanish pointwise, and the `m` term vanishes pointwise for
`d>=2`. For `d=1`, the same free-bit pairing at `X_(m+1)` used above
applies, since `m` is not in the even set `S`. With `d=0`, any valuation-
three change has a free bit from `R`, while the valuation-two change at
`m` leaves at least two free bits, one from `R` and `X_(m+1)`. Modulo four
all non-last rows have only their shifted diagonal and the last-row factor
is constant, so summing those two bits gives a factor four. Products of two
column-zero changes are already divisible by 16. This proves the mixed
moment assertion.

Consequently, for a set `J` of even rows and any Boolean pattern `c` on `J`,
let `p_0(z)=1-z`, `p_1(z)=z`. The helper with those unit-clause pins obeys

```
sum_X [prod_(j in J) p_cj(z_j)] [prod_(x notin J)(1-z_x)]
      * prod_(j in J) E(t_j,z_j)
 = 8 prod_(j in J) p_cj(t_j) mod 16.                    (7)
```

Here the integral external forms `t_j` are independent of the filler bits.
For each row, `p_c(z) E(t,z)` equals `p_c(t) p_c(z)` plus a multiple of
`z(1-z)`. Expanding every positive pin as `z=1-(1-z)` reduces each error
to a mixed moment with nonempty `R union S`; it vanishes. The main pin
scalar is congruent to `(-1)^|{j:c_j=1}| S_L=8 mod 16`, since every term
with a removed pin vanishes. This proves (7). The direct
[mixed-pin screen](mixed-pin-screen.py) checks every disjoint removed-pin/
moment pattern and every pin/gate pattern for `L=8,16` with three selected
even rows. Its hash-bound output is finite evidence, not independent review.

## 8. An explicit subdivided unit-clause family

The even-row pinning lemma closes the subdivision step for a specified valid
packing. More precisely, for arbitrarily large sizes there are fixed-density
CNF inputs consisting solely of unit clauses, including repeated identical
clauses, whose **per-edge subdivided clause/variable tensor network** admits
a specified valid root packing with `exp(Omega(M/sqrt(u)))` retained
odd-node child-product summands nonzero at the prescribed precision, at
`t=1` with `zeta=1` in the evaluation set. The source's particular default
labeling need not choose this packing, and a preprocessor that removes the
repeated unit clauses changes the input network. The formula is trivially
simplifiable; this is not a SAT or algorithmic time lower bound.

### Network and actual reduction size

Let `S_0=2^N`, `u=floor(epsilon N)`, `a=2u`, `L=2^a`, `r=64`, and
`D_arr=L^12`. Set

```
B_pad = 4L floor(S_0/(4L D_arr)),  M = B_pad D_arr.
```

Allocate `B_pad` real edges to every ordered pair of vertex labels and form
full packets by the source orientation rule. The number of packets of each
unordered pair-label type is a multiple of four. Partition each type's
packets into quartets `(T,T',H,H')`, using identical slot-orientation
conventions within each quartet. Select every quartet whose coordinate-zero
pair is unequal. Their number is

```
P = (r-1) M/(4r L) = Theta(M/L).
```

Choose `b` as in Section 1, and let `J={0,2,...,2(b-1)}` be the selected
even row slots. For each selected quartet, define its old row vertices:

* At each slot `x in J`, `T` has a negative unit clause, `H'` has a
  negative unit clause, and the ports at `T'` and `H` belong to the same
  binary variable-equality vertex.
* At each other slot, `T` and `H` have degree-one variable vertices, while
  `T'` and `H'` have unit clauses. All those clauses are negative except
  the clause at slot `L-3` of `T'`, which is positive.

The two ports of each binary variable vertex have identical complete row
labels, because the packet copies have the same unordered type, orientation
and slot. At every slot, join the corresponding **column** ports of `T`
and `T'` into a binary subdivision equality, and do the same for `H` and
`H'`. Column labels match for the same reason. Each such subdivision vertex
connects a clause endpoint to a variable endpoint. Thus these are exactly
the row/column types of the source's fixed-density per-edge subdivision.
The two clauses incident to each selected degree-two variable are repeated
negative unit clauses.

For each unselected quartet, use two disjoint filler pairs from Section 7.
Every packet remains full, every ordered label-pair class has load `B_pad`,
the collision variance is zero and each symbol has `M/r` ports on each
side in every coordinate. All vertices and assignments are constructible in
time polynomial in `S_0`.

There is one degree-two variable vertex per selected row, so the number of
old clause and variable vertices, and hence the reduction's own size
parameter, is `s=n+m=M-Pb`. Since `b=O(L/sqrt(u))` and `M=S_0-O(L D_arr)`,
we have `s/S_0 -> 1`; in particular `2^(N-1)<s<2^N` for large `N` and
`ceil(log2 s)=N`. Thus the source really chooses the displayed `u,a,L` for
this input. Also `M<=2s`, `M>H`, the source degree and packing inequalities
hold, and `m/n` is bounded. This accounting does not treat `S_0` as the
reduction's exact size when it is not.

### Coefficients after the helper and target pins

At the selected node, the `H/H'` pair is the filler-pinning construction of
Section 7 with equality gates attached at the even rows `J`. Divide its
contribution by `2^3`. Equation (6) says that, modulo two, it pins the
corresponding external `T'` row forms to zero. All other `T'` rows are unit
clauses: they pin their row forms to zero, except row `L-3`, which pins one.
The Cauchy matrix modulo two is the shifted identity `W_xy=[y=x+1]`.
Consequently, after summing the tied column bits of `T/T'`, every target
column bit except `X_0` is fixed modulo two: the sole one is
`X_(L-2)=1`. All local columns of selected even target rows are zero.

Select only mode tuples whose support contains mode 0. Their exponent
`beta_0` is positive. In the even source tile, the mode-0 value is
`X_0+1` modulo two; for every `k>=1`, the value is the unit
`sigma_k(K-1)` because `sigma_k(0)=0`. Thus, in the source-mode product,
the free boundary assignment `X_0=1` contributes zero and `X_0=0`
contributes one. No unsupported division by a boundary factor is used.

The selected `T` rows are negative unit clauses. After dividing each
crossing coefficient by its odd-node weight and reducing modulo two, their
product is the same invertible-Pascal polynomial (2), with minus signs
irrelevant in `F_2`. The Boolean-quotient argument therefore supplies an
odd normalized original coefficient for every support containing mode 0:
`2^(b-1)` distinct tuples per selected quartet, each of total degree at
most `b`. The source-mode values for that tuple are units at the sole
surviving boundary assignment.

### Actual precision and count

Every selected `H/H'` pair contributes `2^3` times the pin polynomial
modulo the next bit; every unselected filler pair contributes `2^3` times
a unit by Section 7. Let `F` be the number of unselected filler pairs.
The normalized complete coefficient of every selected global tuple is odd,
so its valuation is exactly `3(P+F)` plus its source mode weight. Since
`P+F<=M/(2L)`, the extra precision cost is at most `3M/(2L)`.

The total mode weight is at most `P b(a+1+4b)` and hence `o(ML/u)` plus a
small fixed fraction of `ML/u`, exactly as in Section 4. The prescribed
`p_t>=24ML/u` therefore exceeds the valuation and the weight for large
`N`. With `P=Theta(M/L)` and `b=Theta(L/sqrt(u))`, the number of distinct
complete surviving tuples is at least

```
2^(P(b-1)) = exp(Omega(M/sqrt(u))).
```

The [reduction-gadget checker](reduction-gadget.py) explicitly checks the
four-packet endpoint types and labels, sums the helper equality gates modulo
16, enumerates target assignments including the boundary bit, and checks all
support witnesses containing mode 0 for `(L,b)=(8,2),(16,4)`. These bounded
checks do not independently review the all-size proof. In particular the
conclusion concerns a specified valid packing and the specified odd-node
expansion, not every packing, a lower bound against preprocessing or
aggregation, or an improved SAT algorithm.

## 9. A version without repeated clauses

Equation (7) removes the repeated-clause requirement at the cost of making
the already trivial input explicitly contradictory. Keep the four-packet
construction of Section 8 but replace the `H'` unit clause at each selected
even row by a **positive** unit clause. Its variable's other incident
clause, in `T`, remains negative. Each selected degree-two variable therefore
appears once positively and once negatively; every other variable appears in
one unit clause. There are no duplicate clauses. The input is unsatisfiable
by immediate unit propagation, and a solver can detect this before using the
tensor contraction.

The helper now pins each selected `T'` row form to one modulo two after
removing its factor `2^3`. Since `W mod 2` is the shifted identity, the
selected target rows have local value one. Their negative unit clauses
therefore contribute the normalized homogeneous product

```
prod_r (sum_k V[r,k] Z_k)  mod 2.                        (8)
```

The invertible matrix `V` has first column all ones. On Boolean inputs,
(8) is one exactly when `Vz` is the all-ones vector, whose unique solution
is `z=e_0`. Its Boolean-quotient representative is
`Z_0 prod_(k>=1)(1+Z_k)`. Thus every mode support containing 0 again has
an odd original coefficient. The boundary source bit is handled exactly
as in Section 8: mode 0 suppresses the `X_0=1` assignment. All selected
tuples have degree at most `b`; in fact they are homogeneous of degree `b`.
Equation (7), the filler factors, packing and precision estimates are
unchanged. This gives the same scoped `exp(Omega(M/sqrt(u)))` conclusion
for a no-duplicate, fixed-density unit-CNF family and its literal per-edge
subdivision, still under the specified valid packing.

The [four-packet checker](reduction-gadget.py) tests both the repeated-clause
and contradictory no-duplicate variants at `(L,b)=(8,2),(16,4)`, including
all helper pin patterns needed, original coefficient witnesses and the free
boundary bit. The result is emphatically not a lower bound on SAT,
preprocessing, the source's default labeling, or arbitrary aggregation.

## Evidence and open obligations

The [checker](verify.py) tests `(L,b)=(16,2),(32,4),(64,8)`: exact
odd-node coefficients and their normalized binary matrix, the residue
permutation and rank, original exponent-tuple witnesses for every support,
source units, full kernel identities, and complete local contractions.
For `b<=4` it independently recomputes selected normalized coefficients as
exact rationals. These finite checks do not review the all-size proof or
implement the full recursion. The frozen source labels are
`lem:tensor-packets`, `lem:tapered-hermite`, `eq:tensor-mode-budget`, and
`eq:tensor-recursion-identity`; root `SOURCES.json` supplies hashes and
licenses.

Both unit-clause families give specified valid packings of the literal
per-edge subdivision; one retains duplicate clauses and the other has
opposing unit clauses. Default packing, preprocessing and aggregation
remain separate. An algorithmic lower bound would separately need to rule out
simplification, aggregation and alternate packing. No such claim is made.
