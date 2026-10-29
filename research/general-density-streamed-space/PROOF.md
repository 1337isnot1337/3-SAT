# Streaming the general-density outer reduction

This is an author-checked conditional composition using the cited Anthropic
source's `thm:onelog:a`, its proof sketch for disjoint sparsification, and the
field-query interfaces in PRs #60 and #94. Substantial Codex assistance; no
independent or formal review. It neither proves the source theorem afresh nor
selects a new SAT result.

## Statement and prerequisites

Fix k. Assume all source master crossing-rank, recurrence and uniform-time
hypotheses, including a polynomial-time bracket for its `e_l` values; assume
the root/factor polynomial-workspace and field-clique contracts in PR #94;
and assume a uniformly computable polynomial-workspace/time good-prime
inventory, covering every recursive denominator and normalizer, as in PR #60
or a separately proved equivalent. Set `alpha=log2(1/rho)>0`.

Under those assumptions, the source arbitrary-density counting route admits
a deterministic depth-first implementation using polynomial(n+m) workspace
and the source time envelope

```math
 poly(n+m) + 2^{O_k(n log log(3+n)/(log(2+n))^alpha)}.
```

Here n includes the declared variables, and exact binary output has at most
n+1 bits. The source disjoint-sparsification construction and its leaf/time
bounds are prerequisites, not reproved by the bounded experiments. A better
rho would still require an actual valid family satisfying every hypothesis.
No such family or improvement is supplied here; the accepted OpenAI baseline
already has the alpha=1/2 general-density envelope in polynomial space.

## Polynomial-depth sparsification stack

After discarding tautologies and duplicate literals, represent clauses as
sets of at most k signed literals, and remove every clause properly
containing another. Let U be all non-tautological signed clauses of width at
most k over the n variables, including the empty clause. For fixed k,
`|U| <= sum_(j=0)^k 2^j binom(n,j) = n^O(k)`.

Define the upward syntactic-subsumption closure of a formula as the clauses
in U containing one of its clauses. Deleting subsumed clauses leaves this
closure unchanged. The source's branch chooses a nonempty H and nonempty F of
current clauses E properly containing H. In the first child it adds H. In the
second it adds each `E\\H`, E in F. Neither H nor any `E\\H` is already in
the current closure: otherwise a current clause would be a proper subset of E,
contradicting the preceding subsumption reduction. Both children therefore
strictly enlarge the closure. Along any path this can happen at most |U|
times. If the source terminates early on an empty clause, this only shortens
its stack.

Enumerate the binary branch tree depth first. Store one polynomial-size
formula, branch flag and the carried set of unit clauses per level. The
unit-clause set does not affect branch choice, as in the source, and has at
most 2n distinct members. The stack is polynomial in n for fixed k; one leaf
is processed and discarded at a time. The source's disjointness, leaf count,
occurrence bound and time estimate are invoked unchanged. This argument
requires the stated normalized branching rule; it is not a generic claim that
an arbitrary exponentially large binary tree has polynomial depth.

## One leaf: queries, profiles and greedy state

After normalization there are at most `n^O(k)` clauses. Source parameters
`beta`, the number of checks r, degree/mark bounds, g, P, B, profile
coordinates and candidate descriptions have polynomial(n+m) bit lengths
for fixed k; the source explicitly bounds `r<=10n`, `M<=14n` and the
low-occurrence leaf's gP and B in its large-n range. The finitely small cases
use direct enumeration. The candidate family is polynomial-sized; the
selected check list and incidence counts are polynomial-size, and candidates
are visited one at a time. The rational objective Upsilon can be kept as
exact integer numerator/denominator pairs: its powers have polynomial
exponents and polynomial-bit bases, so comparisons use polynomial workspace.

Enumerate admissible profiles lexicographically with polynomial-bit counters,
not as a stored list. For each original signed integer network, there are at
most `2^(gP)` assignments and each product of g original tensor entries has
absolute value at most `2^(gB)`. Thus

```math
 |Z_profile| <= 2^(g(P+B)).
```

Choose one computable polynomial bit bound covering every candidate, profile
and leaf, and select primes whose product is larger than twice that bound on
magnitude. All profile root entries and local equality factors are evaluated
in polynomial workspace using the source's marking and subset-ranking rules.
For each prime, evaluate the complete profile network using grouping and the
streamed field-clique executor. CRT-recover its **signed integer** value
before adding it to a profile sum or reducing that sum modulo `2^beta` or
`2^(n+1)`. Field accumulators and integer CRT state are polynomial bits; the
profile sum is reduced incrementally at the precision specified by the
source. Intermediate values are not bounded merely by the final SAT count.

After X and F are reconstructed in the source's order, choose the next check
and continue; retain only the chosen candidate and its objective. The source
proof establishes that X=0 makes F the exact leaf count. Process each leaf,
accumulate its count into an n+1-bit total and discard its state.

## Time, scope and controls

The source's `thm:onelog:a` charges candidate and profile queries, grouping,
sparsification and all leaf counts. The prime inventory and the polynomial
number of fields and CRT operations add polynomial factors; source factor
and root-query times are charged at each invocation. The nonmemoizing
execution uses the same on-demand entry counts, so it does not introduce an
unpriced exponential recomputation. The resulting fixed-k time is the
stated source envelope. Small n and empty formulas use direct fallbacks;
unused declared variables are retained or multiplied back as appropriate.

The finite checker tests both source branch forms on small normalized clause
antichains and independently checks the X=0/F identity and signed CRT on
small formulas. It does not implement full profile tensor construction, the
actual Calabro branch-selection rule, or the master recursion, and does not
prove the external time and disjointness theorems. The all-size composition,
prime certificate and inherited source prerequisites require independent
review.
