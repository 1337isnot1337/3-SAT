# Three-partition low-shift space

Status: `scoped_checked`. This is an author-checked, AI-assisted argument,
not an independent or formal review. No improved SAT bound or selected
result is claimed. Base `f1c4ec3a48b823ab749f93cfe8f81dfe8ca0336f`;
task `contraction-schedule`; contributor Cinna Davis with substantial
OpenAI Codex assistance.

The [proof](PROOF.md) improves PR #59's uncharged **full partition-space**
shift-rank lower bound to
`2h+max(0,h-4)+2 max(0,floor(h/2)-2)+[h>=4]+2[h>=6]+[h>=9]`:
4h-4 for even h>=10 and 4h-5 for odd h>=9. An explicit normal-order
formula identifies three-part output rows with their partition multiplicity
vectors. Their span has dimension h-3; its h-4-dimensional kernel at the
one-part coordinate gives low-support rows independent of PR #59's hook and
moment witnesses. A diagonal low-support row adds one further symmetric
direction, another two-part input adds two for h>=6, and a further input
adds one for h>=9. Two-part
constructions in opposite label orders supply two independent
one-sided low-support spaces, also independent of the symmetric space.

The added input state `(h)` may be omitted by the original binary codebook.
The previous encoded-codebook bound is unchanged. A rank obstruction for
this family does not by itself constrain changed pieces or improve a SAT
running time. The selected owner-accepted baseline is unchanged.

Reproduce offline, with Python 3.11+ and standard library:

```sh
python3 -I -B research/low-shift-cancellation/verify.py
make verify
```

The checker compares the three-part normal-order formula with the original
PR #10 recurrence for all three-part and both orders of two-part outputs
at h=4,5,6. For
h=4,...,40 it checks the three-part formula against an independently
enumerated normal-order sum and verifies the h-3, h-4 and one-sided
multiplicity-vector ranks, and the combined low-support rank, modulo a prime.
The saved [output](verification.json) can be compared byte-for-byte. The
modular ranks are finite lower bounds; the upper bounds and all-size claim
are the written argument, not an independent or formal verification.

Sources are PR #59's [proof and source pins](../scalar-relation-witness/PROOF.md)
and [PR #10's source record](../anthropic-operator-ranks/SOURCES.json):
Anthropic, Hexagon 2610.00577v1, Appendix B, CC BY 4.0, `eq:ops`, `eq:Q`,
`eq:two-orders` and `lem:dual`. The accepted OpenAI source is pinned in
`certificates/selected-result.json`. The next question is whether another
input or label family can fill the remaining rank gap to 4h, with actual
binary-codebook coverage addressed separately.
