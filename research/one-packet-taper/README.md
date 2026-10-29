# One packet for two taper levels

Status: `scoped_checked`, author-checked with substantial OpenAI Codex
assistance; no independent review. A single prescribed `L`-slot Cauchy
packet realizes the first generic tapered factor `H_1` exactly over
`Z_(2)`, using an affine row table and a column table supported on zero and
one-hot inputs. A divided-difference identity factors its shift coefficients
into the two length-`L` tables. The last level `H_a` also has a one-packet
construction at every prescribed finite precision, via coprime Hensel lifting.
At `L=4` its exact rational factorization fails; the finite-residue claim
does not assert an exact `Z_(2)` realization. See [PROOF.md](PROOF.md).

Canonical nonnegative integer lifts preserve the complete shifted jets
modulo any requested `2^p`. With `h` independent packets the odd-node
precision collision has exact content `h(2L-1)` and `M=hL` edges. This
is `Theta(M)`, not the predecessor's generic `Theta(ML)` precision scale
for the same actual edge count. These are prescribed packets; compatibility
with the source's balanced packing is not shown. Boolean tensor entries,
intermediate taper levels, and a SAT bound improvement are not claimed.

## Reproduction

From the repository root, Python 3.11+ with only the standard library:

```sh
python3 -I -B research/one-packet-taper/verify.py
python3 -I -B research/one-packet-taper/last_level.py
make verify
```

The exact checker covers four complete rational factorizations at
`L=2,4,8,16` and 48 complete shifted-jet comparisons after canonical integer
lifting at `L=2,4`, precisions `1,...,4`, and every grid node. It checks
finite instances. The last-level checker adds 20 Hensel factorizations, 36
complete canonical-lift jet comparisons, 52 exact-content checks, and an
irreducibility control.
The all-size proofs have not received independent review.

## Sources and comparison

Initial main `4ce0cb947bdb6837718c7061e45d3a723219d703`; refreshed
base `f64e1babba809276639257f37cd218ee18824257`; accepted OpenAI
source `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`, frozen in
[SOURCES.json](../../SOURCES.json). The generic tapered witness and its
content formula are from
[parity-recovery-precision](../parity-recovery-precision/PROOF.md).
Concurrent [PR #52](https://github.com/1337isnot1337/3-SAT/pull/52), at
`c65f8778bc702c2b6dbf05ddbe4295cb7fda53ba`, gives two-packet interpolation
for all taper levels and degree-two interpolation of `H_1` powers. Its
`2L ceil(h/3)`-edge construction may beat the independent `hL`-edge
construction here; the present gain is the single factor in one packet.
[PR #85](https://github.com/1337isnot1337/3-SAT/pull/85) proves a distinct
obstruction when the zero column is excluded. The lane is tracked in
[issue #35](https://github.com/1337isnot1337/3-SAT/issues/35).

Contributor: Cinna Davis, with substantial OpenAI Codex assistance. New
material is Apache-2.0. No priority claim, selected-bound change, or upstream
modification is made.
