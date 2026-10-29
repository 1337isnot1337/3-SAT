# Fixed-density clause networks with streamed field queries

This is an author-checked conditional composition of the source clause
network with PRs #60 and #94. Substantial OpenAI Codex assistance; no
independent or formal review. It does not select a new SAT result, improve
alpha, or establish the unrestricted general-density reduction.

## Conditional statement

Fix k and D. Suppose the field-clique executor, its two-direction crossing
family and rho satisfy the full source master time/rank hypotheses together
with PR #94's uniform polynomial-workspace entry and metadata hypotheses.
Suppose the relevant good-prime inventory is deterministically computable in
polynomial workspace/time with the compact certificate of PR #60 (or a
separately proved equivalent supply), uniformly across all call lengths.
Write `alpha=log2(1/rho)>0`. Then the source clause-network route can count
all satisfying assignments of a k-CNF with m<=Dn on n declared variables in

```math
 poly(n+m) + 2^{O_(k,D)(n/(log(2+n))^alpha)}
```

bit operations and polynomial(n+m) workspace, including the exact binary
output. This is an interface consequence under the stated hypotheses. In
particular, PR #84's structured examples have known rate obstructions, so
they are **not** asserted to supply a new useful rho. The selected OpenAI
baseline already has deterministic polynomial-space alpha 1/2 at fixed
density; this composition does not improve it.

## Network and original query bound

Handle an empty clause immediately. Deleting duplicate literals and
tautological clauses, and deduplicating clauses if desired, preserves the
count on the declared variable set. Empty formulas give `2^n`. Record unused
variables explicitly. These transformations and all input storage require
polynomial(n+m) workspace; n is charged explicitly because binary output
`2^n` itself has n+1 bits even when n is encoded compactly.

In the source construction, order the remaining m clauses and partition them
into `g=3K^8` clusters of at most `ceil(m/g)` clauses. Each literal occurrence
has one Boolean setting bit. Link successive occurrences of each variable by
equality tests; intra-cluster tests enter the node indicator, and
inter-cluster tests enter the corresponding equality edge. Every occurrence
is incident to at most two such tests. Node entries check their clauses and
internal equalities; edge-factor entries check their indicated occurrence
bits. They are computable in polynomial workspace and time from the input,
cluster and setting, with no stored truth tables.

Let t<=km be the number of remaining occurrences. There are at most 2^t
node-setting assignments and every original network summand is 0 or 1, so
its complete integer value Z satisfies `0<=Z<=2^t`. In fact Z is the number
of satisfying assignments of occurring variables; the looser 2^t bound is
used for CRT. Multiplying by `2^(n-u)`, where u is the number of occurring
variables, restores assignments of declared unused variables. The bound is
on the **original network query**, not on an individual prime residue or an
inner field factor.

## Query recovery, workspace and time

Obtain the polynomial-size inventory of distinct certified good primes with
product greater than `2^(t+1)` as in PR #60. For each prime, run the source's
first good grouping search and its streamed field-clique algorithm from
PR #94; group settings and entries are recomputed one at a time. Source
`lem:grouping-explicit` bounds the grouping and entry-enumeration cost, while
PR #94 bounds the recursive stack. All occurrence/test lists, prime inventory,
current grouping, counters, field elements and a CRT accumulator are
polynomial(n+m) bits. The network and all primes are processed sequentially.
Recover the balanced integer Z by CRT only after each complete field network
query; then multiply by the unused-variable factor. No modulo-2 operation is
applied directly to an odd-prime residue.

The source fixed-density cost calculation gives `U<2km`,
`gP<=2k(m+g)`, and polynomial-time root entries. With its choice of K and
level, the logarithm of the query time is
`2 e k m + O(km/K+K^8 log K+K^2 log(km))`, with
`e=O((log m)^(-alpha))`. The polynomial number of prime queries, polynomial
field and CRT operations, and polynomial preprocessing are charged. For
m<=Dn the resulting time is bounded by the displayed expression; finitely
small m are handled by direct enumeration of occurring variables, not by
enumerating n unused bits. The selected algorithm's finite exceptions and
input-reading costs are preserved.

The finite checker enumerates actual clause/equality network assignments for
small formulas and groupings, checks CRT and the unused-variable correction
against direct truth tables, and exercises empty clauses and tautologies. It
does not implement the source recursion, the large prime-supply sieve, or an
asymptotic SAT solver. The arbitrary-density greedy/profile/sparsification
outer reduction has not been composed here.
