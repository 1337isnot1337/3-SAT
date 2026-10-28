# Clause-width and occurrence defects

Status: author-checked elementary bookkeeping, substantially AI-assisted, with no independent review. This builds on [the merged maximum-deficiency interface](../matching-deficiency-interface/PROOF.md) and makes no novelty claim for degree counting or the underlying SAT theorem.

## A checkable sufficient condition

Normalize an at-most-3-CNF F by deleting tautological clauses and duplicate literals and clauses. If an empty clause remains, report UNSAT. Let d(v) be the number of clauses containing variable v, w(C) the number of distinct variables in clause C, and define

    S(F) = sum_C (3 - w(C)),
    E(F) = sum_v max(d(v) - 3, 0),
    P(F) = S(F) + E(F).

All these quantities are nonnegative and computable in polynomial time. Let k(F) be maximum clause-set deficiency, defined in the predecessor package. Then

    3 k(F) <= P(F).                                           (1)

Indeed for any subfamily A of clauses and its incident variables V(A), writing d_A(v) for the number of A-clauses containing v,

    3|A| = sum_(C in A) w(C) + sum_(C in A) (3-w(C))
          <= 3|V(A)| + sum_(v in V(A)) max(d_A(v)-3,0) + S(F)
          <= 3|V(A)| + E(F) + S(F).

Maximize |A|-|V(A)| over all A. The empty family covers the zero case. Szeider's source-pinned theorem then decides F in polynomial space and time `poly(N) 2^floor(P(F)/3)`, with N the original input length. This is a corollary of the published maximum-deficiency algorithm, not a new unrestricted 3-SAT algorithm or a new general alpha. The exact k is itself polynomial-time computable by maximum matching and is never larger than this upper bound; use of P provides a simple sufficient structural condition, not a faster solver than measuring k directly.

For a fixed gamma>1/2, inputs satisfying P(F)=O(n/(log(n+4))^gamma) have decision time `poly(N) 2^O(n/(log(n+4))^gamma)` under this corollary. This is a bound for the stated, efficiently checkable input class. It does not establish a reduction of all 3-CNF to that class. Moreover m-n <= k <= P/3 for the normalized formula's used-variable count, so this promise implies fixed density for large n; comparisons should use the accepted fixed-density bound, not the weaker general-density envelope. Original unused variables have no effect on decision.

## Sharpness and limitations

Both parts of (1) are separately sharp. For all eight sign patterns on three variables, every clause has width three, every variable has degree eight, P=E=15, and k=8-3=5. For the six positive 2-clauses corresponding to the edges of K4, all variables have degree three, P=S=6, and k=6-4=2. The complete family is itself the maximizing subfamily in both examples. The first example is UNSAT; the second is trivially SAT.

The estimate can also be much looser than k. Take r clauses `(x OR a_i OR b_i)` with distinct private a_i,b_i. They have width three and P=r-3 for r>=3, but the incidence graph matches every clause to its private variable, so k=0. The example has a pure variable and is easy to simplify. It shows that P cannot be substituted for the exact matching parameter when making a tight instance-specific claim.

## Restriction cost

Let F' be obtained by assigning a single variable x and simplifying, with empty clauses retained for the calculation; duplicate residual clauses are removed. Let d be the old degree of x, and u the number of its clauses that survive the assignment and hence lose x. Then

    P(F') <= P(F) + u - max(d-3,0) <= P(F)+3.                (2)

S grows by one for each surviving x-clause and does not grow when a satisfied clause or duplicate is removed. Other variables' degrees cannot increase, while deleting x removes its contribution max(d-3,0) to E. As u<=d, the last inequality follows. Assigning (x=0) in the three clauses `(x OR a_i OR b_i)` for i=1,2,3 attains the increase three. An actual solver can immediately return UNSAT if an empty clause appears.

Thus t arbitrary variable assignments give P <= P_0+3t, and exhaustive branching on t variables followed by the defect-bound solver costs at most `poly(N) 2^(t+floor((P_0+3t)/3))`, i.e. `poly(N) 2^(P_0/3+2t)` up to constants. The cost of constructing or enumerating branches is included. This coarse guarantee alone cannot justify a speedup from branching: it increases the paid exponent. Better results require a proved decrease in the total defect on the actual branches or an independently sharper cost analysis. Neither this bound nor the small finite controls prove such a reduction.

## Checks and sources

`python3 -I -B research/occurrence-defect-interface/verify.py` checks (1) by exhaustive clause-subset enumeration on 1,200 seeded small formulas, checks (2) on 8,400 assignments, and verifies the three equality cases. These are finite controls. Szeider's *Minimal Unsatisfiable Formulas with Bounded Clause-Variable Difference are Fixed-Parameter Tractable*, JCSS 69 (2004), Theorem 4, is pinned by URL and PDF hash in the predecessor proof; the theorem and accepted baseline are not implemented here.
