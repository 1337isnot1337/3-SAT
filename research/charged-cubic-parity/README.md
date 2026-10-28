# Charged cubic moments on partition-length parity sectors

Status: `scoped_checked` for the finite tests. The all-grade component
argument is written and author-checked; it has not received independent or
formal review. Contributor: Cinna Davis, with substantial OpenAI Codex
assistance. No selected result or SAT bound is changed.

## Result and scope

For the charge-q source pieces Q_s, the weighted sum
`sum_s (s^3-s)/6 Q_s(a,b)` compresses to a scalar on each output sector
of fixed partition-length parity, with the same scalar on both sectors.
The statement allows source labels indexed at the same grade (including the inhomogeneous dual
labels), output energy and
integer charge. It is a **compression**, not invariance: the cubic zero mode
also has terms that split or merge one part and map between the two sectors.
[PROOF.md](PROOF.md) derives the result from the charged low-weight zero-mode
algebra and proves that either output sector contains at least
`(p(E)-1)/(E^2+1)` basis states at energy E>=2. This retains the full leading
partition-capacity exponent, up to polynomial factors.

The input-label scalar pairing has to be sufficiently high rank before it
can be normalized into a crossing. In finite full-label calculations at
h=E=3,4,5,6 and q=1, its ranks are 2,4,5,8. They match
`p(h)-p(h-3)` in these cases only; we prove no all-grade pairing-rank formula.
No full SAT algorithm, independent review, new rho or improved alpha follows.
This cubic deletes shifts -1,0,1 only; the remaining shifts ±2 retain the
source's leading central rank envelope as h grows.

## Checks

```sh
python3 -I -B research/charged-cubic-parity/verify.py > /tmp/charged-cubic-parity.json
cmp /tmp/charged-cubic-parity.json research/charged-cubic-parity/verification.json
make verify
```

The standard-library checker first compares the cubic zero-mode formula
against 76 direct normal-ordered calculations through energy 5 and charges
-1, 0, 1, 2. It then constructs complete label/output tensors at
(h,E)=(2,2),(3,2),(3,3),(3,4),(4,4),(5,5), q=1, and verifies every diagonal
and every within-parity off-diagonal entry. Additional complete tests at
(h,E)=(3,4) use q=-1,0,2. It computes the full label-pairing rank at h=6
from one output state, without constructing the full h=6 output tensor.
The saved report records these scopes and SHA-256 binds the code and shared
predecessor modules. The operator implementation is shared; these finite
checks are not independent confirmation of the all-grade proof.

## Predecessors and next question

[PR #11](../charged-operator-moments/PROOF.md) provides the charged
normal-ordering identities and zero mode. PR #19 supplies asymmetric
normalization and bounded rational transfer. The low-weight moment argument
is adapted from the uncharged `operator-moment-recovery` branch at commit
`8191d2e2813615e4941216c012b151c96c5d7ce5`; it does not by itself claim
this charged parity compression. [PR #62](https://github.com/1337isnot1337/3-SAT/pull/62)
found the grade-6 cubic codebooks and the merge/split graph, prompting this
proof. See [source pins](../charged-asymmetric-crossing/SOURCES.json) for
the upstream Anthropic operator construction and license.

The next precise question is whether the scalar pairing has rank
`exp(pi sqrt(2h/3)-O(log h))` uniformly, with a computable minor and
normalizer. A proof of such rank would still need all entry, precision,
query, recursion, recovery, time and space costs, and a fixed-fraction shift
filter or a better actual-rank estimate, to change the SAT bound.
