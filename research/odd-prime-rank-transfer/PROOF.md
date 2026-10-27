# Rational crossing ranks suffice for a bounded randomized transfer

Author-checked all-size argument; no independent or formal review. No
cheaper rank family or improved SAT bound is claimed. Standard primality
and field linear algebra are credited in
SOURCES.json; the new interface is exact bounded integer-query recovery
around the existing tensor protocol. Substantial Codex assistance.

## 1. Rational rank-only contract

Fix constants c,C and 1/2<=rho<1. For each lambda>=1 assume polynomially
many rational functions A_i on four lambda-bit strings, a nonzero rational
d_lambda, and positive rank bounds r_i,c_i, with

```math
 \sum_i A_i=d_\lambda[x=v][y=u],\qquad
 \lceil\log_2r_i\rceil+\lceil\log_2c_i\rceil
       \le4\rho\lambda+c\log_2(2\lambda).
```

The bounds are for the two required rational flattening ranks. All indices,
the normalizer, rank bounds and each exact rational entry are computable
in `2^(C lambda)` BIT operations, after enlarging C for finite cases.
Fractions are returned as signed integers with nonzero integer denominators.
This implies exponentially bounded output bit lengths. It does not require
polynomial-height pieces, normalizers or exact integer factors.

The family depends only on lambda and its displayed indices and arguments.
It does not depend on arbitrary oracle table values in a recursive call.
This uniformity is used to control every bad denominator at once.

For the arbitrary-density n-variable envelope, retain the source's separate
computability hypothesis: the required constant-factor bracket of rho to
the power ell is computable in time polynomial in K_ell. It holds for the
available rho=1/sqrt(2). A noncomputable real rank envelope alone does not
establish that uniform dense reduction.

## 2. A global bad-prime bound

For one lambda take the product E_lambda of all denominators of all entries
of all pieces, the denominator of d_lambda and its NONZERO numerator.
Absolute values can be used. The product is a nonzero integer. There are
at most `(2 lambda)^c 2^(4 lambda)+2` factors and each has at most
`2^(C lambda)` bits. Thus for a fixed sufficiently large integer kappa,

```math
 \log_2|E_\lambda|\le2^{\kappa\lambda}.
```

This product is only a counting witness. The algorithm never constructs
it. If all recursive call lengths are at most S, the product over lambda
from one to S has logarithmic height at most H=`S 2^(kappa S)`. The number
of its prime divisors in `[2^T,2^(T+1))` is at most H/T, because each such
prime contributes at least T to the logarithm of the product.

Consequently one good prime covers all possible piece entries at all call
lengths, including adaptively chosen queries, rather than requiring a
union bound over the algorithm's exponentially many entry evaluations.
S is a proved call-size cap, not an empirical observed maximum.

## 3. Bounded prime sampling

Use Rosser--Schoenfeld (1962), equations (3.5)-(3.6):
`pi(x)>x/ln(x)` for x>=17 and `pi(x)<1.25506 x/ln(x)` for x>1.
For integer T>=8 these give more than `2^T/(2T)` primes in
`[2^T,2^(T+1))`: subtract the bounds, use ln(2)<1 and the rational
inequality `16/9-125506/100000>1/2`.

Independently sample at most 64T uniform integers in that dyadic interval,
using exactly T random bits per candidate, and test them by a deterministic
polynomial-time primality algorithm (AKS, with its corrected proof).
Choose the first prime, or report FAIL if none is found. Every random
outcome takes polynomial time in T; there is no unbounded retry loop.
The chance of FAIL is less than `2^-32`: group the trials into 32 blocks
of length 2T and use `(1-1/(2T))^(2T)<1/2`.

Conditioned on finding a prime, its distribution is uniform among interval
primes, including under the trial cap: each prime has the same probability
of being the first selected prime. The conditional bad-prime probability
is at most

```math
 \frac{H/T}{2^T/(2T)}=\frac{2H}{2^T}.
```

Take T at least `kappa S+ceil(log2(S))+10`. This probability is at most
`2^-9`. The combined failure bound is below `2^-9+2^-32<1/100`.
Finite checker fixtures use exact trial division only on small candidates;
they do not implement or claim to benchmark AKS.

## 4. Recover every original signed integer query

For an integer tensor network with E Boolean wire bits and original tensor
values bounded in absolute value by `2^(B_v)` at vertex v, its integer
contraction Z has

```math
 |Z|\le2^{E+\sum_v B_v}.
```

This follows by bounding each product and the number of wire assignments.
Obtain a uniform polynomial bit bound B_query for ALL integer networks
queried by the outer reduction, including all rejected greedy candidates
and all profiles. Also take `T>=B_query+2`. Then the selected prime exceeds
twice every absolute query bound. Its field residue has a unique balanced
representative in `(-p/2,p/2)`, and that representative is exactly Z.

Recover that signed integer at the boundary of EVERY original network
query, before using its value in a greedy comparison or in an outer sum.
The dense reduction's modulo-two truncation remains an identity over the
integers and the designated powers of two. It is NOT asserted over F_p.
Large intermediate profile values, not just the final count<=2^n, determine
B_query. Negative values must use balanced recovery, not ordinary residues.

The original networks of the quantitative reduction have polynomial wire
budgets, polynomially many original vertices, and polynomial entry bit
bounds. Their E+sum B_v bounds are therefore polynomial in input length.
The outer reduction has explicit uniform network bounds, so obtaining this
cap does not require enumerating its exponentially many queries in advance.
Created inner field factors are not original outer-query tensors; their
integer magnitudes do not enter this exact boundary-recovery bound.

## 5. Field compilation and recursion

Reduce each rational entry modulo p by inverting its denominator. If a
denominator or normalizer numerator vanishes, report FAIL. For a good prime
this never happens. Reducing a valid rational matrix cannot increase its
rank: clear its denominators (units modulo p), and reduce its vanishing
minors. Enumerate its two flattenings and perform ordinary field rank
factorization. This costs `2^O(lambda) poly(T)` bit operations and space,
including exact rational entry evaluation and reduction. Both factors have
T+1-bit entries; their term counts stay within r_i and c_i.

Run the same crossing expansion, choose the same cheaper direction and
perform the same grouping and tensor recursion in F_p. Every crossing
identity is valid in the field and its normalizer is invertible. Powers
and inverses of that normalizer are computed modulo p. An exponentially
large rational numerator or two-adic denominator therefore does not create
an integer precision increment. The field has fixed characteristic across
the whole execution; no inconsistent lifts or cross-prime identities are
used.

Section 4 recovers each outer integer query exactly from the completed
field contraction. The outer deterministic reduction then proceeds over
the integers unchanged, using its own comparisons and modulo-two sums.

If a selected prime is bad but no division fails, each actually evaluated
rational entry and identity still reduces correctly, and the computed
query values remain valid. A bad prime is an upper bound on possible
failure, not permission to continue after a zero denominator. No invalid
inverse is ever used. On any FAIL the decision algorithm returns NO.

Thus an unsatisfiable formula always returns NO. On each fixed satisfiable
formula, probability at least 99/100 selects a prime good for all possible
calls and follows the exact reduction, returning YES. This is stronger
than the required 2/3 completeness. For counting, the same algorithm may
return FAIL but every returned count is exact. These guarantees concern
each fixed input, not an average distribution of formulas.

## 6. Full time and space ledger

The source's master recurrence has depth O(log log N_root), and the loose
child bound `N_child<=(c+3)N_parent` derived in PR 16 gives a polynomial S
for all internal wire budgets and lambda values. Increase c for the new
compiler's fixed constants if necessary. B_query is also polynomial in
original input length, so T and all field element bit lengths are polynomial.

For the fixed-width SAT consequence, first remove duplicate clauses,
tautologies and repeated literals, and handle an empty clause immediately.
For fixed width k there are at most `(2n+1)^k` distinct normalized clauses.
This costs polynomial time in the original input size; subsequent query
and prime-bit bounds are polynomial in n for fixed k. Thus a huge repeated
input does not enter a K-dependent polynomial prefactor. Unused variables
are handled by their known power-of-two multiplicity outside the reduction.

Dense factor construction and entry computation contribute
`2^O(lambda) poly(T)`, including the full matrix and elimination, rather
than a free rank oracle. The source's master ledger absorbs this as its
existing `2^(c lambda)` entry term and a prefactor
`(K(lambda+B+T))^(C_0 K^2)` for a larger fixed C_0. Prime sampling is a
single polynomial-time preparation. Every subsequent random outcome has
the same deterministic time cap, including early FAIL paths.

All grouping enumeration, crossing branches, outer reduction branches,
profile and candidate queries, integer boundary recovery and final
amplification are included. No amplification is needed beyond the stated
prime sampling because the failure bound is already below 1/100.
No dense formula is silently assumed sparse. At fixed rho this transfers
the same source master envelope `alpha'=log2(1/rho)` and the same general-
density correction, with the explicit randomized guarantee above.
The source's finite-size exceptions keep their direct deterministic fallback.

The compiler stores exponential-size matrices in lambda. Its space is
bounded by its running time; no polynomial-space guarantee is claimed.
There is no smaller rho here, so no improved alpha or selected result.

## 7. What this changes and what remains open

The two-adic transfer required a paid polynomial normalizer valuation.
Here uniform rational generation in `2^O(lambda)` bit time already bounds
the total bad-prime height sufficiently. A normalizing inverse with
exponential integer bit height is therefore not automatically disqualified.
It must still produce valid rational crossing pieces with the required
two rank bounds and polynomial piece count. A singular pairing is still
singular; a normalization acting nonlocally across a required cut can
destroy its rank bound. Neither issue is solved by modular arithmetic.

The test conjugation by `2I-S_N` demonstrates the larger allowed coefficient
class while preserving both ranks. It does not improve those ranks. A
new global rho bound, uniformity proof and independent review remain open.
