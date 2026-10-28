# Three-partition low-shift space

This argument is author-checked, AI-assisted, and not independently reviewed.
We use the pinned Anthropic Appendix-B operators, in the notation and with
the hypotheses of [PR #59](../scalar-relation-witness/PROOF.md). The
accepted OpenAI theorem remains a separate premise. All partitions in this
note belong to the full weight-h partition space.

## Statement

For every h>=2, the shift span of the full uncharged crossing-piece family
has rank at least

```
2h + max(0,h-4) + 2 max(0,floor(h/2)-2) + 2[h>=4] + 2[h>=6] + [h>=9].
```

For even h>=10 this is 4h-3, and for odd h>=9 it is 4h-4. This
strengthens PR #59's lower bound of roughly 7h/3.
Both remain below its 4h upper bound. Moreover, for h>=9 the fixed
all-ones label slice has shift-span rank exactly 2h: the symmetric
low-support witnesses below have dimension h, the predecessor's h
high-support F_l rows are independent of them, and PR #59 gives the
matching upper bound. The new witnesses use y=(h), which can be absent
from the source's lexicographic binary codebook; no stronger binary-codebook
bound, SAT algorithm, or time improvement is asserted.

## The three-partition formula

Fix h>=4, labels x=v=e=(1^h), and input y=(h). For each three-part
partition u of h, write m_j(u) for the multiplicity of j and P_u(z) for
the corresponding Laurent polynomial `sum_s [t^u]Q_s t_h z^s`.
Normal ordering gives

```
P_u(z) = C_h / product_j m_j(u)! * (z-1)^4 z^(-h-2)
         * sum_{j=1}^{h-2} m_j(u) (z^j + z^(2h-j)),
C_h = 4h binom(h,2)^2 (h-2)! > 0.                             (1)
```

Indeed t_h permits exactly one annihilation and u requires three
creations, so there are precisely four uncontracted t_1 fields: two from
each copy. The remaining h-2 fields pair in `(h-2)!` ways, and the two
uncontracted fields are chosen on each side in `binom(h,2)^2` ways.
If the annihilation occurs at z, one creation is at z and two are at 1;
if it occurs at 1, two creations are at z and one is at 1. Summing over
the distinguished part j gives the two monomials in (1). The coefficient
4h counts the annihilation, its two possible positions, and the order of
the two creation slots. Equal parts contribute their displayed factorial.

The expression is symmetric under z -> 1/z. Its coefficient at z^(h+1)
is `C_h m_1(u)/product m_j(u)!`, and by symmetry the negative endpoint
is the same; no shift outside `[-h-1,h+1]` occurs. Each j has unique
monomials z^j and z^(2h-j), because `1<=j<=h-2`. Thus multiplication by
the common nonzero Laurent polynomial in (1) embeds the rational vector
space spanned by the multiplicity vectors `(m_1,...,m_{h-2})` into the
space spanned by the piece entries.

## Dimension of the multiplicity-vector span

The span of the three-partition multiplicity vectors over Q has dimension
h-3. To prove this, let `(c_1,...,c_{h-2})` annihilate every such vector.
For each `1<=i<=h-2`, the partition `(i,1,h-i-1)` gives

```
c_i + c_1 + c_{h-i-1}=0.
```

For each `1<=i<=h-3`, the partition `(i,2,h-i-2)` gives
`c_i+c_2+c_{h-i-2}=0`. Subtracting, the successive differences
`c_j-c_(j-1)` are all equal for 2<=j<=h-2. Hence `c_j=A+Bj`.
The three-partition equations reduce to `3A+Bh=0`, which defines a
one-dimensional annihilator. Conversely every such affine vector does
annihilate every three-part partition. The span dimension is therefore
`(h-2)-1=h-3`.

The coordinate functional m_1 is nonzero on this span, for example on
`(h-2,1,1)`. Its kernel has dimension h-4. By (1), that kernel corresponds
to an h-4-dimensional space of genuine rational combinations of piece
entries supported entirely in `[-h,h]`: m_1=0 cancels both endpoint
coefficients. Multiplicity-vector embedding ensures no nonzero vector in
this kernel maps to the zero Laurent polynomial.

## A diagonal symmetric low-shift row

Still using x=v=e and y=(h), let P_diag be the row with output (h), and
let P_ref be the row for the three-part output `(h-2,1,1)`. The original
crossing identity gives `P_diag(1)=h!`, while P_ref(1)=0. At z^(h+1),
the first operator produces `h^2 t_1^(h-1)`. To return to t_h, the
second annihilates all h-1 ones and creates t_h, in h choices, so the
diagonal endpoint is `h^2 h!`. Formula (1) gives the P_ref endpoint
`C_h=(h-1) h^2 h!`. Therefore

```
W_diag = (h-1) P_diag - P_ref
```

is symmetric and supported in [-h,h]. It is annihilated by L, since both
of its rows lie in the all-ones label slice, and `W_diag(1)=(h-1)h!`.
Every row of the three-part low-shift space vanishes at z=1, by (1).
Consequently W_diag adds one independent symmetric direction.

## A second symmetric input

Assume h>=6, set y=(h-1,1), and take labels x=v=e. For a two-part
output u=(a,b), a+b=h and a,b>=2, its shift polynomial is

```
P_(a,b)(z)= K_h/Z_(a,b) * (z-1)^4 z^(-2) * [
  z^(-h)+z^h+z^(1-a)+z^(a-1)+z^(1-b)+z^(b-1) ],
K_h=4(h-1) binom(h,2)^2 (h-2)!.                            (2)
```

Both input parts must be annihilated and both output parts created; no
other normal-ordered field count can contribute. Thus exactly two fields
remain on each side, and the h-2 remaining pairs give `(h-2)!`. In the
normal-ordered four-field term, choose which two of the events
`-(h-1),-1,+a,+b` occur at z. The six possible exponent sums give the
six terms displayed. The factor 4 orders the two z and two unit slots,
the annihilation multipliers give h-1, and Z accounts for repeated
output parts. This also covers a=b.

Let u=(h-2,2) and v=(h-3,3), and form `W=Z_u P_u-Z_v P_v`.
The z^h and z^-h terms cancel; all other exponents in (2) give shifts
inside [-h,h]. The row is symmetric, annihilated by L, and vanishes at
z=1. After division by the common nonzero Laurent factor
`K_h (z-1)^4 z^(-h-2)`, its coefficient of z^(h-1) is exactly one:
u contributes its part 2, while neither part of v does. In contrast,
the three-partition low-shift space from (1) has no z^(h-1) term after
this same division. The diagonal row cannot help because it is nonzero
at z=1. Thus W adds a further independent symmetric direction for h>=6.

## A third symmetric direction

Continue with y=(h-1,1), u=(h-2,2), labels e,e, and h>=6. Write
`D_y` for the diagonal row with output y, `P_(y,u)` for the row in (2),
`D_h` for the diagonal row with input and output (h), and `P_ref` for the
three-part row `(h-2,1,1)` with input (h). Let Z_u be u's multiplicity
factor. The combination

```
V = (h-1)(D_y - Z_u P_(y,u) - D_h) + P_ref
```

is symmetric, supported in [-h,h], annihilated by L and zero at z=1.
To see support, the four-uncontracted-field terms of D_y and Z_u P_(y,u)
have the same extreme terms z^h and z^-h in (2), so they cancel. The
remaining two-field diagonal terms have support in [-h,h]. The final
`-(h-1)D_h+P_ref` is the negative of W_diag above.

All terms in V have zero first moment; L(V)=0 and V(1)=0 give zero second
moment. Symmetry then forces a zero of order at least four at z=1. Divide
by `(z-1)^4 z^(-h-2)`. Its coefficient at z^h is

```
2h(h-1)^2(h-2) h! > 0.                                    (3)
```

Here is the coefficient calculation. D_h's constant cancels D_y's
constant. D_y's two-field contribution is

```
h h! (z-1)^2 [(h-1)(z^(h-2)+z^(-h)) + 1+z^(-2)],
```

and D_h's is `h^2 h! (z-1)^2 (z^(h-1)+z^(-h-1))`. Using
`(1-z)^(-2)=sum_{n>=0}(n+1)z^n`, their difference contributes
`-2h(h-1)^2 h!` to the specified coefficient after the outer h-1
factor. The four-field part of D_y contributes two central terms; with
`K_h=h(h-1)^2 h!` from (2), this adds `2(h-1)K_h`. The other terms of
`P_(y,u)` and P_ref have no central coefficient after division. Their sum
is (3).

The three-part low-shift space has no central coefficient after the same
division, nor does the preceding second-input row: its residual exponents
are h plus or minus a-1 or b-1, with a,b>=2. W_diag is nonzero at z=1,
so it also cannot participate in a relation for V. Thus V adds another
symmetric direction for every h>=6.

## A fourth symmetric direction

Assume h>=9. Take e,e labels, input y=(h-3,3), and outputs
u=(h-2,2), v=(h-4,4). The two input parts are distinct, and neither
output shares an input part. For a general such pair y=(h-p,p),
u=(h-a,a), normal ordering gives

```
Z_u P_(y,u)(z) = K_(h,p) (z-1)^4 z^(-2) * [
 z^(-h)+z^h+z^(a-p)+z^(p-a)+z^(h-p-a)+z^(-h+p+a) ],
K_(h,p)=4p(h-p) binom(h,2)^2 (h-2)!.
```

All four input/output events must remain uncontracted; the input
annihilation multipliers give p(h-p). The six choices of two events at z
produce the displayed exponent sums, just as in (2). Subtract the two
rows after multiplying each by its output multiplicity factor Z. The
universal extreme terms cancel, and the remaining shifts are inside
[-h,h]. This symmetric low-shift row W has L(W)=0 and W(1)=0.

After division by `K_(h,3)(z-1)^4 z^(-h-2)`, its residual is exactly

```
z^5 + z^(2h-5) - z^7 - z^(2h-7).                           (4)
```

Since h>=9, its center and its z^(h-1) coefficient vanish. Therefore a
relation with the earlier symmetric rows has zero coefficients on the
central witness and the z^(h-1) witness; W_diag also has zero coefficient
because W(1)=0. The remaining three-part low-shift space corresponds to
vectors in the hyperplane `sum_j (3j-h)v_j=0`. The vector in (4) has
v_5=1, v_7=-1 and all other lower-half coordinates zero, giving -6 under
that functional. Thus W is outside the earlier symmetric space and adds
one direction for h>=9. The case h=9 has a pair of repeated middle terms
at j=7 only when j=h, which does not occur; the four displayed powers
remain distinct.

## A one-sided space from two-part outputs

Set d=(2,1^(h-2)), with x=d, v=e and y=(h). For a two-part partition u,
let `Z_u=product_j m_j(u)!` and let Q_u(z) be its shift polynomial. The
normal-order expansion gives, for h>=4,

```
Q_u(z) = -h h!/Z_u * (z-1)^3 z^(-h-2) * [
    (h+1)-(h-1)z
    + sum_j m_j(u) z^(h+j) ((j+1)z-(j-1)) ].                 (2)
```

For completeness, here is the contraction count. With
`a^d=-(t_2+2t_1)t_1^(h-2)` and `b^e=t_1^h`, reaching two output parts
from t_h requires one annihilation and two creations, hence three fields
remain uncontracted: one from a and two from b. Let
`D=-binom(h,2)(h-2)!=-h!/2`. Using the source's contraction constants
`Gamma_11=1` and `Gamma_21=-2`, the component where the t_2 field is
contracted combines with the lower homogeneous component to give `2D`
times `:J_1(z)J_1(1)^2:`. The component where t_2 remains uncontracted
gives D times `(z-1):J_2(z)J_1(1)^2:`. The remaining factors are
`(z-1)^3`. Between t_h and t^u, the two normal-ordered entries are

```
2h/Z_u [z^(-h-1) + sum_j m_j(u) z^(j-1)],
2h/Z_u [-(h+1) z^(-h-2) + sum_j m_j(u)(j-1) z^(j-2)],
```

respectively. Substitution gives (2), including repeated parts.

For each `2<=a<=floor(h/2)` let u_a=(h-a,a), and normalize
`R_a=-Z_(u_a) Q_(u_a)/(h h!)`. Subtract R_2. Equation (2) cancels the
common negative-power term and gives

```
R_a-R_2 = (z-1)^3 sum_j [m_j(u_a)-m_j(u_2)]
          z^(j-2) ((j+1)z-(j-1)).                            (3)
```

Every j in (3) lies between 2 and h-2. Thus these polynomials have no
negative shifts and no shifts greater than h. The multiplicity vectors
of u_a are independent: each unordered pair `{a,h-a}` is disjoint from
every other such pair, with a repeated middle part handled by its
multiplicity. Their differences from u_2 are consequently independent.
The polynomials `z^(j-2)((j+1)z-(j-1))` have distinct degrees and
nonzero leading coefficients, so (3) maps those vectors injectively.
There are `max(0,floor(h/2)-2)` independent differences.

PR #59 proves that every x=d, v=e entry has zeroth and second moments
zero, so L annihilates this one-sided space. It meets the previous
symmetric low-support space only at zero: a polynomial both symmetric
under z -> 1/z and supported on nonnegative shifts is constant, while
(3) is divisible by `(z-1)^3` and therefore vanishes at z=1.

## A second one-sided space and its independence

Reverse the labels: x=e, v=d, still with y=(h), and put
`c=h!/[2(h-2)!]`. For a two-part output u, normal ordering gives

```
Q^rev_u(z) = c h h!/Z_u * (z-1)^3 * [
  2(h-2) z^(h-2) -(h+1)(z-1) z^(h-2)
  + 2(h-2) sum_j m_j(u) z^(j-h-2)
  + (z-1) sum_j m_j(u)(j-1) z^(-j-2) ].                    (4)
```

Here `b^d=c t_2 t_1^(h-2)` and `a^e=t_1^h`. Three uncontracted
fields consist of two from a and one from b. If b's t_2 is contracted,
`Gamma_12=2` and its partner can be chosen in h-2 ways; if t_2 remains
uncontracted it carries one extra factor z-1. Between t_h and t^u the
resulting normal-ordered entries are

```
2h/Z_u [z^(h-2) + sum_j m_j(u) z^(j-h-2)],
2h/Z_u [-(h+1)z^(h-2) + sum_j m_j(u)(j-1) z^(-j-2)].
```

The common contraction factor is `c binom(h,2)(h-2)!=c h!/2`, giving
(4). For the same u_a as in the previous section, normalize by
`Z_(u_a)/(c h h!)` and subtract the normalized u_2 row. The first two
terms in (4) cancel. Since each remaining part j satisfies 2<=j<=h-2,
the resulting rows have only nonpositive shifts and are supported in
[-h,h]. Their normalized multiplicity differences are independent, as
shown above. To see that (4) maps them injectively, its first sum supplies
an extreme negative exponent `j-h-2` with nonzero coefficient for the
smallest j in a nonzero vector; the second sum may overlap it, so a
separate algebraic argument below proves injectivity together with the
stronger independence statement.

Let V be the space of coefficient vectors v with v_j=v_(h-j), supported
on 2<=j<=h-2. Every difference of the pair multiplicity vectors belongs
to V. Its associated polynomial
`U_v(z)=sum_j v_j z^(j-1)` obeys `U_v(z)=z^(h-2)U_v(1/z)` and
`U_v(0)=0`. After factoring out `(z-1)^3`, the positive-only rows from
(3) have the form

```
(z-1) U_v'(z)+2U_v(z),
```

and the reversed negative-only rows, after z -> 1/z, have the form

```
(z-1) U_w'(z)-2(h-2)U_w(z).
```

We prove these two images have zero intersection. Suppose they agree,
put D=U_v-U_w and n=h-2, and rearrange to

```
2(h-1) U_w = -[(z-1)D'+2D].                              (5)
```

D and U_w are reciprocal of degree n. Thus the bracket in (5) is also
reciprocal. Comparing it with its reciprocal and cancelling the nonzero
factor z-1 gives `(z-1)D'=nD`. The only polynomial solutions are
`D=C(z-1)^n`; since D(0)=0, C=0. Equation (5) then gives U_w=U_v=0.
This also proves each image map injective, by setting the other input
to zero. Hence the new negative-only space has dimension
`max(0,floor(h/2)-2)`.

It remains independent of the augmented symmetric low-support space,
including W_diag, both second-input rows and the fourth-input row,
together with the previous positive-only space. If S is symmetric and P,N are the
positive- and negative-only rows with S+P+N=0, then
`P(z)-N(1/z)` is both a polynomial in z and a polynomial in z^-1, hence
constant. Both P and N vanish at z=1, so that constant is zero; the
zero-intersection result forces P=N=0 and then S=0. All these rows are
annihilated by L: the symmetric slice and the x=d,v=e slice were handled
above, while PR #59's all-ones second-moment proof uses only field counts
and likewise makes the x=e,v=d zeroth and second moments zero. For the
latter, b^d has h-1 fields and a^e has h; a weight-two uncontracted
term cannot leave equal numbers for contraction, while the only weight-one
term is an energy-changing current. Duality gives the zero zeroth moment.

## Independence from the predecessor witnesses

PR #59 constructs h symmetric rows F_l with nonzero endpoints at +/-(h+l),
h-1 nonsymmetric rows G_l with positive support <=h+l and a nonzero
negative endpoint at -(h+l+1), and a diagonal row H separated from all
F_l and G_l by the even moment functional
`L(P)=sum_s (s^2-4h^2)[z^s]P`. Its all-ones label slice satisfies L=0,
so every row in the low-support space above is also annihilated by L.

In a relation between that space and the predecessor rows, L first forces
the coefficient of H to zero. At shift +2h only F_h remains among the
other rows, so its coefficient is zero; then shift -2h isolates G_(h-1).
Proceeding downward through h+2 successively eliminates F_l and G_(l-1);
shift h+1 finally eliminates F_1. All three low-support spaces have no terms at those shifts and their
sum is direct, so that sum meets the predecessor span only at zero.
Their dimensions give rank at least
`3h-3+2 max(0,floor(h/2)-2)+2[h>=6]+[h>=9]` for h>=4.
For h=2,3 the predecessor's 2h bound applies. The previous PR's
low-support witnesses are not counted again.

## A nonsymmetric high-shift direction

For h>=4, take labels x=d, v=e, input `(h-1,1)` and output `(h)`.
Call its shift polynomial R. As before, the mixed zeroth and second
moments vanish, so L(R)=0. Normal ordering gives

```
R(z)=-(h-1)h! (z-1)^3 [
 h z^(-h-1) -(h-2)z^(-h) +2z^(-3)
 +(h+1)z^(h-1) -(h-1)z^(h-2) ].                            (5)
```

Indeed exactly one field remains uncontracted on the a side and two on
the b side. The coefficient of `:J_1(z)J_1(1)^2:` is `-h!`, and that
of `(z-1):J_2(z)J_1(1)^2:` is `-h!/2`. Between input `(h-1,1)` and
output `(h)` their entries are respectively

```
2(h-1)[z^(-h)+z^(-2)+z^(h-1)],
2(h-1)[-h z^(-h-1)-2z^(-3)+(h-1)z^(h-2)],
```

which gives (5). In particular R is supported in `[-h-1,h+2]` and
its four relevant endpoint coefficients obey

```
(R_(-h-1)-R_(h+1))/(R_(-h-2)-R_(h+2)) = -(3h+2)/(h+1). (6)
```

Let G_1 be the first nonsymmetric predecessor hook row. Its input is
(h), its labels are d,e, and its output is e for even h and d for odd h.
It has no positive shift h+2, a nonzero negative shift -h-2, and

```
(G_1,-(h+1)-G_1,h+1)/G_1,-(h+2)
  = -h                                                    if h=2k,
  = -(2k^3+3k^2+4k+2)/(k+1)^2                           if h=2k+1. (7)
```

For a direct derivation, set
`D=-binom(h-2,k-1)binom(h,k+1)(h-k-1)!`. Normal ordering the d,e labels
and input (h) leaves k fields on the a side and k+1 on the b side. If
h=2k, the output is e and

```
G_1(z)=D h (z-1)^(h+1) [(h+1)z^(-h-2)-z^(-h-1)+(h+2)].
```

If h=2k+1, the output is d and

```
G_1(z)=D h (z-1)^h [
 2k(((k-1)z+(k+1))z^(-h-1)+(k+1)(z+1))
 +(z-1)(-(h+1)((k-1)z+(k+1))z^(-h-2)
          +(k-1)z^(-h-1)+(k+1)) ].
```

These expressions use the same `Gamma_21=-2` contraction and the
`J_1,J_2` definitions as (2); expansion gives (7). The normal-order
checker compares them with the original recurrence at h=4,5,6.

The values in (6) and (7) differ for every h>=4. In the even case this
is `h^2-2h-2>0`; in the odd case k>=2 and the difference after clearing
positive denominators is `(k-1)(2k+1)^2>0`.

R cannot lie in the preceding span. If it did, L(R)=0 and all low rows
and F_l,G_l have zero L, while L(H)!=0, so H's coefficient would vanish.
R has no shifts beyond h+2 in magnitude. Descending through high shifts
forces all F_l with l>=3 and all G_l with l>=2 to vanish, leaving only
F_1,F_2,G_1. Since F_1,F_2 are symmetric and G_1 has zero positive
h+2 endpoint, their antisymmetric endpoint ratios would force (6) to
equal (7), a contradiction. Thus R adds one independent direction for
all h>=4. It uses states that may be absent from the binary codebook.

## Limits

The proof invokes the predecessor's all-size identities and source normal
ordering; neither has independent review here. The finite check is not an
all-size proof. The lexicographic codebook, crossing ranks, factor sizes,
recursive schedule, outer reductions, precision and recovery would all
need separate treatment for an algorithmic consequence.
