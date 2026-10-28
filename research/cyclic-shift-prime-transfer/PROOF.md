# Deterministic good primes for cyclic rational conjugation

This conditional, author-checked argument extends the compact-certificate CRT
transfer in [PR #60](../deterministic-crt-transfer/PROOF.md). It has substantial
OpenAI Codex assistance, has not been independently reviewed, and proves no
better crossing rank or SAT exponent.

## A large, structured denominator

Let `N=2^lambda` and let `C` be the N-by-N cyclic upper shift:
`C[i,j]=1` when `j=i+1 mod N`. Then `C^N=I`. Define

```math
 B=2I-C,\qquad B^{-1}={\sum_{t=0}^{N-1}2^{N-1-t}C^t\over 2^N-1}.
```

The formula follows by telescoping `(2I-C) sum_t 2^(N-1-t) C^t`.
An inverse entry is exactly `1/(2^N-1)`, so its reduced denominator has N
bits. Entries and their exact rational representation are still computable in
`2^O(lambda)` bit operations. This is a cyclic shift, distinct from the
nilpotent shift used in PR #17. The large denominator alone does **not** prove
that a polynomial-bit integer covering all its prime divisors cannot exist.

Conjugate any rational crossing pieces by B on the x axis and its inverse on
the opposite v axis, exactly as in PR #17. The crossing sum and normalizer are
unchanged since `BB^-1=I`. Each required flattening is multiplied by invertible
matrices on its separate row and column axes, preserving both rational ranks.
Uniform generation remains `2^O(lambda)` bit time. Thus this is a new allowed
coefficient family, not an improved piece rate.

## A single progression avoids every cyclic denominator

For any prime `p = 7 mod 8`, the supplementary quadratic reciprocity law says
`(2/p)=1`. Euler's criterion gives `2^((p-1)/2)=1 mod p`. As `(p-1)/2` is
odd, the multiplicative order of 2 modulo p is odd; it exceeds one because
`2` is not congruent to 1 modulo p. Hence it cannot divide any power of 2.
Consequently

```math
 p does not divide 2^(2^lambda)-1, for every integer lambda >= 0.
```

The conclusion holds simultaneously for *every* lambda; no large denominator
or product of them is computed or factored during prime selection. It also
applies to any products and powers of such factors, provided the overall
rational entry-generation contract remains within `2^O(lambda)` bit time.

## An explicit deterministic supply

Let `D(S)` cover the odd bad primes from the **base** pieces and their
normalizers through call-size cap S as in PR #60; its bit length `Q` is
polynomial in input size. The new cyclic denominator factors need not be
included in D. Let B bound all signed original integer query magnitudes by
`2^B`, and set `K=B+2+Q`. Sieve all primes `p <= X` in the progression
`p = 7 mod 8`, where

```math
 X = max(8,000,000,000, 256(K+1)^2).
```

Bennett, Martin, O'Bryant and Rechnitzer's explicit published estimate,
quoted in [SOURCES.json](SOURCES.json), implies for `X>=8*10^9` that
`theta(X;8,7) > X/5`. Each counted prime contributes at most `log X`, so
there are more than `X/(5 log X) >= sqrt(X)/5 > K` such primes. Here
`log X <= sqrt X` for X>=4. At most Q primes divide D, so after deterministic
remainder tests at least `B+2` primes remain. Their product is greater than
`2^(B+1)`. The sieve limit and all arithmetic costs are polynomial in B and Q.
The explicit threshold has a very large constant: this establishes an
asymptotic uniform algorithm, not a practical recommendation. The finite
checker uses small primes and does not run the threshold-sized sieve.

CRT-recover the balanced signed integer at each original query boundary before
any outer greedy comparison or modulo-two operation. Run the complete inner
field recursion independently for each selected prime; do not mix fields.
All base denominators, cyclic denominators and normalizers are invertible.
The compact certificate and source rank/recurrence contracts are assumptions,
and the same exact-recovery and cost proof as PR #60 applies. A polynomial
number of field runs and CRT leave the master time envelope unchanged, while
matrix storage remains exponential in lambda. Exact counting and decision
are deterministic under the stated hypotheses, with no amplification. This
is not a polynomial-space guarantee and does not establish a smaller rho.

## Actual construction, control and limit

The predecessor's symmetric and three-bit macro adapted-basis families have
polynomially computable common denominators per length. Their cyclic
conjugates therefore fit the structured condition even though their raw
inverse denominators have exponentially many bits in lambda. Their existing
symmetry obstacles and rank limitations still apply. The exact checker builds
the six-class R=1 pieces, verifies the full crossing sum and both field
factorizations over five progression primes, and recovers all 256 predicate
counts. The finite check is not a proof of the master algorithm or an
asymptotic rank bound.

The general PR #17 rational-generation contract does not require the base
certificate or the cyclic denominator form; this does not derandomize that
full contract. For a genuinely cheaper crossing family one must prove the
crossing identity, two simultaneous rate bounds, uniform generation and an
appropriate good-prime supply, and charge the full outer reduction.

## Extension to a fixed finite set of integer bases

The same mechanism covers every fixed finite collection of integers
`a_1,...,a_t >= 2`. Set `q=8 lcm(a_1,...,a_t)` and take primes
`p = -1 mod q`. Such p is 7 modulo 8 and is greater than every `a_j+1`.
For each odd prime factor ell of any a_j, quadratic reciprocity gives

```math
 (ell/p) = (p/ell) (-1)^((ell-1)/2) = 1,
```

since `p=-1 mod ell` and `p=3 mod 4`. Also `(2/p)=1` because `p=7 mod 8`.
Thus each `(a_j/p)=1`, so Euler's criterion shows that the multiplicative
order of a_j modulo p divides the odd number `(p-1)/2`. It exceeds one
because `1<a_j<p-1`. Therefore no such prime divides any
`a_j^(2^lambda)-1`. The conjugation is

```math
 (a_j I-C)^-1 = (a_j^(2^lambda)-1)^-1
                 sum_(r=0)^(2^lambda-1) a_j^(2^lambda-1-r) C^r.
```

For this explicit version assume the **fixed** modulus `q<=100000`, so the
same cited progression estimate applies. For `K=B+2+Q` choose

```math
 X = max(8*10^9, 2^(2q), [4q(K+1)]^2).
```

The explicit error bound implies `theta(X;q,q-1)>X/(2 phi(q))`: indeed
`log X >= 2q log 2`, making `1/(160 log X) < 1/(2q) <= 1/(2 phi(q))`.
There are therefore more than `X/(2q log X) >= sqrt(X)/(2q) >= 2(K+1)`
primes in this progression. Sieve and remove the at most Q base-bad primes
as before. Because q is fixed, the threshold `2^(2q)` is an enormous
constant, and X is polynomial in B and Q. This does **not** give polynomial
time uniform in a growing modulus or a growing list of arbitrary bases.

Uniformly generated compositions of such conjugations fit if their entry
bit-time remains `2^O(lambda)` and every base-family denominator and
normalizer is covered by D(S). The finite replay now uses base 3 on the
actual six-class crossing, as well as independent modular controls for six
finite base sets. The result does not prove that their raw large denominators
lack compact radical certificates, nor does it improve their rank profiles.
