# Sparse oscillators do not preserve the unchanged crossing identity

This tests one changed premise in Claude (Anthropic), *A 2^{o(n)} Time
Algorithm for 3-SAT*, [Hexagon v1](https://hexagonmath.org/2610.00577v1),
Appendix B, Lemma 9. The source repository is pinned at
`16a5ce41304fcdaea4e0be7c132e1c361dc26da5`. Its
[proof index](https://github.com/anthropics/formal-math/blob/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth/proof/PaperIndex.lean)
names that identity as `AppHalfPieces.lemmaQ`. This package is an
AI-assisted, author-checked extension screen, not a review or refutation
of the source theorem. It does not change the accepted OpenAI baseline.

## 1. Precise changed construction

For a set `S` of positive integers containing 1, work on
`Q[t_k : k in S]`. Keep the source's creation and annihilation operators

```math
 D_{-k}f=t_kf,\qquad D_k f=k\frac{\partial f}{\partial t_k}\quad(k\in S),
```

and put `D_k=0` when `|k|` is not in `S`, including `D_0=0`. Keep
the formula for the field of `t_1`, namely `t_1[r]=D_{-r}`, and keep
the alternating coefficients in the source's `Q_s` identity.

The success test is Lemma 9(a): exchanging the two operator factors
must leave every `Q_s` unchanged. This condition is needed for the two
directional factorizations to describe the same crossing piece. A
smaller grade dimension without this identity is insufficient.

For `a=b=t_1` and `h=1`, let `k_i=s+i-1` and define

```math
 Q_s=\sum_{i=0}^2(-1)^i\binom2iD_{-k_i}D_{k_i},\qquad
 Q_s^{\rm rev}=\sum_{i=0}^2(-1)^i\binom2iD_{k_i}D_{-k_i}.
```

Set `g(0)=0` and `g(k)=k[|k| in S]` for nonzero integer `k`.
The exact commutator is `[D_k,D_-k]=g(k) Id`. Therefore

```math
 Q_s-Q_s^{\rm rev}
 =-\bigl(g(s-1)-2g(s)+g(s+1)\bigr)\operatorname{Id}.       \tag{1}
```

This calculation acts on every polynomial, not only a finite truncation.

## 2. An all-size obstruction and explicit witness

If Lemma 9(a) held for this changed construction at all shifts, (1)
would say that the second difference of `g` vanishes everywhere.
Thus `g(k)=ck`, since `g(0)=0`; because `1 in S`, `c=g(1)=1`.
It follows that `S` must contain every positive integer. The empty
set also has zero commutator, but cannot supply the nonempty label
space of the proposed construction.

More concretely, let `m>=2` be the first missing positive integer.
At `s=m-1`, `g(m-2)=m-2`, `g(m-1)=m-1`, and `g(m)=0`. Hence

```math
 Q_{m-1}-Q_{m-1}^{\rm rev}=m\operatorname{Id}.              \tag{2}
```

For square-indexed oscillators, `m=2` already gives a defect of
`2 Id` at `s=1`. At `s=2`, the defect is `-Id`: on the vacuum
polynomial 1, the original order gives zero and the reversed order
gives one. The failure is exact over the source's integer/rational
coefficient ring. Reducing modulo a specially chosen prime could
hide an individual witness; it does not restore the source identity
over the stated ring or its exact integer recovery.

The result excludes deleting modes while preserving these operators
and the `h=1` coefficients. It does not exclude a changed operator
identity, a different graded representation, or another SAT algorithm.

## 3. Why square-only grade growth was tempting

Let `p_q(E)` count partitions of `E` into positive qth powers, for a
fixed integer `q>=1`. Its generating function is

```math
 \prod_{k\ge1}(1-z^{k^q})^{-1}.
```

For every `theta>0`, its coefficient is at most

```math
 \exp\left(\theta E+
 \sum_{j\ge1}\frac1j\sum_{k\ge1}e^{-\theta j k^q}\right).
```

The inner sum is at most
`integral_0^infinity exp(-theta*j*x^q) dx = C_q(theta*j)^(-1/q)`.
The sum over `j` converges, so optimizing proves
`log p_q(E)=O_q(E^(1/(q+1)))`. For the reverse bound, take all
subsets of the parts `2^q,...,B^q`, with `B=c_q E^(1/(q+1))`
and a sufficiently small fixed positive constant. Their total weight
is at most E; pad each subset to E with parts equal to 1. Distinct
subsets retain distinct parts greater than 1. Thus

```math
 \log p_q(E)=\Theta_q(E^{1/(q+1)}).                          \tag{3}
```

Square modes therefore have a smaller growth power, `1/3` in place
of `1/2`. The conditional cost calculation in the literature scan
would suggest an alpha target of `2/3` if the full operator and dual
label contracts could be retained with the required sharp growth
asymptotic. Equation (2) shows that the unchanged construction fails
before those rank or entry-cost questions arise. Equation (3) alone
is not a better SAT algorithm and supplies only growth order, not
every asymptotic hypothesis of that conditional calculation.

## 4. Finite polynomial locality cannot rescue zero-density index sets

There is a broader elementary obstruction for an infinite zero-density
set `S`. Consider the scalar commutator series

```math
 G(z)=\sum_{n\ge1}n[n\in S]z^n.
```

It is not rational over Q. To see this, suppose it were rational.
Its coefficients would satisfy an eventual recurrence
`sum_(j=0)^d q_j (n-j) a_(n-j)=0`, with integer `q_j`, `q_0!=0`,
and `a_n=[n in S]`. Write this as `n A_n=B_n`, where
`A_n=sum q_j a_(n-j)` is an integer and
`B_n=sum j q_j a_(n-j)` has absolute value at most
`K=sum j|q_j|`. For all sufficiently large `n>K`, this forces
`A_n=B_n=0`. Hence the binary sequence `a_n` satisfies a fixed
constant-coefficient recurrence. Its last d bits are a finite state,
and `q_0!=0` determines the next bit, so the sequence is eventually
periodic. An eventually periodic binary sequence of density zero
is eventually zero, contradicting that S is infinite.

Consequently no nonzero finite polynomial denominator makes this
one-sided commutator series polynomial. This blocks the direct
finite-polynomial locality repair based on this same scalar
commutator. It is not an impossibility result for all possible
operator constructions or for a truncation whose denominator degree
and cost are allowed to grow with the instance; such a repair needs
its own complete bit-cost analysis.

## 5. Arithmetic thinning only rescales energy

For comparison, retaining just the multiples of a fixed `q` gives
`dim V_E=p(E/q)` when `q` divides E, and zero otherwise. Use the
same q when comparing the label grade h and the intermediate grades
near 2h. Along divisible grades, the leading dimension ratio is still
`log p(2h/q)/log p(h/q) -> sqrt(2)`.

Letting q depend on the instance h does not permit replacing it by
`q(2h)` for the intermediate space of that same instance. That
diagonal-parameter substitution would manufacture a smaller apparent
growth power. Arithmetic thinning by itself therefore does not
produce the proposed alpha improvement through the partition envelope.
It also has to modify the source locality relation, which is already
outside the unchanged construction: for `q>1`, its `t_1` label is
absent. Relabelling the retained oscillator indices restores the original
dimension growth rather than producing a smaller ratio. For a growing
q(h), a label family of unbounded size still requires `h/q(h)` to grow.

## Scope and next premise

The natural sparse-index proposal is refuted under its stated unchanged
identity. Do not repeat a dimension-only enumeration for the same
operators. Reopen after specifying different operator coefficients or
a different representation that proves both directional identities,
the label pairing and uniform bit costs. The checker verifies finite
commutator instances, first-omission witnesses and partition counts;
it does not mechanically verify these all-size arguments or implement
the external or accepted subexponential algorithms.
