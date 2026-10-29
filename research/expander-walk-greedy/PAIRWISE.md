# Polynomial-size greedy candidate family

This strengthens the walk bounds in PROOF.md and SMALL-BIAS.md. It is a deterministic candidate enumeration for the source's greedy sparse parity selection, not a randomized SAT algorithm. Pairwise-independent indices also motivate the distinct randomized-hash work in [issue #53](https://github.com/1337isnot1337/3-SAT/issues/53); we credit that overlapping idea and do not claim priority for it or for the standard finite-field construction.

## Construction

Let q be the least power of two at least m. Let H be the least power of two at least max(2,q,P), and h the least power of two at least 2P. Construct F_H and F_h deterministically by the irreducible-polynomial enumeration in SMALL-BIAS.md. Choose distinct t_0,...,t_(P-1) in F_H (for example the first P binary representations). Let pi:F_H -> F_2^(log_2 q) be the linear projection onto the first log_2 q coordinates in the chosen polynomial basis; q=1 uses the zero map. Identify its q values with graph vertices, of which m are real indices.

For each a,b in F_H, set vertex v_j=pi(a t_j+b). For each of the h² coefficient strings c from SMALL-BIAS.md, emit the P-pair list (v_j,c_j) at real vertices, and (1,0) at dummy vertices. Enumerate all H²h² lists with multiplicity. Since H<=2 max(q,P) and h<4P, their number is less than 64 max(q,P)^2 P^2, and enumeration and field construction take poly(m,P) time and space. All repeated visits and zeros are retained as list entries.

## Hitting and parity

For q>1, every v_j is uniform on q vertices: b is uniform and pi is surjective. For j != k, the field pair (a t_j+b, a t_k+b) is uniform on F_H² because t_j-t_k is nonzero; projecting both entries preserves their independent uniform distributions. The q=1 case is trivial. For any S subset [m] with |S| >= m/P, define Z=sum_j 1[v_j in S]. Its mean is mu=P|S|/q >= 1/2 because q<2m. Pairwise independence gives E Z² = mu² + P delta(1-delta) <= mu²+mu, with delta=|S|/q. Cauchy--Schwarz gives Pr(Z>0) >= mu²/E Z² >= mu/(1+mu) >= 1/3. This argument remains valid when P exceeds q, since the t_j are distinct in the larger field F_H.

Fix any index sequence that hits S, and let J be its nonempty set of hit positions. By SMALL-BIAS.md at least 1/4 of coefficient strings give odd parity over J, regardless of repeated indices. Thus at least 1/12 of all H²h² candidate lists reject S.

## Greedy counting composition

Retain the source's initial sparse-check matrix, whose surviving nonsatisfying assignments have violation support at least m/P. At each of 8n rounds count N(A;h) for every candidate and append a minimizer. Since satisfying assignments pass all candidates and the finite candidate family rejects each surviving nonsatisfying assignment at least 1/12 of the time, the nonsatisfying count decreases by a factor at most 11/12. Because 2(11/12)^8 < 1, after 8n rounds it is zero. At most 8n H²h² candidate count calls plus one final count suffice; the candidate system has at most 11n+1 equations, each with at most 2^k max(D0,P) monomials of degree at most k. All candidates, including rejected ones, are included in this budget. Enumeration, stored current matrix, polynomial-bit oracle outputs, and the source counter use polynomial space.

This replaces the source's exp(polylog n) greedy candidate multiplicity by poly(n,m,P) calls for its stated P=polylog n. It does not alter the initial sparse-check construction, the density reduction or the count-call contraction cost, so it establishes no improved selected alpha or full SAT exponent. Unlike the optional constant-degree walk refinement, it uses no external expander theorem. The proof is author-checked, not independently reviewed or formally verified.
