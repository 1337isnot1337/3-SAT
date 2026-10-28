# Cyclic locality transfer for sparse queries

Status: `scoped_checked`; AI assisted, not independently reviewed. No
selected-result change or general SAT improvement.

The sparse-query support witness in the predecessor has `t^n` retained
incidence monomials. Yet its equations have cyclic span `L=k floor(log2 n)`,
so a direct exact transfer computation counts its satisfying assignments in
`n^O(k)` time and polynomial space for fixed `k`. The result bypasses that
particular incidence representation; it does not contradict its lower bound.

[PROOF.md](PROOF.md) proves an exact transfer interface for explicitly listed
polynomial systems with a supplied cyclic order and span `L`: time
`poly(n+B) 2^(2(L-1))` and space `poly(n+B) 2^(L-1)` bits. It also proves
that sparse quadratic systems on complete binary trees require
`Omega(n/log n)` cyclic span in every order. These tree examples are easy by
other means, so the limitation is of the interface, not a hardness claim.

Reproduce with Python 3 and the standard library from the repository root:

```sh
python3 -I -B research/cyclic-locality-transfer/verify.py
make verify
```

The exact checker compares the transfer implementation with independent
brute-force enumeration for 3,356 local polynomials, 1,200 seeded systems,
and 15 cyclic-witness instances. It checks all 5,040 circular orderings of
the seven-vertex tree. Saved output is [verification.json](verification.json).
These finite tests do not establish the all-size proof. No native fast SAT
solver, independent review, or formal verification is claimed.

The missing general step is a uniform replacement for locality across every
sparse query and every candidate in the outer reduction, with all processing,
query, space and time costs charged. A special-family polynomial algorithm
does not alter the accepted general-density bound or alpha. Hybridization
with a general fallback has only the fallback's worst-case guarantee.

Sources: canonical main `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`;
accepted OpenAI source `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`,
`lem:tensor-sparse-query`, `eq:sharp-incidence-degree`,
`eq:sharp-wire-budget`, `subsec:sharp-dense`; the cited cyclic witness and
its support bound are from [the predecessor](../newton-parity-compression/PROOF.md).
The tree-locality counterexample is separate from the aggregate packing
limitation in [PR #18](https://github.com/1337isnot1337/3-SAT/pull/18).
Contributor: 1337isnot1337 with substantial OpenAI Codex assistance. The transfer
idea is standard; no priority is claimed. New material is Apache-2.0.
