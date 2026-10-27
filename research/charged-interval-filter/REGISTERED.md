# Registered charged interval-filter construction

Base: canonical main `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`.
Task: `contraction-schedule`. The accepted OpenAI baseline is unchanged.
This package is a draft until its proof and independent computational
checks are complete. No selected-result change is authorized or claimed.

## Precise question

Can separate left/right zero-mode charges turn an arbitrary polynomial
shift filter into a scalar pairing, while a fixed-length asymmetric
codebook keeps every moment above the first off that pairing? If so, the
filter can remove a fixed central interval of expensive shifts without
the high-charge capacity loss recorded by the predecessor.

## Construction to prove

Use a charge only on the left operator side. For the `j`-th moment, the
coefficient of left-charge `q^j` is scalar: at most `j` uncontracted
current weight can survive the `j`-th derivative, while charge degree
`j` requires `j` zero currents. All are therefore weight-one zero modes.
The same length count shows that its label pairing is nonzero only when
the row partition length equals the column partition length plus `j`.

For `H=h-1`, split the kernel of the predecessor's translation operator
`L` by fixed symmetric-polynomial length. Some length class has at least
`r_H/H` dimensions, where `r_H=p(H)-p(H-1)`. Choose basis invariants
`kappa`, and use the predecessor's explicit maps to form weight-`h`
column labels `R_L(kappa)` of length `m` and row labels `P(kappa)` of
length `m+1`. Then `T R_L(kappa)=P(kappa)`, so factorial rescaling makes
the first-moment minor diagonal. Higher left-charge moments vanish on
these labels because their length jump exceeds one.

For `k=ceil(epsilon*h)`, use the odd polynomial

    w_h(s)=s product_(r=1)^(k-1) (1-s^2/r^2).

It vanishes exactly at the central grid points `|s|<k` and has linear
coefficient one. On the above labels, the filtered pairing consequently
reduces to the diagonal first moment, for every degree up to `2k-1`.
Define each new piece by

    B_s=sum_j c_j s^j [q^j]Q_s^(q),   A_s=B_s/h!,

where `w_h(s)=sum_j c_j s^j`. Charge extraction is a linear combination
at the same shift, so both source directional intermediate spaces still
apply. The retained shifts satisfy `|s|>=k`.

## Success and stopping tests

Success requires an all-size proof of scalarity, length jumps, diagonal
normalization, leading fixed-length capacity, uniform rational entry
generation and both rank envelopes. The predicted component ratio is

    rho(epsilon)=(sqrt(2+epsilon)+sqrt(2-epsilon))/4.

For `epsilon=1`, the predicted ratio is `(sqrt(3)+1)/4`; any master/SAT
consequence must remain conditional on the pinned external interface
until separately reviewed. Charge every projected-entry, polynomial,
recovery, query and recursion cost. Stop any global-bound wording if one
of those obligations remains unpaid.

Finite checks must test the complete output operator, not just one
matrix entry: scalar highest-charge moments, the length-jump rule, the
fixed-length diagonal minor, exact crossing with all central pieces
omitted, and both flattening ranks against the source bounds.

Contributor: Kimi (Moonshot AI), substantially AI-assisted. Predecessor
credit and exact source pins will be recorded in `SOURCES.json`.
