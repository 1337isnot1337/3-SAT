# Sparse parity candidates from walks

## Statement

Let m >= 1 and P >= 1 be integers. There is a deterministically enumerable multiset of binary rows, each represented by a list of P clause-index/bit pairs, of size at most q d^(P-1) 2^P, where q is the least power of two at least m and d = O(log(m+2)). For every nonempty S subset [m] with |S| >= m/P, at least 1/20 of the lists have odd intersection with S. The multiset and its graph are constructible in exp(O(log^2(m+2))) time and polynomial space. Repetition and zero coefficients count toward list length, as in `eq:hash-query`.

## Construction

Set q as above and embed [m] in the group G = F_2^r of order q. For q > 1 choose d = ceil(32 ln(2q)) shifts (repetitions allowed), with all nontrivial Walsh eigenvalues bounded in absolute value by d/2. Enumerate shift tuples lexicographically until the condition holds, checking all q-1 characters. Existence follows by independent uniform shifts and the Hoeffding bound: a fixed nontrivial character has absolute sum greater than d/2 with probability at most 2 exp(-d/8); union over q-1 characters gives less than 1. Enumeration costs q^d poly(q,d) = exp(O(log^2(m+2))) and polynomial space. For q=1 use d=1 and the zero shift. This is the same Walsh-Cayley construction as `lem:sparse-checks`, specialized to constant spectral gap; no external expander construction is assumed.

Enumerate each starting vertex uniformly, each of the d choices for each of P-1 steps, and every P-bit coefficient string. At every visited real vertex e emit (e,c); for a dummy vertex emit (1,0). Thus every list is legal, including when m=1; the multiset retains multiplicities.

## Avoidance and rejection

For q>1, let T be the symmetric walk matrix, U=G\S, delta=|S|/q, and D the projection onto U. The operator norm of DTD is at most 1-delta/2. Indeed, for a unit vector f supported in U, its constant-component squared is at most |U|/q=1-delta. The constant eigenvalue is 1, and all other eigenvalues lie in [-1/2,1/2], so the Rayleigh quotient is at most 1/2+(1/2)(1-delta), and at least -1/2. Hence the absolute eigenvalues obey the bound. Starting uniformly, the probability of avoiding S at all P positions is at most (1-delta)(1-delta/2)^(P-1), by Cauchy--Schwarz and the symmetric spectral norm.

Since q<2m for m>1, delta >= 1/(2P). If P>=2, avoidance is at most exp(-(P-1)/(4P)) <= exp(-1/8) <= 8/9. If P=1, the initial position hits S with probability delta >= 1/2. The q=1 walk hits every nonempty S with probability one. Given any walk that hits S, the independent uniform coefficient bits make the resulting parity on S uniform, even with repeated vertices: one hit position has a fresh coefficient bit independent of all others. Thus rejection is at least 1/18, hence at least 1/20, in every case.

## Greedy composition and cost

Retain the initial matrix A^(0) from `lem:sparse-checks`. For an accepted nonsatisfying assignment, its violation support satisfies the required threshold. At each of 14n rounds, enumerate every list, compute N(A;h) using the accepted sparse-polynomial counter, and append a minimizer. The satisfying assignments pass every row, so averaging shows D shrinks by at least a factor 19/20 each round. Since 2(19/20)^14 < 1, after 14n rounds D < 1 and hence D=0. The procedure does not need to know #F. It makes at most 14n q d^(P-1) 2^P candidate count calls plus one final count, with at most 17n+1 equations in a candidate system (a conservative bound), and candidate row length P. Existing initial-row length D0 and the degree and monomial limits remain max(D0,P) and 2^k max(D0,P), including rejected candidates. Graph construction, counters, and one candidate at a time use polynomial space; counter outputs and row indices have polynomial bit length. There is no random algorithm here: probability is used only to prove existence and the averaging lemma.

Compared with 3n(2m)^P source calls, this is 14n q d^(P-1)2^P, and q<2m, d=O(log(m+2)); the reduction is meaningful when P grows and m dominates log m. Both are exp(polylog n) under the source parameters B=polylog(n), P=polylog(n), so this establishes no improved asymptotic SAT exponent, alpha, or master-contraction bound. Constants hidden in the sparse-polynomial theorem must accommodate 17n+1 equations. No tighter initial Tanner code, query wire bound, or runtime for the tensor contraction is asserted.
