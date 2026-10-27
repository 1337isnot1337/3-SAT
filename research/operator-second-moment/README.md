# Exact second operator moment

Status: `scoped_checked`. The all-size operator formula and singularity argument
are author-checked and substantially AI-assisted; independent review is still
required. No SAT bound, crossing ratio, alpha or selected-result improvement is
claimed.

Task: `contraction-schedule`. Canonical base:
`630041c9da3a26edb8c8f59d5f8a4132a188c8bd`.
Contributor: 1337isnot1337, with substantial AI assistance from Kimi.

## Question and changed premise

PR 11 derived a square-zero charged first moment. PR 19 used an asymmetric minor
to omit the central shift and left higher moments and wider filters open. This
round asks whether the **uncharged second moment** has an exact algebraic form
that supplies a genuinely new normalization or a precise obstruction.

The success test was an all-size formula with independent finite operator checks.
The stopping test for naive common-label inversion was a uniform singularity
proof. Both tests are reached.

## Statement and scope

[PROOF.md](PROOF.md) defines `A=exp(L)`,
`F=sum_(r>=1)(-1)^(r-1)r u_r`, and

```math
 U_h=\frac1{2h}F(FA+2A\partial_{u_1}).
```

On every output energy space, the uncharged second moment is

```math
 \sum_s s^2Q_s(a_\mu,b_\nu)
 =4hE\,h!\,\frac{m_\mu!}{m_\nu!}[u^\mu]U_h(u^\nu)\operatorname{Id}.
```

The full common-label pairing is singular for every `h>=2`; the proof includes
an explicit uniform kernel construction for `h>=4`. This closes naive inversion
on the full label space without preventing an asymmetric minor.

Exact elimination additionally observes rank `p(h)-p(h-2)` and the cubic
`U_h(U_h-1)(U_h+(h-2)/h)=0` for `1<=h<=10`. These are finite observations, not
all-size claims.

## Possible improvement and complete cost boundary

At output energy `h`, the moment pair suggests a quadratic `1-s^2` crossing
filter omitting shifts `+1` and `-1`, conditional on a uniform paid inverse of
`I-4h^2U_h`. No such actual filter is constructed in this package. Proving its
all-size invertibility and charging both directional ranks, inverse heights,
entries and recursion is the next concrete experiment. Even success would leave
the central and nearby shifts and would not automatically improve rho.

This round constructs no SAT reduction or tensor network and adds no queries,
branches, entries, modes, precision, randomness or amplification. The accepted
general and fixed-density time envelopes remain unchanged.

## Evidence and reproduction

From the repository root, offline with Python 3.11+ and only the standard
library:

```sh
python3 -I -B research/operator-second-moment/verify.py
make verify
```

The checker compares 594 exact second-moment entries against the independent
normal-ordered implementation through weight 6 and checks ten exact polynomial
rank/spectral matrices through weight 10. [verification.json](verification.json)
records the actual scopes, values and source hashes. Finite matrices do not
prove the all-size rank or spectral pattern.

## Sources and next question

[SOURCES.json](SOURCES.json) pins the external paper, PR 11's operator modules,
and the latest asymmetric first-moment predecessor. The next task is an all-size
proof or counterexample for the observed spectral cubic, followed by a paid
quadratic-filter construction if the nonzero spectrum remains suitable. Do not
claim the finite rank formula as a theorem.
