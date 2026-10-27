# A precise remaining interval-filter target

The current actual family uses weight w_s=s and normalizes a full-rank
asymmetric first-moment minor. This removes only s=0. To improve the
supplied rank envelope, a successor needs a fixed epsilon>0 and a valid
identity with weights vanishing throughout `|s|<epsilon h`, not merely
at one point. It must keep at least `exp(kappa sqrt(h)-O(log h))` labels
on BOTH input and output axes, polynomially many pieces and uniform
`2^O(lambda)` exact rational generation.

One concrete sufficient target is a scalar filtered pairing

    sum_s w_s Q_s(a_mu,b_nu)|_W = G(mu,nu) Id_W,

where w_s=0 in the central interval, G has that leading label rank, and
the output codebook W has the same leading dimension. Row/column label
sets may differ. A local-axis inverse of a nondegenerate minor can then
use the construction in PROOF.md without increasing either rank.
The scalar-output property and the dimension of W must be PROVED.
General higher moments are operator-valued, and a generic inverse across
two axes need not preserve the other cut.

If all these conditions held, the largest remaining directional term
sum would have the conditional ratio

```math
 \rho(\epsilon)=\frac{\sqrt{2+\epsilon}+\sqrt{2-\epsilon}}4
       <\frac1{\sqrt2}.
```

For epsilon=1 this would mean rho=(sqrt(3)+1)/4 and a conditional
alpha=`log2(4/(sqrt(3)+1))`, about 0.55, with the same full cost transfer.
This is a target, NOT an achieved bound. A loss of leading codebook capacity
can cancel the gain and must be charged before interpreting the ratio.

The existing uncharged moment-recovery branch classifies a different
scalar-weight/codebook interface at small sizes. Reusing it unchanged
would not be a new experiment. A new screen could classify scalar weights
on the present charged asymmetric codebooks, allowing a nonprincipal
label pairing. Test the exact scalar-output constraints and full pairing
rank before looking at the smaller shift costs.

A second, genuinely changed premise is a controlled combination of charge
values or output codebooks that scalarizes a higher filter without losing
leading capacity. There is an elementary necessary bound for extracting
the coefficient of q^d from a combination of the RAW charged pieces with
weights independent of q. Each monomial of a_mu has length(mu) currents,
and b_nu has length(nu). Each zero current contributes one q. Hence the
coefficient vanishes whenever length(mu)+length(nu)<d. Its label matrix is
covered by rows or columns of length at least t=ceil(d/2), so its rank is
at most twice the number of such partitions. By conjugating partitions
and removing a largest part, that number is at most
`sum_(r=t)^h p(h-r) <= h p(h-t)`. Any scalar output pairing extracted this
way consequently has label rank at most `2h p(h-ceil(d/2))`.

This all-size support argument permits arbitrary fixed output projections,
but it is not a theorem about charge-dependent weights or normalizations.
It does not prove a complete filter/rate obstruction. Charge any leading
capacity loss before a large-charge search; a scalarizing construction
with genuinely different charge dependence remains open. The current
checker verifies first-moment pieces rather than this combinatorial lemma.

Do not replace these obligations by a finite successful inverse, a low
third-cut rank, or a conjectured generic full rank. Preserve every valid
negative result and source credit. The user goal stays active after this
component is archived.
