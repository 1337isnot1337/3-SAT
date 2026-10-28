# Finite-field threshold for the source crossing pieces

Status: `scoped_checked`; the written all-size transfer is author-checked,
not independently reviewed or formally verified. No SAT improvement is
claimed.

The [proof](PROOF.md) reduces the actual integer pieces and both source
factorizations in Anthropic's Appendix B modulo a prime p. The original
normalizer `h!` is invertible exactly when `p>h`. Such a p gives a normalized
finite-field equality crossing with the original two directional length
bounds. When `p<=h`, the original summed pieces reduce to zero, so a scalar
rescaling of those same pieces cannot implement equality. The source has an
integer representation, so the reduction is valid even for intermediate
weights above p; there is no need to impose `p>2h` for this local result.

A suitable prime can be found deterministically in polynomial time in h,
and the source's h is quadratic in the crossing bit length asymptotically.
This is a local field component. It does not provide exact integer query
recovery, one-sided decision success, a changed crossing rank, or a complete
SAT algorithm. The merged odd-prime rank-transfer package and open CRT
transfer PR #60 address related but separate recovery interfaces.

Reproduce from the repository root using Python 3.11+ and the standard library:

```sh
python3 -I -B research/source-pieces-finite-field/verify.py
python3 -I -B research/source-pieces-finite-field/pieces.py
make verify
```

The finite replay evaluates the source's Lemma 10 pairing directly from
its operator formula (47), using exact integer sums and reductions: 2,165
pairing reductions and 30 normalizer checks for `h=2,...,7` and
`p=2,3,5,7,11`. A second exact replay evaluates source operator order on 428 cases at
`h=1,2,3`, checks the summed crossing identity, and reduces it modulo four
primes. These checks do not verify the all-size source identities, full
factorization lengths, or a SAT implementation. The first attempt to run the
second checker failed because isolated Python omits the script directory from
imports; the checker now has its own small partition enumerator.

Source: Anthropic, *A 2^{o(n)} Time Algorithm for 3-SAT*, Appendix B,
Lemma 9, Lemma 10, and equations (47), (48), (53)-(55), source commit
`16a5ce41304fcdaea4e0be7c132e1c361dc26da5`. Retained PDF and licenses are
pinned in [the source scan](../recent-breakthrough-scan/SOURCES.json).
This builds on the merged [digit pairing investigation](../frobenius-digit-pairing/PROOF.md),
[odd-prime rank transfer](../odd-prime-rank-transfer/README.md), and
[CRT transfer PR #60](https://github.com/1337isnot1337/3-SAT/pull/60).
Base `ec45f184710a6adcd74e1aea31f29d7d1c44d0e2`. Contributor: Cinna Davis,
with substantial OpenAI Codex assistance. New material Apache-2.0.
