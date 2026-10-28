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
2h + max(0,h-4) + 2 max(0,floor(h/2)-2) + 2[h>=4] + 2[h>=6] + [h>=9] + [h>=11 and h odd].
```

For every h>=10 this is 4h-3; at h=9 it is 4h-4. This
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

## Four exact antisymmetric moment constraints

For any Laurent polynomial supported in [-h,h], define

```
M_k(P)=sum_{s!=0} sign(s) |s|^k [z^s]P,    k=1,2,3,4.
```

All rows in either one-sided low-shift space satisfy these four equations.
To check this, let `b_j=j^k` for j>=0 and write
`Delta^3 b_t=b_(t+3)-3b_(t+2)+3b_(t+1)-b_t`. On the positive-only
basis polynomial for a part j, M_k evaluates to

```
(j+1) Delta^3 b_(j-1) - (j-1) Delta^3 b_(j-2).
```

For the reversed negative-only basis the corresponding expression, up to
a common sign, is

```
(j-2h+3) Delta^3 b_(j-1) - (j-1) Delta^3 b_(j-2).
```

For k<=2 these are zero. For k=3 they are constants in j; for k=4 they
are affine in j, since `Delta^3 j^4=24j+36`. The multiplicity differences
are symmetric under j -> h-j and have coefficient sum zero, so sums of
both constants and affine terms vanish. The symmetric low-shift rows also
have M_k=0 automatically.

For even h>=4 the two one-sided spaces have combined dimension h-4, and
their antisymmetric projection is injective by the preceding section.
The antisymmetric low-shift space has dimension h. The four moment
functionals are independent there: their values on shifts 1,2,3,4 form a
nonsingular Vandermonde-type matrix. Hence the antisymmetric projection
of the two constructed spaces is **exactly** the joint kernel of M_1,...,M_4.
For odd h>=5 there is one additional explicit moment. Put h=2k+1 and
define rational numbers x_0,...,x_(h-3) as follows. Set x_0=0, x_1=1,
y_1=1, and for 2<=a<=k set

```
y_a=-(a-1)y_(a-1)/(h-a-1),    x_a=x_(a-1)+y_a.
```

Put `K=x_(k-1)+x_k`, and for 2<=a<=k set
`x_(h-a-1)=K-x_(a-1)`; the final assignment is consistent with x_k.
Define q_0=q_1=q_2=0 and, for 0<=t<=h-3,
`q_(t+3)=x_t+3q_(t+2)-3q_(t+1)+q_t`. Thus `Delta^3 q_t=x_t`.
The fifth moment is

```
M_q(P)=sum_{s!=0} sign(s) q_|s| [z^s]P.
```

It vanishes on the constructed one-sided spaces. Indeed, their pairwise
partitions require the sum over j=a,h-a of each of the two displayed
finite-difference expressions to be constant in a. The recurrence gives
`(h-a-1)(x_a-x_(a-1))=-(a-1)(x_(a-1)-x_(a-2))`, and reflection gives
`x_(a-1)+x_(h-a-1)=K`. Substitution shows the positive expression sums
to 2K and the reversed expression to `-2(h-2)K`, independently of
2<=a<=k. Differences from the reference pair therefore vanish.

M_q is independent of M_1,...,M_4. Otherwise its weights q_j would be a
linear combination of j,j^2,j^3,j^4, whose third differences are affine
in j. But x_0=0, x_1=1 and x_2=1-1/(h-3) are not affine. The constructed
antisymmetric projection has dimension h-5 for odd h, so these five
independent equations characterize it exactly. These are statements about
the constructed low-shift subspace, not universal moment relations for
every crossing piece.

## Breaking the odd fifth moment

For odd h>=11, take labels x=d,v=e, input y=(h-1,1), and outputs
u=(h-6,3,3), v=(h-7,4,3). Neither output shares an input part, and
both have all parts at least 3. Put `W=Z_u P_u-Z_v P_v`.

Here exactly two fields on the a side and three on the b side remain
uncontracted. Let

```
D=-(h-2)h!/6,       C=6(h-1)D=-(h-2)(h-1)h!.
```

Normal ordering gives the following explicit formula. Let the five signed
events be `-(h-1), -1` and the three positive parts of the output. For an
unordered pair of events with sum t, write
`B_t(z)=z^(t-3)[(t+2)z-(t-2)]`. Then

```
Z_w P_w(z) = C (z-1)^5 sum_{event pairs} B_t(z).             (8)
```

To derive it, the coefficient of
`:J_1(z)^2 J_1(1)^3:` is 2D and that of
`(z-1):J_2(z)J_1(z)J_1(1)^3:` is D. The input annihilation factor is
h-1. Choosing two events at z gives 2!3! orderings in the first term;
in the second, choosing which of the two is the J_2 event contributes
the sum of its signed event weights minus two. This yields (8), including
repeated output parts.

In W the pair of negative input events cancels. For an output part j,
the remaining pair sums are `h-j`, `j-1`, and `j-h+1`. Because every
output part lies in [3,h-6], the surviving terms have support inside
[-h,h]. Duality and the mixed second-moment identity give L(W)=0.
Let q be the odd-grade weights from the preceding section and define
`B_s=sign(s)q_|s|`, B_0=0. For an integer t, put

```
H(t)=(t+2) Delta^5 B_(t-2) - (t-2) Delta^5 B_(t-3).
```

Oddness of B implies H(-t)=H(t). Formula (8), and the output-multiplicity
difference `e_(h-6)+e_3-e_(h-7)-e_4`, give

```
M_q(W)/C = H(5)-H(7)+H(2)-H(3)
           +H(h-3)-H(h-5)+H(h-7)-H(h-8).                  (9)
```

For odd h>=13 the recurrence for q has the closed difference form

```
Delta^2 x_t = (-1)^(t+1) [1/binom(h-3,t+1)+1/binom(h-3,t)]
```

through the indices used here, and reflection gives
`x_(h-t-2)=K-x_t`. Substitution into (9) simplifies to

```
M_q(W)/C = -(h-2)(6h^4-182h^3+2042h^2-9986h+18024)
           / [(h-5)(h-6)(h-7)(h-8)(h-9)].                  (10)
```

The quartic is strictly positive for h>=9: with t=h-9 it is
`6t^4+34t^3+44t^2+40t+240`. For h=11, direct rational evaluation of
(9) gives -54/5, so the same nonvanishing holds. The exact checker tests
(10) for odd h=11,...,39, but the recurrence calculation is the all-size
argument.

W is independent of all previous rows. L first removes the diagonal high
row; the independent high-shift R and triangular hook rows are then forced
to zero because W is low-supported. The remaining constructed low space
is annihilated by M_q, but W is not. Therefore W adds one full-space rank
direction for odd h>=11. Its input and outputs need not lie in the binary
codebook.

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
`3h-3+2 max(0,floor(h/2)-2)+2[h>=6]+[h>=9]` for h>=4; the later
high-shift and odd-moment sections add their stated directions.
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
