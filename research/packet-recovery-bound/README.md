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
| 8 | 1 | 226 |
| 8 | 2 | 85 |
| 8 | 3 | 35 |

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

The larger screen `lattice_screen.py` uses the optional dependency
`python-flint==0.9.0`, installed for this experiment only under
`/tmp/3sat-packet-flint`. It compresses all 65,536 L=8 generators via exact
integer Hermite forms. See [METHOD.md](METHOD.md) for the equivalence and
for the distinction between universal linear recovery and nonlinear recovery
on legal Boolean tensor pairs. Reproduce the larger experiment with:

```sh
python3 -m pip install --target /tmp/3sat-packet-flint python-flint==0.9.0
python3 -I -B research/packet-recovery-bound/lattice_screen.py --flint-path /tmp/3sat-packet-flint --L 8 --precision 320
```

The L=8 replay takes several minutes and stays outside default CI. It also
tests the heterogeneous precision profile p_i=q D_i, which is the profile
relevant to the paid mode budget. Saved files are `lattice-L2.json`,
`lattice-L4.json` and `lattice-L8.json`.

`checkpoint.json` records the original standard-library scope and code hashes. Runtime fields printed by the
screen are not benchmark claims. The heterogeneous profile p_i=q D_i has exact minimum integer q values
5 at (L,u)=(2,1), 13 and 7 at L=4, and 29,16,10 at L=8. Both endpoints
of each search are certified. These finite values do not exhibit a better
asymptotic cost scale. Larger unchanged scans are stopped; continuing this
route requires a changed recovery premise with a full global composition.
The full goal remains a better unrestricted bound, not a finite threshold.

Accepted source: OpenAI commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`,
`eq:tensor-cauchy`, `eq:tensor-mode-budget`, `eq:tensor-precision-bound`.
Related limits: `parity-recovery-precision`, `tensor-precision-witness`, and
`tensor-precision-realization`; their generic and actual tensor scopes differ.
The source is unchanged. New work is Apache-2.0 and substantially OpenAI
Codex-assisted. No independent review or selected-result change.
