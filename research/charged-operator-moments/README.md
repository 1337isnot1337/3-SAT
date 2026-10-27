# Charged crossing pieces and an exact first-moment pairing

Adding a scalar zero mode D_0=q Id preserves the crossing sum and its two
factorization envelopes. It changes the first moment into a nonzero pairing.
After diagonal normalization, that pairing is `q h! P L`, where L is a
translation derivative and `L P=0`. On the full weight-h space, h>=2,
its rank for nonzero charge is exactly `p(h)-p(h-1)` and its square is zero.

Status: `scoped_checked` for bounded exact checks. The written all-size
arguments are author-checked, AI-assisted and not independently reviewed.
There is no larger alpha or improved full SAT time envelope. The accepted
OpenAI theorem and selected result are unchanged.

## Changed mechanism and result

The source is [Anthropic's Appendix B](https://hexagonmath.org/2610.00577v1),
with formal repository commit `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`.
The source excludes index zero. This variation allows it, with the
normal-ordered coefficient specified in [PROOF.md](PROOF.md).
The proof derives the unchanged zeroth crossing and the charged first
moment directly from contractions, then identifies its polynomial formula.

This supplies a family of crossing components with the original
`rho=1/sqrt(2)` ratio. The first-moment pairing is singular: every common
principal choice of label states is nilpotent by partition length. A naive
inverse therefore cannot remove the central piece. The image dimension
still has `log p(h)+O(log h)` label bits, leaving a possible asymmetric
recovery route. Uniform coordinates, denominators and bit heights for
that recovery remain obligations; a generic inverse is insufficient.

The polynomial module provides explicit right inverses for the separate
translation and invariant-image maps. Those identities are not yet a
complete uniform choice of dual label coordinates or a faster algorithm.
Even deleting only the central shift would leave nearby shifts with the
same leading ratio. A larger alpha needs a further change.

## Evidence and reproduction

```sh
python3 -I -B research/charged-operator-moments/verify.py
make verify
```

The checker uses standard-library Python. [Saved output](verification.json)
records 448 independent normal-order/recurrence comparisons, including
112 zero-charge predecessor controls; 144 contraction-binomial identities;
917 first-pairing entries at full grades h=2..8; 608 zeroth/first-moment
cases on positive input grades and charges -1,0,1,2; and 3,224 full
output-vector comparisons of the two operator orders.

A separate polynomial formula checks square zero, the Weyl commutator,
275 right-inverse cases and exact ranks through h=10. Its larger-rank
cases do not enumerate the charged operators at those energies. The
finite direct-operator ranks at h=2..8 are 1,1,2,2,4,4,7, matching the
written all-size formula. Label-capacity inequalities are checked through
h=128. The proof, code and source metadata are SHA-256 bound in the output.

These are finite component checks, not mechanical verification of the
all-size proof or implementation of a full SAT algorithm. The checker
runs in under a minute on the authoring host and is separate from default CI.

## Source and predecessor credit

Contributor: 1337isnot1337, with substantial OpenAI Codex assistance.
New analysis and code are Apache-2.0. The predecessor
[PR #10](https://github.com/1337isnot1337/3-SAT/pull/10) already supplies
an exact uncharged rank screen and its zero first-moment relation.
This package copies that work's operator module unchanged as
`predecessor.py`, pinned at commit
`3f38ce1313a6c34e67f8d45ea4f94121e908fa48` with its hash and attribution
in [SOURCES.json](SOURCES.json). It does not repeat the uncharged rank screen
or claim exclusive priority. The [literature scan](../recent-breakthrough-scan/README.md)
retains the external paper, licenses and formalization evidence boundaries.

The next concrete task is a uniform nondegenerate pairing on selected row
and column image coordinates, with all integer costs charged. Reopening
whole-space inversion or repeating the same finite rank list is not useful.
