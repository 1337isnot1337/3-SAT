# Interpolating the tapered witness with Cauchy packets

Work over `Z_(2)` and its fraction field. Let `L=2^a`, `a>=1`, and
`S={-L,...,L-1}`. Write `C(T)=product_(t in S)(T-t)`, `C0=C'(0)`, and
`W_d(T)=C(T)/(C0(T-d))` for `d=-L+1,...,L-1`, as in the accepted source.
Each `d` is a difference of two slots in a full packet. The omitted grid
point `-L` is not a slot difference, so all `W_d(-L)=0`. For `d,e` in `S`
with `d != -L`,

```
W_d(e) = 0 if e != d, and W_d(d) = C'(d)/C'(0).
```

The complete residue grid modulo `2L` gives `v2(C'(d))=v2(C'(0))`;
therefore `W_d(d)` is a unit of `Z_(2)`.

For `0<=j<a`, define the polynomial

```
P_j(T) = product over nonzero t in S with v2(t)<=j of (T-t)/(-t).
```

Its degree is `2L-L/2^j < 2L` and `P_j(0)=1`. It has integral values at
every grid node: a root gives zero, and at any nonroot `t`, either `t=0`
or `v2(t)>j`, so every factor has valuation zero. Its coefficients need
not be in `Z_(2)[T]`; only its grid values are used here. Let

```
c_* = P_j(-L),
c_d = (P_j(d)-c_*) / W_d(d).
```

All `c_*` and `c_d` lie in `Z_(2)`. Both sides of

```
P_j(T) = c_* + sum_d c_d W_d(T)                         (1)
```

have degree at most `2L-1` and agree at all `2L` points of `S`, proving (1).
The rational coefficients have polynomial bit length in `L`: they consist
of products and ratios of `O(L)` integers of size `O(L)`. Their residues
modulo `2^p` can be calculated in polynomial time in `L,p` by inverting odd
integers modulo `2^p`.

Use two full packets. In the first fix the column bits to zero except for
`X_(L-1)=1`; its rows `x=0,...,L-1` produce shifts `d=L-1-x`.
In the second fix all column bits to zero except `X_0=1`; its rows
`x=1,...,L-1` produce the negative shifts `d=-x`. Mark these `2L-1`
rows, and on them use the single tensor

```
A(Y) = c_* + sum_d c_d Y_(x_d).
```

The one unmarked row is unrestricted, represented by a unary `(1,1)` tensor;
column bits are fixed by unary `(1,0)` or `(0,1)` tensors. In the source's
multilinear affine deformation, summing row bits replaces each marked
`Y_(x_d)` in `A` by `(WX)_(x_d)=W_d(T)`. The unmarked row sum is one.
Equation (1) proves that the deformed contraction is exactly `P_j(T)`.
Tensor entry evaluation is a sum of `2L-1` stored coefficients.

For `1<=u<=a`, the predecessor's generic witness with multiplicity parameter
`h>=1` is exactly

```
H(T) = product_(j=0,...,u-1) P_j(T)^h.                  (2)
```

Indeed a nonzero node of valuation `i` occurs once for each `j>=i`, giving
multiplicity `h max(0,u-i)`. Independent copies multiply contractions. Thus
(2) is realized with `M=2huL` real ports, one degree-`2L-1` row tensor per
factor copy, and all remaining tensors unary. There are no hidden sums in
the entry oracle beyond polynomially many operations; denominators are odd.
The construction does not show that this prescribed packetization satisfies
all balance conditions of the source's packing lemma or that a corresponding
Boolean network exists.

For a retained node of valuation `i<u`, the predecessor's exact content
formula and bounds give `Theta(hL/2^i)`. With `M=2huL`, this becomes
`Theta(M/(u 2^i))`, a factor `L` below the generic witness's
`Theta(ML/(u 2^i))` scale when its multiplicity is chosen from this same
actual port budget. The relevant constants are uniform under the stated
parameter restrictions. Neither observation is a lower bound on tensor-aware
algorithms that inspect these simple tensors. No reduction, recursion, entry,
leaf or SAT cost is claimed to improve.

For the integer-entry observation, at `T=-L` every `W_d` is zero, so the
contraction is `A(0) sum_X B(X)`, an integer when all tensor entries are
integers. At `L=4`, `u=h=1`, multiplication over odd roots gives
`H(-4)=35/3`. This excludes literal equality in that narrower class, while
multiplication by 3 removes this specific obstruction and leaves the origin
odd.

## Finite-precision integer lifts

Fix any positive precision `P`. For every entry of each row tensor,
replace its `Z_(2)` value by the unique integer in `[0,2^P)` congruent to it
modulo `2^P`. Keep the unary zero/one tensors unchanged. The replacement is
an entrywise congruence, even though the integer-valued row tensor need no
longer be affine as a function of its Boolean arguments. Its entry oracle
still uses `O(L)` modular additions and odd-denominator inversions with
`P`-bit arithmetic.

At every grid node, the accepted `lem:tensor-integrality` says all entries of
`W(t+2Lz)` have coefficients in `Z_(2)`. Hence every affine bit factor in the
deformed contraction is integral coefficientwise. Expanding the finite sum
shows that replacing tensor entries by congruent integers preserves the
entire shifted polynomial modulo `2^P`, simultaneously at all nodes. At
`T=0` the contraction is congruent to `H(0)=1` modulo `2^P`. If every active
node is read at precision at most both `P` and the predecessor's content
bound for this `h`, the lifted network and the zero network have identical
complete active-node jets at those precisions and opposite origin parities.
The same finite-precision realization holds for arbitrarily large `P`, with
`P`-bit entries and their computation charged. It does not give literal
polynomial equality over the rationals, canonical Boolean tensors, a better
precision scale, or compatibility with arbitrary packetization.

## Quadratic interpolation and three powers per packet pair

The preceding linear construction can share packets across powers. Keep the
two fixed columns, but now use *all* `2L` row bits in a single row tensor.
The resulting row values are `W_d` for `-L<d<L`, plus a second independent
row with the same value `W_0`. We prove that every
`F in Z_(2)[T]` of degree at most `4L-2` is a polynomial of degree at most
two in these row values, with coefficients in `Z_(2)`.

Divide by the monic integer polynomial `C`: write `F=P+C R` with
`deg P<2L`. Both `P` and `R` lie in `Z_(2)[T]`, and `deg R<=2L-2`.
Linear interpolation expresses `P=c_*+sum_d c_d W_d`, with
`c_*=P(-L)`, `c_d=(P(d)-c_*)/U_d`, and units
`U_d=W_d(d)`. In particular the coefficients are 2-integral.

Set

```
Q=(W_0^2-W_0)/C,     beta=L C0 R(-L).
```

`Q` is a polynomial: on the grid, `W_0` is one at zero and zero at all
other points. Differentiating at `-L` gives `Q(-L)=1/(L C0)`. Thus
`R-beta Q` has degree at most `2L-2` and vanishes at `-L`.
For every nonzero slot difference put

```
q_d=(d C0 R(d)+beta)/U_d.
```

These coefficients are 2-integral. For `d != 0`, the Cauchy identity is

```
W_d W_0 / C = (W_d-W_0)/(d C0).                        (3)
```

As polynomials, the right sides of (3) vanish at `-L`. At any nonzero grid
node `e`, only `d=e` is nonzero, and `Q(e)=-1/(C0 e)`. Therefore
`sum_(d!=0) q_d (W_d W_0/C)` agrees with `R-beta Q` at all `2L-1` nodes
other than zero. Both have degree at most `2L-2`, so they agree identically.
Consequently

```
F = c_* + sum_d c_d W_d + beta (W_0^2-W_0)
      + sum_(d!=0) q_d W_d W_0.                         (4)
```

All multiplications in (4) use distinct row bits: the two zero-shift rows
provide `W_0^2`, and each other `W_d` has its own row. A single tensor whose
Boolean table is the right-hand multilinear expression realizes `F` after
row summation. Its *polynomial* degree is two and its tensor vertex has `2L`
ports. Given a polynomial-size coefficient description of `F`, evaluating
its tensor entry takes polynomially many operations in `L`, coefficient size,
and requested precision; this is not an exponential table lookup.

The `j=0` factor `P_0` has odd root denominators and hence lies in
`Z_(2)[T]`, with degree `L`. Its powers one, two, and three have degree at
most `4L-2` for `L>=2`, so each uses two full packets. For arbitrary `h`,
partition `P_0^h` into `ceil(h/3)` such factors; use the earlier linear
construction for each of the other `h(u-1)` factors. This preliminary construction realizes the same
tapered witness with

```
M = 2L (ceil(h/3) + h(u-1))
```

real ports. For `u=1`, the resulting `h` is asymptotically `3M/(2L)` rather
than `M/(2L)`, still a factor `Theta(L)` below the generic `h=Theta(M)` at
the same port budget. The argument retains the preceding 2-adic coefficient,
finite-precision integer-lift, prescribed-packing, and Boolean limitations.
It proves no all-size result for higher powers; the next section handles
pairs of the remaining taper factors.

## Sharing pairs of every taper factor

The quadratic interpolation also realizes `P_j^2` for every `0<=j<a`, even
though `P_j` need not lie in `Z_(2)[T]`. Its degree is
`4L-2L/2^j <= 4L-4`. To check the same coefficient formulas, let `A` be the
monic product over the selected roots of `P_j`, so `P_j=A/A(0)`, and let
`B=C/A`, the monic product over complementary roots including zero. Divide
`A=B Q+E` over `Z[T]`, with `deg E<deg B`. Then

```
P_j^2 = A E/A(0)^2 + C * A Q/A(0)^2.                  (5)
```

The first term has degree below `2L` and agrees with `P_j^2` on the whole
grid: on roots of `A` both vanish, and on roots of `B` one has `E=A`.
Thus it is the polynomial remainder used in quadratic interpolation. Its
grid values are integral, so all linear interpolation coefficients are
2-integral.

Let `R=A Q/A(0)^2` be the quotient in (5). Since `C0=A(0)B'(0)`,

```
C0 R(t) = B'(0) Q(t) A(t)/A(0).
```

For every grid node the final ratio is either zero or a 2-adic unit, as in
the first section, and `Q(t)` and `B'(0)` are integers. Therefore
`C0 R(t)` is 2-integral at every node. The formulas in the quadratic section
then show that both `beta=L C0 R(-L)` and every
`q_d=(d C0 R(d)+beta)/U_d` are 2-integral. This proves the exact two-packet
realization for the square, with polynomial-time entry evaluation.

For general `h`, group each factor `P_j^h`, `j>=1`, into `ceil(h/2)` squares
or a final singleton. Together with grouping `P_0^h` in threes, the entire
witness therefore uses

```
M = 2L (ceil(h/3) + (u-1) ceil(h/2))                   (6)
```

real ports, improving the earlier all-size port count. This is still a
constant-factor saving in the principal parameter `L`, not a realization at
the predecessor's generic multiplicity for the same `M`. The same source
packing, degree cap, Boolean input, and independent-review qualifications
apply.

## Sharp degree boundary for the two fixed-column packets

Consider precisely the two full packets used in the quadratic construction,
with one column bit fixed to one in each and all other column bits fixed to
zero. The row tensor may be any rational-valued table on all `2L` row bits;
its unique multilinear polynomial gives a rational linear combination of
products of distinct row factors. These factors are `W_d` for all
`-L<d<L`, with `W_0` present twice.

Define the monic polynomial

```
D(T) = T (T+L)^3 product_(t in S excluding 0,-L) (T-t)^2.
```

Its degree is `4L`. Every product of three distinct row factors is divisible
by `D`: at each grid node other than zero and `-L`, at most one factor is
nonzero; at zero at most two are nonzero; and at `-L` every factor is zero.
The same holds for every product of more factors. Products of zero, one, or
two factors have degree at most `4L-2`. Consequently every contraction in
this fixed-column model has remainder of degree at most `4L-2` on division
by `D`. In particular no polynomial of degree exactly `4L-1` is realizable,
even with arbitrary rational row entries. The previous quadratic theorem is
therefore sharp as a universal degree statement for this model.

Let `H_1=P_0` be the odd-root factor. It is an even polynomial of degree
`L`. Write `c` for the nonzero leading coefficient of `H_1^4`. The
coefficient of `T^(4L-1)` in `H_1^4` is zero, whereas the coefficient of
`T^(4L-1)` in `D` is `3L` (the sum of its roots is `-3L`). Thus the
remainder of `H_1^4` modulo `D` has coefficient `-3Lc` at that degree and
cannot occur in the fixed-column model. This holds for every power-of-two
`L>=2` and does not depend on 2-adic integrality.

The obstruction assumes these particular fixed column assignments and this
single-pair port budget. It does not cover column sums, other packetizations,
more packets, or equality only modulo a finite precision. It is not a
lower bound for general tensor contraction or SAT.

### Arbitrary fixed one-hot columns in the two packets

The degree obstruction and quartic exclusion extend to any positions
`y_1,y_2` of the two fixed one-hot columns. At node `t`, let `r_t` be the
number of the `2L` row factors which are nonzero. Each packet contributes at
most one, so `r_t<=2`; summing over grid nodes gives `sum_t r_t=2L` because
each row has exactly one slot-difference node. Thus

```
D_y(T) = product_(t in S) (T-t)^(3-r_t)
```

is monic of degree `6L-2L=4L`. Every product of at least three distinct row
factors is divisible by `D_y`, since at most `r_t` factors survive at `t`.
The products of at most two factors still have degree at most `4L-2`.
Therefore the remainder of any such contraction modulo `D_y` has degree at
most `4L-2`, ruling out every polynomial of degree exactly `4L-1` for every
choice of fixed one-hot columns.

The value of `H_1^4` at `-L` is nonzero and its values at `L-1` and
`-L+1` are zero. If no row survives at either extreme, all matrix entries
are zero there and the contraction equals its value at `-L`. Thus any
realization must have a selected column `L-1` to support `t=L-1`, and a
selected column `0` to support `t=-L+1`. With only two columns, this forces
the endpoint pair already excluded above. Hence no pair of fixed one-hot
columns realizes `H_1^4`, even over the rationals. Different column
assignments, unfixed columns, and more packets remain outside this statement.
