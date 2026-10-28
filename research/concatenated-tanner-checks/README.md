# Fixed-density Tanner checks with constant relative distance

Status: `scoped_checked` for finite controls; the all-size construction is
author-checked and not independently reviewed. Contributor: 1337isnot1337
with substantial OpenAI Codex assistance. Base
`c7c5a03434b396e227e9ab573b5b7cdea52b47fa`. No improved SAT exponent or
selected alpha is claimed.

An explicit concatenated local code replaces the source's local random-code
search. Its outer code has a finite-field Vandermonde check; its short binary
inner code is found by exact conditional expectation over at most `4d^2`
words. With a changed Tanner degree and mixing budget, this gives, for
`m<=Bn`, at most `3n` binary checks of weight
`O(B^4 log^2(B+2) log(m+2))` whose kernel has distance at least
`m/O(B^4 log^2(B+2))`. Construction is polynomial in n,m and numeric B.
For fixed B the kernel distance is a constant fraction of m and row weight
is logarithmic. A rank argument shows logarithmic port degree is also
necessary within the XOR-Cayley mixing mechanism, though this does not lower
bound arbitrary check-row weight. The extra B^2 factor can make the bounds
worse when B grows;
constants are enormous and no practical advantage is claimed.

For the B=8 sparse-code isolation interface, the code checks and isolation
rows both have O(log n) terms. Its random trials and all contraction costs
remain, so the known global `n log log n/sqrt(log n)` exponent is unchanged.
[PROOF.md](PROOF.md) gives explicit constants, finite fallbacks, construction
costs and limitations.

Reproduce with Python 3.11+ and the standard library:

```sh
python3 -I -B research/concatenated-tanner-checks/verify.py
make verify
```

[verification.json](verification.json) records bounded numerical and
concatenated-code controls. They do not implement the all-size construction,
a source-scale q>1 Tanner graph, or an end-to-end SAT solver. Credit: accepted
OpenAI source commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`,
`lem:sparse-checks`; [PR #78](https://github.com/1337isnot1337/3-SAT/pull/78)
for polynomial-time shifts and the source-parameter Vandermonde construction;
and [PR #107](https://github.com/1337isnot1337/3-SAT/pull/107) for the
preceding degree-sensitive parameters. No literature priority is claimed.
Apache-2.0.
