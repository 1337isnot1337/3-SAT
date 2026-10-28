# Tseitin controls for separator and deficiency interfaces

Status: source-credited argument and bounded checks, substantially AI-assisted; no independent review. The parity formulas are classical Tseitin formulas, not a new construction. The results below concern specific structural measures and regular-resolution output, not the complexity of unrestricted SAT decision.

## Construction and exact accounting

Let G=(V,E) be a finite connected simple cubic graph, let q=|V| and n=|E|=3q/2, and choose charges c_v in {0,1} of odd total parity. Associate one Boolean variable x_e with each edge. At each vertex v impose the linear equation over F2

    sum_(e incident to v) x_e = c_v.

For each of the four assignments to the incident triple that violates this equation, add the unique 3-clause falsified by that assignment. This gives the standard Tseitin CNF T(G,c) with four distinct clauses per vertex and m=4q=8n/3 clauses. Simple G ensures different vertex blocks have different triples. Each variable occurs in its two endpoint blocks, twice per sign in each, hence exactly four positive and four negative occurrences. There are no units, repeated variables in a clause, pure literals or singular literals. The primal graph is the line graph L(G), with maximum degree four.

Adding all vertex equations cancels each edge twice and gives 0=1, so T(G,c) is UNSAT. Conversely, after deleting all four clauses of any one vertex, the remaining parity equations are independent and consistent. More generally the only F2 dependency among the vertex equations is their total sum: a vertex subset yields zero incidence vector precisely when it has no edge leaving it, so connectedness forces the empty set or all V. Therefore any proper subset of vertex blocks is satisfiable. In fact, if G has no articulation vertex, the CNF is minimally unsatisfiable: removing any single clause makes it satisfiable. Suppose the removed clause lies at v and is falsified by the wrong-parity triple a on its three incident edges. Fix those edges to a. The remaining parity equations lie on connected G-v, with adjusted charges. Their total charge is even: the old total charge was odd, and a has parity opposite to c_v. A connected graph incidence system is consistent exactly when its charges have even total parity, so assign its internal edges to satisfy the other vertices. At v, the chosen triple falsifies exactly the removed clause; the other three clauses in its block are true. The claim applies to K4 and the cube and to any 2-vertex-connected graph in the family. The connectivity hypothesis cannot simply be dropped: the checker joins two edge-subdivided copies of K4 by a bridge, puts the odd charge on one side, and removes a clause at the other bridge endpoint whose falsifying triple gives the bridge the wrong value. The remaining formula is still unsatisfiable. This example does not assert anything about expander families. The full system is decidable by Gaussian elimination, or directly by checking charge parity on each graph component; it is not an unrestricted SAT hardness example.

The incidence graph matches all n variables to distinct clauses. Orient each graph edge arbitrarily to one endpoint; at each vertex assign its at most three oriented edges to distinct clauses of its four-clause block. Hence maximum deficiency k=m-n=5q/2=5n/3. Its occurrence defect is E=5n, width shortfall is zero, and the inequality 3k<=S+E from the predecessor is an equality.

## Local reductions and short resolvents

For a nonempty set X of edge variables, let U be its endpoint set. Since 2|X|<=3|U| and all four clauses of every touched vertex belong to F_X,

    |F_X|-|X| = 4|U|-|X| >= 5|X|/3.

For |X|=1 the surplus is 7, and for |X|>=2 the integer surplus is at least 4. In particular the formula is 2-expanding and matching lean. By Szeider's published Lemma 12, cited and hash-pinned in [the maximum-deficiency package](../matching-deficiency-interface/PROOF.md), every single-variable restriction reduces k. Matching-autarky, unit, pure and singular elimination do not simplify the initial instance, but linear-algebraic preprocessing does.

Within one vertex block, the four falsifying assignments have the same parity. Two distinct such bit strings differ in exactly two positions. Resolving their corresponding clauses on one differing variable produces a tautology because the other differing variable remains with both signs. Clauses from different blocks share at most one variable, so any non-tautological resolvent from them has exactly four distinct literals. Thus no non-tautological one-step resolution of two original clauses creates a unit, binary, or ternary clause. This does not constrain later, unrestricted reasoning.

## Expander separators and regular-resolution output

There exist arbitrarily large simple cubic edge expanders by Friedman's theorem, cited and pinned in [the line-graph predecessor](../separator-hierarchy/LINE-GRAPH.md). On that family, the argument in that predecessor shows L(G) also has constant edge expansion and bounded degree, hence every two-thirds-balanced vertex separator of the primal graph is linear in n. This excludes small balanced *primal* separators for this encoding, not changed encodings or other algorithms.

Constant-degree edge expansion also forces tw(G)=Omega(q): a tree decomposition of width w has a two-thirds-balanced vertex separator of size at most w+1, while expansion gives every such separator size Omega(q). Itsykson, Riazanov and Smirnov, *Tight Bounds for Tseitin Formulas*, SAT 2022, Theorem 4.3 and Appendix C.1, prove a lower bound on the size of every regular-resolution refutation of an unsatisfiable Tseitin formula on a connected graph. The proof explicitly gives at least `2^(Omega(tw(G)))/q`; with tw(G)=Omega(q), that is `2^Omega(q)` here. The source PDF is https://drops.dagstuhl.de/storage/00lipics/lipics-vol236-sat2022/LIPIcs.SAT.2022.6/LIPIcs.SAT.2022.6.pdf, fetched 2026-10-28 with SHA-256 `df4245b223b2fa884570afb45516a8513b4272f9c1b9f6223339965031b6ddf5`.

This is a lower bound on the number of clauses in an explicitly emitted regular-resolution refutation. It implies exponential output time for an algorithm required to emit such a refutation on these inputs. It does not give a lower bound on SAT decision, general proof systems, or the owner-accepted counting algorithm. The latter need only output a count, and the Tseitin inputs are independently polynomial-time decidable by parity elimination. The result is consistent with the source deficiency algorithm's ability to emit regular refutations: here its parameter is linear.

## Finite controls

`python3 -I -B research/tseitin-deficiency/verify.py` constructs odd-charge formulas for K4 and the cube, exhaustively checks unsatisfiability and satisfiability after deleting each vertex block or each individual clause, checks all original one-step resolvents, computes matching deficiency, enumerates all variable subsets for expansion, checks both restrictions of every variable, and checks the articulation counterexample. It is a finite construction check; it does not prove the external expander theorem, the cited proof-size theorem, or an all-size SAT lower bound.
