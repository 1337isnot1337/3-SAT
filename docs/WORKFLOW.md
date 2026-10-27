# Workflow origin and repository layout

The reference was `CrocSwap/integer-mult-bounds` at
[`de5ec2e7a6074068452f45b1a191b5c72832df4a`](https://github.com/CrocSwap/integer-mult-bounds/tree/de5ec2e7a6074068452f45b1a191b5c72832df4a).
Its root instructions, contribution guide, selected-result record and minimal
package guide were reviewed. Its mathematical constructions and historical
research archive are unrelated to this project and were not imported.

| Reference pattern | Initial 3-SAT implementation |
| --- | --- |
| One selected-result authority | `certificates/selected-result.json` |
| Source-bound results | Frozen `upstream/` plus `SOURCES.json` |
| Current task cards | `docs/tasks.json` with concrete first steps and stopping rules |
| Donated-session entry point | `autoresearch.md` and a reusable donation prompt |
| Scoped evidence and handoffs | `research/<slug>/README.md` and `CLAIM.json` |
| Exact-cost comparison before expansion | `satbounds/cost.py` and baseline models |
| Scope-aware review | `CONTRIBUTING.md`; archive intake does not select a theorem |
| Cheap reproducible checks | `make verify`, offline source/metadata checks and targeted tests |

We did not copy its mature queue machinery, thousands of historical packages,
task weights, Discussion IDs, conditional assumptions, or frontier values.
The 3-SAT baseline is accepted as a theorem by owner direction. Additional
coordination machinery should be added when the work actually requires it.

Use `research/` for scientific attempts, `certificates/` for selected state and
small machine-readable evidence, `satbounds/` for shared reference tools,
`scripts/` for workflow tools, and `tests/` for meaningful failure controls.
New external sources should have separate source pins and attribution; never
edit an old frozen source to make a new proposal pass.
