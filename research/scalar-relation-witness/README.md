# Hook witnesses for uncharged crossing pieces

Status: `scoped_checked`. Written proof is author-checked, AI-assisted and
not independently reviewed. No improved rho, SAT time bound, or selected
result is claimed. Task: `contraction-schedule`; base
`630041c9da3a26edb8c8f59d5f8a4132a188c8bd`. Contributor: Cinna Davis
with substantial OpenAI Codex assistance.

The [proof](PROOF.md) gives an all-h lower bound h on the shift-span rank
of full partition-space operator pieces using explicit hook-partition
entries, while showing that the fixed all-ones label slice has symmetric
positive and negative shifts and therefore at most 2h+1 directions. The
prior uncharged first-moment relation bounds full rank by 4h; the remaining
gap is open. A binary codebook containing the two small reference states and
q of the specified hooks inherits rank at least q. The source's actual
lexicographic codebook may omit hooks; do not substitute h for q there.

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

The first command checks endpoint formulas, symmetry, support and exact
integer entries for h=2,...,6, plus a full-rank modular triangular minor;
it reports actual codebook coverage for lambda=1,2,3. The all-size
conclusion is the written argument, not an extrapolation from the finite
screen. The [saved output](verification.json) can be compared byte-for-byte
with a fresh run. The checker invokes the predecessor's recurrence and is not an
independent implementation, formal proof or full SAT replay.

This is a rank lower bound and a screen limitation, not a new algorithm;
there is no claimed reduction to cost, precision, recursion, amplification
or output recovery. A genuine improvement would need a realizable crossing
family and all those costs. The next question is whether nonsymmetric
label choices can give a second triangular family or whether additional
relations survive in the original lexicographic codebook.
