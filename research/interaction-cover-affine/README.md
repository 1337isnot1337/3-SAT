# Interaction-cover affine counting

Status: `scoped_checked`; substantially AI assisted; no independent review
and no selected-result or unrestricted SAT improvement.

A vertex cover of the monomial interaction graph is an affine backdoor for a
listed Boolean polynomial system: after fixing the cover, every equation is
linear in the remaining variables. Exact Gaussian-elimination counting gives
`2^|C| poly(input)` time and polynomial space, including unused variables and
prescribed fixed-bit branches. A greedy maximal matching supplies a cover of
size at most twice the minimum without assuming that minimum is computable in
polynomial time. Width-3 CNF converts directly with no auxiliary variables.

The result is a standard structural interface, not a new general bound.
A sparse system of disjoint quadratic pairs has minimum interaction cover
`n/2` even though its count is simply `3^(n/2)`. It demonstrates that the
source sparse-query assumptions do not supply the desired small cover, not a
hardness result. See [PROOF.md](PROOF.md) for the complete local costs,
outer-reduction obligations, bounds under an explicit promise, and predecessor
credit.

Reproduce from the repository root with Python 3 and the standard library:

```sh
python3 -I -B research/interaction-cover-affine/verify.py
make verify
```

The saved [verification.json](verification.json) covers 128 individual
polynomials, 1,600 seeded systems and fixed branches, 1,600 matching-cover
certificates, 400 small 3-CNF conversions, six disjoint-pair controls and an
invalid-cover rejection. Brute-force enumeration is independent of the
affine reference routine. These checks are finite; the all-size argument
awaits independent review.

Canonical base `f64e1babba809276639257f37cd218ee18824257`; accepted OpenAI
source `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`, particularly
`lem:tensor-sparse-query` and `subsec:sharp-dense`. Related counting-backdoor
work by Nishimura, Ragde and Szeider is pinned and credited in the proof; the
bipartite precursor is PR #73. Contributor: 1337isnot1337 with substantial
OpenAI Codex assistance. New material is Apache-2.0.
