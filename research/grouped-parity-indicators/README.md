# Grouped parity indicators: exact cost certificates

Status: `scoped_checked` for registered finite checks; the written sufficient
interface is author-checked and awaits independent review. **The global 3-SAT
bound has not improved.** This is a checkpoint in the ongoing goal in
[issue #148](https://github.com/1337isnot1337/3-SAT/issues/148).

The [proof](PROOF.md) composes grouped Boolean indicators with the accepted
contraction theorem under explicit, simultaneous certificates for profile
count, wires, maximum tensor degree, entry computation, field embedding and
preprocessing. It credits the predecessor grouped-coefficient identity and its
persistent-degree obstruction; those are not claimed as new findings.

The executable checker computes actual Boolean cancellations and the exact
profile/index networks. It compares 1,163 weighted identities to direct truth
enumeration, visits 8,670 profiles, and checks 19,280 invalid index assignments.
It also exhausts all 203 groupings of one six-equation nonlinear fixture,
retaining four Pareto groupings. These are finite controls, not a fast
contraction implementation or an inference about unknown runtime constants.

A positive control lowers combined degree from four to three by grouping two
nonlinear equations. A negative control shows that one group containing h
disjoint quadratic equations still has degree 2h. Any proposed improvement
must charge that degree and the original-scope coefficient discovery cost.
The selected alpha remains 1/2 and no unrestricted time improvement is claimed.

Reproduce with Python 3.11+ and the standard library, from the repository root:

```sh
python3 -I -B research/grouped-parity-indicators/verify.py > /tmp/grouped-check.json
cmp /tmp/grouped-check.json research/grouped-parity-indicators/verification.json
make verify
```

The finite checker materializes small coefficient tables. The written
polynomial-space variant instead scans coefficients and profiles sequentially;
it is a sufficient algorithmic interface, not an implementation of the accepted
fast contraction. No independent review, formal verification, or priority is
claimed. Contributor: OpenAI Codex with substantial AI assistance, under
Apache-2.0. Canonical base `c600b21ee7800a49c05718a254be50168e6b355b`.
See [SOURCES.json](SOURCES.json) for exact predecessor file hashes.

Next: determine whether the special coefficient tensors can be split or
contracted with their generated boundary factors cheaply enough to pass the
certificate. A fast standalone coefficient oracle does not supply that
boundary contraction. No uniform construction for all sparse queries is known
from this checkpoint; the goal is still incomplete.
