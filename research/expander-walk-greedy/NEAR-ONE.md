# Approaching one greedy equation per variable

This is a continuation of the affine-index/trace-coefficient handoff in PR #64, credited in HANDOFF-64.md. It trades a polylogarithmic increase in row width for fewer greedy equations, while retaining polynomially many candidates. It is author-checked and does not change the selected SAT alpha.

Let A^(0) satisfy the source support promise: every nonzero violation vector in its kernel has weight at least m/P. Fix integer t>=8 and set L=tP. Pad m to q, the least power of two at least m. If L<=q, enumerate all affine pairs A,B in F_q on L distinct field positions. If L>q, use each padded coordinate once. Independently enumerate all X,Y in F_Q, where Q is the least power of two at least tL, and put c_j=Tr(Y X^j) on each used position. Dummy coordinates are emitted with coefficient zero; repeated positions are kept before their coefficients are combined. The same polynomial-time field setup and row expansion as HANDOFF-64.md apply.

For a support S of size at least m/P in the affine case, the hit count has pairwise-independent indicators and mean at least t/2 because q<2m. The second moment bound therefore gives Pr(hit)>=t/(t+2). In the fallback the hit probability is one. Conditional on any hitting position set, its nonzero polynomial has degree <L; at most L-1 of the Q choices of X are roots, and a uniform Y gives an unbiased trace otherwise. Hence Pr(odd | hit)>=(1-1/t)/2. A uniform seed pair therefore rejects each eligible support with probability at least

    p_t = (t-1)/(2(t+2)),     rho_t = 1-p_t = (t+5)/(2(t+2)).

There are at most q²Q² < 16 m² t^4 P² candidates per round, including all discarded candidates; in the fallback the index seed can be omitted. Every candidate has at most L=tP listed pairs. Selecting the minimum count reduces the surviving nonsatisfying count by rho_t.

Let T=n+ceil(32n/t)+1. Then 2^n rho_t^T<1 for every n>=1 and t>=8. Indeed ln(2rho_t)=ln(1+3/(t+2))<=3/(t+2), and ln 2>=1/2. Thus

    n ln 2 + T ln rho_t
      <= n[ -32 ln 2/t + 3(1+32/t)/(t+2)]
      <= n(64-13t)/(t(t+2)) < 0.

After T rounds the exact nonsatisfying count is zero. The computation uses T q²Q² candidate oracle calls plus one final count, polynomial field setup and sequential polynomial space; all candidate systems meet the source sparse-query contract provided tP and the initial width remain polylogarithmic.

For the original-parameter polynomial construction of initial checks in PR #78, its author-checked ROW-COUNT.md proves a0=O(n log log n/log n) uniformly on polylog-density leaves. Choose t=max(8,ceil(log log(n+16))) using a fixed logarithm base. Then t->infinity, tP is polylogarithmic and T=n+o(n); the full query system has a0+T=n+o(n) equations, including the candidate under evaluation. In the source incidence-degree bound K=k(a+2(n+1-1)), this gives K <= (3k+o(1))n. Every test still has polylogarithmically many monomials, all rejected queries are charged, and variable branching, degree arrays, entries, precision, contraction and outer sparsification are unchanged. Thus this improves a leading equation-count coefficient and not the asymptotic O(n log log n / sqrt(log n)) runtime or alpha. The o(n) initial-row assertion here uses the original, weaker source distance; it cannot simply be substituted for the stronger retuned distance, as PR #78's REDUNDANCY.md explains.

The count n+o(n) is close to sharp for the particular unpreprocessed unit formula F=AND_i x_i under an exact common-zero interface on the original n violation bits: exactness requires ker A={0}, hence rank(A)=n and at least n total rows. A SAT algorithm that preprocesses the formula, changes its interface, or uses another reduction can bypass this observation; it is not a SAT lower bound.
