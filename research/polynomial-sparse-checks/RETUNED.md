# Retuned Tanner distance and row width

This is an all-size, author-checked parameter change to the initial-check construction, not a new SAT exponent. It uses the same graph, Tanner mixing proof, conditional-expectation shift construction and Vandermonde local code as PROOF.md, but replaces the source's `mu` in its local distance parameter by a bound on the field extension degree. All constants below are integer-explicit.

## Statement

For positive integers n,m,B with m<=Bn, let mu=floor(log2 m)+1 and put

    R = 64 + 8 ceil(log2(B mu + 2)),
    P' = 20000 B² R²,
    D' = 320000 B² R² mu.

There is a deterministic polynomial-time and polynomial-space construction of a binary matrix with at most 3n rows, each of weight at most D', whose nonzero kernel vectors have weight at least m/P'. In fact deleting zero rows gives fewer than n/25 rows. For polylogarithmic B, R=O(log log(n+2)), yielding P'=O(B²(log log(n+2))²) and D'=O(B² log(n+2)(log log(n+2))²). The source uses P=20000 B² mu² and D0=320000 B² mu³. The ratio of both retuned parameters to the source's is (R/mu)²; the retuned choice is eventually smaller, but may be larger at finite sizes.

## Construction and exact bounds

Set d=min(m,D'), and let q be the least power of two with qd>=m. Set r=ceil(log2 d) for d>=2, else r=0, epsilon=1/(200 B R), delta=2 epsilon, c=ceil(d/(8B)) and h=ceil(delta d)-1. We first show r<=R. Let t=ceil(log2(B mu+2))>=2, so R=64+8t. As D'<2^19 B²R²mu, and B,mu<=Bmu+2<=2^t,

    r <= ceil(log2 D') <= 20 + 3t + 2 log2 R <= 32 + 5t <= R.

Here R=64+8t <= 2^(6+t). Since d<=D', the first inequality holds. The generous integer constants avoid relying on a hidden asymptotic threshold.

If q>1 then d=D', and qd<2m implies q<m because d>=2. Exactly as in PROOF.md, the rational potential with t0=epsilon/2 picks d shifts in polynomial time. Its final value cannot contain a bad character: epsilon²d/4=2mu and exp(2mu)>2^(mu+1)>2(q-1). Thus the nontrivial Walsh eigenvalues are at most epsilon d in absolute value. If q=1, every shift is zero and there are no nontrivial characters.

Use the local h-by-d field Vandermonde construction of PROOF.md. For h>0, h<delta d and r<=R, so rh<d/(100B)<=c. Thus its binary expansion fits the same c-row local budget and excludes all nonzero words of weight <delta d. For h=0 this distance condition is vacuous and no local row is needed. When q>1, the source's edge-mixing proof yields a nonzero Tanner word of weight at least delta(delta-epsilon) qd = qd/P' >= m/P'. For q=1, the same conclusion follows directly: every nonzero local word has weight at least delta d >= d/P'=m/P', since delta>=delta²/2=1/P'. Shorten the qd edges to m coordinates, preserving the lower bound.

The original row-count argument remains applicable: for q=1, 2c<=m/(4B)+2<=3n; for q>1, d=D'>=8B and 2qc<=(qd)/(2B)<m/B<=n. Each row has <=d<=D' entries. Eliminating zero rows gives at most 2qrh < m r/(25 B R) <=n/25, with h=0 yielding zero rows. The rational potential, finite-field construction, tensor of endpoint checks and shortening run in poly(n,m,B) time and space, with no numerical spectral test or random outcome.

## Dense-reduction composition and limits

The surviving violation supports now have size >=m/P'. Apply the credited PR #64 candidate distribution as composed in PR #51, replacing P by P'. It yields O(m²(P')²) candidate lists per round, at most 2P' entries per list, and 3n greedy rounds. All candidates, including those rejected by minimization, are sparse-polynomial instances with <=3n+n/25 equations and <=2^k max(D',2P') monomials per equation. With B=polylog(n), these quantities satisfy the source sparse-query interface uniformly; all graph setup, local-code work, degree arrays, entries, source sparsification branches, recovery, and oracle calls remain charged. Polynomial space follows by sequential processing. The fixed-density path is unchanged.

Both D' and 2P' remain polylogarithmic in n, so the source incidence encoding still uses O(n log log n) wires. The unchanged oracle and contraction envelope therefore remain 2^{O(n log log n / sqrt(log n))}; no improved alpha or full new asymptotic runtime is claimed. The stated improvement is narrower sparse rows and a stronger nonzero-kernel weight threshold, with smaller polynomial candidate and row-expansion parameters when R<mu. The cross-PR composition is conditional on those author-checked arguments and needs independent review.
