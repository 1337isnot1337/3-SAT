# Deterministic CRT transfer with a compact bad-prime certificate

This is an author-checked, AI-assisted conditional interface result. It
modifies the randomized rational-rank transfer of PR #17; it does not prove a
better crossing rank or SAT exponent. The complete master implementation is
not provided, and the all-size argument has not been independently reviewed.

## Statement and certificate

Take the exact uniform rational crossing-family and two rank-envelope
hypotheses of [PR #17](../odd-prime-rank-transfer/PROOF.md), including its
call-size cap `S`, root-query bit bound `B`, and the source master recurrence.
Thus every original integer network query obeys `|Z| <= 2^B`, including all
rejected candidates and intermediate profiles, with `B,S` polynomial in the
input size after the same fixed-width normalization.

Add this **compact bad-prime certificate**: a positive integer `D(S)`,
computable in polynomial time in the normalized input size, has polynomial bit
length, and for every `1 <= lambda <= S` every odd prime dividing any entry
denominator, the normalizer denominator, or the nonzero normalizer numerator
also divides `D(S)`. It is enough to give a uniform polynomial-time procedure
for a polynomial-bit per-length certificate and multiply these up to S. The
certificate is an arithmetic theorem about the family, not merely a list of
observed denominators. It need not be factored.

Under these conditions the PR #17 transfer becomes deterministic, returns the
exact integer on each query and hence the exact count and decision answer,
and has the same stated master time envelope up to polynomial factors. It
retains exponential-in-lambda matrix storage; it does not establish polynomial
space. No new rank bound follows from the certificate.

## Deterministic prime supply

Let `Q=bit_length(D)` and `K=B+2+Q`. Put
`T=8+2 ceil(log2(K+1))`. The explicit dyadic prime lower bound cited and
proved from Rosser--Schoenfeld in PR #17 gives more than `2^T/(2T)` primes
in `[2^T,2^(T+1))`, which exceeds K for every positive integer K. Put `a=ceil(log2(K+1))`. Since `a <= K+1` and `2^a >= K+1`,
`2^T/(2T) >= 128(K+1)^2/(10+2K) > K`.

Sieve all integers through `2^(T+1)-1`, retain the primes in that interval,
and discard divisors of D using ordinary remainder arithmetic. At most Q
primes divide D, since each contributes at least one bit to its product.
At least `B+2` remain. Keep exactly that many. The sieve limit is
`O((K+1)^2)` and its bit space and time are polynomial in B and Q. In
particular no factorization of D, unbounded search, randomized step, or
unknown prime-gap assumption is involved. The finite checker uses a smaller
trial-division enumeration for convenience; it does not implement this sieve.

The chosen primes are distinct, odd, and good for every possible call length.
Their product P is greater than `2^(B+1)` because each exceeds 2 and there
are `B+2` of them. This deliberately simple count is polynomial even when it
is far from optimal. A checker must reject an insufficient product, not
silently reconstruct an ambiguous signed value.

## Contract each query separately, then recover the integer

For each prime independently, reduce and compile the rational crossing pieces
and perform the PR #17 field recursion. Because all rational denominators and
normalizers are units, the identities and both rational rank upper bounds
specialize to the field. The factors need not be the same across primes.
Never mix factors across fields within a single recursion. Reduce the original
integer tensors modulo each prime, execute the entire field contraction, and
collect the residue of the *original query*. By CRT there is one integer in
`(-P/2,P/2)` matching all residues, namely Z. Recover that balanced integer
before the next outer comparison or any sum or reduction modulo a power of two.

This boundary matters: directly reducing a field residue modulo a power of two
is invalid, and the final SAT count's bound need not bound intermediate queries.
All fields use the same fixed prime inventory, so adaptive outer queries do not
need a union bound. Unexpected division by zero signals a violated certificate;
it is an implementation error, not a randomized NO answer. The algorithm and
its deterministic correctness rely on the certificate being proved.

## Time and space

Prime selection and CRT use polynomial time and memory in the input and
query-bound bits. Each query executes at most `B+2` independent field
contractions, a polynomial multiplier. Each field element has `O(log(B+Q))`
bits; rational entry generation, two rank factorizations, description growth,
recursive grouping, crossing branches, and leaf costs are charged exactly as
in PR #17. The original outer reduction, all its candidates, branches, profiles,
and exact integer recovery remain charged. The source's `2^O(lambda)` compiler
term absorbs the per-field matrix work; the polynomial number of field runs
and CRT do not change its exponent. Standard small-input direct fallbacks are
unchanged. Counting and decision are deterministic, with no amplification.

This is conditional on the same full recurrence assumptions as PR #17 and the
new certificate, not a standalone implementation or an improvement to the
owner-accepted alpha 1/2. Field compilers store matrices exponential in lambda;
we claim only time-bounded space, not the selected theorem's polynomial space.

## The nilpotent conjugation example

For `N=2^lambda`, PR #17 uses `B_lambda=2I-S_N` with the **nilpotent** upper
shift and inverse entries `2^-(j-i+1)` for `j>=i`. Suppose a base crossing
family has normalizer 1 and all entry denominators divide `2^e D_lambda`,
where `D_lambda` has polynomial bit length and can be computed in polynomial
time in lambda. Conjugating on the opposite crossing axes introduces only
powers of 2 in denominators. Multiplication, summation, and cancellation
cannot introduce an odd prime outside `D_lambda`. The crossing normalizer
remains 1 and both rational flattening ranks are preserved by invertible
row/column transformations. Therefore `D(S)=product_(lambda<=S) D_lambda`
is a polynomial-bit certificate computable in polynomial time, provided the
per-length uniform hypotheses hold.

In particular, the prior symmetric and three-bit macro constructions specify
polynomial-size rational adapted-basis data and a polynomial-bit common
denominator. Their exact coefficient matrices and denominator are uniformly
computable in polynomial time in the macro count; their Pauli formula adds
only a power-of-two denominator. Padding string lengths by at most two bits
retains the certificate. Thus their nilpotently conjugated families satisfy
this compact-prime condition, whether or not their rank envelopes meet the
master's required rho. The existing symmetry barriers and missing/impossible
rate conditions still apply. The checker uses the six-class R=1 family; that
finite example does not prove the general certificate or a new rank.

## Boundaries and next step

A rational family with arbitrary `2^O(lambda)`-bit denominators need not
provide a polynomial-bit certificate. PR #17 remains more general and
randomized; this result does not derandomize all its families. A useful next
step is to construct an actual improved-rho family with such a certificate or
prove a different efficient deterministic good-prime selection mechanism. Do
not infer either from the conjugated example or from finite CRT checks.
