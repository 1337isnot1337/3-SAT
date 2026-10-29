# A conditional sparsification/width cost law

## Cost model, not a lower bound

Fix constants a,b,beta>0 and c>=0. For lambda>1 and a continuous sparsification parameter 0<sigma<=1, consider the explicit modeled exponent per variable

    E_lambda(sigma) = a sigma + (b/sqrt(lambda)) [c log(lambda) + beta (L + log L)],
    L = log(2/sigma).

Logs here are natural. This is a named bookkeeping envelope: the first term models a source-style 2^{O(sigma n)} sparsification tree; L+log L models the logarithm of sigma^{-1} log(2/sigma), the basic density factor in the source sparsification guarantee; c log(lambda) models a separately charged polynomial-in-lambda width factor. Coefficients are positive fixed hypothetical cost coefficients, not numerical values recovered from unspecified O-notation. The source's density guarantee is an upper bound, and E is not a lower bound on actual leaf density, contraction time, or any SAT algorithm. It also omits any term not explicitly modeled here; actual entry evaluation, branches, field construction and recovery must be charged before asserting a runtime.

## Exact optimizer and asymptotics

For sufficiently large lambda, E has a unique minimizer in (0,1). Its derivative is

    E' = a - (b beta)/(sigma sqrt(lambda)) (1 + 1/L).

Since L>=log 2 > (sqrt(5)-1)/2,

    E'' = (b beta)/(sigma² sqrt(lambda)) (1 + 1/L - 1/L²) > 0.

The derivative tends to negative infinity as sigma->0 and is positive at sigma=1 for sufficiently large lambda, giving the unique root. At that root,

    sigma sqrt(lambda) = (b beta/a)(1 + 1/L).

Since L>=log 2, the right side is bounded above and below by positive constants; therefore sigma=Theta(lambda^-1/2), L=(1/2) log(lambda)+O(1), and 1/L=O(1/log lambda). Consequently

    sigma = (b beta)/(a sqrt(lambda)) (1 + O(1/log lambda)),
    min E = (b/sqrt(lambda)) [(c+beta/2) log(lambda)
                              + beta log log(lambda) + O(1)].

The constants in O(1) depend only on a,b,beta,c. This is a precise optimum of this model. In particular no alternative sigma can reduce this *modeled* quantity to O(lambda^-1/2-epsilon) for any fixed epsilon>0. It does not exclude a sharper density theorem, fewer actual branches, another encoding, more efficient contraction, cancellations, or formula-dependent preprocessing.

## Relation to the repository construction

The accepted sparsification source uses B=O_k((sigma^-1 log(2/sigma))^(k-1)). If one charges a proxy width W=B² lambda times polylogarithmic factors and a contraction envelope proportional to n log W/sqrt(lambda), its main log W terms have the form above with beta=2(k-1) and c=1, after choosing a particular numerical upper-cost model. PR #78 offers retuned checks with D'=320000 B² R² mu and R=O(log(B mu)); with mu=Theta(lambda) this has that proxy form up to lower-order log R terms. These are interface upper bounds; no assumption says every leaf attains them. The source's precise theorem uses constants depending on fixed polylogarithmic width exponents, and changing sigma with lambda requires rechecking those uniformity conditions. The argument here does not claim an executable improved algorithm.

The complete source algorithm includes the fixed-density branch, sparsification tree, initial matrix, every discarded and selected greedy query, high-degree variable branches, degree arrays, tensor descriptions and entry procedures, recursion, precision, recovery and polynomial-space scheduling. A model optimum leaves all those implementation obligations open. The preprocessing reductions in PRs #51/#78 concern two of these terms and do not imply that the model is an exact running time.
