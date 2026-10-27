# Recent SAT and contraction results: October 27, 2026

The scan found one directly useful additional construction: Anthropic's
[new paper](https://hexagonmath.org/2610.00577v1) attains fixed-width alpha
`1/2` through operator-based crossing decompositions. It supplies a different
improvement target. Among the other primary sources checked, none supplies
a larger all-input classical 3-SAT alpha. This is a bounded scan, not an
exhaustive bibliography.

Status: `scoped_checked` for source integrity and metadata. No independent
theorem review, external Lean build, or selected-result change. Contributor:
1337isnot1337, with substantial OpenAI Codex assistance.

Base: `fd6df02023122badbdd888803146f0bd92002214`. The accepted OpenAI
theorem and frozen sources are unchanged. Owner acceptance applies to that
theorem; Anthropic is a separately attributed external result here.

## What to incorporate

Read Anthropic's Theorem B and Lemmas 9-10 in Appendix B, together with
Definition 7 and Theorem A. They replace a crossing by polynomially many
integer pieces, each factoring cheaply in both directions. Operators on a
partition-graded ring give `rho=1/sqrt(2)`, and the square-growth schedule
gives `alpha=log2(1/rho)=1/2`. A smaller feasible rho, with all entry and
recursive costs paid, is a concrete new target. The elementary eight-square
route alone has `rho=11/12`, giving a weaker result.

The [method comparison](METHODS.md) states the interface and next experiments.
The paper also makes its dependence on k explicit:
`2^O(min{k^2 n log log n/sqrt(log n), k m/sqrt(log m)})` for normalized
inputs. Our accepted theorem fixes k and hides its dependence in constants.
This parameter dependence does not establish better fixed-k alpha or an
end-to-end time constant. The new theorem does not state the accepted
polynomial-space guarantee; it must not be imported silently.

## Other results checked

[SCAN.json](SCAN.json) records all 12 sources, versions, dates, actual reading
scopes and adoption decisions. Abstract-only checks are labelled as such.

| Source | Consequence for this project |
| --- | --- |
| [Shpilka, explicit exponent 9/4, Oct 27](https://eccc.weizmann.ac.il/report/2026/281/) | A new explicit matrix-multiplication exposition and base-size bound; useful if a changed subroutine uses large products. |
| [Solomonik-Blaser, aggregation, Oct 22 v2](https://arxiv.org/abs/2610.26563v2) | Exact and border-rank gadgets for selected batches. No improvement in omega; directional costs and border recovery need separate bounds. |
| [Jain-Peng-Stephan-Xiao, restricted #SAT, Oct 11](https://arxiv.org/abs/2610.15426v1) | Weighted counting improvements measured by clauses; possible restricted-instance fallbacks. |
| [Jain et al., Parity-SAT, May 15 v2](https://arxiv.org/abs/2605.14093v2) | Structural parity algorithms. Plain parity cannot decide SAT; a decision wrapper needs a paid guarantee. |
| [Jiang-Cai, PPSZ, July 12](https://arxiv.org/abs/2607.10697v1) | Already recorded here; retain as the constant-base comparison. |
| [Kutzkov, complementary branching, IJCAI 2026](https://ijcai.org/proceedings/2026/254) | Exact branching and a `1.637^n` bound; a possible finite fallback with alpha zero. |
| [Mohapatra, interpolation, published Oct 27](https://eccc.weizmann.ac.il/report/2026/278/) | A finite-field tool; current recovery is polynomial already, and algebraic and Las Vegas conditions need checking before transfer. |
| [Carenini, blocky matrices, Aug 22](https://eccc.weizmann.ac.il/report/2026/153/) | Improves `gamma^6` to `gamma^4` in the piece-count exponent. A blocky piece can have full rank; this is not automatically a cheap crossing. |
| [Brand et al., many-mode tensors, Feb 2026](https://eccc.weizmann.ac.il/report/2026/025/) | Relevant rank/circuit distinctions; neither substitutes for both directional bit costs without proof. |
| [Rossman-Zhu, SoS connection, Dec 2025](https://arxiv.org/abs/2512.01227v1) | Crossing and arithmetic-complexity context, not a SAT algorithm. |
| [Ben Daniel, affine isolation, Oct 8](https://arxiv.org/abs/2610.11432v1) | A scoped consequence of strong explicit isolation; do not assume that primitive for free or treat it as an unconditional runtime lower bound. |

These are technical leads, not automatic SAT improvements. News summaries
were excluded from the evidence; random-input and quantum-input guarantees
were excluded from all-input classical comparisons. Polynomial arithmetic
improvements were not presented as alpha gains.

## Source and formalization record

[SOURCES.json](SOURCES.json) pins 12 unmodified files, including both the
Hexagon v1 PDF and GitHub PDF, at formal repository commit
`16a5ce41304fcdaea4e0be7c132e1c361dc26da5`. Their bytes differ. Poppler
extraction becomes identical after removing the Hexagon watermark and
whitespace: [receipt](pdf-comparison.json). That is a text-extraction check,
not a general proof of PDF equivalence. Printed page 32's factorization
formulas were also visually inspected.

The GitHub files are Apache-2.0, with original
[LICENSE](sources/anthropic/LICENSE) and [NOTICE](sources/anthropic/NOTICE).
The Hexagon PDF is CC BY 4.0, with
[separate attribution](sources/anthropic/HEXAGON-LICENSE.txt).
The original README is preserved as `README.source.txt`; its relative links
refer to the full upstream project, which is not vendored. New analysis is
Apache-2.0.

The development pins Lean `v4.33.1` and Mathlib commit
`0df444a360eaa60ab8c11dca51a86af692955474`. Its paper and README report
standard-axiom, replay and Comparator/nanoda checks. The publisher's
[verify (eth) job](https://github.com/anthropics/formal-math/actions/runs/40442388505/job/121985557508)
was observed passing at the pinned commit. These are publisher claims and
a publisher CI receipt. This session did not build the 1,050-module proof,
reproduce its axiom output, or run an independent kernel. Pinned statements
and proof-index excerpts identify the exact contracts.

## Reproduce and continue

```sh
python3 -I -B research/recent-breakthrough-scan/verify.py
make verify
```

The standard-library checker verifies hashes, pins, license attribution,
metadata and verification scope, not cited proofs. To repeat the optional
PDF comparison, install Poppler and run:

```sh
python3 -I -B research/recent-breakthrough-scan/compare_pdfs.py
```

The concurrent [PR #5](https://github.com/1337isnot1337/3-SAT/pull/5)
already compares Anthropic's scalar parity encoding and identifies its
piece-rank target. That is predecessor context and overlaps the comparison
here. This package adds the broader scan, reusable source capture, explicit
reading scopes and transfer screens. No exclusive priority or independent
review is claimed. Next change one named operator or factorization and
account for its complete uniform construction and recursion.
