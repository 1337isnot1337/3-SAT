# Rational output compression for growing charged moments

Status: `scoped_checked` for the finite controls; the all-size argument is
author-checked, substantially OpenAI Codex-assisted, and not independently
reviewed. No improved SAT bound or selected-result change is claimed.

Allowing rational embedding/projection maps on the two output axes replaces
an exponential diagonal-signature loss by a polynomial loss. For M integer
operators, including identity, whose union transition graph has maximum
degree Delta, the [proof](PROOF.md) constructs U,V with

    UV=I_k,   U A_a V=c_a I_k,   k >= N/((Delta+1) M(M+1)/2).

The maps act separately on the two output axes and do not increase either
directional flattening rank. They are oblique maps, not orthogonal
projections. The construction and rational bit lengths are explicitly paid.

For the charged partition zero modes, this supports moment order
`Theta(sqrt(E)/log^2 E)` while retaining
`exp(pi sqrt(2E/3)-o(sqrt(E)))` output states, in `exp(O(sqrt E))` bit time
and space. The basis-subset predecessor supports `Theta(log^2 E)` with that
leading capacity. The removed central interval remains o(E). Input-pairing
rank and a smaller full SAT exponent are still unproved.

The affine-packing algorithm is in [compression.py](compression.py).
Each compressed scalar is the diagonal entry of one original partition
state, giving a concrete input-pairing matrix for the next investigation.

Reproduce offline with Python 3.11+ and the standard library:

```sh
python3 -I -B research/rational-moment-compression/verify.py > /tmp/rational-moments.json
cmp /tmp/rational-moments.json research/rational-moment-compression/verification.json
make verify
```

The [report](verification.json) contains exact affine-packing checks, sparse
matrix checks, actual charged filters, independent small normal-ordering
comparisons, and negative controls. A diagonal example with 32 distinct
signatures gives a 16-dimensional code where signature equality gives only
one state. Charged cases include nontrivial degree-five compressed outputs.
The checker does not implement a SAT solver or independently prove the
all-size theorem. Default repository CI only checks package consistency;
the separate reproduction command checks this package's calculations.

Predecessor: [partition transition codebooks](../partition-transition-codebooks/README.md)
and issue #108, including the charged moment argument of PR #89. Base:
`c600b21` (the full pin is in [CLAIM.json](CLAIM.json)). Source/license pins
and remaining costs are in [PROOF.md](PROOF.md). Coordination:
[issue #150](https://github.com/1337isnot1337/3-SAT/issues/150).
New work is Apache-2.0; no literature-priority claim is made.
