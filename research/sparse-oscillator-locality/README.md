# Sparse oscillator locality screen

Deleting oscillator indices does not preserve the unchanged operator identity
in Anthropic's Appendix B. At the first missing index m, the h=1 identity
has the exact defect `m Id`. Square-only oscillators already fail at m=2.
This refutes a precise candidate extension; it is not a refutation of the
source theorem or a lower bound for arbitrary SAT algorithms.

Status: `scoped_checked` for bounded exact checks. The written all-size
arguments are author-checked with substantial OpenAI Codex assistance and
have no independent review. The accepted OpenAI bound is unchanged.

## Question and result

The [recent literature scan](../recent-breakthrough-scan/README.md) identified
an alternative route to alpha: keep a smaller graded space while retaining
cheap crossing pieces in both directions. Partitions into squares have
`log dimension = Theta(E^(1/3))`, suggesting a conditional alpha target of
2/3 if the entire operator, pairing and cost interface could be preserved.

The [proof](PROOF.md) tests that missing condition first. In the source's
h=1 case, reversing the operator factors changes Q_s by the second
finite difference of `g(k)=k[|k| in S]`. Equality at every shift forces
S to be the full positive integers if 1 is retained. A first omission gives
an explicit scalar defect on every polynomial. Infinite zero-density
index sets also have a nonrational scalar commutator series, so a finite
polynomial-denominator repair of that same series cannot work.

The proof supplies an elementary all-size growth argument for partitions
into qth powers, and checks the separate arithmetic-thinning proposal:
fixed-spacing modes rescale energy without changing the square-root
dimension ratio. An instance-dependent spacing must stay fixed when the
same instance's label and intermediate grades are compared.

## Reproduction

```sh
python3 -I -B research/sparse-oscillator-locality/verify.py
make verify
```

[Saved output](verification.json) records 34,080 exact operator comparisons
for all 128 index subsets containing 1 within 1..8, shifts -7..7, and all
allowed monomials through grade 6. There are 127 explicit first-omission
witnesses; the full-index interior is a passing control. The square-only
vacuum at shift 2 gives original order 0 and reversed order 1. The checker
also includes exact restricted partition counts and 1,032 arithmetic
energy-rescaling checks. It uses standard-library Python and takes under
a second on the authoring machine. No source theorem or formal development
is mechanically verified.

The proof and checker are SHA-256 bound in the output. Neither a complete
subexponential contraction nor a SAT solver is implemented. Reported alpha
values for the changed grade-growth models remain explicitly conditional.

## Sources, overlap and next premise

Claude (Anthropic), [Hexagon 2610.00577v1](https://hexagonmath.org/2610.00577v1),
Appendix B, Lemma 9 and equations (47)-(48); formal repository commit
`16a5ce41304fcdaea4e0be7c132e1c361dc26da5`. The merged
[source capture](../recent-breakthrough-scan/SOURCES.json) retains both
PDFs, license attribution and formal-statement excerpts. No external proof
build was run. New analysis is Apache-2.0 and AI-assisted.

PR #5 already identifies the general smaller-rho target. This package tests
the distinct sparse-index premise, rather than claiming ownership of the
overall piece-rank program. It credits the source identity and makes no
priority claim.

Do not repeat a dimension-only scan of the same thinned operators. Reopen
after specifying different coefficients or another graded representation
that proves the two-order identity and the dual label pairing, with every
entry and recursion cost paid. Rank compression of the actual unthinned
pieces is a different remaining route.
