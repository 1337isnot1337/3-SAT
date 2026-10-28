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

The changed premise is essential: the network uses a unary tensor `(1,2)`
and is a general weighted tensor-network input, not claimed to be the
literal SAT-to-network reduction. The source's default deterministic
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

A stronger result for actual SAT-reduction tables would need a different
input construction: `(1,2)` is not one of the stated clause/equality
input tables. An algorithmic lower bound would separately need to rule out
simplification, aggregation and alternate packing. No such claim is made.
