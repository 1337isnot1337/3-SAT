# A universal-oracle floor and the thin-grid relaxation

## Exact clique-oracle lower bound

Fix `K>=2` and `lambda>=1`. A clique instance has one independent
`lambda`-bit variable per unordered edge, and an arbitrary table `W_i` on
the `K-1` incident edge strings at vertex `i`. Its value is

    Z = sum_{edge assignments} product_{i=1}^K W_i(incident strings).

For deterministic algorithms that receive the tables only through point
queries and must return exact `Z` on every input, **some input requires at
least `2^((K-1)lambda)` queries**, even for tables with values in `{0,1}`.

Proof. Set all tables except `W_1` identically to one, and answer zero to
every query of `W_1`. If the algorithm halts without querying some incident
string `z`, compare this zero table with the table that is one only at `z`.
Their transcripts are identical, while their values of Z are respectively
zero and `2^(binom(K-1,2)lambda)`. They cannot both be answered correctly.
Thus on the all-zero `W_1` input, every one of its `2^((K-1)lambda)`
entries must be queried. This holds for adaptive algorithms and permits
arbitrary computation and queries to the other tables.

For the source's achievable-pair convention, an upper bound of the form
`C 2^(e K² lambda) (B+lambda)^C` for fixed `K` and all `lambda`, including
`B=1`, therefore requires

    e >= (K-1)/K².                                      (1)

With exact ordered edge-bit normalization `K(K-1)lambda`, the corresponding
coefficient is at least `1/K`. The polynomial and fixed constants cannot
cover a strict exponential gap as `lambda` grows. This is an information
bound for the *unrestricted table-oracle interface*. It does not exclude
faster algorithms when the tables have additional promised structure, nor
is it a lower bound for SAT. It also does not assert the same bound for a
bounded-error randomized algorithm without a separate argument.

## Consequence for an ideal thin rectangular split

Use the explicit rectangular relaxation of PR 61. For `p,q>=2`, let

    a=(p-1)/(pq-1), c=(q-1)/(pq-1), b=(p-1)(q-1)/(pq-1),
    F = max_{x,y>=0, x²+y²<=1} min(u(a+bx), v(c+by)),

where `u,v>0` are the costs of the row and column continuation respectively.
Put `d=c+b=1-a` and `z=(v/u)d/b`. If `z<=1`, then

    d (1-z²) <= F/v <= d.                               (2)

For the upper bound use `y<=1`. For the lower bound take
`x=z`, `y=sqrt(1-z²)`: the row cost is at least `v d`, while the column cost
is `v(c+b y) >= v d y >= v d(1-z²)`. This is a bound on the *continuous
worst-case cost certificate F*, not on true tensor ranks or an algorithm's
runtime.

For any fixed `P>=2`, if `2<=p<=P`, `q -> infinity`, `v -> 0` and
`u>=1/P`, then `F/v -> 1`. Indeed `a<=1/q`, `b>=1/3` for `p,q>=2`,
and `z<=3Pv`; from (2), for `3Pv<=1`,

    1 - 1/q - 9P²v² <= F/v <= 1.                     (3)

The oracle floor motivates `u>=1/P` when the row continuation must satisfy
the unrestricted source contract on at most P nodes and uses the exact
ordered-edge normalization. Formula (3) proves that its ideal thin-grid
relaxation has **no fixed-factor decrease** relative to the large-child
coefficient as that coefficient tends to zero. This corrects the temptation
to reuse the equal-child `p=2` example when one child remains bounded.

This conclusion assumes the model's uniform coefficients, the continuous
quarter-disk worst case, and the stated placement of the two continuation
costs. It does not prove that a rectangular recursive construction is
feasible, that actual pieces attain the disk, or that total runtime equals
F. Grouping and changed child sizes, local evaluation, finite overhead,
branching, precision, recovery, reduction and space still need full
accounting. A changed table interface or better realized rank curve may evade
this *certificate* barrier. The accepted OpenAI result remains unchanged.
