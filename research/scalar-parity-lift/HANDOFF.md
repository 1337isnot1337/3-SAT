# Handoff

Date: 2026-10-27. Canonical base: `fd6df02023122badbdd888803146f0bd92002214`.
Branch: `research/scalar-parity-lift`.

## Result and acceptance boundary

The scalar parity projector gives coefficientwise degree
`min(N,k(a+p-1))` modulo `2^p`, with exact zero-indicator values before
reduction. Grouped-network entries use polynomial space and the same
allowed subexponential-in-polylog entry budget. Taking p=f+1 yields
deterministic exact branch counts. The accepted contraction theorem
applies with scalar coefficients, ell=1.

The degree envelope and coefficient representation improve, but the
full general-density time is unchanged and alpha is still 1/2. This
package is author-checked and AI-assisted; it is not independently
reviewed or selected. Its finite oracle is not a fast SAT solver.

## Evidence

[verification.json](verification.json) is deterministic output from
`python3 -I -B research/scalar-parity-lift/verify.py`. It includes exact
source and artifact hashes, separate coefficient calculations, truth
table comparisons, explicit grouped contractions, precision/branch
checks and failure controls. `make verify` checks source integrity and
repository consistency plus 17 tests. Neither command mechanically
verifies the written asymptotic proof.

At the submission boundary, concurrent PR 3 had developed the same
scalar cutoff and support-entropy conclusions, crediting the initial
`ca0a7f5` checkpoint. Its observed head was
`10e6eafc5fbf18325968218b7773e9175a11a4ef`. Preserve that credit and
coordinate any eventual integration; the two packages are overlapping
derivations and checks, not two distinct exponent improvements.

## Do not repeat unchanged

- Reducing k(a+f) by one fails: the cyclic two-monomial examples have a
  unique surviving top coefficient 2^f modulo 2^(f+1).
- Merely using this scalar lift does not reduce the generic monomial
  indexing to O(n) wires: the cyclic L-term family in Section 6 has
  L^n retained odd coefficients and no high-incidence branch. This is
  an encoding obstruction, not a lower bound on preprocessing or SAT.
- Evaluating the OpenAI deformation at an even nonzero node does not
  preserve its value modulo two. Section 7 gives W_00(0)=1 and
  W_00(-2)=0 despite shifted integrality. A global congruence would
  need an additional proved hypothesis.

## Changed premises worth testing

1. Aggregate coefficient families or change the equation row basis
   before incidence indexing. The support witness itself has a sparser
   basis, so it must not be cited as an obstruction to all such changes.
   Charge the transformed monomial list sizes and coefficient entries
   on every outer query, not only favorable selected systems.
2. Investigate the different operator pieces in the user's
   [Hexagon paper](EXTERNAL-COMPARISON.md). The full piece contract,
   rather than a finite count, is the target. Its current rho=1/sqrt(2)
   gives alpha=1/2; a smaller rho with the uniform costs preserved
   could improve that saving under the stated master recursion.

For the latter, first inspect live work and fetch canonical main again.
One concrete bounded experiment is the actual row/column flattening
ranks of small Appendix-B pieces versus their partition-space bounds.
No such rank screen was run here. Do not infer a new asymptotic exponent
from a finite rank reduction. Preserve the external version, hash,
license and formal-source pin in [EXTERNAL-SOURCES.json](EXTERNAL-SOURCES.json).
