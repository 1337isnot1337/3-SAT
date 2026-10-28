# Connected critical-deficiency examples

Status: author-checked construction and source-dependent corollary, substantially AI-assisted; no independent review. This extends [matching-deficiency-interface](../matching-deficiency-interface/PROOF.md) and [occurrence-defect-interface](../occurrence-defect-interface/PROOF.md). The example is deliberately easy to satisfy and does not imply a SAT lower bound or a general improvement.

## Family

Fix r>=3. For i modulo r create variables a_i,b_i,c_i and the four clauses

    (a_i OR b_i OR c_i),    (a_i OR NOT b_i OR NOT c_i),
    (NOT a_i OR b_i OR NOT c_i),  (NOT a_i OR NOT b_i OR c_i).

Add one connector `(a_i OR a_(i+1) OR b_(i+1))` for each i. There are n=3r variables and m=5r distinct clauses, each with three distinct variables. The primal graph is connected. The all-true assignment satisfies every clause. In the block clauses each variable occurs twice positively and twice negatively; connectors add two positive occurrences of each a and one positive occurrence of each b. Hence each literal occurs at least twice and each variable occurs at most six times. There are no units, pure literals or singular literals (literal occurrence count one).

The incidence graph matches all variables to distinct local block clauses, so a maximum matching has size n and k=m-n=2r. Since every clause has width three and each variable's degree is at least three, the defect P=S+E of the cited predecessor equals total degree minus 3n, which is 3m-3n=6r=3k. Thus its sufficient bound is attained on this connected, bounded-occurrence family.

## Expansion and criticality

For X a nonempty set of variables let F_X denote the clauses containing a variable of X. Suppose X intersects t blocks. All four local clauses of each touched block lie in F_X, so |F_X|-|X| >= 4t-|X| >= t. For t>=3 the surplus is at least 3. For t=2, if |X|<=5 the same bound gives at least 3; if |X|=6 then X contains both complete blocks, and at least one connector is touched, again giving at least 3. For t=1, if |X|=1 the local bound gives 3; if |X|=2, X includes a or b, and at least one connector is touched; if |X|=3 a connector is also touched. The surplus is therefore at least 3 in every case. It is exactly 3 for X={c_i}, which touches only its four local clauses. Thus the family is 3-expanding in Szeider's variable-side sense.

In particular it is 1-expanding and matching lean: a nonempty matching autarky would need a matching covering every clause touched by its assigned variables, but touching any one variable in a block touches all four local clauses, which collectively contain only the three variables of that block. Hall's condition fails. Equivalently, no maximum-matching alternating-path autarky removes a clause: each block has at most three matched local clauses, so at least one is an unmatched root; from that clause all three local variables are reached, and from those variables all matched clauses are reached. Every unmatched clause is a root.

The family is also 2-expanding and has no pure or singular literals. By Szeider, *Minimal Unsatisfiable Formulas with Bounded Clause-Variable Difference are Fixed-Parameter Tractable*, JCSS 69 (2004), Lemma 12, every such formula is maximum-deficiency-critical: for every variable x and either truth value, the normalized restriction has maximum deficiency at most k-1. The exact source URL and PDF SHA-256 are recorded in the predecessor proof. This conclusion uses the published lemma; it is not re-proved here. It means the specific matching-autarky, pure/singular and 2-expansion reduction tests do not reduce this family before reaching the critical state. It does not say that no other preprocessing can solve it: simply testing all true succeeds immediately.

## Evidence and limitation

`python3 -I -B research/critical-deficiency-examples/verify.py` checks r=3,4,5, enumerating all nonempty variable subsets for surplus, computing deficiency by matching, checking both restrictions of every variable, verifying occurrence counts and the defect equality. It does not verify the all-size argument, Szeider's lemma, or the hardness of any input. These examples do not obstruct algorithms using polarity, global assignments, or stronger reductions.
