# Exact counting with an interaction cover

## Interface and theorem

Let `P_1,...,P_a` be explicitly listed polynomials over F2 in `n` declared
Boolean variables, with each polynomial given as a list of monomials. Boolean
multilinearize repeated powers, and combine duplicate terms modulo two. The
interaction graph has all declared variables as vertices and an edge `{u,v}`
whenever distinct variables u and v occur together in a remaining monomial.
Let `C` be a supplied vertex cover of that graph, `t=|C|`, and `B` the input
size. The number of common zeros is computable exactly in
`2^t poly(n+B)` bit operations and `poly(n+B)` bits of space. If a consistent
partial assignment is supplied, the same procedure counts its extensions
in `2^(number of unfixed vertices of C) poly(n+B)` time and polynomial space.

This is the standard backdoor idea specialized to an explicitly listed
polynomial interface, not a claim of a new counting paradigm. The cover and
all monomial supports can be checked in polynomial time. An invalid cover is
not silently accepted. The proof does not assume a minimum cover can be found
in polynomial time.

## Proof and complete local costs

Enumerate assignments of the unfixed cover variables, respecting the fixed
bits. No monomial contains two variables outside C, since those two variables
would form an uncovered edge. After substituting the assigned cover bits,
every monomial is zero, a constant, or a single remaining variable. Combining
terms gives a system of affine linear equations over F2 in the remaining
variables. Include prescribed fixed bits outside C as unary equations.
Gaussian elimination returns zero if inconsistent; otherwise it returns
`2^(r-rank)`, where r is the number of remaining declared variables. This
includes variables never used by any equation. Sum the counts over the
cover assignments; every complete assignment occurs in exactly one branch.
Constant-one, constant-zero and empty systems have their ordinary meanings.
All sums have at most `n+1` bits, branches are processed serially, and
polynomial input, elimination and integer operations give the claimed time
and space. Constructing the graph requires enumerating all pairs in each
listed monomial, polynomial in the explicit input length.

A cover can also be generated without a supplied certificate: compute any
maximal matching by greedily taking an edge with two uncovered endpoints, and
include both endpoints of every selected edge. Maximality makes this set a
cover. If the graph's minimum cover has size `tau`, each vertex cover contains
at least one endpoint of each disjoint matching edge, so the constructed cover
has size at most `2 tau` and at most n. Thus the automatic bound is
`2^min(n,2 tau) poly(n+B)` time and polynomial space. This uses a polynomial
matching computation and does not compute tau or require knowing it.

## Fixed-width CNF

For a CNF clause, the product of its literal-falsity indicators is one
exactly when the clause is false. Impose that polynomial equal to zero for
each clause. Each width-3 clause expands to at most eight listed terms over
F2, including constants; repeated variables and tautologies are handled by
Boolean multilinearization and cancellation. The polynomial-system zeros are
exactly the formula's satisfying assignments, without auxiliary variables.
The interaction graph of the reduced polynomials is a subgraph of the usual
primal graph in which each clause's variable scope is a clique. Therefore a
supplied primal-graph cover also gives a `2^t poly(n+m)` exact 3-CNF count in
polynomial space. Unused declared variables contribute through nullity.

This is a structural-promise result: for example, if the minimum interaction
cover is `o(n log log n / sqrt(log n))`, the automatic method has exponent
`o(n log log n / sqrt(log n))` on that promised family. This compares proven
upper-bound envelopes, not measured running times or lower bounds on the
accepted algorithm. Fixed-density comparisons use its sharper `n/sqrt(log n)`
envelope. The result does not imply this promise for arbitrary SAT or sparse
queries, and does not improve the unrestricted selected alpha.

## Sparse-query assumptions do not force the promise

For even n, use `n/2` equations `P_i=x_(2i)x_(2i+1)=0` on disjoint pairs.
Each equation has one degree-two monomial and each variable occurs in one
scope. It satisfies the listed sparse-query size and degree constraints, and
its original presentation triggers no high-incidence branch. Its interaction
graph is a matching of size `n/2`, so every cover has size at least `n/2`,
and one endpoint from each edge gives equality. This makes the cover-based
bound exponential in n on this family; the family itself is easy, with exact
count `3^(n/2)`. It is not an SAT hardness or a lower bound for other methods.
Even the greedy cover chooses all n vertices here, illustrating the factor-two
bound in this representation.

For use inside the accepted dense reduction, a stronger claim would need a
uniform small-cover guarantee or an adaptive fallback for every generated
sparse query, including rejected greedy candidates, and a complete sum of
preprocessing, branches, queries, entries and counting costs. No such guarantee
is established here. Exact counts on individual promised systems do not pay
those outer costs.

## Credit and evidence

Nishimura, Ragde and Szeider, *Solving #SAT Using Vertex Covers* (Acta
Informatica, 2007), already use vertex-cover-based backdoors to tractable
counting classes; their obstruction graph and target class differ from the
simple monomial-interaction graph here. Their author-hosted paper is
[available here](https://cs.uwaterloo.ca/~plragde/papers/sharpsat_AI.pdf),
SHA-256 `51634b33c93a104408184713ad924fb7d9158778158e6ef7d7fc9e3ead956431`
for the retrieved file. It is background and credit, not a dependency of the
self-contained proof. No priority claim is made for the backdoor idea.
The initial bipartite linear-algebra example is recorded in PR #73. The
accepted OpenAI theorem is used as the comparison premise, not audited.

The proof is author-checked with substantial AI assistance and has no
independent human or formal review. The reference implementation and finite
controls are not the accepted fast contraction algorithm.
