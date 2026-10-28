# Sparse-hash distance versus frontier width

Status: `scoped_checked` for exact finite controls; the all-size argument is
author-checked and awaits independent review. No SAT time improvement or
unrestricted lower bound is claimed. Task `decision-only`; base
`630041c9da3a26edb8c8f59d5f8a4132a188c8bd`. Contributor: Cinna Davis, with
substantial OpenAI Codex assistance. Apache-2.0.

[PROOF.md](PROOF.md) shows that an m-column binary matrix with kernel dimension
k and minimum nonzero kernel weight at least D>=2 has maximum ordered
prefix/suffix frontier width at least `k/ceil(m/(D-1))`, for **every** ordering.
The stronger sum over regularly spaced cuts is proved as well. The reasoning
partitions columns into independent short blocks and bounds nullity gained in
each block by its preceding frontier width.

For the accepted sparse-check matrix plus t arbitrary appended rows, its
minimum-distance guarantee and at-most `3n+t` rows imply width at least
`max(0,m-3n-t)/(2P+1)` when `m>P`, where P is the source's polylogarithmic
parameter. This is useful only if the displayed nullity lower bound is
positive. In a conditional linear-nullity regime it prevents the proposed
frontier method of PR #37 from obtaining uniformly small width by reordering.
It does not establish that this regime occurs for every leaf, that the full
state upper bound is attained, or that arbitrary SAT algorithms are slow.
A direct sum of long independent circuits has large distance but width one,
showing why nullity is needed.

## Reproduction and evidence

```sh
python3 -I -B research/hash-frontier-width/verify.py
make verify
```

The checker exhausts 4,096 binary 3-by-4 matrices, checking all 24 column
permutations whenever the minimum kernel weight is at least two, including
the stronger block-sum inequality. It also tests direct sums of circuits in
20 parameter cases, with brute-force distance checks when the total length
is at most 18. The [hash-bound output](verification.json) records exact
counts. The finite controls do not independently review the proof.

## Scope, sources and next question

The accepted OpenAI `lem:sparse-checks` is in
[main_full_version.tex](../../upstream/openai-eth-2026/build/main_full_version.tex)
and pinned at commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a` by
[SOURCES.json](../../SOURCES.json). The decision wrapper is credited to PR #2,
and the frontier application to PR #37. Standard linear-algebraic dimension
and minimum-distance facts are used; no priority is claimed.

A next step is to establish the actual rank/nullity and width for specific
sparse-check and appended-hash matrices or find an alternative representation
whose cost exploits more than width. A complete faster SAT algorithm must
still account for all other components. The selected result is unchanged.
