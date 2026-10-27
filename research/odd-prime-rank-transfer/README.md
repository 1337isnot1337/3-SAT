# Rational crossing ranks through exact integer query recovery

Status: `scoped_checked` for the named exact controls; the all-size argument
is author-checked and awaits independent review. No improved rho or SAT
bound is claimed. The accepted OpenAI theorem remains selected unchanged.

Task: `contraction-schedule`; base
`6245ff589cdd461c75114308f4571af45dfb809d` (PR 16).
Contributor: Cinna Davis, with substantial OpenAI Codex assistance.

## Result and changed premise

[PROOF.md](PROOF.md) gives a bounded randomized transfer for **uniform
rational** crossing pieces with proved two-direction rational rank bounds.
The pieces, nonzero rational normalizer and each exact rational entry must
be computable in `2^O(lambda)` bit time; piece count stays polynomial.
Polynomial-height integer factors and normalizers are no longer required.

The transfer uses one large odd prime, generic field rank factorizations
and exact recovery of each bounded signed integer network query. A single
global denominator-height bound covers all possible adaptive queries. At
most 64T primality tests give a strict time cap on every random outcome.
For each fixed input, success exceeds 99/100. Any returned query/count is
exact; failure yields a flag, or NO for decision. Unsatisfiable formulas
always return NO. The source's same master time envelope follows under
the rank-only contract, with explicit exponential-space compilation.

The dense reduction is kept over the integers. Each network query is
recovered before greedy comparisons and modulo-two sums. In particular,
an odd-prime residue is not used as a parity/count residue directly, and
the final count bound is not substituted for larger intermediate bounds.
Prime bit size, all rejected candidates, denominators, branches, queries,
factor construction, recursion and output recovery are charged.

This is a sufficient interface for future rank constructions. It proves
no smaller ranks, fixes no singular pairing and does not implement a new
full SAT algorithm. It does not preserve polynomial space. A normalization
acting across a required cut can still destroy its rank advantage.

## Actual stress construction

[CONJUGATION.md](CONJUGATION.md) applies `B=2I-S_N` to one string axis and
B inverse to the opposite axis. This preserves the exact crossing sum and
both flattening ranks while allowing dyadic denominators exponential in
lambda. The all-size formulas supply the denominator-growth argument;
the finite screen is not extrapolated.

At N=8 the checker uses four actual predecessor pieces, verifies 8,192
exact crossing entries, preserves both rank envelopes over F101, and
recovers all 256 Boolean predicate counts. The observed maximum denominator
is 2^9. This basis change cannot improve rho; it tests the relaxed rational
coefficient interface.

## Reproduction and evidence limits

Standard Python only, offline:

```sh
python3 -I -B research/odd-prime-rank-transfer/verify.py
python3 -I -B research/odd-prime-rank-transfer/crossing.py
make verify
```

The first command checks 2,387 rational field-matrix cases, 738 bad
denominator rejections, 19,388 signed query recoveries and every prime in
the dyadic intervals T=8,...,16. It checks capped all-composite failure,
first-prime selection, a zero normalizer, insufficient intermediate range
and an incorrect signed-to-modulo-two conversion. The second command is
the actual rational crossing test above. Saved outputs are hash-bound.

The finite tests use trial division on small prime fixtures. The all-size
proof uses the established deterministic polynomial-time primality theorem,
including its published correction. No AKS implementation, full recursive
master solver, full dense-reduction replay, human review or formal proof
is claimed. The stated transfer is a written mathematical argument with
bounded component evidence.

## Sources, credit and next question

[SOURCES.json](SOURCES.json) pins the source contract/master analysis,
Rosser--Schoenfeld's explicit prime bounds and the primary AKS paper with
its correction. Prime sampling, bad-prime exclusion and Gaussian
elimination are standard methods; no novelty is claimed for them.
The new interface combines them with exact integer query recovery and
the full adaptive cost boundary. No third-party source is redistributed.

PR 16 supplies the deterministic two-adic rank compiler and precision
ledger. The actual test family comes unchanged from PR 15 and its PR 14
Pauli/Bell engine before the stated conjugation. The operator-rank package
and PR 11 charged moments motivated the normalization question; neither
is promoted by this transfer. All new work is Apache-2.0 and substantially
AI-assisted.

The next target is a cheaper **valid rational rank family**. Expensive
integer normalization alone is now an insufficient reason to discard a
uniform rational candidate. Valid crossing identities, both cut ranks,
piece count and uniform generation still need proof. The live checkpoint
is [CHECKPOINT.md](CHECKPOINT.md); the user goal remains active.
