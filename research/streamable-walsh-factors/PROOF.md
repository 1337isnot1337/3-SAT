# Streamable field factors after cyclic conjugation

This author-checked argument is substantially Codex-assisted and awaits
independent review. It constructs individual field-factor entries, not a
full polynomial-space SAT algorithm, a new rank rate, or a selected bound.
It builds on the Pauli/Bell identities in PR #14 and the cyclic good-prime
interface in PR #71.

## Input contract and output

Let `N=2^lambda`, `a>=2` be a fixed integer, and `C` the cyclic upper shift.
Work over a prime field `F_p` with `p` odd and `p` not dividing `a^N-1` or any
coefficient denominator. For a rational coefficient function f on pairs of
lambda-bit labels, let `hat f` be its symplectic Walsh transform as defined
in [the predecessor](../symmetric-walsh-pieces/CONSTRUCTION.md). Suppose:

1. f and hat f can be evaluated and reduced modulo p in workspace polynomial
   in lambda and log p, and their rational denominators are units modulo p.
2. For each support, its cardinality and an unranking function for precisely
   its rational nonzero labels are computable in polynomial workspace in
   lambda and log p. Unranking an invalid binary code returns an invalid
   marker. Finite running time `2^O(lambda) poly(log p)` is allowed.

Then both required flattenings of the cyclically conjugated crossing piece
have exact field factorizations with one term per indexed nonzero f or hat f
label. An individual factor entry, including invalid-code handling, is
computable in polynomial workspace and `2^O(lambda) poly(log p)` bit time.
If additional coefficients vanish modulo p, keeping their zero terms is
valid; shrinking rational support after specialization is unnecessary.

The prior fixed-alphabet symmetric and macro-adapted families meet the
entry-value and support-unranking contracts: polynomially many type counts,
polynomial-bit rational adapted-basis data and multinomial/class unranking
are established in PRs #14 and #15. Their support rates are still subject to
the proved symmetry barriers. PR #71 supplies good primes under its additional
certificate hypotheses. These statements do not establish that any family
meets a better rho.

## Explicit formulas

Let `G_{s,t}(i,j)=[i=j xor s] * (-1)^(t dot j)` and
`E_{c,d}(i,j)=[j=i xor c] * (-1)^(d dot i)`. Put

```math
 U = aI-C,
 V=U^-1,  V[s,v] = a^(N-1-((v-s) mod N))/(a^N-1).
```

All fractions are field operations. The piece and its conjugate are

```math
 M_f(x,y,u,v)=N^-1 sum_(s,t) f(s,t) G_(s,t)(x,y) G_(s,t)(u,v),
 M'_f(x,y,u,v)=sum_(r,w) U[x,r] M_f(r,y,u,w) V[w,v].
```

The row flattening `(x,y)|(u,v)` factors with terms indexed by `supp f`:

```math
 L_row(x,y;s,t)=f(s,t) N^-1 (-1)^(t dot y)
       (a [x=y xor s] - [(x+1) mod N = y xor s]),
 R_row(u,v;s,t)=(-1)^(t dot (u xor s)) V[u xor s,v].
```

For the column flattening `(x,u)|(y,v)`, terms are indexed by `supp hat f`:

```math
 L_col(x,u;c,d)=hat f(c,d) N^-2 (
       a (-1)^(d dot x)[u=x xor c]
       - (-1)^(d dot ((x+1) mod N))[u=((x+1) mod N) xor c]),
 R_col(y,v;c,d)=(-1)^(d dot y) V[y xor c,v].
```

They follow by substituting the source's Pauli and Bell expansions and
performing the single surviving delta sum on the inverse side. Thus each
factorization reconstructs the same conjugated tensor. Invalid code slots
of `ceil(log2 support size)` bits return zero, independently on both factors.

## Cost and actual boundary

A modular exponent has an exponent of at most lambda bits: compute it by
repeated squaring, retaining O(1) field elements and an O(lambda)-bit counter.
The denominator's inverse uses polynomial field-bit workspace; the supported
prime contracts guarantee it exists. Formula evaluation stores only indices,
coefficient data, and a constant number of field elements. Polynomial-size
type computations and support unranking add polynomial workspace; their time
is explicitly charged. The number of factor terms remains the rational
support count, and no dense `N^2`-by-`N^2` matrix or Gaussian elimination is
needed to *generate one entry*.

That conclusion does not automatically bound the whole recursive protocol's
space: intermediate tensor descriptions, recursive evaluation, enumeration,
CRT and the outer sparse reduction must all be composed. Nor does it apply to
arbitrary PR #17 rational pieces lacking the stated support and evaluation
oracles. A factor evaluation oracle is not a new lower-rho piece family.

The finite checker constructs the predecessor's actual six-class R=1 pieces,
uses base a=3 and primes 23 and 47, compares both explicit factor sums with
an independently calculated conjugated tensor at every index, and checks
binary support-code padding. It stores arrays to speed the bounded test, so
that checker is not a polynomial-space implementation of the full protocol.
The written all-size argument and the cited unranking contract have not been
independently reviewed.
