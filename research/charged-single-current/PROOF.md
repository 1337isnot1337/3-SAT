# Vanishing moments for the single-part source label

This is an author-checked, AI-assisted component argument, not an independent
or formal review and not a SAT improvement. We use the charged Q pieces and
normal-ordering conventions of [PR #11](../charged-operator-moments/PROOF.md),
which extend the source's two-order Laurent construction by a central zero
mode. The basic encoded dual labels and contraction identity below are from
that predecessor.

## Statement

Let h>=1, let `a^(h)=(-1)^(h-1) sum_(j=1)^h binom(h,j)t_j` be the
dual label indexed by the one-part partition `(h)`, and let b be any
homogeneous polynomial of weight h. For every integer charge q, output
energy E>=0, and d=1,...,h,

```math
 \sum_{s=-E-h}^{E+h} s^d Q_s^{(q)}(a^{(h)},b)=0
 \quad\text{as an operator on }V_E.                    \tag{1}
```

The shifts are finite by the predecessor's energy bound. By linearity,
for every polynomial f of degree at most h,

```math
 \sum_s f(s)Q_s^{(q)}(a^{(h)},b)
 =f(0)\sum_s Q_s^{(q)}(a^{(h)},b).                    \tag{2}
```

In particular, if f(0)=0 then the filtered row indexed by `(h)` vanishes
on the **whole** output space, not merely on a parity compression. The
statement does not say that other input rows vanish or that a high-capacity
asymmetric minor cannot exist.

## Proof

It is enough to take b to be a partition monomial of weight h; repeated
parts are treated as labeled when choosing contractions. For each j,
the homogeneous component `t_j` of a^(h) has one field. Let F_j(w1,w2)
be its contribution to the common Laurent polynomial in the source's
two-order calculation, after multiplication by `(w1-w2)^(j+h)`. As in
PR #11, partial contractions pair one first-side current with one
second-side current. The charged D_0 is central and contributes only
regular uncontracted fields; the nonzero-mode contraction kernel is
unchanged.

There are only two cases.

1. With no contraction, the entire factor `(w1-w2)^(j+h)` remains. The
   normal-ordered coefficient is regular at w1=w2=1, even with charge.
   Every such term is divisible by `(w1-w2)^(h+1)` because j>=1.
2. With one contraction against a second-side part of size k, its kernel
   is `gamma_(j,k)/(w1-w2)^(j+k)`, where

   ```math
   \gamma_{j,k}=(-1)^{j-1}(j+k-1)!/((j-1)!(k-1)!).
   ```

   The remaining power is `(w1-w2)^(h-k)`. All remaining fields are on
   the second side, so their normal-ordered coefficient is independent of
   j. Summing over the encoded first-side components leaves the factor

   ```math
   \sum_{j=1}^{h}(-1)^{h-1}{h\choose j}\gamma_{j,k}
    =k {k-1\choose h-1}.                                \tag{3}
   ```

   This is the binomial identity proved in PR #11, section 2. It vanishes
   for k<h. Since the parts of b sum to h, k=h can occur only when b is
   the single part `(h)`. In that case no fields remain and the term is a
   constant times the identity, independent of w1 and w2.

Therefore, with w1=1+z and w2=1, the sum F of these contributions satisfies

```math
 F(1+z,1)-F(1,1) \in z^{h+1}\,\mathbb Q[[z]]
```

for every output matrix coefficient. This uses only expansion at z=0,
where the Laurent coefficients are regular; no analytic limit is needed.
The source's coefficient identity reads
`F(w1,w2)=sum_s <Q_s> w1^s w2^(-s)`. For d>=1 the operator
`(w1 partial_(w1))^d` has no zeroth-order term and at w1=1 uses derivatives
of order at most d. It therefore annihilates the displayed difference for
d<=h, while the coefficient reading gives the left side of (1). This holds
for every matrix entry and hence as an operator. Equation (2) follows by
expanding f.

## Sharpness for every grade

Take any integer q, `b=b^(h)=(h-1)! t_h` and the input/output state `t_h` in V_h.
The only no-contraction contribution at order h+1 comes from the j=1
component of a^(h), whose coefficient is `(-1)^(h-1)h`; the sole fully
contracted term is constant. At coincident coordinates the diagonal
coefficient of the normal-ordered product of the t1 and th fields is

```math
 q^2(-1)^{h-1}+h\left(1+{-h-1\choose h-1}\right).
```

The first term uses the two charge-q zero modes. The other two terms
annihilate the part h and then recreate it, with the two possible choices
of which field supplies the creation. Multiplying by the encoded a and b
coefficients and applying the (h+1)-st logarithmic derivative gives

```math
 [t_h]\left(\sum_s s^{h+1}Q_s^{(q)}(a^{(h)},b^{(h)})\right)t_h
 =(h+1)!h!\left(q^2+h{2h-1\choose h-1}+(-1)^{h-1}h\right)>0. \tag{4}
```

Here `{ -h-1 choose h-1}=(-1)^(h-1){2h-1 choose h-1}`; the displayed
integer is positive for every h>=1 and every integer q. Thus the cutoff in (1) is sharp at
every grade. The checker independently compares (4) to exact finite operator
vectors for h=1,...,6.

Equation (1) explains one zero row of the cubic parity pairing when h>=3
and f(s)=(s^3-s)/6. It gives no bound stronger than one lost input direction
and does not establish the conjectured `p(h)-p(h-3)` rank or any complete
algorithm. A filter of degree at most h may still use other asymmetric
input labels and the row `(h)` need not be in the chosen codebook. Precision,
source rank bounds, all global costs, and a growing or fixed-fraction shift
exclusion remain separate obligations.
