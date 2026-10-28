# A tensor realization of one tapered witness

Status: `scoped_checked`, substantially AI assisted, without independent review.
Starting from [the generic precision witness](../parity-recovery-precision/PROOF.md),
we realize its `u=1` family exactly by prescribed Cauchy packets over the
source's 2-adic coefficient ring. This does not realize the predecessor's
matching `h=floor(M/(2u))` parameter choice: our construction uses
`M=hL(2L-1)` real matched ports and a row tensor of degree `2L-1`. Its
precision obstruction is only `Theta(M/L)`. It does not improve a SAT bound,
claim an alpha improvement, or settle Boolean-input realizability.

## Statement

Let `L=2^a`, `a>=1`, and `S={-L,...,L-1}`. Define

```
H_1(T) = product over odd t in S of (T-t)/(-t).
```

For any positive `h`, there is an explicitly described packet network over
`Z_(2)` whose deformed contraction is `H_1(T)^h`. Each copy uses `2L-1`
full packets of `L` matched ports and one row tensor of degree `2L-1`;
all other tensors are unary. Thus this is an existence result for a specified
packetization, not a proof that the source's packing procedure will select it.
The tensor entries are generally not Boolean or integers, although their
odd denominators are units in the source coefficient ring. The construction
and its costs are given in [PROOF.md](PROOF.md).

In particular, the literal generic witness cannot be ruled out merely by
requiring an actual packet contraction over the 2-adic coefficient ring.
For integer-entry networks, however, every packet matrix is zero at `T=-L`,
so the contraction value there is an integer. At `L=4`, the literal
`H_1(-4)=35/3`; it is therefore not an integer-entry contraction. Multiplying
by an odd denominator removes this particular obstruction while preserving
2-adic parity and precision, so it does not rule out a Boolean replacement.

## Reproduction and limits

Run from repository root with Python 3.11+ and the standard library:

```
python3 -I -B research/tensor-precision-witness/verify.py
make verify
```

The first command checks all 56 Cauchy entries and exact polynomial
identities for `L=2,4,8,16`, together with 2-adic integrality of the
interpolation coefficients. It is a finite check of the construction, not
independent review or a run of the accepted contraction algorithm.

The all-size argument is author-checked. Boolean or bounded-degree realization
with the predecessor's full `h=Theta(M)` for `u=1` remains open. No complete
SAT algorithm or complexity claim is made. The selected result is unchanged.

Base: `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`. Frozen OpenAI source:
`7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`, labels `eq:tensor-cauchy`
and `eq:tensor-deformed-contraction`. The predecessor's witness and precision
analysis are credited above. Contributor: Cinna Davis, with substantial
OpenAI Codex assistance. New material is Apache-2.0.

Concurrent [issue #33](https://github.com/1337isnot1337/3-SAT/issues/33)
and [issue #35](https://github.com/1337isnot1337/3-SAT/issues/35) investigate
the same general realization question. Their checkpoints report candidate
Boolean networks with stronger simultaneous precision obstructions; those
claims are separate and not verified here. This package addresses literal
realization of the specified `u=1` polynomial over `Z_(2)` and its cost.
