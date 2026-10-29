# Separate entropy budgets for wide and narrow parity checks

Author-checked, substantially Codex-assisted; independent review pending.
The OpenAI contraction theorem is accepted. The changed Tanner parameters
and characteristic-two interface are repository predecessor arguments,
not independently reviewed theorems selected by the maintainer. This file
states their dependencies explicitly and gives the new composition.

## 1. Claimed density-sensitive decision bound

Fix clause width k and a constant c>=1. Normalize a CNF on n declared
variables by removing duplicate literals, tautologies and duplicate clauses;
an empty clause is immediately unsatisfiable, and no clauses is satisfiable.
Let m be the remaining clause count and B=max(1,ceil(m/n)) for n>=1.
Handle n=0 directly. Put

    lambda=ceil(log2(n+2)), L=ceil(log2(lambda+2)), f=L.

For m<=n lambda^c, the proposed randomized algorithm has worst-outcome time

    poly_k,c(n+m) 2^{O_k,c(n [log2(B+2)+log2(L+2)]/sqrt(log2(n+2)))}.  (1)

It uses polynomial space and succeeds with probability at least 5/6 on
satisfiable inputs and at least 31/32 on unsatisfiable inputs. This is a
bounded-error decision claim, not exact counting or a one-sided algorithm.
For example, if B=(log log n)^O(1), the exponent is
O(n log log log n/sqrt(log n)), strictly below the accepted general-density
log-log envelope. This includes unbounded density families, though the
accepted fixed-density route remains stronger when B is constant.

For a uniform all-input algorithm, use (1) only when its displayed density
condition holds and retain the accepted general algorithm otherwise. The
accepted clause-network algorithm can also be run by step interleaving;
it gives exponent O((n+m)/sqrt(log(n+m))) on every input. The first finished
algorithm supplies the answer. An incorrect answer still requires that the
randomized algorithm err, so interleaving does not worsen its error bound.
The polynomial-space property is preserved. Thus this construction retains
all accepted guarantees and improves a specified growing-density regime.
It does NOT improve the unrestricted worst-case bound or alpha=1/2.

## 2. Fewer wide initial checks

Use the explicit retuned Tanner construction in
`research/polynomial-sparse-checks/RETUNED.md` with parameters

    n0=ceil(n/f), B0=B f, m<=B0 n0,
    mu=floor(log2 m)+1,
    R=64+8 ceil(log2(B0 mu+2)),
    P=20000 B0^2 R^2, D=320000 B0^2 R^2 mu=16 P mu.

That construction gives a binary matrix A0 with at most 3n0 rows, row
weight at most D, and every nonzero kernel vector of weight at least m/P.
It is deterministic polynomial time and space in numeric n0,m,B0. No
variable of the CNF is removed by replacing n with n0: n0 is only the
check-count budget supplied to the coding lemma. There are still n
assignment variables. The condition m<=B0 n0 is exactly what permits this
changed invocation. The even stronger nonzero-row bound in the predecessor
is unnecessary here.

At B<=O(lambda^c), f=Theta(log log(n+2)), mu=O_c(log(n+2)), and
R=O_c(L). For large n, n0<=2n/f. Consequently

    log(P+2)=O_c(log(B+2)+log(L+2)),
    log(D+2)=O_c(L+log(B+2)+log(L+2)).                       (2)

All parameters are polylogarithmic in n, with fixed powers depending on c.
The predecessor's exact constants and small-parameter cases are retained.
Its finite q=1 replays and author-checked q>1 argument remain dependencies;
this package does not claim to have independently reviewed that construction.

## 3. Narrow appended checks and fixed-input error

For an assignment x, let v(x) be its Boolean clause-violation vector.
Every true solution has v(x)=0 and survives all checks. Any false assignment
surviving A0 has at least m/P violated coordinates. Pad the coordinate
universe to m'=2^ceil(log2 m)<2m (with equality m'=m when m is a power of
two), adding zero coordinates. A random appended row draws 2P independent
uniform indices in that universe and 2P independent coefficient bits.
Repeated indices combine modulo two. A fixed surviving nonzero vector is
hit with probability

    1-(1-wt(v)/m')^(2P) >= 1-(1-1/(2P))^(2P) > 1/2.

Conditioned on a hit, a coefficient bit makes its parity uniform; rejection
probability is at least 1/4. If the support lower bound is nonintegral it
still gives this inequality; if no nonzero kernel vector exists the claim
is vacuous. Draw t=8(n+1) independent rows. A union bound over all 2^n
assignments bounds the probability of any false survivor by

    2^n(3/4)^t < 2^(-2n-3) <= 1/32,  n>=1.                (3)

Every loop has fixed length. Each draw consumes ceil(log2 m) index bits
and one coefficient bit. Zero index bits for m=1 are permitted. Generation
cost and all sampled coefficients, including those that cancel, are paid.
This is the predecessor's randomized wrapper used without sparsification
and with a smaller initial-check budget.

Each width-k violation polynomial has at most 2^k squarefree monomials
of degree at most k. A parity row therefore gives an F2 polynomial P_i
with at most 2^k times its row weight monomials, after normalization.
The two equation families have budgets

    a0<=3n0, T0=2^k D;       a1=t, T1=2^(k+1) P.           (4)

Capping row weight by m is valid but unnecessary to the bound.

Choose independently uniform weights r_v in F_(2^e), where 2^e>=6n is
the least such power of two. Evaluate exactly

    Z(r)=sum_x product_v r_v^(x_v) product_i (1+P_i(x)).    (5)

For any fixed choice of rows, (5) is the multilinear fingerprint of the
surviving assignment set. Distinct assignments give distinct monomials,
so any nonempty set gives a nonzero polynomial of degree at most n.
The elementary polynomial-root bound gives probability at most 1/6 that
(5) vanishes. A satisfiable input always has a nonempty survivor set, even
on bad hash outcomes, so its false-negative probability is at most 1/6.
An unsatisfiable input can give nonzero (5) only on the event in (3).
Return YES iff Z is nonzero. These are per-fixed-input guarantees and need
no expected-time or average-input assumption. Field construction, weights,
and arithmetic are polynomial-time as in the credited characteristic-two
interface.

## 4. Heterogeneous incidence encoding

Here is the additional evaluator needed for (4). There are two families of
a_j=O(n) degree-at-most-k equations with at most T_j=polylog(n) monomials
per equation. Then (5) can be evaluated deterministically in polynomial
space with exponent

    O((n+a0 log(T0+2)+a1 log(T1+2))/sqrt(log(n+2))).        (6)

Unlike an invocation using max(T0,T1) for every equation, this charges each
family separately. This is a structural encoding change, not an asserted
improvement of a hypothetical numeric cost model.

Normalize monomials. For every test-variable incidence use a separate
symbol z_iv and the factor C_i=1+P_i in those symbols. The product for
family j is multilinear in its incidences, has total degree at most
K_j=k a_j, and uses at most N_j<=k a_j T_j incidence symbols. Families
are disjoint on the test side but share the original variable side.

Put J=ceil(n^(1/4)). Let N=N0+N1 and fix in all ways every variable
occurring in more than

    Dstar=max(1,ceil(N/n)) ceil(n^(1/20))

tests. There are at most n/ceil(n^(1/20)) such variables. Substitution
preserves the family budgets. Multiply each branch by its fixed-variable
weight. Keep all free declared variables, including those that disappear
from every test; they contribute 1+r_v to the branch fingerprint.
Zero equations may be dropped, and a constant-one equation kills a branch.

For each family partition its tests into J groups by greedy incidence
load. Partition the free variables into J groups by their total incidence
load. Greedy least-loaded placement gives a test-group load at most
N_j/J+k T_j and a variable-group load at most N/J+Dstar. These are
n^(3/4) polylog(n). Test tensors belong to two separate layers; both layers
connect to the same variable-group tensors. The graph is already bipartite.

For each family j and group pair (g,h), enumerate the number d_jgh of
selected incidences, with sum_gh d_jgh<=K_j. There are at most
product_j (K_j+1)^(J^2) arrays, a cost exp(O(sqrt(n) log n)). Empty
families require no layer. Given an array, use
ceil(log2 binom(N_jgh,d_jgh)) wires for its subset index; nonexistent bit
codes have zero entry. Zero-wire unique subsets, including empty ones,
are decoded directly. The number of wires in family j is at most

    J^2 + log2 binom(N_j+K_j,K_j)
    <= J^2 + K_j log2(e(N_j+K_j)/K_j)
    = O_k(J^2+a_j log(T_j+2)).                             (7)

The K_j=0 case is handled directly rather than dividing by zero.

A test-group tensor multiplies the coefficients of the selected monomial
in its factors C_i. Each coefficient is a direct 0/1 lookup. In a
variable-group tensor let b_v be the number of selected incidences of v
across BOTH layers. Its entry is

    product_{v:b_v>0} r_v product_{v:b_v=0} (1+r_v).        (8)

Summing (8) with all test-group factors counts each incidence monomial
once, and sums each Boolean variable exactly, proving (5). In particular,
the layers do not introduce independent copies of the original variables.
Binomial subset decoding, coefficients and field products take polynomial
time and space; the descriptions have polynomial length.

Take s=ceil(n+a0 log2(T0+2)+a1 log2(T1+2)). Formula (7) gives O_k(s)
wires. Since log(s)=Theta(log n) and s>=n, all tensor degrees, bounded by
the incidence loads above, eventually lie below ceil(s^(9/10)). There
are at most 3J group vertices. To fit the accepted coefficient ring, lift
each canonical field entry to its degree-less-than-e representative in
F2[V], and compute modulo V^ell with ell=3J(e-1)+1 and P0=1. No product
of vertex entries reaches degree ell, so truncation loses no information.
Reduce the result modulo the field's irreducible polynomial afterward.
This uses a ring homomorphism at final reduction, not a claim that canonical
entry representatives themselves multiply homomorphically. We have
ell=O(J log n)=O(s), as required.

The source contraction theorem now gives the exponent in (6). The branch
cost O(n^(19/20)) and array cost O(sqrt(n) log n) are lower order than
n/sqrt(log n). All random choices, normalization, descriptions, entries,
field construction and final reduction are polynomial. Process branches
and arrays sequentially to retain polynomial space. For fixed k,c the
inequalities fail only for a bounded range of n: a uniform implementation
checks them and exhausts the original n-bit input in those exceptions.
No enormous small-n asymptotic claim is inferred from finite measurements.

## 5. Compose the budgets and state the remaining gap

Substitute (2) and (4) into (6). The initial layer costs

    a0 log(T0+2) = O_k,c((n/L)[L+log(B+2)+log(L+2)]),

and the appended layer costs

    a1 log(T1+2) = O_k,c(n[log(B+2)+log(L+2)]).

Their sum plus n proves (1). There is one hashed system and one weighted
evaluation, with the errors in Section 3; no hidden query or rejected greedy
candidate is present. The exact-entry, field, precision, recursive and space
costs are accounted in Section 4. The polynomial Tanner construction and
hash sampling remain lower order. No sparsification occurs in this claimed
input regime.

For unrestricted formulas, applying the source sparsifier at its usual
parameter can produce B=poly(log n), with log B=Theta(log log n) in the
available upper envelope. The new bound then returns the old log-log
factor. Optimizing the sparsification parameter in the existing cost law
does not remove that term. Thus this is a growing-density improvement
conditional on the named author-checked component arguments, not a new
selected unrestricted bound, an alpha increase, or an independently
reviewed theorem. To improve the unrestricted result, a further mechanism
must reduce the log B term or the sparsification overhead.

## Credit and dependencies

Canonical base c600b21ee7800a49c05718a254be50168e6b355b. Accepted source:
OpenAI commit 7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a, specifically
`thm:tensor-contraction`, `lem:tensor-sparse-query` and their subset encoding.
The retuned checks are the written result of PR #78's RETUNED.md, with the
independent degree-sensitive variant in `tanner-local-distance` credited
as related work. The weighted decision polynomial, field-ring embedding
and random-check rejection proof are from `characteristic-two-decision`.
The new changes are the reduced n0 budget and separately charged incidence
layers. They do not assert novelty for Tanner coding, fingerprinting,
multilinear encoding or standard entropy inequalities. Concurrent #148
studies semantic equation grouping; this construction keeps individual
factors and relies on no cancellation within a product of equations.
