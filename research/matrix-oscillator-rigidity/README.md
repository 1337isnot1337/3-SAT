# Matrix-valued oscillator rigidity

Status: `scoped_checked`; written all-size argument is author-checked and has
no independent review or formal verification. No SAT speedup is claimed.

This tests a stronger, explicitly assumed all-colour-pairs version of the
h=1 two-order relation in Anthropic's oscillator construction. The
[proof](PROOF.md) classifies its scalar matrix commutators as `C_k=kC` for one
symmetric matrix C. For the usual vacuum-derivative pairing, its nondegenerate
quotient has `rank(C)` oscillator colours at every grade; a positive rank
retains ordinary partition growth. A different identity, cross-grade coupling,
or different pairing remains open. The all-pairs relation is not derived from
the scalar source identity. This is neither a complete crossing construction
nor a lower bound on SAT algorithms.

From the repository root, using Python 3.11+ and the standard library:

```sh
python3 -I -B research/matrix-oscillator-rigidity/verify.py
make verify
```

The exact finite checker enumerates 4,096 three-grade binary matrix cases,
81 scaled matrices including nonzero controls, 236,196 direct polynomial
commutators, and 81 exact degree-two pairing ranks. These checks do not prove
the all-size classification or the Hilbert series.

The question and stopping condition were to determine whether scalar mixing
of a fixed number of colours changes the h=1 commutator obstruction under
this all-pairs hypothesis, including the pairing radical. A productive changed
premise would drop or replace that hypothesis, or change the pairing or
cross-grade algebra, and then prove the actual two-direction crossing and
complete entry, encoding, recursion, precision, and reduction costs.

Source: Anthropic, *A 2^{o(n)} Time Algorithm for 3-SAT*, Appendix B, Lemma 9,
source commit `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`; pinned captures
and licenses are in [the source scan](../recent-breakthrough-scan/SOURCES.json).
Credit the [sparse oscillator predecessor](../sparse-oscillator-locality/PROOF.md)
and the scalar weighted extension in [PR #43](https://github.com/1337isnot1337/3-SAT/pull/43).
Canonical base `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`. Contributor:
Cinna Davis with substantial OpenAI Codex assistance. New work is Apache-2.0.
