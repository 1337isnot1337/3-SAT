# One-hot affine one-packet obstruction

Status: `scoped_checked`, author-checked with substantial OpenAI Codex
assistance; no independent review. For every `L=2^a>=2` and `1<=u<=a`, a
single Cauchy packet with a row table affine modulo two and a column table
supported exclusively on one-hot inputs cannot reproduce the tapered
polynomial's grid-node residues, even modulo two. The proof uses a
characteristic-two convolution and applies over the source residue field.
[PROOF.md](PROOF.md) gives the exact statement and a counterexample when
zero column input is allowed.

The counterexample is itself a canonical Boolean packet: a row parity table
and a column table supported on zero and one-hot inputs match the `u=1` taper
node values and complete jets modulo two. It only covers precision one.
Neither result rules out nonlinear rows or general columns, proves a
higher-precision barrier, constrains balanced packet choices, or implies a
SAT time bound.

## Reproduction

From the repository root, Python 3.11+ with only the standard library:

```sh
python3 -I -B research/onehot-taper-obstruction/verify.py
make verify
```

The exact finite checks cover `L=2,4,8` and all `u<=a`, 98,568 one-hot
binary row/column candidates satisfying the necessary nonzero total, six
polynomial factorizations, 308 rational Cauchy-node jets, and 28 Boolean
escape node checks. The all-size argument is separate and has not been
independently reviewed.

## Source and credit

Initial main `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`; refreshed
base `f2a153bac5f73c5dc2d77abe229655fb1fd954ec`; accepted
OpenAI source `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`, pinned in
[SOURCES.json](../../SOURCES.json). The taper construction and its contents
are from [parity-recovery-precision](../parity-recovery-precision/PROOF.md).
Concurrent [PR #52](https://github.com/1337isnot1337/3-SAT/pull/52) at `1267136bc6e0287b138155bc07eeb2cdd657d6f3` gives
a two-packet interpolation and a separate finite screen using nonlinear rows
and fixed Boolean columns. It motivated this restricted one-packet test. [Issue #35](https://github.com/1337isnot1337/3-SAT/issues/35)
tracks this lane. No priority claim is made.

Contributor: Cinna Davis, with substantial OpenAI Codex assistance. New
material is Apache-2.0. The selected result and upstream bytes are unchanged.
