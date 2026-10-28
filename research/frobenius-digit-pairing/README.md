# Finite-characteristic digit pairing

Status: `scoped_checked`; the all-size argument is author-checked and has not
been independently reviewed or formally verified. No SAT improvement is claimed.

For each original grade k, replace an unbounded occupation by base-p digits,
each stored in a truncated oscillator at grade `k p^j`. The [proof](PROOF.md)
gives a nondegenerate vacuum pairing on every grade and an exact bijection to
ordinary partitions. The dimension is therefore exactly P(E), with no
state-count saving. A direct vacuum witness shows that the obvious unit
creation/derivative operators fail the existing source h=1 two-order
identity in every characteristic. Carry-aware operators on the same digit
labels recover the source commutator, but their generated vacuum pairing
again has factorial radicals; that pairing is distinct from the full digit
pairing. The factorial obstruction follows for any operators with a scalar
commutator and the stated vacuum conditions, whenever the p-th raised state
is nonzero; extra annihilators remain possible. The representation supplies neither a crossing construction nor
an alternative complete SAT algorithm.

Reproduce with Python 3.11+ and the standard library:

```sh
python3 -I -B research/frobenius-digit-pairing/verify.py
make verify
```

The finite replay checks 52 grade bijections through grade 12 over four prime
fields, 1,088 nonzero diagonal pairings, and 15,219 direct operator
comparisons across all three-mode digit states for p=2,3,5,17, plus 4,848
carry-commutator and pairing formula checks. These finite
checks do not replace the written proof or verify any SAT algorithm.

The local number of usable digit variables through grade E is at most 2E;
single entries and encoding are polynomial in E and log p, but all P(E)
label states remain. The distinct missing obligations are the actual
crossing identity and its two directional factors, label recovery in that
identity, normalizers, source entries, recursion, reductions, finite field
choice, bit complexity and space. A genuinely changed two-order identity or
operator realization is needed to reopen this route.

This builds on the merged [weighted oscillator and characteristic-p pairing
analysis](../weighted-oscillator-rigidity/PROOF.md), and the original
[sparse-oscillator test](../sparse-oscillator-locality/PROOF.md). Anthropic,
*A 2^{o(n)} Time Algorithm for 3-SAT*, Appendix B, Lemma 9, pinned source
commit `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`; retained source and license
are recorded in [the source scan](../recent-breakthrough-scan/SOURCES.json).
Repository base `4ce0cb947bdb6837718c7061e45d3a723219d703`. Contributor:
Cinna Davis, with substantial OpenAI Codex assistance. New material Apache-2.0.
