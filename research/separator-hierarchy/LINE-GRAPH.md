# A linear 3-CNF obstruction with bounded occurrence two

Status: author-checked, substantially AI-assisted; no independent review. This extends the structural counterexample in [PROOF.md](PROOF.md). The family is existential, based on a cited expander theorem; the two finite controls are explicit. The formulas are intentionally satisfiable and do not give a SAT lower bound.

## Construction

Let G be a simple connected cubic graph. It contains a cycle. Direct that cycle cyclically, then direct a spanning forest on the remaining vertices towards the cycle; direct all other edges arbitrarily. Every vertex has an outgoing edge. For every edge e create a Boolean variable x_e. At each vertex v make one clause of its three incident edge variables, positive for an edge directed out of v and negative for an edge directed into v. All-true satisfies each clause, since each vertex has an outgoing edge.

Every clause has exactly three distinct variables, every variable occurs exactly twice, once positively and once negatively, and any two clauses share at most one variable. Therefore there are no units, tautologies or pure literals, and resolving any pair on a shared variable produces a non-tautological clause with exactly four literals. This statement covers one resolution step on the original formula only. The primal graph is exactly the line graph L(G): edge-variables are adjacent precisely when their edges share a vertex. L(G) has maximum degree four. A different procedure, including variable elimination and longer resolution sequences, can simplify the formula; the all-true assignment solves it immediately.

## Expansion transfer

Suppose G has edge expansion h>0: every vertex set U of size at most |V|/2 has at least h|U| edges crossing its boundary. Let F be a nonempty set of at most |E|/2 edges. For each vertex v put a_v=|{e in F: e meets v}|, let t be the number of vertices with a_v=1 or 2, and let A be the set with a_v>=2. Each mixed vertex contributes exactly a_v(3-a_v)=2 edges to the cut of F in L(G). Every edge in that line-graph cut has a unique common vertex because G is simple, so the cut has size exactly 2t.

Each G-edge crossing A to its complement has at least one mixed endpoint, hence there are at most 3t such edges. Expansion gives min(|A|,|V minus A|) <= 3t/h. Also |F| <= 3|A|+3t: an F edge not touching A has a mixed endpoint, and at most 3t edges meet mixed vertices. Similarly |E minus F| <= 3|V minus A|+3t. Since |F|<=|E minus F|, both bounds imply

    |F| <= 3 min(|A|,|V minus A|) + 3t <= (9/h + 3)t.

Thus L(G) has edge expansion at least 2/(9/h+3), uniformly in G. The balanced-separator argument in PROOF.md applies with max degree four, so every separator of L(G) whose remaining components have at most two thirds of its vertices is linear in its number |E| of vertices.

A family of simple cubic expanders exists: Joel Friedman, *A proof of Alon's second eigenvalue conjecture and related problems*, arXiv:cs/0405020v1, Corollary 1.4 and the discussion immediately following it, applies to uniformly random simple 3-regular graphs on even vertex counts. Choosing epsilon below 3-2 sqrt(2) gives a uniform positive spectral gap with probability tending to one; the standard variational bound gives a uniform positive edge expansion. In particular there exist arbitrarily large connected simple cubic expanders. This supplies existence, not a claimed polynomial-time construction of a particular family. The PDF fetched 2026-10-28 from `https://arxiv.org/pdf/cs/0405020v1` had SHA-256 `bcdb86f1bc0d7151ac4e982b1b9a40e832665c60683a90a373e68bffa832440d`. The finite checker does not prove Friedman's theorem or the expansion transfer.

## Check

`python3 -I -B research/separator-hierarchy/linegraph.py` constructs the formulas for K4 and the cube from directed Hamiltonian cycles. It checks their clause widths, occurrence and polarity counts, pairwise intersections, all original one-step resolvents, and the identity |cut_L(F)|=2t for all 41 and 2,509 eligible edge subsets respectively. These finite instances are controls of the construction and transfer identity, not evidence of a uniform expansion constant.
