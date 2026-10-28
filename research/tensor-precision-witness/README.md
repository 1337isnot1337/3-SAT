# A tensor realization of the tapered witness

Status: `scoped_checked`, substantially AI assisted, without independent review.
Starting from [the generic precision witness](../parity-recovery-precision/PROOF.md),
we realize the full family exactly by prescribed Cauchy packets over the
source's 2-adic coefficient ring. The construction uses
`M=2L(ceil(h/3)+h(u-1))` real matched ports and row tensors of at most `2L`
ports. Its multiplicity `h` remains a factor proportional to `L` below the
predecessor's matching choice when `u=1`. It does
not improve a SAT bound, claim an alpha improvement, or settle Boolean-input
realizability.

## Statement

Let `L=2^a`, `a>=1`, `1<=u<=a`, `h>=1`, and `S={-L,...,L-1}`. Define

```
H(T) = product over nonzero t in S of ((T-t)/(-t))^(h max(0,u-v2(t))).
```

There is an explicitly described packet network over `Z_(2)` whose deformed
contraction is exactly `H(T)`. The construction factors `H` into polynomials
and uses two full packets per factor. Quadratic interpolation realizes up to
three copies of the odd-root factor per packet pair; all other tensors are unary. This is an existence result for a specified packetization, not a
proof that the source's packing procedure will select it. The tensor entries
are generally not Boolean or integers, although their odd denominators are
units in the source coefficient ring. The construction and its costs are in
[PROOF.md](PROOF.md).

For `u=1`, the predecessor's content formula yields `Theta(M)` shifted
precision content for this network. Its generic witness, using the same `M`
but multiplicity `floor(M/2)`, has content `Theta(ML)`. This construction
therefore leaves a factor `Theta(L)` gap.

For integer-entry networks every packet matrix is zero at `T=-L`, so the
contraction value there is an integer. At `L=4`, `u=h=1`, the literal
`H(-4)=35/3`; it is therefore not an integer-entry contraction. Multiplying
by an odd denominator removes this particular obstruction while preserving
2-adic parity and precision, so it does not rule out a Boolean replacement.
More generally, for any precision `P`, reducing every row-tensor entry to a
nonnegative integer modulo `2^P` preserves all shifted jets modulo `2^P`
and origin parity. This gives integer-entry collisions at the same scoped
precision, with `P`-bit entries; it is not a Boolean realization.

## Reproduction and limits

Run from repository root with Python 3.11+ and the standard library:

```
python3 -I -B research/tensor-precision-witness/verify.py
python3 -I -B research/tensor-precision-witness/screen_one_packet.py
python3 -I -B research/tensor-precision-witness/check_integer_lifts.py
python3 -I -B research/tensor-precision-witness/screen_two_packet_powers.py
python3 -I -B research/tensor-precision-witness/screen_one_packet_nonlinear.py
python3 -I -B research/tensor-precision-witness/verify_quadratic.py
make verify
```

The first command checks all 56 Cauchy entries and 10 exact interpolation
and taper factorization identities for `L=2,4,8,16`, together with 2-adic
integrality of the interpolation coefficients. It is a finite check of the
construction, not independent review or a run of the accepted algorithm.
The second command exhausts all fixed Boolean column assignments for one full
packet at `L=2,4,8`. Exact rational linear algebra finds no realization of the
`u=1,h=1` witness with a single affine row tensor, even when its coefficients
may be arbitrary rationals. This finite screen does not rule out nonlinear row
tensors, unfixed columns, or larger packet lengths. The third command
explicitly sums all row assignments for five integer lifts at `L=2` and
compares the full shifted polynomials at all four grid nodes.
The fourth permits an arbitrary row table on all `2L` rows of the same two
fixed-column packets. It constructs 2-integral realizations of `H_1^2` for
`L=2` and `H_1^2,H_1^3` for `L=4`; `H_1^4` is outside this span even over
the rationals. A fifth screen exhausts fixed Boolean columns at `L=2,4`
and permits an arbitrary row tensor: no power `H_1^k` for `1<=k<=L` is in
that one-packet rational span. These are finite results and do not establish
an all-size saving or obstruction. The quadratic checker verifies 61 exact
identities, including every monomial in the stated degree range for `L=2,4,8`
and the square and cube of the odd-root factor for `L=2,4,8,16`.

The all-size argument is author-checked. Boolean realization and realization
with the predecessor's multiplicity `h=Theta(M/u)` remain open. No complete
SAT algorithm or complexity claim is made. The selected result is unchanged.

Base: `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`. Frozen OpenAI source:
`7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`, labels `eq:tensor-cauchy`
and `eq:tensor-deformed-contraction`. The predecessor's witness and precision
analysis are credited above. Contributor: Cinna Davis, with substantial
OpenAI Codex assistance. New material is Apache-2.0.

Concurrent [issue #33](https://github.com/1337isnot1337/3-SAT/issues/33)
and [issue #35](https://github.com/1337isnot1337/3-SAT/issues/35) investigate
the same general realization question. Their respective [PR #56](https://github.com/1337isnot1337/3-SAT/pull/56)
and [PR #65](https://github.com/1337isnot1337/3-SAT/pull/65) describe Boolean
networks with separate precision bounds; those claims are not verified here.
[PR #85](https://github.com/1337isnot1337/3-SAT/pull/85) separately studies
one-packet one-hot restrictions and a modulo-two escape. This package addresses literal
realization of the specified polynomial over `Z_(2)` and its cost.
