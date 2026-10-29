# One-hot affine one-packet obstruction

This concerns the prescribed single-packet deformation interface and the
node residues of the generic taper polynomial. It does not rule out a
single-packet construction with another column support or a nonlinear row
table, nor does it give a counting or SAT lower bound. It is motivated by
the two-packet interpolation in [PR #52](https://github.com/1337isnot1337/3-SAT/pull/52).

## Statement

Let `L=2^a>=2`, `1<=u<=a`, and use the source Cauchy deformation on a
single full packet. Work over its two-adic scalar ring (or its unramified
extension with residue field `k` of characteristic two). Suppose the row
table is affine modulo two,

```math
 A(Y)\equiv a_0+\sum_{x=0}^{L-1}a_xY_x,
```

and the column table is supported **only** on the `L` one-hot inputs. Let
`F(T)` be the deformed contraction. There is no such construction for which,
at every grid node `t` in `S={-L,...,L-1}`,

```math
 F(t)\bmod 2=\begin{cases}
 \gamma,&2^u\mid t,\\
 0,&2^u\nmid t,
 \end{cases}\qquad \gamma\in k^\times.
 \tag{1}
```

In particular this rules out an odd scalar multiple of any positive power
of the level-`u` taper factor, or of the full tapered polynomial with
parameter `u`, under these table restrictions. It already fails at the
node-value level, so supplying more jets cannot repair this specific model.

For `u=1`, relaxing the column support to include the all-zero input yields
an explicit canonical Boolean counterexample to the obstruction: the
row table `A(Y)=1+sum_x Y_x mod 2` and the column table equal to one on
zero and all one-hot inputs, and zero elsewhere, satisfy (1) with `gamma=1`.
The source's complete shifted jets at each node reduce modulo two to their
constant node value, so its odd-node jets vanish modulo two. This escape
only establishes precision one, not the high-precision tapered witness.

## Proof

At any node `t`, the Cauchy entry `W_xy(t)` is zero unless `y-x=t`.
In that case it is `C'(t)/C'(0)`, a two-adic unit and hence equal to `1`
after reduction to `k`. At `t=-L` every entry is zero because the slot
range only allows differences `-L+1,...,L-1`.

Let `b_y` be the column table's value at one-hot input `e_y` modulo two,
and set `B=sum_y b_y`. The affine row assumption gives

```math
 F(t)=a_0B+\sum_{y-x=t} a_xb_y\quad\text{in }k,
 \qquad -L\le t<L.
```

By (1) at `t=-L`, `a_0B=gamma`, hence `B != 0`. Introduce polynomials

```math
 R(z)=\sum_{x=0}^{L-1}a_xz^{L-1-x},\qquad
 Q(z)=\sum_{y=0}^{L-1}b_yz^y.
```

The coefficient of `z^(t+L-1)` in `R Q` is the sum over `y-x=t`.
Equation (1) therefore forces

```math
 R(z)Q(z)=\gamma P(z),\qquad
 P(z)=\sum_{\substack{-L+1\le t<L\\2^u\nmid t}}z^{t+L-1}.
```

Writing `q=2^u`, in characteristic two this polynomial factors as

```math
 P(z)=\left(\sum_{j=0}^{q-2}z^j\right)
       \left(\sum_{r=0}^{2L/q-1}z^{qr}\right)
     =\left(\sum_{j=0}^{q-2}z^j\right)(1+z)^{2L-q}.
```

The first factor evaluates to `q-1=1` at `z=1`, so the multiplicity of
`1+z` in `P` is exactly `2L-q`. Since `q<=L`, this multiplicity is at least
`L`. But `Q(1)=B != 0`, and `deg R <= L-1`. Therefore `R Q` cannot have
this multiplicity, a contradiction. This argument works over any residue
field of characteristic two and requires no rational factorization.

For the claimed taper specialization, each root of valuation less than
`u` forces value zero. At any other grid point, each normalized root factor
is a two-adic unit congruent to one, including the value at `-L`. The same
holds after taking positive powers and multiplying by a scalar whose residue
is `gamma`. Thus its node residues are exactly (1).

## The zero-column escape

Use canonical Boolean tables as stated. Modulo two, the row table is
`1+sum_x Y_x`, including its multilinear representation. The column table
has `L+1` allowed inputs and total parity one, because `L` is even. At a
node `t`, the sum of the shift indicators over all `x,y` is `L-|t|` for
`|t|<L`, and zero at `t=-L`. Consequently

```math
 F(t)=1+(L-|t|)\equiv1+t\pmod2
```

for all `t` in `S`, including `-L`; this is one at even nodes and zero at
odd nodes. Here the coefficient polynomial of the one-hot part still has
both its row and column factors divisible by `(1+z)^(L-1)`; the extra zero
input changes the total column sum to one. That is precisely why the
preceding proof's `Q(1) != 0` conclusion no longer applies.

In the shifted grid coordinates, each `W_xy(t+2Lz)` has constant reduction
the displayed shift indicator and all higher coefficients divisible by two,
by the source integrality lemma. Any contraction made from integral tables
therefore has constant reduction modulo two throughout its full shifted jet.
Thus the example's odd-node jets vanish at precision one. No claim is made
about the exact content beyond one, all-node high-precision recovery, actual
balanced packing, or a general single-packet lower bound.

### This particular escape fails at precision two

At `t=1`, every nonzero Cauchy entry has value

```math
 \frac{C'(1)}{C'(0)}=-\frac{L+1}{L-1}.
```

The all-zero column and the one-hot column at `y=0` each contribute one.
Each of the remaining `L-1` one-hot columns has exactly one nonzero row
coordinate, with value `w=-(L+1)/(L-1)`. The probability polynomial for
our Boolean even-parity row table then evaluates to `1-w`. Therefore

```math
 F(1)=2+(L-1)(1-w)=2(L+1).
```

Because `L` is even, `v_2(F(1))=1`. The complete shifted jet at node one
thus has exact content one: it is divisible by two coefficientwise, but its
constant coefficient is not divisible by four. This is an all-size
precision-two failure for this particular Boolean escape, not an obstruction
to other row or column tables.
