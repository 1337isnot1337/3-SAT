# Research state

Bootstrap: October 26, 2026. Priority revision: 1.

The owner accepts OpenAI's October 25 theorem as completely true. The
[selected record](../certificates/selected-result.json) fixes that accepted
baseline at source commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`.
No baseline proof audit or reimplementation is required.

| Guarantee | Accepted bound |
| --- | --- |
| General fixed-width exact counting | `(n+m)^O_k(1) 2^O_k(n log log n / sqrt(log n))` |
| Fixed density `m <= Dn` | `(n+m)^O_k,D(1) 2^O_k,D(n / sqrt(log n))` |
| Space | `(n+m)^O_k(1)` bits |
| 3-SAT decision comparison | `alpha = 1/2`, deterministic |

The [source manifest](../SOURCES.json) pins the PDF, all four supplied TeX files,
the upstream README and license. The public Speedrun page labelled the result
Claimed at capture. Owner acceptance here is separate from that external label.
This repository has no selected improvement and no human or Lean review record.

The initial [cost-model package](../research/baseline-cost-model/README.md)
provides exact bookkeeping and counterexamples to misleading improvement
inferences. A small exhaustive DIMACS counter is a reference oracle for future
experiments. Neither tool implements the accepted subexponential algorithm.

First work should change a mechanism rather than repeat the baseline proof:
weighted modes, contraction architecture, a smaller general-density encoding,
or a decision-only alternative. See [tasks.json](tasks.json). The full cost
preflight is available for every proposed lane. All tasks start unclaimed;
check live PRs/Issues and local packages before choosing work.

Update this page, the selected record and affected task coverage when a reviewed
improvement is selected. Put individual attempts and handoffs in their own
research packages, not in a growing root diary.
