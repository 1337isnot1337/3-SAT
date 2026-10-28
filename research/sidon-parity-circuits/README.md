# Cancellation-free parity circuits on Sidon query supports

Status: `scoped_checked`; substantial AI assistance; no independent review.
Task: `dense-encoding`. Base: `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`.
No selected bound or alpha changes.

[PROOF.md](PROOF.md) gives an explicit low-load quadratic sparse-query family
for which every cancellation-free, binary shared-XOR circuit for the given
rows has exactly n(L-1) or more distinct gates, where L=floor(log2 n)-2.
Distinct row supports meet in at most one formal monomial, preventing any
nontrivial gate from being shared. The source high-incidence preprocessing
branches on no variable. For the direct per-gate network this entails
Omega(n log n) gate-to-gate wires. A separate-tree construction meets the
gate count and produces a Theta(n log n)-wire network.

This is a restriction on a proposed encoding, not a SAT or circuit lower
bound without the disjoint-support hypothesis. Row-basis changes,
cancellation, Boolean relations among monomials and tensor aggregation are
outside the claim. The source's incidence-monomial indexer is a different
representation and already has a better O(n log log n) wire envelope.
No generalized runtime improvement is claimed. For power-of-two n, the
proof also derives an exact polynomial-time count for this same witness: its
answer is F_(n-1)+F_(n+1), plus one when L is even. This uses a cyclic
row-space change and the structure of the actual quadratic monomials, both
outside the restricted circuit model. More generally, the same family at
arbitrary n has a deterministic polynomial-space exact count in time
`poly(n) 2^d`, where `d=deg gcd(g,Y^n-1)` and `d` is at most
`gcd(n_odd,2^L-1)`. This is polynomial only under an explicit parameter
condition, such as `d=O(log n)`. In fact, the infinite subsequence
`n=5(2^L-1)` has `d=(n-5)/10`; this enumeration is exponential there.

The question was whether simple gate-level parity sharing uniformly gives
O(n) wires for low-load sparse queries. Success is a rigorous obstruction
within an explicit circuit model; stop before generalizing it to row changes,
nonlocal gates, or arbitrary algorithms. The all-size proof and exact scope
are in [PROOF.md](PROOF.md).

## Reproduction

From the repository root, with Python 3.11+ and only the standard library:

```sh
python3 -I -B research/sidon-parity-circuits/verify.py
python3 -I -B research/sidon-parity-circuits/arbitrary.py
make verify
```

The bounded checker directly verifies all pairwise row intersections, all
variable loads and the source threshold, and the constructed gate counts at
n=16,20,31,32,64,100,128,256,512. It checks 680 gate-constraint assignments
and 9,504 quadratic scope assignments. It also checks the binary matrix rank
at five power-of-two sizes and exhausts all 65,536 original assignments at
n=16, obtaining 2,208 solutions. The arbitrary-size checker verifies the
full kernel enumeration at 14 sizes, including d=7, and exhausts the
original Boolean assignments at n=16,17,18. Six additional exact gcd
checks cover the linear-kernel subsequence without enumerating it. These
finite checks do not mechanically
prove the all-size statement. No external dependency or heavy check is added
to default CI.

## Sources and credit

The accepted source is OpenAI's October 2026 paper, frozen commit
`7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`; relevant labels are
`lem:tensor-sparse-query`, `eq:sharp-wire-budget`, and
`thm:tensor-contraction` in `upstream/openai-eth-2026/build/quantitative-reduction.tex`.
The low-load and encoding motivation comes from
[scalar-parity-lift](../scalar-parity-lift/README.md) and
[newton-parity-compression](../newton-parity-compression/README.md).
[Issue #29](https://github.com/1337isnot1337/3-SAT/issues/29) independently
studies row-basis-resistant coefficientwise support; this package uses a
different circuit model and makes no row-basis claim. Issue #28 studies a
transfer algorithm for a different, short-span cyclic witness. Sidon sets,
parity circuits, and the gate-count argument are elementary; no literature
priority or novelty claim is made. Contributor: Cinna Davis with substantial
OpenAI Codex assistance. New material is Apache-2.0.

## Next questions

A materially changed route must handle cancellation, row operations, or
aggregate tensors while paying output and entry costs. In particular, measure
whether a concrete algorithm can share gates using cancellation on this
family and on all queried systems. Do not infer an improvement from a finite
example or from a gate count without its network translation and full outer
reduction costs.
