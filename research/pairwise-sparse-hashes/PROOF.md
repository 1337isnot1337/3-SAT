# Pairwise-independent indices for sparse random checks

This is an author-checked change to the extra randomized hash rows in
`research/characteristic-two-decision/PROOF.md`, Section 5. It does not alter
or audit the accepted OpenAI theorem, and no independent review is claimed.

## Construction and per-row guarantee

Let the original violation vector have m>=1 coordinates, and let P>=1 be an
integer. Assume a nonzero violation vector v has at least m/P nonzero
coordinates, as guaranteed for the surviving vectors by the predecessor's
initial sparse checks. Pad with zero coordinates to q=2^ceil(log2 m), so
m<=q<=2m. Set L=2P.

If L<=q, fix a representation of the field F_q and enumerate L distinct
field elements a_1,...,a_L. Sample A,B independently and uniformly in F_q;
let index I_i=A*a_i+B, interpreted as one of the q padded coordinates. Draw
independent uniform bits c_1,...,c_L. Output the binary row whose coefficient
at coordinate j is the parity of c_i over occurrences with I_i=j.

For distinct i,j, the linear map (A,B) -> (I_i,I_j) is invertible over F_q,
so all pairs of indices are uniform on F_q^2. This remains true when A=0,
where all sampled indices coincide; A=0 must not be discarded. Let X count
the sampled occurrences in the support of v, with repetitions counted.
Writing rho=|supp(v)|/q gives E[X]=L rho>=1. Pairwise independence gives

    E[X^2] = (E[X])^2 + L rho(1-rho) <= (E[X])^2 + E[X].

Cauchy--Schwarz applied to X and 1_{X>0} yields

    Pr[X>0] >= E[X]^2/E[X^2] >= E[X]/(E[X]+1) >= 1/2.

Conditional on the indices, the dot product of the row with v is the XOR of
c_i over the nonempty set of hitting occurrences. Since the c_i are mutually
independent and uniform, this parity is uniform. Repeated indices do not
invalidate this argument: the sampled occurrence bits are independent before
identical coordinates are combined. Thus Pr[row dot v=1]>=1/4.

If L>q, use every padded coordinate once, with one independent uniform
coefficient bit per coordinate. Since v is nonzero, the row dot v is uniform
and rejection probability is 1/2. This case uses q<L sampled coordinates.
For q=1 use this fallback; no field construction is needed.

The support of either output row has size at most 2P. Cancellation and padded
zeros cannot enlarge it. The first case uses exactly 2 log2 q + 2P unbiased
random bits, and the second uses q<2P. The predecessor's independent-index
construction uses 2P(log2 q+1) bits for each row. The new bound is
O(P+log m) instead of O(P log(m+1)) per row; when a parameter is bounded there
need not be an asymptotic reduction. This is not a reduction in row width.

## Uniform construction and all other costs

For q>=2 construct an irreducible polynomial of degree log2 q over F2
by enumerating monic candidates and testing divisibility by all monic
polynomials of degree at most half that degree. Standard existence of finite
fields gives termination. There are q candidates and O(sqrt(q)) trial
divisors, so the deterministic bit work is polynomial in q<=2m. Represent
field elements by their log2 q coefficient bits, and sample A,B directly;
no rejection sampling is required. Generating all L indices and combining
repetitions costs polynomial time and space. The explicit field construction
is performed once per leaf (or reused for equal q) and its polynomial cost is
charged; it does not depend on the fingerprint field.

Use independently seeded rows and the predecessor's unchanged count

    t_j = 8(n + ceil(log2(j+1)) + 1)

for leaf j. For each false assignment that survives the initial checks, its
violation vector meets the support promise; the chance it survives all rows
is at most (3/4)^t_j. The same union bound over at most 2^n assignments and
all sparsification leaves gives the predecessor's false-positive error below
1/32. True assignments always survive. The separate weighted-fingerprint
false-negative probability is at most 1/6, conditional on the hashes, with its
own independent field weights. Replacing the extra rows therefore preserves the
predecessor's error guarantee, including the fixed bit and worst-run budgets.

Each new row is a parity of at most 2P clause-violation polynomials. Its degree
and monomial-count envelope are unchanged. Charge the initial sparse checks,
sparsification leaves and branches, polynomial field setup, row expansion,
all degree arrays, entry work, tensor descriptions, modes, precision,
recursive contraction, recovery and fingerprint arithmetic exactly as in the
predecessor. Sequential execution retains polynomial space. The number of
fingerprint evaluations and the contraction wire budget do not decrease.
The complete general-density time remains
`poly(input) * 2^{O_k(n log log n / sqrt(log n))}` and the accepted
fixed-density fallback is unchanged. This result changes random-bit use, not
the time exponent, alpha, or the selected bound.

## Evidence and limits

The bounded verifier exhausts every support meeting the promised threshold
for padded universes of sizes 2, 4, and 8, including affine and whole-universe
fallback cases. It checks pairwise uniformity and the hit bound for each
support and seed, and separately exhausts coefficient hit patterns up to
length 8. These checks do not establish the all-size proof or implement the
accepted tensor contraction. The all-size argument and inherited wrapper need
independent review. A smaller seed, fewer coefficient bits, or fewer hash
rows would require a separately proved guarantee for every permitted support.
