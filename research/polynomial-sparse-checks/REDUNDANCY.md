# Distance versus the number of initial checks

For any binary r-by-m matrix A, let C=ker A. If every nonzero codeword has weight at least m/P, then, with

    t = floor((ceil(m/P)-1)/2),

we have

    rank(A) >= log2(sum_{j=0}^t binom(m,j)).

Indeed the Hamming balls of radius t around distinct codewords are disjoint, because their pairwise differences are nonzero codewords of weight at least ceil(m/P)>2t. Each ball has the displayed cardinality. Rank-nullity gives |C|=2^{m-rank(A)}, and packing the balls into F_2^m gives the inequality. The number of rows is at least rank(A); this argument applies even to dependent or repeated checks. If t=0 it is vacuous.

For P>=1 and m/P>=4, t>=m/(4P), while t<m/(2P). Since binom(m,t)>= (m/t)^t,

    number of rows >= (m/(4P)) log2(2P).

For P=1 the premise forces C={0}, and the same displayed estimate is still a valid weaker bound. When m/P<4, do not use this simplified estimate.

For the retuned parameter P'=20000 B² R² in RETUNED.md, in the asymptotic regime m=Theta(n) and fixed positive B we have R=Theta(log log n). Every matrix satisfying that stronger distance contract must therefore have at least

    Omega(n log log log n / (log log n)^2)

rows. In this regime the source-parameter construction's O(n log log n/log n) row count from ROW-COUNT.md is asymptotically smaller. There is no contradiction: that row-count upper bound belongs to the weaker source distance m/P, whose P scales like log² n, not the retuned P'. Thus the source sublinear row-count estimate cannot be transferred unchanged to the retuned distance requirement. This is an interface-level coding bound; it does not apply to checks that exploit the restricted set of realizable violation vectors and is not a lower bound for SAT time, alpha, or formula-aware preprocessing.

The verifier exhausts every small binary matrix in its stated domain and checks the packing inequality from its exact kernel. The proof is independent of that finite check. Hamming ball packing is standard; no priority claim is made.

## Realization by a unit-clause formula

The same matrix-interface lower bound can occur on a real width-at-most-3 CNF, even if A is selected after reading the formula. Take n=m and F=AND_{i=1}^m x_i. As x ranges over Boolean assignments, its violation vector ranges over all of F_2^m, with v_i=1-x_i. Hence any matrix A for this formula that makes every nonsatisfying accepted assignment violate at least m/P clauses necessarily has a kernel satisfying the distance hypothesis above. The Hamming lower bound therefore holds for that promise on this actual formula, including after arbitrary formula-aware selection of A.

This observation is restricted to the specific stage contract: an algorithm that directly solves or preprocesses the unit formula, changes the variables, changes the set of indexed violations, or avoids the promise need not pay this row bound. It still does not imply a SAT time lower bound. It also does not assert that all large supports survive a particular selected A; the packing proof applies to the entire kernel that remains.
