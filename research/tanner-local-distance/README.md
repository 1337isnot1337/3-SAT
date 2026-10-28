# Degree-sensitive Tanner sparse checks

Status: `scoped_checked` for bounded controls; all-size argument author-checked,
not independently reviewed. Contributor: 1337isnot1337 with substantial
OpenAI Codex assistance. Base `e1e57cd165d9806b1bbf6500153ee1f37fedf093`.
No improved 3-SAT exponent, alpha, or selected result is claimed.

The source Tanner check uses local-code distance proportional to `1/log m`.
Using a finite-field Vandermonde local code, the needed local redundancy
instead depends on `log d`, where d is graph degree. With explicit constants
and a conditional-potential construction, the same at-most-3n-row interface
can use degree `O(B^2 log m (log(B log m))^2)` and guarantee kernel weight at
least `m/O(B^2 (log(B log m))^2)`, with standard `+2` guards made precise in
[PROOF.md](PROOF.md). The source bounds have degree `O(B^2 log^3 m)` and
weight denominator `O(B^2 log^2 m)`. The logarithmic order improves when
`log B=o(log m)`; very rapidly growing B need not benefit. Construction is
polynomial in n,m and numeric B. The asymptotic constants are large, so no practical speedup is
asserted.

At B=8 this also reduces the row-length envelope in the
[sparse-code isolation interface](../sparse-code-isolation/README.md) from
`O(log^3 n)` to `O(log n (log log n)^2)`. All isolation and contraction
costs are still charged, and the global SAT exponent remains unchanged.

Reproduce with Python 3.11+ and the standard library:

```sh
python3 -I -B research/tanner-local-distance/verify.py
make verify
```

[verification.json](verification.json) records seeded integer and local-code
controls; no huge q>1 graph was constructed. Source: OpenAI commit
`7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`, `lem:sparse-checks`; see
[SOURCES.json](../../SOURCES.json). The explicit Vandermonde and rational
potential mechanisms are credited to [PR #78](https://github.com/1337isnot1337/3-SAT/pull/78)
(head `7003b57622dbb327f7ee2e30fa2c9d36aa0ed774`), which retains the source
parameters. No literature priority is claimed. Apache-2.0.
