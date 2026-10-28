# 3-SAT bounds

[![Verify](https://github.com/1337isnot1337/3-SAT/actions/workflows/verify.yml/badge.svg)](https://github.com/1337isnot1337/3-SAT/actions/workflows/verify.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB)](#quick-start)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-59636e)](LICENSE)

An open research effort to improve worst-case algorithms for 3-SAT.
We start from OpenAI's October 2026 subexponential-time theorem and work toward
stronger bounds, with explicit cost accounting and reproducible results.

[Start contributing](autoresearch.md) · [Research directions](docs/RESEARCH.md) ·
[Read the paper](upstream/openai-eth-2026/paper.pdf) · [Current state](docs/STATE.md)

## Starting point

We accept the OpenAI proof as true and use it as the foundation for new work.
For a 3-CNF formula with $n$ declared variables and $m$ clauses, the accepted
algorithm counts satisfying assignments deterministically in polynomial space
and time

```math
T(n,m)=(n+m)^{O(1)}\,2^{O\!\left(\frac{n\log\log n}{\sqrt{\log n}}\right)}.
```

For each fixed clause density $m\le Dn$, the exponent is
$O_D(n/\sqrt{\log n})$. A positive count decides satisfiability.
The source is [Theorem 1.1](upstream/openai-eth-2026/paper.pdf), with the sharper
construction in Appendix D. The original PDF and TeX files are frozen in this
repo, with their commit and hashes recorded in [SOURCES.json](SOURCES.json).

The main target is to improve the denominator exponent in the
[Big O Speedrun problem](https://bigospeedrun.com/3sat):

```math
O^*\!\left(2^{\,n/(\log n)^{\alpha-o(1)}}\right),
\qquad \alpha>\frac12.
```

Removing a $\log\log n$ factor is also useful progress, with the same
$\alpha=1/2$. Decision-only and randomized approaches are welcome under the
[problem's rules](docs/PROBLEM.md).

**Current status:** the accepted alpha is still $1/2$. No local package claims
a better complete SAT time envelope or removal of the general-density
$\log\log n$ factor. The
[selected-result record](certificates/selected-result.json) tracks that state.

## Research progress

The merged work now includes constructive component changes as well as scoped
obstructions. These are author-checked research packages, with their proof,
reproduction commands and limits recorded separately.

| Component | Result and remaining limit |
| --- | --- |
| [Scalar parity encoding](research/newton-parity-compression/README.md), with [separate cross-checks](research/scalar-parity-lift/README.md) | A smaller retained-degree bound and scalar coefficient ring for exact counting. Actual nonzero support still has enough entropy to require the same wire order in this encoding. |
| [Newton Cauchy modes](research/cauchy-newton-modes/README.md) | Stronger coefficient valuations reduce the leading constants in the mode-count envelope, including a stronger odd-node case. The square-root-logarithmic saving remains. |
| [Anthropic operator pieces](research/anthropic-operator-ranks/README.md) | An exact first-moment relation removes one crossing piece while preserving both factorization costs. It does not reduce the dominant piece-cost ratio. |
| [Weighted decision fingerprints](research/characteristic-two-decision/README.md) | A characteristic-two decision interface avoids cancellation of the unweighted parity count. The current degree and wire-entropy costs remain. |
| [Asymmetric charged crossings](research/charged-asymmetric-crossing/README.md) | A uniform rational construction removes the central shift while retaining both rank bounds. The supplied factorization ratio is unchanged. Fixed-codebook screens at [grades four and six](research/asymmetric-scalar-filter/README.md) and [grade nine](research/grade-nine-filter/README.md) do not resolve other codebooks or all grades. |
| [Sparse-support detection](research/sparse-support-deterministic/README.md) | A deterministic fingerprint test works under a promised support bound. Its conditional SAT composition retains the accepted time envelope; it does not provide a general speedup. |
| [Separator hierarchies](research/separator-hierarchy/README.md) | A supplied hierarchy can be composed with the accepted counting algorithm. Bounded occurrence alone does not guarantee the small separators needed for a general improvement. |
| [Clause-polynomial rank](research/clause-polynomial-rank/README.md) | Linear relations among original clause polynomials alone cannot generally remove the density dependence. The result does not exclude nonlinear or formula-aware preprocessing. |

The obstruction packages narrow specific routes:
[formal mode counts, tapering and local bases](research/mode-taper-obstructions/README.md),
[generic recovery precision, even for parity](research/parity-recovery-precision/README.md),
and [sparse oscillator indices in the unchanged operator identity](research/sparse-oscillator-locality/README.md).
They do not rule out every contraction or decision algorithm.

The [primary-source comparison](research/recent-breakthrough-scan/METHODS.md)
adds Anthropic's independently developed operator/partition construction as a
second mechanism to improve. Its stated alpha is also $1/2$. A smaller feasible
two-direction factorization cost, or aggregation that removes a dominant
enumeration cost, would be a substantive next step. Improving a finite rank,
one direction alone, or an unchanged polynomial subroutine is insufficient.

Merging a package archives its stated result; it does not independently review
the proof or select a new SAT bound. Check live PRs before starting another
attempt, and read the package handoffs before repeating a tested route.

## Quick start

Requires **Python 3.11+**. Verification uses the standard library and runs offline.

```sh
git clone https://github.com/1337isnot1337/3-SAT.git
cd 3-SAT
make verify
```

Without Make, run `python3 -B scripts/verify.py` followed by
`python3 -B -m unittest discover -s tests -v`.

Explore a task, compare cost envelopes, or try a small SAT instance:

```sh
python3 scripts/tasks.py --task weighted-modes
python3 -m satbounds.cost certificates/models/general.json
python3 -m satbounds.cnf examples/tiny.cnf       # 3 satisfying assignments
python3 -m satbounds.cnf examples/unsat.cnf      # 0 satisfying assignments
```

The cost tool compares exact symbolic exponents under supplied assumptions.
The SAT counter is an exhaustive reference for small experiments, with a default
20-variable limit. The subexponential algorithm is not implemented here.

## Where to contribute

| Direction | Starting question |
| --- | --- |
| [Weighted modes](docs/RESEARCH.md#weighted-modes) | Can the actual mode structure reduce enumeration? |
| [Contraction schedule](docs/RESEARCH.md#contraction-schedule) | Can packing and recovery, or the alternative operator pieces, lower the dominant cost? |
| [General-density encoding](docs/RESEARCH.md#general-density-encoding) | Can sparse queries use fewer wires? |
| [Decision-only algorithms](docs/RESEARCH.md#decision-only-algorithms) | Can SAT decision avoid the cost of exact counting? |
| [Complete cost accounting](docs/RESEARCH.md#complete-cost-accounting) | Does a proposed gain survive every other cost? |

Each [task card](docs/tasks.json) names a first experiment, existing evidence,
and stopping conditions. Check [open PRs](https://github.com/1337isnot1337/3-SAT/pulls)
and [Issues](https://github.com/1337isnot1337/3-SAT/issues) for overlap before
choosing work. Partial results, useful obstructions, and reproducible failed
approaches are welcome alongside complete improvements.

## Make a contribution

Read [AGENTS.md](AGENTS.md), [autoresearch.md](autoresearch.md), and
[CONTRIBUTING.md](CONTRIBUTING.md), then create a focused research package:

```sh
git switch -c research/my-idea
python3 scripts/new_experiment.py my-idea \
  --task weighted-modes --author 'Your name'
```

The generator records the base commit and accepted source in a draft package.
Add the changed construction, complete cost, evidence, and remaining questions.
Run its scoped checks and `make verify` before submitting a PR.

To donate an agent session, use the [ready-to-copy prompt](autoresearch.md#donation-prompt).

## Repository guide

| Guide | Contents |
| --- | --- |
| [Current state](docs/STATE.md) | Accepted result and current project state |
| [Construction map](docs/CONSTRUCTION.md) | Accepted algorithm and its improvement points |
| [Result records](certificates/) | Selected-result record and exact cost models |
| [Research packages](research/) | Scoped attempts, evidence, and handoffs |
| [Reference tools](satbounds/) | Shared cost and SAT reference tools |
| [Examples](examples/) | Small runnable DIMACS formulas |
| [Original sources](upstream/) | Unchanged OpenAI paper, TeX sources, and license |

`make verify` checks source integrity, metadata, local links, cost bookkeeping,
and SAT reference cases. Passing these checks validates that stated scope;
new asymptotic claims need their own complete argument and review.

## Sources and credit

The starting theorem is OpenAI, *The Exponential Time Hypothesis is False*,
revised October 25, 2026 ([frozen source](upstream/openai-eth-2026/README.md)).
See [CITATION.cff](CITATION.cff) for citation metadata.

Anthropic's [*A $2^{o(n)}$ Time Algorithm for 3-SAT*](https://hexagonmath.org/2610.00577v1)
is pinned and compared in the [source scan](research/recent-breakthrough-scan/README.md).
The paper supplies another construction with the same stated exponent; its
Lean-development claims and the checks actually run here are distinguished
in the package. Its own license and attribution are retained with the source.

The research workflow draws on
[CrocSwap/integer-mult-bounds](https://github.com/CrocSwap/integer-mult-bounds);
[docs/WORKFLOW.md](docs/WORKFLOW.md) records what was carried over.
Original repository contributions are [Apache-2.0](LICENSE). Upstream attribution is preserved
in [NOTICE](NOTICE). This repository was prepared with OpenAI Codex assistance.
