# Registered question and stopping contract

Base: `6245ff589cdd461c75114308f4571af45dfb809d`, which merges PR 16.
Check live main/branches/PRs again before submission. No overlap was found
with charged moments (PR 11), docs (PR 12), or the advertised empty
aggregate-packing branch. Frozen sources and selected alpha remain unchanged.

Question: do uniform rational crossing pieces with proved two-direction
rational rank bounds suffice for a bounded randomized master transfer,
without polynomial-height integer factors or a polynomial-height rational
normalizer? The mechanism is a large odd prime, exact bounded integer query
recovery, and the existing outer reduction retained over the integers.

The intended theorem assumes polynomial piece count; every rational piece
entry, rank bound and nonzero rational normalizer is computable exactly in
`2^O(lambda)` bit time. This already bounds all output numerator/denominator
bit lengths by `2^O(lambda)`. The full finite collection of piece entries
has at most exponentially many bad denominator bits. All call lengths are
at most a polynomial S in the original input size, from the source's master
size recurrence and PR 16's ledger.

For every lambda<=S, include denominator primes and normalizer numerator
primes. Their total logarithmic product height is at most `2^O(S)`. A
uniform prime from a dyadic interval with O(S) or more bits should avoid
all of them with constant success probability. Include enough bits to
exceed twice the absolute value bound of EVERY original integer network
query. The signed bound `2^(edge_bits+sum tensor_bound_bits)` is sufficient.
Then recover the exact signed integer query before any greedy comparison,
truncation modulo two powers, or summation in the outer reduction.

Finite registered checks: field factorization on small rational matrices;
all primes in dyadic intervals with T=8,...,16 for the density lower bound;
capped prime failure and first-prime controls; signed integer recovery;
an actual N=8 crossing/count construction conjugated by the bidiagonal
matrix `2I-S_N` and its inverse, which preserves both flattening ranks but
introduces denominators `2^Theta(N)`; bad-prime rejection. Do not claim a
complete SAT solver, AKS implementation, independent review or smaller rho.

Success: a complete source-pinned transfer with per-fixed-input success
at least 2/3, time bounded on EVERY random outcome, charged bit arithmetic,
all bad denominators across adaptive queries, and explicit space cost.
The evidence must include a separately checkable bounded crossing test.
Stop if the global prime bit size ceases to be polynomial, the rational
piece generation costs more than `2^O(lambda)`, or the outer exact integer
query bounds cannot be supplied. Never run the outer modulo-two truncation
directly in odd characteristic.

All work is substantially Codex-assisted. A transfer is only a sufficient
interface: a cheaper rank family is still needed for an SAT improvement.
