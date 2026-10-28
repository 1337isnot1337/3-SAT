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

The Boolean-clause family uses clause, pin and unary tables, but a result
for the exact subdivided SAT-reduction output still needs its additional
equality wires placed and analyzed through the deformation. An algorithmic lower bound would separately need to rule out
simplification, aggregation and alternate packing. No such claim is made.
