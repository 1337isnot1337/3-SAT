# Rectangular grid crossing ledger

## Exact graph identity

Take a complete graph on the `pq` points of `[p] x [q]`, `p,q>=2`.
Each original edge carries `lambda>=1` equality bits. For each choice of
2 rows and 2 columns, expand its two diagonal equalities as one crossing
piece; choose one piece per rectangle. Each diagonal edge belongs to exactly
one rectangle. Call the remaining same-row or same-column edges straight.

Merge whole rows, respectively whole columns, keeping straight equalities
between the resulting nodes and using the appropriate factorization of each
crossing piece. Denote its available factorization bit costs by
`r_Q,c_Q` for each rectangle `Q`, and put `R=binom(p,2)binom(q,2)`.
These are factorization *upper bounds*, not necessarily minimum ranks. The
resulting ordered-pair sums of the supplied edge-cost bounds are exactly

    U_row = p(p-1)q lambda + 2 sum_Q r_Q,
    U_col = q(q-1)p lambda + 2 sum_Q c_Q.             (1)

Indeed there are `p(p-1)q` ordered straight edges crossing row groups;
each rectangle contributes its row factorization to one unordered pair of
row groups, counted twice. The column expression is symmetric. Edges inside
a merged group belong to the local table and are not counted in that group's
external sum. Equation (1) is exact for these specified supplied costs even
if some factors vanish or admit a shorter representation.

Let `N=pq(pq-1)lambda` be the *exact ordered* original edge-bit total, and
let

    a=(p-1)/(pq-1),   c=(q-1)/(pq-1),
    b=(p-1)(q-1)/(pq-1).

Then `a+c+b=1`. For each rectangle write
`x_Q=r_Q/(2lambda)`, `y_Q=c_Q/(2lambda)`, and their averages `x,y`.
Dividing (1) by N gives `U_row/N=a+b x` and
`U_col/N=c+b y`. This normalization differs from the source's convenient
square-grid upper envelope `g^4 lambda`, which counts a few absent loops.

## Ideal weighted envelope, with offsets

Suppose hypothetically that each `(x_Q,y_Q)` is in the unit quarter disk.
The average is in that disk. Let `u,v>0` be continuation exponents for row
and column networks, with no other costs, and let the algorithm choose one
whole direction for this term. Its normalized coefficient is bounded by

    F = max_{x,y>=0, x²+y²<=1} min(u(a+b x), v(c+b y)).  (2)

Set `A=u a`, `B=v c`, `P=u b`, `Q=v b`. These are positive except that
A,B can be zero in limiting cases. The exact value of (2) is the unique
largest `t` satisfying

    ((t-A)_+ / P)^2 + ((t-B)_+ / Q)^2 <= 1.          (3)

Proof: for a value `t` to be achieved, both coordinates must be at least
`(t-A)_+/P` and `(t-B)_+/Q`; such a point exists in the disk exactly when
(3) holds. The left side is continuous and strictly increasing after
`min(A,B)`, starts at zero and diverges. A maximizing point is obtained by
taking those lower bounds at the largest feasible t. Thus (3) handles both
interior equalization and endpoint cases without solving a quadratic.

When `u=v=e` and `p=q=g`, symmetry and (3) yield

    F = e [1/(g+1) + (g-1)/(sqrt(2)(g+1))].          (4)

For fixed `p=2`, equal coefficients and `q -> infinity`, (3) instead gives
`F -> e/2`: here `a->0`, `c->1/2`, `b->1/2` and the optimum is `(x,y)=(1,0)`.
This is a difference in an ideal *local certificate*. It is not an improved
recursion: the row network has only two nodes, so its continuation exponent
cannot simply be assumed equal to that of an arbitrarily large column
network. The actual row and column algorithms, their input sizes and all
costs must be constructed together. The source square-grid proof has no
such unequal-child result.

## Relation to the source and full costs

Anthropic's pinned Appendix B has upper bounds
`r_s <= C sqrt(2h+s)+O(log lambda)` and
`c_s <= C sqrt(2h-s)+O(log lambda)`, with
`C sqrt(h)=lambda+O(log lambda)`. After division by `2lambda`, the ideal
quarter disk describes their leading upper envelope; the finite error must be
paid separately. It is not a lower bound on actual factorization sizes, and
actual finite shift values can occupy a strict subset. Replacing them by a
continuous disk is a relaxation. Although each rectangle may have a
different shift, (2) chooses a direction only once for the entire term.

No claim here supplies a grouping lemma for both rectangular child sizes,
controls the size of local tables, or bounds branching, entry computation,
precision, recovery, denominator, memory, outer reduction or total runtime.
The original selected alpha 1/2 remains unchanged. One next question is
whether the source's grouping hypotheses can be made simultaneous for
unequal child sizes with appropriate node-dependent `u,v`; until then the
`p=2` example must not be iterated as a 3-SAT improvement.
