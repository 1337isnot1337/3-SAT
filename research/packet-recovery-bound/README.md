# Active attempt: lower the precision of actual packet recovery

Status: incomplete research toward a better unrestricted bound. No improvement
claimed; no component-only PR planned. Coordination: issue #155. Base main:
`c600b21ee7800a49c05718a254be50168e6b355b`.

The attempted mechanism is lower-precision recovery on the actual packet
operator lattice, to reduce the `sqrt(M p_t/D)` mode cost. This changes the
recovery premise, following rejection of the naive second-contraction cost
balance. It must eventually provide a uniform identity, affordable generation,
all node/profile costs and a complete arbitrary-density composition.

The old fixed-column draft at
`/home/cinna/3sat-packet-recovery-20261027/research/packet-recovery-lattice/probe.py`
is preserved verbatim as `previous_probe.py`. Its exact chart/polynomial
constructor is reused; its threshold routine is NOT used by the new solver.
This is predecessor credit, not an assertion that the old draft was validated.

`recovery.py` diagonalizes modulo a declared power of two and independently
substitutes both the recovery dual and an ambiguity kernel vector into the
original matrix. The solver is checked against exhaustive kernel enumeration
in 1,124 small cases. The packet calculation uses a COMMON functional across
all Boolean column inputs and all multilinear row coefficients. A threshold
for a fixed column input does not supply that common functional.

Current exact finite thresholds, with all shifted jets available:

| L | retained valuation levels u | uniform precision |
|---|---|---|
| 2 | 1 | 10 |
| 4 | 1 | 50 |
| 4 | 2 | 17 |

Both the upper recovery certificate and the one-bit-smaller ambiguity
certificate pass direct substitution. The output `cutoff_unresolved` means
recovery is impossible from those data AT THE DECLARED MODULUS, with a
verified kernel witness. It is not a non-membership result at all precisions.
These finite data do not establish asymptotic growth or an SAT lower bound.

Reproduce from the repository root, standard-library Python:

```sh
python3 -I -B research/packet-recovery-bound/recovery.py --validate-only
python3 -I -B research/packet-recovery-bound/recovery.py --L 2
python3 -I -B research/packet-recovery-bound/recovery.py --L 4
```

`checkpoint.json` records scope and code hashes. Runtime fields printed by the
screen are not benchmark claims. The next check is a larger packet/operator
lattice and then an all-size recovery argument if the data support a saving.
The full goal remains a better unrestricted bound, not a finite threshold.

Accepted source: OpenAI commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`,
`eq:tensor-cauchy`, `eq:tensor-mode-budget`, `eq:tensor-precision-bound`.
Related limits: `parity-recovery-precision`, `tensor-precision-witness`, and
`tensor-precision-realization`; their generic and actual tensor scopes differ.
The source is unchanged. New work is Apache-2.0 and substantially OpenAI
Codex-assisted. No independent review or selected-result change.
