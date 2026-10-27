# Charged operator moments: active checkpoint

Status: draft. No all-size component theorem or improved SAT bound is claimed
at this checkpoint. Contributor: 1337isnot1337, with substantial OpenAI Codex
assistance. Apache-2.0.

This tests a different representation of Anthropic's Appendix-B fields:
add the scalar zero mode D_0=q Id. The nonzero Heisenberg operators and
normal-ordered coefficients are retained. The external source is
[Hexagon 2610.00577v1](https://hexagonmath.org/2610.00577v1), formal commit
`16a5ce41304fcdaea4e0be7c132e1c361dc26da5`.

The precursor exact rank screen is already supplied by the concurrent
`research/anthropic-operator-ranks` branch. This package copies its
operator module unchanged as `predecessor.py`, with source commit and hash
in [SOURCES.json](SOURCES.json), and implements the charged extension in
[charged.py](charged.py). Credit belongs to that predecessor for the
original finite operator and rank routines. This is not a repeat of its
uncharged rank screen.

Initial exact checks pass 448 independent normal-order versus recurrence
evaluations, with zero-charge agreement to the predecessor. Zeroth and
first moments also pass on all labels at h=2,3,4, all input states through
energy 2, and charges -1,0,1,2. These checks are being assembled into a
saved deterministic reproduction artifact.

The exploratory [probe](probe.py) finds first-moment ranks 1,1,2,2,4,4,7
on the full partition-labelled spaces at h=2 through 8 in a separate run,
matching p(h)-p(h-1). The compact probe here prints the source's binary
prefix cases h=2,4,6. The first-moment pairing is singular, so a naive
inverse cannot recover an identity crossing. There is also a length
filtration pattern to explain algebraically.

Next derive the pairing and determine its image, coefficient heights and
uniform recovery costs. A finite rank pattern is not an asymptotic theorem;
no larger alpha, complete SAT implementation or independent review is claimed.
The accepted OpenAI theorem and selected result remain unchanged.
