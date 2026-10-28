# Output-rank obstruction for extreme-shift scalar filters

This is a written, author-checked, substantially AI-assisted argument based
on the charged two-order identity in [PR #11](../charged-operator-moments/PROOF.md)
and the asymmetric crossing interface in [PR #19](../charged-asymmetric-crossing/PROOF.md).
It awaits independent or formal review. It is a statement about this operator
interface, not a SAT lower bound or a bound improvement.

## Exact finite statement

Let `V_k` be the partition space of energy k over the rational field, with
dimension `p(k)` and `p(0)=1`. Fix label grade `h`, output energy `E`, an
integer charge `q`, and a fixed pair of input labels in the charged
predecessor construction.
Each label may itself be an arbitrary linear combination of the predecessor's
labels, using their common grade-h mode convention.
For the raw piece `Q_s` with `|s|<=E+h`, put

```math
 t_s=E+h-|s|,\qquad
 K_s=\sum_{k=\max(0,t_s-2h)}^{t_s}p(k).
```

Let `W` be any D-dimensional vector space with linear maps `I:W -> V_E` and
`P:V_E -> W`. For a set S of shifts and arbitrary rational weights `w_s`,

```math
 \operatorname{rank}\!\left(\sum_{s\in S}w_s P Q_s I\right)
 \le \sum_{s\in S}K_s. \tag{1}
```

In particular, if the left side is a scalar `g Id_W` and the right side is
strictly below D, then `g=0`. The same inequality holds for each input-label
pair and even if the scalar weights vary with the pair, provided each term is
a single predecessor piece. Applying it to every entry of a scalar pairing
matrix makes that entire pairing zero. The choice of W need not be a
coordinate subspace, and P need not be an orthogonal projection.

More generally, for a sum of L pieces with independently chosen shifts,
separable label pairs and charges, the same rank bound holds with one `K_s`
for each summand, including repeated shifts. Each of those labels may be an
arbitrary linear combination; L counts separable pairs, not the number of
basis labels used to write them.

## Proof

Use the definition of the charged piece as the sum over `0<=i<=2h` of
compositions of two energy-homogeneous modes. In the original order the
intermediate energy is `E+h-s-i`. For `s>=0` this runs over the integers
from `t_s-2h` to `t_s`; negative intermediate energies contribute zero.
In the reverse order the intermediate energy is `E-h+s+i`. For `s<0`
this runs over the same interval. The predecessor's two-order identity
allows the corresponding order to be used for each shift.

Each nonzero composition factors through `V_k`, so its rank is at most
`p(k)`, regardless of the input labels, coefficients or charge. Summing
ranks over i gives `rank(Q_s)<=K_s`. Pre- and postcomposition by I and P
cannot increase rank, and rank is subadditive across shifts, proving (1).
A nonzero scalar multiple of `Id_W` has rank D, giving the final claim.
No unproved generic-rank or noncancellation assumption is used.

The predecessor's `Q_s(a,b)` is bilinear in its labels. In particular,
mixing any number of row labels on one axis with the other label fixed is
exactly one piece with the mixed row label; simultaneous separate linear
mixing on both axes is also one piece. This includes the local inverse used
in PR #19, even though its coordinate expansion can have N terms. An
arbitrary joint mixture need not be separable: it must be decomposed into
separable label pairs and each pair charged once. The bound does not assert
that K_s is attained.

## Unequal output and label energies

The rank bound also gives a location condition without assuming `E=h`.
Let E tend to infinity, let the output dimension satisfy
`D_E>=p(E)/E^C`, and form a nonzero scalar entry from L raw summands of
common grade h and output energy E. Set
`t_max=max_j(E+h-|s_j|)`. If `t_max>=E`, one supported shift already has
`|s_j|<=h`. Otherwise, rank subadditivity gives

```math
 p(t_{\max})\ge\frac{p(E)}{E^C L(2h+1)}.
```

Applying the same partition estimate as below, uniformly for
`0<=t_max<E`, gives

```math
 \min_j|s_j|\le h+O_C\!\left(\sqrt E\,[\log(E+1)+\log L+\log(2h+1)]\right).
```

For example, if h and L are polynomially bounded in E, the additive term
is `O(sqrt(E) log E)`. If `log(2h+1)+log L=o(sqrt E)`, then for every
fixed epsilon>0 a nonzero scalar entry cannot use only shifts
`|s_j|>=h+epsilon E`. For larger mixtures the displayed bound may be too
weak to restrict the shift range; no stronger conclusion is implied.

## Large-capacity consequence

Now set `E=h` and suppose the output codebook dimension satisfies
`D_h >= p(h)/h^C` for some fixed C and all large h. Fix `0<epsilon<1` and
allow only shifts with `|s| >= (1+epsilon)h`. Their intermediate energies
satisfy `t_s <= floor((1-epsilon)h)`. Since there are at most `4h+1` shifts
and `p(k)` is nondecreasing,

```math
 \sum_s K_s\le(4h+1)(2h+1)p(\lfloor(1-\epsilon)h\rfloor).
```

The Hardy-Ramanujan partition estimate gives
`log p(h)=pi sqrt(2h/3)+O(log h)`; the last bound is
`o(p(h)/h^C)`. For all sufficiently large h it is strictly below D_h.
Consequently every scalar pairing formed in this raw-piece manner from
only those extreme shifts is zero, irrespective of input-label rank.
More quantitatively, every nonzero scalar pairing under this capacity
condition has at least one supported shift with
`|s| <= h+O_C(sqrt(h) log h)`. To see this, let
`t_max=max_s(2h-|s|)`. If `t_max>=h`, the bound is immediate. Otherwise,
the rank condition and the same polynomial envelope imply
`p(t_max)>=p(h)/h^{C+O(1)}`. The partition estimate then gives
`sqrt(h)-sqrt(t_max)=O_C(log h)`, and hence
`h-t_max=O_C(sqrt(h) log h)`. Since the smallest supported absolute shift
equals `2h-t_max`, the stated bound follows. This shift need not lie close
to zero.

The same conclusion allows polynomially many mixed raw pieces per scalar
entry: if `L_h<=h^A`, replace the number of shifts in the rank budget by
`L_h`. The quantitative error becomes `O_{A,C}(sqrt(h) log h)`. More
generally, the fixed-epsilon extreme-support exclusion still holds when

```math
 \limsup_{h\to\infty}\frac{\log L_h}{\sqrt h}
 < \pi\sqrt{2/3}\,(1-\sqrt{1-\epsilon}).
```

This includes `log L_h=o(sqrt(h))`. The local normalization of PR #19 is
covered as one separable pair per shift, regardless of the number of basis
labels in its expansion. An arbitrary nonseparable joint normalization may
require many separable pairs and must be charged accordingly.

Conversely, a nonzero scalar entry supported on those extreme shifts needs
at least

```math
 L_h\ge \frac{D_h}{(2h+1)p(\lfloor(1-\epsilon)h\rfloor)}
 \ge\exp\!\left(\pi\sqrt{2/3}\,(1-\sqrt{1-\epsilon})\sqrt h-O_C(\log h)\right),
```

where the exponential expression is a lower bound under the stated capacity
assumption. For PR #19's selected dimension this is
`L_h >= N^{1-sqrt(1-epsilon)-o(1)}`. This is a necessary separable-piece
count, not a runtime lower bound for every possible representation or algorithm.
For example, support restricted to `|s|>=7h/4` requires at least
`N^{1/2-o(1)}` separable label-pair summands for a nonzero scalar entry.
When charge is fixed and a shift-s term is written in fixed label bases
with coefficient matrix `C_s`, rational matrix-rank factorization writes it
as `rank(C_s)` separable pairs. Every such representation of a nonzero
scalar entry therefore satisfies the sharper finite inequality

```math
 D_h\le\sum_s \operatorname{rank}(C_s)K_s.
```

In particular, the preceding lower bound applies to `sum_s rank(C_s)`.
This is a statement about coefficient representations; it does not imply
that expanding or evaluating every summand separately is unavoidable.

For the predecessor's unchanged directional term-count envelope, this also
limits what a support-only calculation can certify, provided the proposed
construction has separately justified using that envelope after its label
mixing. Its normalized envelope at `u=|s|/h` is

```math
 \rho(u)=\frac{\sqrt{2+u}+\sqrt{2-u}}4,\qquad 0\le u\le2.
```

This function decreases with u. With polynomially many raw summands, the
necessary shift above gives `u<=1+o(1)`, so the maximum of these *upper-bound
expressions* over retained shifts is at least
`(sqrt(3)+1)/4-o(1)`. Thus this particular term-count envelope cannot, from
support exclusion alone, certify a smaller leading rho. This is not a lower
bound on actual tensor ranks: improved rank estimates, exponentially many
mixed summands, or a different decomposition are not excluded.

In particular, the grade choice in PR #19 has `D_h=N=2^lambda` and
`p(h)<h^2 N`, so its output dimension meets this condition with C=2.
Its locally normalized piece has, for each fixed x and v, the form
`s Q_s(a'_x,b_v)` for the mixed label
`a'_x=sum_a (M^-1)_(x,a) a_a`. Hence a crossing identity supported only on
the stated extreme shifts is impossible even after that normalization:
taking x=v would give the forbidden nonzero scalar output identity.
The estimate is asymptotic and does not provide a numerical threshold here.
It also applies to other output spaces with the stated dimension bound.

This excludes a *more restrictive* support choice than the open target in
[NEXT.md](../charged-asymmetric-crossing/NEXT.md): excluding only
`|s|<epsilon h` still allows many intermediate shifts. It does not rule out
that target, alternative operator families, sufficiently large nonseparable
label mixtures, or a different full SAT algorithm. It supplies no improved
rho, alpha, selected bound, or implementation.

Indeed, for `E=h`, an embedded output space has `D<=p(h)`. If even one
retained shift satisfies `|s|<=h`, its intermediate range contains h, so
`K_s>=p(h)>=D`; the criterion `sum K_s<D` is then already false. Thus the
rank-budget method by itself cannot exclude any support containing such a
shift. Sharper restricted-operator ranks or additional structural equations
would be needed to address that part of the central-gap target.

This limitation is exact for a relaxed model that retains only the channel
dimensions and allows their maps to be chosen independently. Let one
intermediate space `U_(s,i)` of dimension `p(k)` be given for every
nonnegative intermediate energy k, and put `B=sum_s K_s`. If `B>=D`, embed a
D-dimensional W into the direct sum of the U spaces and choose a left
inverse. Writing the identity as the sum of its coordinate-channel
compositions gives an abstract scalar crossing supported on S. If `B<D`,
the rank proof above excludes it. Thus `B<D` is the exact threshold in
this relaxed factor-through-spaces model. The real charged operators have
coupled, explicitly specified mode maps; the relaxed construction is not a
charged crossing and says nothing about its realizability or SAT costs.

Finite checkers also give a direct control: at grades 4, 6, 9 and 12, the
last selected row/column label pair has full output rank D on the
predecessor codebook for every integer shift `|s|<=h`. This is stronger than
observing that the upper budget is large in those finite cases, but it does
not say the piece is scalar or prove an all-size claim.

A naive route to proving this control uniformly also fails: in the
predecessor's output ordering, the `s=-h` matrix for that pair is lower
triangular at grades 4, 6 and 9, but not at grade 12. At grade 12 its entry
at output index 2 and input index 7 is `-34488115200`, and the reverse entry
is `-6157022699520`. Because both are nonzero, no common permutation of the
input and output basis can make this matrix triangular. A uniform argument
would need a non-permutation basis change or a different structural invariant.

The same sampled full-rank pattern also depends on charge. At `s=-h`, the
last selected label pair has rank 0, 0 and 3 at grades 4, 6 and 9 when
`q=0`, whereas the respective output dimensions are 2, 4 and 8. At those
three grades, charges 1 and 2 have full rank at shifts `-h,0,h`. These are
finite controls, not a classification of charge values or larger grades.

## Output-rate and mixing tradeoff

The same rank argument quantifies a loss in the output-codebook exponent.
Write `kappa=pi sqrt(2/3)` and suppose, for fixed `0<theta<=1` and
`0<=eta<kappa theta`, that

```math
 \log D_h\ge\kappa\theta\sqrt h-o(\sqrt h),\qquad
 \log L_h\le\eta\sqrt h+o(\sqrt h).
```

Here L counts separable label-pair pieces in one scalar entry. A nonzero
scalar entry then requires

```math
 \min_j |s_j|/h\le
 2-(\theta-\eta/\kappa)^2+o(1).                           \tag{2}
```

Indeed, `D_h<=L_h(2h+1)p(t_max)` and the partition estimate imply
`sqrt(t_max/h)>=theta-eta/kappa-o(1)`. Equation (2) follows from
`min |s_j|=2h-t_max`. Thus a fixed-fraction cutoff beyond the right-hand
side forces a zero scalar entry under the stated capacity and mixing rates.
For theta=1 and subexponential mixing this recovers `|s|/h<=1+o(1)`.

As an accounting illustration, assume additionally that `D_h=N_h` satisfies
`log N_h=kappa theta sqrt(h)+o(sqrt(h))`, mixing is subexponential, and the
predecessor's *unchanged* term-count envelope is valid for the resulting
pieces. The maximum normalized upper-bound expression over retained shifts is
at least

```math
 \frac{\sqrt{4-\theta^2}+\theta}{4\theta}-o(1)
 \ge \frac{\sqrt3+1}{4}-o(1).
```

The first inequality uses (2), the decreasing function `rho` above, and
the changed relation between log N and sqrt(h); the second follows from
`sqrt(4-theta^2)/theta>=sqrt(3)` for `0<theta<=1`. This is a limit on
that particular support-only *upper-envelope
calculation*. It is not a lower bound on actual ranks or on any SAT running
time, and another rank bound may improve on the envelope.

The same threshold survives the elementary cap `N_h^2` on each flattening
rank. The resulting normalized upper-bound expression is

```math
 \rho_{\rm cap}(\theta,u)=\frac{1}{4}\left[
 \min\!\left(2,\frac{\sqrt{2+u}}{\theta}\right)+
 \min\!\left(2,\frac{\sqrt{2-u}}{\theta}\right)\right].
```

For fixed theta it is nonincreasing in u: before clipping the sum decreases;
if the larger first term clips, the remaining second term decreases; and if
the second term clips, both are clipped. At `u=2-theta^2`, it equals
`[min(2,sqrt(4-theta^2)/theta)+1]/4`, which is at least
`(sqrt(3)+1)/4` for `0<theta<=1`. Equation (2) therefore gives the same
support-only threshold even after this dimension cap. This remains a
statement about the evaluated upper-bound expression, not a lower bound on
actual tensor ranks.

## Reproduction and scope

`python3 -I -B research/extreme-shift-output-rank/verify.py` performs exact
finite checks of both operator orders and output-matrix ranks for four label
pairs at each of grades 4 and 6, including the two endpoint shifts. It also
checks separable mixtures of those labels against the single-piece bound and
bounded integer endpoint weights against the scalar-zero implication.
Further checks use grade 4 at output energies 0, 1, 3 and 5 with charges 1
and 2, comparing both orders and the unequal-energy rank bound. A grade-6
control also uses a non-coordinate output embedding and a non-orthogonal
left inverse.
These checks test the implementation and finite consequences; the all-size
argument above is not established by those examples. The predecessor code
and its source/attribution pins remain unchanged. `make verify` checks
repository integrity, not this proof.
