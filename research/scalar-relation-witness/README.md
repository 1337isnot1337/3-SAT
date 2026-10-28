# Hook witnesses for uncharged crossing pieces

Status: `scoped_checked`. Written proof is author-checked, AI-assisted and
not independently reviewed. No improved rho, SAT time bound, or selected
result is claimed. Task: `contraction-schedule`; base
`630041c9da3a26edb8c8f59d5f8a4132a188c8bd`. Contributor: Cinna Davis
with substantial OpenAI Codex assistance.

The [proof](PROOF.md) gives an all-h lower bound 2h on the shift-span rank
of full partition-space operator pieces using explicit symmetric and
antisymmetric hook-partition entries and a moment-separated diagonal entry.
Low-support witnesses strengthen this to
`2h+max(0,floor((floor((2h-3)/3)-1)/2))`. Their input can be absent from the source
codebook. The proof also shows
that the fixed all-ones label slice has symmetric positive and negative
shifts and at most 2h directions, using an exact second-moment identity on
every energy space. The prior uncharged first-moment relation bounds full
rank by 4h; the remaining gap is open. A binary codebook containing the two small reference states and
q of the specified hooks inherits rank at least 2q. The source's actual
lexicographic codebook may omit hooks; do not substitute 2h for 2q there.
For sufficiently large parameters it contains at least
`(2/kappa-o(1)) sqrt(h) log(h)` hooks, with `kappa=pi sqrt(2/3)`.
Consequently its rank is at least
`(8 log(2)/kappa^2-o(1)) lambda log(lambda)`.

The hook construction is a partial answer to the all-size question raised
by [PR #10](https://github.com/1337isnot1337/3-SAT/pull/10), which proved
the first-moment relation and verified full 4h rank only at three finite
binary sizes. Its operator implementation and Anthropic source are used
unchanged; see the predecessor's [source pins](../anthropic-operator-ranks/SOURCES.json)
and `eq:ops`, `eq:Q`, `eq:two-orders`, `lem:dual`, and `thm:halfpieces`.
The accepted OpenAI theorem and `upstream/` remain unchanged.

Reproduce with standard-library Python, from the repository root:

```sh
python3 -I -B research/scalar-relation-witness/verify.py
make verify
```

The first command checks both families of endpoint formulas, the low-support witness against the h=6 recurrence and
a normal-order formula on a larger finite range,
symmetry, support and exact integer entries for h=2,...,6, plus full-rank modular triangular minors; it
also checks second moments for all-ones labels at h=1,...,4, and the mixed
and diagonal identities at h=2,...,4, with E=0,...,h+1. It checks the
sufficient codebook inequalities through h=1000, including largest-part
counts with coefficient c=1/2 for 11<=h<=1000 and reports actual codebook coverage for lambda=1,2,3. The all-size
conclusion is the written argument, not an extrapolation from the finite
screen. The [saved output](verification.json) can be compared byte-for-byte
with a fresh run. The checker invokes the predecessor's recurrence and is
not an independent implementation, formal proof or full SAT replay.

This is a rank lower bound and a screen limitation, not a new algorithm;
there is no claimed reduction to cost, precision, recursion, amplification
or output recovery. A genuine improvement would need a realizable crossing
family and all those costs. The next question is whether additional label
choices can close the gap to 4h, or whether additional relations survive in the original lexicographic
codebook.
