# Deterministic sparse-support fingerprint detection

This is an author-checked interface result, not an independently reviewed SAT
bound. All fields below have characteristic two. Let n>=1 and S>=1.

## Theorem

Given black-box evaluations of an n-variate multilinear polynomial

    Z(R) = sum_{x in A} product_{i:x_i=1} R_i,

where A is an unknown subset of {0,1}^n with |A|<=S, one can decide whether
A is empty deterministically using poly(n,S) evaluations over binary fields
with O(log(nS)) bits per element and poly(n,S) additional bit operations and
space. If |A|>S the procedure can return false negative, but never false
positive. In particular it applies to the solution fingerprint of a Boolean
formula under the stated solution-count promise.

Index bits i=0,...,n-1, and let E(x)=sum_i x_i 2^i. Put L=n(S-1)+1 and let
p range over the first L primes. All primes used are at most 8L^2: for
m=4L^2, the central binomial coefficient satisfies binom(2m,m)>=2^m.
Each prime power dividing it is at most 2m, because each term in Legendre's
factorial valuation difference is either zero or one. Thus
(2m)^pi(2m)>=2^m, so pi(2m)>=m/log2(2m)>=L. Trial division and enumeration
therefore take polynomial time in L.

For each such p form the formal polynomial

    H_p(T)=Z(T^(2^0 mod p), ..., T^(2^(n-1) mod p)).

Its degree is at most d=n(p-1). Choose a binary field F_q with q>=d+1,
represented by an irreducible polynomial of degree e=ceil(log2(d+1)), with
e>=1. A field of that degree exists. Enumerating all 2^e monic candidates
and testing divisibility by every monic polynomial through degree e/2 takes
polynomial time in q, hence poly(n,S), as q<=2(d+1) except the harmless
minimum e=1. Evaluate H_p at d+1 distinct field elements by calling the
fingerprint oracle on the indicated n weights. Interpolate over F_q to obtain
its coefficients. They are 0 or 1 in F_q; reduce the recovered polynomial
modulo T^p-1. Accept if any remainder is nonzero, otherwise reject.

If A is empty every oracle answer and remainder is zero. Suppose instead that
1<=|A|<=S. Choose x in A. All integers E(x)-E(y), y in A\{x}, are nonzero
and have absolute value less than 2^n. Their product has at most
n(|A|-1) prime factors counting multiplicity, and therefore fewer than L
distinct prime divisors. Some one of the first L primes divides none of these
differences. For that p, E(x) has a residue distinct from all other E(y).
Since the exponent in H_p for y is congruent to E(y) modulo p, its reduced
coefficient at E(x) mod p is exactly 1. The algorithm accepts. ∎

The number of oracle calls is at most

    sum_p (n(p-1)+1) <= L(8nL^2+1).

Each field has q=O(nL^2), so e=O(log(nS)); arithmetic and ordinary exact
interpolation are polynomial. Process primes and field points sequentially.
The result also handles the empty support and S=1 without special hypotheses.
The field size is part of the oracle interface; evaluations over fields smaller
than d+1 alone do not justify the interpolation step.

## Fixed-density promised application

Take a k-CNF with m<=Dn for fixed k,D, and suppose it has either zero or at
most S<=n^c satisfying assignments for a fixed c. Clause violation is a
Boolean polynomial of degree at most k and at most 2^k monomials; satisfying
assignments are the common zeros. Use the constraint-parameter weighted
fingerprint evaluator in `research/characteristic-two-decision/PROOF.md`,
Sections 2-4, with a padded to at least n and at most max(n,m), and constant
T=2^k. The choice of evaluation fields above has e=O(log n), hence its
truncated-polynomial embedding still has ell=O(a^(1/4) log n)=O(a), and
its entries, descriptions, decoding and field construction have polynomial
cost. Unused variables can be discarded for decision, and discarding them
cannot increase the number of solutions. Small parameter exceptions use the
predecessor's explicit finite fallback.

For fixed k,D,c, the polynomially many calls give a deterministic promised
algorithm with polynomial space and time

    poly(input) * 2^O_{k,D,c}(n/sqrt(log n)).

This application is conditional on the written, not independently reviewed,
predecessor evaluator and the owner-accepted contraction theorem. It is not
a better bound: the accepted exact-counting algorithm already works
without a solution-count promise in the same envelope. The fingerprint test
cannot be inserted into the general-density sparse-hash wrapper merely from a
promise on the original formula, since a hash system may retain additional
non-solutions and violate the support bound. All sparsification, hash,
reduction, recursion, precision, entries and space costs must be paid for any
new unrestricted use. No such use or alpha improvement is claimed here.

## Reopening questions

Can a sparse-support guarantee be certified or enforced for actual hash
queries without paying for isolation or introducing a false-negative promise?
Can structured source equations yield a comparable deterministic test with
support exponential in n but substantially fewer than poly(S) calls? The
present proof alone answers neither question.
