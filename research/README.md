# Research packages

Each attempt belongs in `research/<slug>/`, with a concise README and a
machine-readable `CLAIM.json`. Those claim files form the local attempt ledger;
the selected result is maintained separately. Do not rename a predecessor's
package or overwrite its frozen evidence to represent a successor.

Create a draft with:

```sh
python3 scripts/new_experiment.py my-idea --task weighted-modes --author 'Your name'
```

Record the exact base commit, source commit/labels, claim scope, changed premise,
complete costs, commands and actual evidence, failed routes, remaining obligations,
and open next questions. Use `draft` until evidence supports a narrower status.
Evidence paths are relative to the repository root; reproduction commands are
argument arrays. Default CI validates the metadata but does not automatically
execute arbitrary package commands. Run those commands explicitly and preserve
their outputs when they support a claim.

The initial [baseline-cost-model](baseline-cost-model/README.md) is bookkeeping
infrastructure. There is no new 3-SAT bound here. A finite check, a conditional
cost envelope, an implemented algorithm and a proved asymptotic improvement are
different outcomes. The accepted OpenAI theorem does not need another audit.
