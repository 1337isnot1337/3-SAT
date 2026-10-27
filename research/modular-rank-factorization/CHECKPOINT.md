# Active research continuation

User goal ACTIVE, INCOMPLETE: work indefinitely toward a mathematical
improvement; commit/push often. Owner has authorized merges. Do not mark
complete or stop because this component is archived. No subagents used.

Working clone `/home/cinna/3-SAT`, branch
`research/modular-rank-factorization`, base
`fdb2d6d5e585b75f12e79fd0f67934eed22af173`. PR 15 is merged there and
was replayed on exact fresh main. Selected alpha is still 1/2. Frozen
upstream and selected-result files remain untouched. Refresh main, PRs,
all advertised branches and changed guidance before a pivot/submission.

The current package is a positive implementation interface: rank-only
integer crossing pieces can be factored modulo a power of two without
small exact integer factors. It pays even normalizers by a global precision
cap and charges the exponential generic compiler. It sacrifices the
baseline's polynomial-space guarantee. All bounded checks pass, including
an actual crossing/count replay. No smaller rho or alpha is proved.

The next materially different mechanism is a rational, odd-prime transfer.
An inverse of an H-by-H integer matrix with polynomial-bit entries has
determinant/numerator bit lengths polynomial in H, hence `2^O(lambda)`
when H=`2^O(lambda)`. Such denominators may have enormous two-adic
valuation but only `2^O(lambda)` total bad-prime height. A prime with
polynomially many input-size bits may avoid all of them with high probability.
Rational ranks then give generic field factorizations in `2^O(lambda)`
time and polynomial field-bit overhead.

Critical boundary: the dense outer reduction discards terms ONLY modulo
two powers. It cannot simply be run in odd characteristic. Instead bound
the absolute integer value of every original network query (wire bits plus
sum of original tensor-entry bit bounds), choose the odd prime above twice
that bound, recover each signed integer query value from its field residue,
then execute the existing outer greedy comparisons and modulo-two sums.
These root query bounds are polynomial in input bit length, even when their
values are exponentially large. Canonical factors created by the inner
compiler need only satisfy identities in the prime field.

Before any claim, prove a uniform bound on bad denominator primes across
all lambda<=a polynomial call-size cap, cap primality trials and failures,
abort on noninvertible denominators, and state success probability on each
fixed formula and time on EVERY random outcome. Generic rank bounds must
remain valid after good-prime reduction. The crossing family must depend
uniformly on lambda and piece indices, not on exponentially many arbitrary
oracle values. This does not fix singular pairings or prove a filter/rank
gain. Exact output bounds and space remain paid obligations.

The briefly considered rectangular-schedule route has a useful cost identity:
the source factor envelope is a quarter circle in normalized row/column
costs, so combining child exponents e1,e2 has ideal minimax exponent
`(e1^-2+e2^-2)^-1/2`. Logarithmic node capacities add. Rectangular aspect
ratios alone therefore retain a square-root energy law in that model.
This observation is not an algorithm lower bound and was not submitted as
a theorem; no unchanged parameter screen was launched.
