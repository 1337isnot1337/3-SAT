# two-scale-cauchy-grid

Status: `scoped_checked` for the component and finite domain below. The full
contraction schedule remains open; no SAT time improvement is claimed.

Task: `contraction-schedule`. Base commit: `8a659c67d4988540aa6ac8393bb06314ecbe81e2`.

Contributor: Cinna Davis (OpenAI Codex assisted). Disclose substantial AI assistance.

## Question and changed premise

Use port coordinates `X={x+2^b y:0<=x<d,0<=y<H}` with `d=2^r`,
`H=2^t`, and `b>=r+2`, instead of a single contiguous interval. The
packet still has `L=dH` slots. The product grid
`S={a+2^b c:-d<=a<d,-H<=c<H}` has only `4L` nodes and contains every
port difference. Can its larger valuation gap improve the joint mode and
recovery cost, rather than only an isolated spectrum? Accept the OpenAI
theorem; this is a proposed replacement of its deformation, not an audit.

## Statement and scope

First prove uniform derivative valuations and integral shifted kernels,
then determine the local Cauchy Smith spectrum. Candidate formula at index
`j` is `4j-2 popcount(j)+2(b-r) floor(j/d)`. A large `b` can strengthen
that spectrum without increasing the number of slots or nodes. Success
for the full objective requires the **same** gap to survive the Hermite
precision, all children and entry costs. Stop an unchanged route if those
costs cancel the spectral benefit. No time or alpha improvement is claimed.

## Complete cost

The packet slot count is unchanged and the grid has `4L` nodes instead of
`2L`; its kernel degree is `4L-1`. Coordinate and coefficient bit lengths
are polynomial in `L,b,t`; at polynomial precision its shifted entries are
computable in polynomial bit time. These facts do not establish a full
contraction. The exact missing costs are changed Hermite precision, actual
crossing-tile factors and multiplicities, inherited precision, child sizes,
leaves, and all outer reduction/query work. The selected result is unchanged.

## Evidence and reproduction

Registered first finite domain: `(d,H)=(2,2),(2,4),(4,2)`, with
`b=r+2,r+5`, odd normalized denominators `c=1,3`, all Cauchy minors;
all product-grid derivative valuations; and complete shifted polynomials
for the same packet parameters, with a bounded representative set of
real port differences. No random selection or external dependencies.
The [proof](PROOF.md) establishes the component formulas. The standard-library
[checker](verify.py) passed 103,228 direct fraction-free Cauchy determinants,
960 complete shifted kernel expansions, and 27,648 integer-coefficient
content checks on that registered domain. It also checks grid derivatives,
matching-node units, dummy nodes and localization bits. The saved output is
[verification.json](verification.json), with proof/checker/source hashes.

```sh
python3 -I -B research/two-scale-cauchy-grid/verify.py
make verify
```

This is an exact finite reference replay, not the accepted contraction or
an independent proof review. The checker is outside default CI.

## Limits and open next questions

The first checkpoint confirms a larger **local** spectrum and a valid
shifted-integral kernel at arbitrarily large gaps. The next calculation is
the exact product-grid Hermite loss functional, normalized by those local
spectral slopes, so any precision cancellation is tested before asserting
a running-time gain. The broad goal remains active. Do not treat a local
invariant-factor change as a complete algorithm.

## Sources and credit

Frozen OpenAI source commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`,
labels `eq:tensor-cauchy`, `lem:tensor-integrality`, `lem:tapered-hermite`,
`eq:tensor-mode-expansion`, and `subsec:tensor-cost`. See
[SOURCES.json](../../SOURCES.json). The accepted theorem is unchanged.
The local fixed-interval spectrum in [PR 1](https://github.com/1337isnot1337/3-SAT/pull/1)
motivates changing the coordinates, rather than another basis change on
that same interval. [PR 4](https://github.com/1337isnot1337/3-SAT/pull/4)
supplies stronger ordinary Newton modes; [PR 6](https://github.com/1337isnot1337/3-SAT/pull/6)
shows why generic recovery precision must also be charged. Current
operator-rank and sparse-oscillator branches concern the other construction
and are preserved. New material is Apache-2.0, with substantial Codex assistance.
