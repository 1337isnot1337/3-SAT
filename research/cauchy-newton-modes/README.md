# cauchy-newton-modes

Status: draft component checkpoint; independent review pending.

Task: `weighted-modes`. Base commit: `fd6df02023122badbdd888803146f0bd92002214`.

Contributor: 1337isnot1337; substantial OpenAI Codex assistance. Disclose substantial AI assistance.

## Question and changed premise

Replace geometric Cauchy modes by the finite rational Newton identity in
[PROOF.md](PROOF.md). The OpenAI theorem is accepted as true.

## Statement and scope

The proposed row coefficients have valuation at least
`a+1-i+3k-2 popcount(k)`, using one mode per tile and index. The formal
enumeration envelope improves by `1/sqrt(3)` in its leading coefficient.
The full asymptotic exponent and alpha do not change. The derivation and
the integration into the accepted recursion are written out; the extension
ring and combined-network checks remain to be added.

## Complete cost

The proof accounts for the unchanged child size, precision, entry evaluation,
descriptions, recovery and outer costs. No complete SAT implementation or
larger-alpha claim is made.

## Evidence and reproduction

`python3 -I -B research/cauchy-newton-modes/explore.py` checks the exact
rank decomposition over rational points for all tile lengths 1 through 15.
It passed on October 27, 2026. `make verify` passes 17 tests and the frozen
source and repository checks. This scratch checker uses only standard-library
Python; it is not a contraction implementation.

## Limits and open next questions

Next add bounded checks over a nontrivial unramified extension, negative
controls for the integrality hypothesis, and a small whole-network identity.
Then publish a reproducible result with saved output and explicit coverage.
The root `M/sqrt(u)` scale is unchanged; a larger alpha needs another idea.

## Sources and credit

Source labels and predecessor credit to PR #1 are given in the proof. Frozen
upstream commit: `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`; see
[SOURCES.json](../../SOURCES.json). No scientific-priority claim is made.
