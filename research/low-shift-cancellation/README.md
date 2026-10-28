# Extremal-shift cancellation

Status: `scoped_checked`. This is an author-checked, AI-assisted argument,
not an independent or formal review. No improved SAT bound or selected
result is claimed. Base `f1c4ec3a48b823ab749f93cfe8f81dfe8ca0336f`;
task `contraction-schedule`; contributor Cinna Davis with substantial
OpenAI Codex assistance.

The [proof](PROOF.md) improves the uncharged **full partition-space** shift
rank lower bound from PR #59 to `2h+max(0,floor((h-3)/2))`. For each odd
output length ell from 3 to h-2, two actual crossing entries have the same
extreme shift but different normalized endpoint coefficients. Their exact
linear combination cancels that endpoint and its negative by symmetry;
their first nonzero derivatives occur at distinct orders. These rows are
independent of the previous hook and moment witnesses.

The added input state `(h)` may be omitted by the original binary codebook.
The previous encoded-codebook bound is unchanged. A rank obstruction for
this family does not by itself constrain changed pieces or improve a SAT
running time. The selected owner-accepted baseline is unchanged.

Reproduce offline, with Python 3.11+ and standard library:

```sh
python3 -I -B research/low-shift-cancellation/verify.py
make verify
```

The checker uses an explicit normal-order coefficient calculation for
h=5,...,40. It verifies both endpoints, cancellation, symmetry, support,
and exact first derivatives for each admissible length; it compares full
Laurent rows to the original PR #10 operator recurrence for h=5,6. The
saved [output](verification.json) can be compared byte-for-byte. This is
finite component evidence, not independent verification of the all-size
proof, or a full SAT replay.

Sources are PR #59's [proof and source pins](../scalar-relation-witness/PROOF.md)
and [PR #10's source record](../anthropic-operator-ranks/SOURCES.json):
Anthropic, Hexagon 2610.00577v1, Appendix B, CC BY 4.0, `eq:ops`, `eq:Q`,
`eq:two-orders` and `lem:dual`. The accepted OpenAI source is pinned in
`certificates/selected-result.json`. The next question is whether multiple
independent low-support rows at a fixed output length can further narrow
the gap to rank 4h, with actual binary-codebook coverage addressed separately.
