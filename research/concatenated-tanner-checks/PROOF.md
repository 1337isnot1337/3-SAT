# Constant-distance local codes for sparse Tanner checks

This is an author-checked component argument, not independent review or an
implemented SAT solver. The owner-accepted OpenAI `lem:sparse-checks` supplies
the Tanner graph and mixing framework. The explicit rational shift potential
and the field-Vandermonde approach were developed in
[PR #78](https://github.com/1337isnot1337/3-SAT/pull/78), and the
log-degree-dependent local-distance variant in
[PR #107](https://github.com/1337isnot1337/3-SAT/pull/107). Here the new
mechanism is a concatenated local code; no literature priority is claimed.

## Result

For positive integers n,m,B with m<=Bn, define

    mu = floor(log2 m)+1,          L_B = ceil(log2(B+2)),
    K  = 2^24 B^2 L_B,             P = 2 K^2,
    D  = 2^54 B^4 L_B^2 mu,       d = min(m,D).

There is a deterministic construction, polynomial in n,m and numeric B in
both bit operations and space, of a binary matrix with m columns, at most 3n
rows, row weight at most d, and every nonzero kernel word of weight at least
m/P. Thus for fixed B the row weight is O(log(m+2)) and the kernel distance
is a constant fraction of m. Uniformly, d=O(B^4 log^2(B+2) log(m+2)) and
P=O(B^4 log^2(B+2)). The extra B^2 factor means these bounds can be worse
than the source or PR #107 when B grows with m; only the fixed-B logarithmic
orders are asserted as improvements. The constants are extraordinarily large.
No improved SAT exponent or alpha follows from this component alone.

## A short binary inner code

For a local degree d>=K, put

    s = ceil(log2 d),  t = floor(s/(64B)),  ell = s+t.

We construct a binary linear length-ell code of dimension at least s and
distance at least s/(40960 B L_B). For t=0 use the full space; its distance
one meets the bound because s<64B. Otherwise set

    L = ceil(log2(2+ell/t)),   h = floor(t/(64L)).

If h=0, any t-by-ell binary check matrix gives distance at least one. If
h>=1, a uniformly random t-by-ell matrix kills any fixed nonzero word with
probability 2^-t. The number of words of weight at most h is at most
`(h+1)(e ell/h)^h`. Let a=t/(64L); since h<=a<=ell/2, the exponent
x log2(e ell/x) is increasing on [0,a]. Also

    log2(e ell/a) = log2(64 e L ell/t) <= 9L,

because log2(ell/t)<=L and log2(64eL)<=8L for L>=1. Finally
log2(h+1)<=h<=a. Thus the number of such words is at most
`2^(10t/64)<2^t`, so the expected number killed is less than one.

Find a good matrix deterministically by assigning its bits one at a time,
choosing the bit minimizing the exact conditional expectation. For each bad
word, each check row is either already forced to parity one, forced to zero,
or still uniformly random; the conditional probability of passing is
therefore zero or a power of one half. A common denominator 2^t makes every
comparison integral. The initial expectation is below one and conditional
expectation never increases, so the final integer number of bad kernel words
is zero. There are at most 2^ell<=2^(2s)<=4d^2 words, and the number of matrix
bits and arithmetic per comparison are polynomial in ell. Gaussian
elimination supplies s independent kernel vectors for an injective inner
encoder. This establishes uniform polynomial bit time and space in numeric d.

The distance is at least h+1>t/(64L) when t>0. If s>=128B then
t>=s/(128B), ell<=2s, and ell/t<=256B. Hence
`L<=8+L_B<=5L_B`, giving distance greater than s/(40960 B L_B). If s<128B,
distance at least one already exceeds that expression. No unbounded random
search is used.

## Concatenation and local row budget

For d<K, use c=ceil(d/(8B)) zero check rows. Every nonzero local word has
weight at least 1> d/K, so the desired local guarantee holds.

For d>=K, use the inner code above. Let N=floor(d/ell) and u=floor(N/(64B)).
Choose a field of size 2^s>=d and N distinct elements. The u-by-N field
Vandermonde parity check has distance at least u+1 and dimension N-u; u=0
means the full space. Select a field basis of its kernel, expand each of its
N symbols to s bits, encode each with the inner binary code, and append
`d-N ell` fixed zero bits. The concatenated code is a binary linear subspace
of length d and dimension (N-u)s. Compute a binary parity-check matrix for
that subspace by Gaussian elimination.

The check count is at most

    N t + u s + (d-N ell) <= d/(32B)+ell.

It is at most d/(8B): indeed ell<=2(log2 d+1), and d>=K implies
`d>=16B ell`. To see the latter, x/(log2 x+1) is increasing for x>=2, and
at x=K, `log2 K+1<=16 L_B`; hence
`K/(log2 K+1)>=2^20 B^2>=32B`. In particular d>=2ell, so
`N s>=d/4` because N>=d/(2ell) and ell<=2s. Any nonzero outer word has at
least u+1>N/(64B) nonzero symbols, each contributing at least
s/(40960 B L_B) binary ones. Therefore its binary weight is at least

    N s/(64*40960 B^2 L_B) >= d/(10485760 B^2 L_B) > d/K.

Pad the resulting check matrix to exactly c rows if desired. All matrices,
field search (2^s<=2d), outer and inner bases, padding and elimination are
constructible in polynomial time and space in d and numeric B.

## Tanner graph and shift construction

Let q be the least power of two with qd>=m, so m<=qd<2m. If q=1 use zero
shifts. Otherwise d=D. Use the source's q-by-q bipartite Cayley graph of degree
d, with local checks at both endpoints. Put delta=1/K and epsilon=delta/2.
For q>1 the exact rational conditional-expectation potential from PR #78
constructs shifts with every nontrivial Walsh coefficient at most epsilon d:
its sum starts at 2(q-1), never increases, and a violation would create a
term exceeding exp(epsilon^2 d/4). Since

    epsilon^2 d/4 = d/(16 K^2) = 4 mu,

this exceeds 2(q-1)<2^(mu+1). All rational numerators have polynomial bit
length and all q shifts can be enumerated at each step. For q=1 the mixing
bound is immediate.

The source mixing argument gives, for any nonzero accepted edge word of
weight w and touched vertex sets U,V,

    w >= delta d max(|U|,|V|),
    w <= d|U||V|/q + epsilon d sqrt(|U||V|),

and therefore `w>=delta(delta-epsilon)qd=qd/(2K^2)>=m/P`. Shortening to m
edge coordinates preserves this. At q>1, d=D>=8B and c<=d/(4B), giving
`2qc<=qd/(2B)<m/B<=n`. At q=1, `2c<=m/(4B)+2<=3n`. Edge generation,
local checks, shifts, shortening and output all have polynomial time and
space in n,m and numeric B.

## Composition and limits

For fixed B, the accepted sparse-code isolation construction in
[the sparse-code package](../sparse-code-isolation/README.md) may use this
matrix at m=8n, B=8. Its distance denominator P is then an absolute constant,
its extra code checks have O(log n) terms, and its isolation rows of length
`8P ceil(log2(2n))` also have O(log n) terms. This is a conditional composition
of author-checked components; the actual constants make it impractical.

In the arbitrary-density reduction B is polylogarithmic in n, so D and P
remain polylogarithmic. The original greedy queries, polynomial descriptions,
sparsification, all candidate counts, high-incidence branches, tensor entries,
modes, precision, recursion, recovery and random trials remain charged. The
accepted contraction still yields
`poly(input) * 2^{O_k(n log log n/sqrt(log n))}`. The fixed-density fallback
is unchanged. Smaller local row lengths do not by themselves remove the
iterated logarithm or increase alpha.

## Evidence and open review

The verifier checks 20,000 seeded integer schedules, directly exercises a
positive-h parameter branch using a 65,537-bit integer, checks 2,000 exact
inner-code entropy cases, checks two scaled
conditional-expectation constructions, and enumerates all 32,767 nonzero
words in a small GF(8)-outer, binary-inner concatenated code. The finite
checks do not verify the general proof, construct a source-scale q>1 Tanner
graph, or implement the global SAT algorithm. The nontrivial inner-code
conditional-expectation routine at source-scale ell remains unexecuted.
Independent review of the entropy, constants, bit complexity, composition,
and the accepted inherited interface remains necessary.
