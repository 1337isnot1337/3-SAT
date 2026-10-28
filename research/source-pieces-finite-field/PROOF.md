# Reducing the source crossing pieces modulo a prime

Source: Anthropic, *A 2^{o(n)} Time Algorithm for 3-SAT*, Appendix B,
Lemma 9, Lemma 10, equations (47), (48), (53)-(55), pinned in
`research/recent-breakthrough-scan/SOURCES.json`. This is an author-checked
component transfer of the source's actual integer construction. It does not
change the accepted OpenAI theorem or claim a new SAT running time.

Fix h>=2 and let p be a prime. The source constructs integer operators and
pieces `A_s`, with s=-2h,...,2h, a set of labels indexed by partitions of h,
and the exact integer identity

    sum_s A_s(x,y,u,v) = h! [x=v][y=u].                         (1)

It gives both directional integer factorizations (54)-(55) with inner
lengths `sum_{i=0}^{2h} P(s+i)` and
`sum_{i=0}^{2h} P(2h-s-i)`. All source coefficients are integers: (47)
uses integer-valued generalized binomial coefficients, (48) uses integer
binomial coefficients, and `h!/z_mu` is integral. The source identities
hold on integer basis inputs; reducing them and each factor entry modulo p
therefore gives the same identities over F_p. In particular, the two
factorization lengths and their bit-cost upper bounds cannot increase under
reduction. This is an upper bound; a modular rank drop is not asserted.

The source's exact normalizer `h!` is nonzero in F_p **if and only if
p>h**. In this case multiplying a piece by `(h!)^-1` gives a valid
normalized finite-field crossing decomposition, with both source directional
length bounds preserved. The source's Lemma 10 pairing reduces to an
invertible diagonal `h! I` on all partition labels. If p<=h, the sum in (1)
is identically zero over F_p, including at inputs where both equalities hold;
no scalar rescaling of these same pieces can turn that sum into equality.
This does not exclude a different decomposition or a different normalizer.

A suitable p exists in `(h,2h)` for h>=2 by Bertrand's theorem; deterministic
trial division of successive integers constructs one in time polynomial in
h. The source chooses the least h with P(h)>=2^lambda, and its stated
partition growth implies h=Theta(lambda^2) for large lambda. Thus this
field has O(log lambda) bits and can be selected in polynomial time in
lambda. Compute original integer piece and factor entries by the source's
algorithm and reduce modulo p; this inherits the source's uniform bounds,
with modular normalization charged explicitly. The relevant grade spaces
can reach 2h, but no extra p>2h condition is needed for this integer
reduction: all equations and both factorizations are reduced from integer
identities, without division by intermediate factorials.

## Limits

This is a local field-valued crossing component, not a deterministic SAT
algorithm. A zero residue of an integer count does not imply a zero count;
reconstructing exact integer queries or proving a one-sided randomized
fingerprint guarantee is a separate obligation. The existing
merged `research/odd-prime-rank-transfer` package and open deterministic CRT
transfer PR #60 treat related transfer/recovery questions; this package does not
assert their hypotheses or reprove them. A complete application must account
for source entries, normalizers, prime selection and count height, every
reduction branch and query, recursion, reconstruction or amplification,
space and worst-outcome time. No improvement in rho or alpha follows from
this local reduction alone.

## A restricted codebook when p<=h

The failure above applies to the source's **common** h! normalization, not
to every partition label. The source proof of Lemma 10 first establishes the
unscaled integral identity

    a_mu[-h] t_nu = z_mu [mu=nu],
    z_mu = product_{k>=1} k^(m_k) m_k!,                       (2)

where m_k is the multiplicity of part k in mu. Define C_{h,p} to consist of
partitions of h for which no part is divisible by p and all multiplicities
are less than p. Exactly for these labels, p does not divide z_mu. Over F_p
set `b_mu = z_mu^(-1) t_mu` for mu in C_{h,p}, retaining the source a_mu.
Reducing (2) yields `a_mu[-h] b_nu = [mu=nu]` for every pair of labels in
C_{h,p}. The source's operator-order and summed identities apply by the same
integer reduction and linearity, so the source piece definition with these
modified label vectors has a normalized equality sum on this restricted
codebook. Both directional factorization-length upper bounds remain those of
the full grade spaces; the modified b entries and z inverses must be charged.

This works for every prime p and every h with a nonempty codebook, including
p<=h. Its cardinality is the grade-h dimension of the vacuum-pairing quotient
studied in `research/weighted-oscillator-rigidity/PROOF.md`. That package gives
`log |C_{h,p}|=Theta(sqrt(h))` uniformly in primes for h>=256, but does not
supply the sharp constants needed to compare the full two-direction source
cost with the original crossing ratio. In particular, smaller fields and an
exponentially large restricted codebook do not by themselves yield a better
SAT exponent. The next section supplies a uniform binary label map and its entry costs.
No full contraction is established.

## Uniform binary indexing of the restricted codebook

A binary label set can be selected uniformly without enumerating all
partitions. For `0<=k,t<=h`, let F(k,t) count admissible partitions of t
using parts at most k. Set F(0,0)=1 and F(0,t)=0 for t>0. For k>=1,

    F(k,t) = sum_{m=0}^{M(k,t)} F(k-1,t-mk),
    M(k,t) = min(p-1,floor(t/k)) if p does not divide k, else 0.

This table counts exactly the codebook, and ascending multiplicity blocks
provide deterministic ranking and unranking: at each k from h down to 1,
subtract block counts until the desired multiplicity is selected. There are
O(h^2) entries and at most O(h) summands per entry; counts have O(h) bits,
since all partitions of t inject into its compositions. Construction,
rank, unrank and computing `z_mu` modulo p and its inverse are polynomial in
h and log p. For n>=256 the preceding predecessor's padding bound gives
`log2 |C_{n,p}| >= floor(sqrt(n/2))/2`, uniformly in p. Taking
`h=max(256, 8(lambda+1)^2)` therefore provides at least 2^lambda labels;
choose the first 2^lambda in the described order. This defines the label map
and its inverses uniformly in polynomial time in lambda and log p. The
source's factor-entry computation and these label costs are thus explicit
at the local crossing interface. Exact global SAT-query recovery remains
outside the result.

## What the uncompressed source factors certify at p=2

For p=2, C_{h,2} consists of partitions into distinct odd parts. Let c_h be
its size. With `q=exp(-t)` and t>0,

    c_h <= exp(t h) product_{j>=0} (1+exp(-t(2j+1)))
        <= exp(t h + pi^2/(24t)).

The second inequality follows by applying the midpoint inequality to the
convex function `f(x)=log(1+exp(-x))` on intervals of width 2t, and using
`integral_0^infinity f(x) dx = pi^2/12`. Optimizing t gives
`log c_h <= pi sqrt(h/6)`. Consequently selecting 2^lambda labels requires
`h >= 6 (lambda ln 2)^2 / pi^2`.

At shift s=0, each of the source's **listed**, uncompressed two-direction
factor lengths is `sum_{i=0}^{2h} P(i)`, hence at least P(2h). The source's
partition asymptotic and monotonicity imply that their combined bit lengths
are at least `4 sqrt(2) lambda - O(log lambda)` for any such h. Therefore
these particular length certificates cannot satisfy a crossing budget
`4 rho lambda + O(log lambda)` with rho<1; in fact their asymptotic
coefficient requires rho>=sqrt(2). This does not lower-bound the actual
field ranks or rule out a different factorization, cancellation, other
codebooks, or another contraction. It explains why the local p=2 codebook
alone is not an improved SAT algorithm.
