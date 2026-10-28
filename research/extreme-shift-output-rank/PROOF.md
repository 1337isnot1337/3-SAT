# Output-rank obstruction for extreme-shift scalar filters

This is a written, author-checked, substantially AI-assisted argument based
on the charged two-order identity in [PR #11](../charged-operator-moments/PROOF.md)
and the asymmetric crossing interface in [PR #19](../charged-asymmetric-crossing/PROOF.md).
It awaits independent or formal review. It is a statement about this operator
interface, not a SAT lower bound or a bound improvement.

## Exact finite statement

Let `V_k` be the partition space of energy k over the rational field, with
dimension `p(k)` and `p(0)=1`. Fix label grade `h`, output energy `E`, charge
`q`, and a fixed input-label pair in the charged predecessor construction.
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

The bound is per raw piece. A construction that sums several different
label-pair pieces at the *same* shift must charge each additional summand;
this result does not automatically survive arbitrary mixing of label axes.
It also does not assert that the upper bound K_s is attained.

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

In particular, the grade choice in PR #19 has `D_h=N=2^lambda` and
`p(h)<h^2 N`, so its output dimension meets this condition with C=2.
The estimate is asymptotic and does not provide a numerical threshold here.
It also applies to other output spaces with the stated dimension bound.

This excludes a *more restrictive* support choice than the open target in
[NEXT.md](../charged-asymmetric-crossing/NEXT.md): excluding only
`|s|<epsilon h` still allows many intermediate shifts. It does not rule out
that target, alternative operator families, multiple paid label mixtures,
or a different full SAT algorithm. It supplies no improved rho, alpha,
selected bound, or implementation.

## Reproduction and scope

`python3 -I -B research/extreme-shift-output-rank/verify.py` performs exact
finite checks of both operator orders and output-matrix ranks for four label
pairs at each of grades 4 and 6, including the two endpoint shifts. It also
checks bounded integer endpoint weights against the scalar-zero implication.
These checks test the implementation and finite consequences; the all-size
argument above is not established by those examples. The predecessor code
and its source/attribution pins remain unchanged. `make verify` checks
repository integrity, not this proof.
