# Maximum-deficiency decision interface

Status: source-credited composition and author-checked argument, substantially AI-assisted; no independent review. The published fixed-parameter theorem is used as a black box, not claimed as new.

## Source and parameter

Normalize a CNF by removing tautological clauses and duplicate literals and duplicate clauses; detect an empty clause directly. The source treats formulas as clause sets. Let n be the number of remaining variables, m the number of remaining clauses, and N the original input length. Define

    k(F) = max over subsets C of F of [ |C| - |var(C)| ],

with the empty subset included. This is maximum deficiency, not merely m-n. It equals the number of unmatched clause vertices in a maximum matching of the clause-variable incidence graph (Szeider, Lemma 6); it is nonnegative and polynomial-time computable. Variables that occur in no remaining clause do not affect decision and are excluded from n.

Stefan Szeider, *Minimal Unsatisfiable Formulas with Bounded Clause-Variable Difference are Fixed-Parameter Tractable*, Journal of Computer and System Sciences 69 (2004), Theorem 4, gives deterministic SAT decision in O(2^k n^3), with a satisfying assignment or a resolution refutation. Source PDF: https://www.ac.tuwien.ac.at/files/pub/szeider-jcss-2004.pdf; fetched 2026-10-28, SHA-256 `60e1a8255b06ecd78c8e35dc58f536c804dbc1401f70f6ed275131573642237d`. The source constructs an explicit search tree whose depth is at most k, using polynomial-time reduction and matching operations. The decision traversal can be run depth first in polynomial space, storing the current path and local reductions; this is our implementation observation, not a claim that an explicitly emitted resolution certificate has polynomial length. No solver is implemented here.

Using that theorem and the owner-accepted OpenAI exact-counting theorem, one can race both deterministic decision procedures by alternating machine steps, ending when either completes. For fixed k-CNF width, the resulting time is bounded, for a suitable constant C, by

    poly(N) * min(2^k(F), 2^(C n log log(n+4) / sqrt(log(n+4))))

and the traversal uses polynomial space. The fixed-density accepted bound gives the sharper baseline term when its own density hypothesis applies. Preprocessing and matching are polynomial in N; there is no randomization, amplification, or numeric precision. The source's k is an integer, so no unspecified constant hides in the first exponent; polynomial overhead is absorbed. The construction is uniform but is a composition of two existing algorithms, not a new unrestricted 3-SAT bound. The accepted theorem is not reimplemented here.

## Alternating-path autarky

A useful polynomial preprocessing can be verified independently of Theorem 4. Find a maximum clause-variable matching M. Start at every unmatched clause; explore from reached clauses to all incident variables, and from each reached variable to its matching clause. Let R be reached clauses, X reached variables. A reached variable must be matched, otherwise there is an augmenting path. Every non-reached clause is matched to a non-reached variable. Set each such variable to satisfy its matched clause. No reached clause contains any assigned variable, because all its neighbors are reached; every non-reached clause is satisfied by its matched variable. Thus this partial assignment is an autarky: it touches only clauses it satisfies. Removing non-reached clauses yields an equisatisfiable formula R, and any satisfying assignment of R extends by the autarky.

Every reached variable matches a reached clause, and every reached clause is either matched to a reached variable or is one of the k unmatched roots. Therefore |R|-|X|=k. X is precisely the set of variables appearing in R. The reduced formula may still be large even for small k, and the matching and simplification do not by themselves prove the 2^k decision bound. The source's full criticality reduction is essential to that theorem. The autarky also does not preserve the number of satisfying assignments.

## Limitations and branching

The maximum-deficiency parameter can be linear even in a connected, bounded-occurrence, satisfiable formula with no units or pure literals. For each j=1,...,r create variables a_j,b_j,c_j and five clauses

    (a OR b OR c), (a OR b OR NOT c), (a OR NOT b OR c),
    (NOT a OR b OR c), (a OR NOT b OR NOT c).

Add (a_j OR a_{j+1}) for each j<r. The all-true assignment satisfies all clauses. Every variable appears in both signs; no unit or tautological clause occurs. Each variable occurs at most seven times, and the primal graph is connected. Here n=3r, m=6r-1. The incidence graph matches all n variables to distinct clauses: in each block match a,b,c to the first three distinct block clauses. Thus k=m-n=3r-1. These easy inputs show that raw k cannot be uniformly bounded by o(n) from bounded occurrence, connectivity or those two local simplifications alone. They do not preclude stronger preprocessing or bound the actual running time of an implementation.

Ordinary branching cannot assume k decreases. For F={(x OR y),(x OR NOT y)}, k(F)=0, but restricting x=0 yields {(y),(NOT y)} with k=1. In general setting one variable raises k by at most one: any subset of distinct residual clauses lifts to equally many distinct parent clauses, whose variable set adds at most the assigned variable. A paid branching reduction using a looser k budget must account for that increase. The cited criticality reduction, rather than this elementary autarky alone, is what makes the source search depth at most the initial k. Running either solver on each branch multiplies the branch count into the cost; a bounded-occurrence or sparsification reduction does not establish a useful uniform k bound without a separate proof.

## Reproduction and limits

`python3 -I -B research/matching-deficiency-interface/verify.py` exhaustively checks the maximum-deficiency identity, autarky properties and equisatisfiability on 1,200 seeded small formulas; it checks the planted family for r=1,...,20 and the branch-increase example. These finite checks do not verify the source theorem, the accepted baseline, or an unrestricted improvement. See README for commands and open questions.
