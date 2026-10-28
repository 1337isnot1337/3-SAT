# Sparse-code isolation for parity-only decision

This is an author-checked construction, not an independently reviewed proof or
an implemented SAT solver. The owner-accepted OpenAI theorem and the written
predecessor decision wrapper are premises. No faster SAT bound is claimed.

## 1. Systematic sparse-check encoding

For n>=1, apply the accepted `lem:sparse-checks` with its parameters
`m=8n`, `B=8`, and its n parameter equal to the input variable count. It
constructs a binary matrix A with N=8n columns, at most 3n rows, row weight at
most D0=320000*8^2*mu^3, and kernel distance at least N/P, where

    mu=floor(log2 N)+1,    P=20000*8^2*mu^2.

The kernel has dimension d>=5n. Compute a kernel basis by Gaussian elimination,
then select d coordinates on which the coordinate projection is invertible;
this is an information set. Designate n of these coordinates for the original
input variables, and set the remaining d-n information coordinates to zero.
Together with A z=0, these unary equations yield exactly one z in {0,1}^N
for every original assignment. Distinct assignments yield codewords at Hamming
distance at least N/P. Each constraint remains a parity equation with at most
max(D0,1)=polylog(n) monomials, and there are O(n) constraints and N=O(n)
variables. The information-set computation does not replace sparse checks by
potentially dense generator equations.

The accepted lemma constructs A deterministically in exp(poly(log(n+2)))
time and polynomial space here, since B=8. Gaussian elimination and all
coordinate choices take polynomial time and space. This preprocessing is
subsumed by the target exponential envelope for all sufficiently large n;
handle the finite exceptional range by exhaustive search.

## 2. Sparse near-pairwise-independent hashes

Set R=2^ceil(log2 N), so N<=R<2N, and pad each codeword by R-N zero bits.
A random hash row samples K=8P ceil(log2(2n)) independent uniform coordinates
of [R], each with an independent uniform coefficient bit; its parity is the
sum of the sampled coefficient times the sampled code bit. Repeated positions
are combined modulo 2. All indices and coefficient bits use a fixed, bounded
number of random bits, because R is a power of two.

For distinct encoded assignments z,z', the difference has at least N/P
nonzero positions, hence the chance a sampled padded position differs is
at least 1/(2P). The expected sign of one coefficient-weighted sampled
difference is at most 1-1/(2P), so the collision probability of one row is

    (1 + (1-w/R)^K)/2 <= (1+eta)/2,
    eta=(2n)^(-4),

where w is the difference weight. Independent rows yield collision probability
at most `((1+eta)/2)^t`. Each row has at most K=polylog(n) nonzero terms.

## 3. Isolation

Let U be any nonempty set of at most 2^n encoded assignments and let S=|U|.
For t=ceil(log2(2S)), choose t independent rows as above and an independent
uniform target b in {0,1}^t. Each z in U maps to b with probability 2^-t.
For distinct z,z', their joint probability of mapping to b is at most
`2^-t ((1+eta)/2)^t`, since b is independent and uniform. Let X be the
number mapping to b. Then

    Pr[X=1] >= E X - E[X(X-1)]
      >= (S/2^t) * (1 - (S-1)((1+eta)/2)^t).

Here `1/4 < S/2^t <= 1/2`, t<=n+1, and
`(1+eta)^t <= exp((n+1)/(2n)^4) < 3/2`. Therefore
`Pr[X=1] >= 1/16`. The same bound holds for any U independently of how it
was selected before these hash bits were drawn. The algorithm need not know S:
try every t=1,...,n+1. At the relevant t, 64 independent trials miss unique
isolation with probability at most `(15/16)^64 < 1/50`.

Each trial appends t sparse affine parity equations to the original system.
If exactly one assignment survives, the unweighted number of solutions is
odd. Consequently an exact parity evaluator detects that trial; it may also
accept when more than one but an odd number survive.

## 4. Composition and all costs

Use the predecessor `characteristic-two-decision/PROOF.md` Section 5's
sparsification and sparse-hash wrapper for the original k-CNF. Its random
clause-violation hashes have a joint good event of probability at least 31/32
on which no non-satisfying assignment survives in any leaf; every true leaf
solution always survives. Encode the original n assignment bits using Section
1, append the Section 3 isolation equations for all t and trials, and evaluate
the parity of each resulting system using the predecessor's
constraint-parameter evaluator over F2 with every assignment weight set to 1.
The parity evaluator must retain every declared variable: an unconstrained
variable contributes the factor 1+1=0, including one that becomes unconstrained
after branching. Equivalently, return zero for that branch; do not apply the
predecessor's decision-only convention of discarding free variables. This
preserves the exact parity and its polynomial cost. Accept if any parity is odd.

For an unsatisfiable input, acceptance requires a false assignment to survive
some original clause-violation hash, so its probability is at most 1/32. For
a satisfiable input, fix a satisfiable leaf independently of all randomness.
On the good event its survivor set is nonempty and consists of genuine leaf
solutions. Given that set, the independent isolation trials fail with
probability at most 1/50. Thus false-negative probability is at most
`1/32+1/50 < 1/10`. A bad clause-hash outcome may introduce survivors; the
argument does not assume isolation repairs that event. Random hash bits, all
trials, and any early exit have bounded worst-outcome time.

The code adds O(n) variables, O(n) parity equations with polylogarithmic
monomial counts, and polynomial-size descriptions. Each trial adds at most
n+1 affine equations with K=polylog(n) monomials. Together with the original
wrapper's O(n) equations and polylogarithmic monomial count, pad its evaluator
parameter a to Theta(n) and T to the maximum polylogarithmic size. Eventually
T<=a^(1/10), and the finite exceptional range is handled by the same explicit
exhaustive fallback. The predecessor evaluator gives

    poly(input) * 2^O_k(n log log n / sqrt(log n))

bit operations and polynomial space for each trial. The polynomial number of
trials, deterministic code construction, sparse hashing, high-incidence
branches, degree arrays, entry computation, recursive contraction, precision,
recovery and sparsification are included in the same envelope, with the
predecessor's space-preserving sequential traversal. Fixed density may use the
accepted deterministic counter and its sharper O(n/sqrt(log n)) exponent.

This removes the *separate random field fingerprint* from the predecessor
wrapper for all inputs, but uses additional random sparse isolation hashes.
It is not a derandomization, a reduction in overall random bits, an improvement
of the selected alpha, or a practical implementation. The accepted deterministic
counter already has the stated general and fixed-density envelopes. Both this
composition and the predecessor's all-size evaluator require independent
review; finite checks do not constitute that review.
