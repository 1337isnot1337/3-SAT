# Finite-field source crossings and restricted codebooks

Status: `scoped_checked`; written all-size arguments are author-checked,
not independently reviewed or formally verified. No SAT improvement is
claimed.

The [proof](PROOF.md) reduces the actual integer pieces and both source
factorizations in Anthropic's Appendix B modulo a prime p. The original
normalizer `h!` is invertible exactly when `p>h`. For `p<=h`, the original
summed pieces vanish, but the source's unscaled dual pairing permits a changed
construction: restrict labels to partitions with no p-divisible part and
multiplicities below p, and normalize each label by its individual `z_mu`.
The resulting piece sum is equality on that codebook, with the original full
grade-space factor-length bounds. The codebook is exponentially large in
sqrt(h) uniformly in p, and an exact dynamic program ranks and unranks it in
polynomial time. Choosing `h=max(256,8(lambda+1)^2)` supplies 2^lambda labels.

For p=2, the proof bounds the codebook size and shows that the source's
listed uncompressed factors at shift zero have combined lengths requiring
asymptotic crossing ratio at least sqrt(2), outside the rho<1 regime. This is
a limitation of those length certificates, not a lower bound on actual field
ranks, compressed factors, other codebooks, or SAT. The full crossing and
entry construction here remains a local component; exact integer query
recovery, a one-sided decision guarantee, recursion and full global cost
remain separate.

Reproduce from the repository root using Python 3.11+ and the standard library:

```sh
python3 -I -B research/source-pieces-finite-field/verify.py
python3 -I -B research/source-pieces-finite-field/pieces.py
python3 -I -B research/source-pieces-finite-field/codebook.py
python3 -I -B research/source-pieces-finite-field/rank_screen.py
make verify
```

Exact finite replays cover 2,165 source pairing reductions, 30 common
normalizer checks, 1,135 restricted pairings, 14 surviving p<=h controls,
428 source-operator order cases, 49 restricted summed identities, and 6,276
rank/unrank states across 100 domains. The rank screen also checks all shifts
for binary codebooks at h=8,9,10,12 and all three two-label subsets at h=12;
its recursive operator implementation agrees with 428 direct source cases
through h=3 and one h=8 piece. Actual rank products are often much smaller
than the uncompressed lengths, but these are only two- and three-label finite
cases, with no asymptotic rank bound. These checks do not establish the written
all-size proofs or a SAT implementation. The first attempt to run the source
operator checker failed because isolated Python omits the script directory
from imports; the checker now has its own small partition enumerator. The first
rank-screen run also exposed a missing test-script import, which was fixed.

Source: Anthropic, *A 2^{o(n)} Time Algorithm for 3-SAT*, Appendix B,
Lemma 9, Lemma 10, and equations (47), (48), (53)-(55), source commit
`16a5ce41304fcdaea4e0be7c132e1c361dc26da5`. Retained PDF and licenses are
pinned in [the source scan](../recent-breakthrough-scan/SOURCES.json).
This builds on the merged [digit pairing investigation](../frobenius-digit-pairing/PROOF.md),
[weighted oscillator quotient bound](../weighted-oscillator-rigidity/PROOF.md),
[odd-prime rank transfer](../odd-prime-rank-transfer/README.md), and
[CRT transfer PR #60](https://github.com/1337isnot1337/3-SAT/pull/60).
Base `ec45f184710a6adcd74e1aea31f29d7d1c44d0e2`. Contributor: Cinna Davis,
with substantial OpenAI Codex assistance. New material Apache-2.0.
