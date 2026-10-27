# 3-SAT bounds

Research toward faster worst-case algorithms for 3-SAT, starting from
OpenAI's October 25, 2026 theorem. The goal is to improve the accepted bound,
with complete algorithms, explicit cost accounting, and reproducible evidence.

We accept the OpenAI proof as true. Reproving or auditing that proof is not a
project task. The accepted baseline is deterministic exact counting for every
fixed clause width, with polynomial space. For general 3-CNF it gives

\[
  (n+m)^{O(1)}2^{O(n\log\log n/\sqrt{\log n})}
  = O^*(2^{n/(\log n)^{1/2-o(1)}}).
\]

For each fixed clause density \(m\le Dn\), the exponent improves to
\(O_D(n/\sqrt{\log n})\). Counting decides satisfiability by testing whether
the answer is positive. The theorem is [Theorem 1.1 in the frozen paper](upstream/openai-eth-2026/paper.pdf);
its source commit and hashes are in [SOURCES.json](SOURCES.json).

The main target is a larger denominator exponent \(\alpha>1/2\) in the
[Big O Speedrun problem](https://bigospeedrun.com/3sat). Removing a
\(\log\log n\) factor is also a useful improvement, but keeps \(\alpha=1/2\).
Decision algorithms may use random bits under the
[problem's rules](docs/PROBLEM.md); they need not retain exact counting or
polynomial space if the changed guarantee is stated.

Start with [AGENTS.md](AGENTS.md) and [autoresearch.md](autoresearch.md).
The [current state](docs/STATE.md), [construction map](docs/CONSTRUCTION.md),
and [task catalogue](docs/tasks.json) identify the first research lanes.
There are no local bound improvements yet. The
[selected-result record](certificates/selected-result.json) is the single
authority for the accepted baseline and any future selected improvement.

```sh
make verify
python3 scripts/tasks.py
python3 -m satbounds.cost certificates/models/general.json
python3 scripts/new_experiment.py my-idea --task weighted-modes --author 'Your name'
```

Python 3.11 or newer is sufficient; no third-party Python packages or network
access are needed for verification. `make verify` checks frozen source hashes,
repository metadata, local documentation links, exact cost bookkeeping, and
small SAT reference cases. It does not reprove the accepted theorem or run a
subexponential SAT implementation. The baseline algorithm has not been
implemented here.

For a small DIMACS fixture, `python3 -m satbounds.cnf path/to/formula.cnf`
prints the exact count. This reference enumerates assignments and defaults to
a 20-variable limit; it is intended for testing new ideas on small cases.

Contributions should follow [CONTRIBUTING.md](CONTRIBUTING.md).
The [workflow reference](docs/WORKFLOW.md) explains which parts of
`CrocSwap/integer-mult-bounds` were carried over. Original material is
Apache-2.0; the unchanged OpenAI source retains its license and attribution.
The initial repository was prepared with OpenAI Codex assistance.
