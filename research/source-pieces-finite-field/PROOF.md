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
