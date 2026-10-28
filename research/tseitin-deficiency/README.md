# Tseitin controls for deficiency and separators

Status: `scoped_checked`; substantially AI-assisted, without independent review. Task `decision-only`, base `c7c5a03434b396e227e9ab573b5b7cdea52b47fa`.

[PROOF.md](PROOF.md) applies classical odd-charge Tseitin CNFs on connected cubic graphs to the repository's deficiency and separator interfaces. These formulas are unsatisfiable, bounded-occurrence, matching lean and deficiency-critical; when the graph has no articulation vertex they are minimally unsatisfiable; on cubic expanders their primal graphs have linear balanced separators. They are polynomial-time decidable by linear algebra. A cited theorem gives an exponential lower bound only for explicitly emitted regular-resolution refutations on the expander family. This does not conflict with the owner-accepted counting theorem and does not establish a general SAT lower bound or an alpha improvement.

```sh
python3 -I -B research/tseitin-deficiency/verify.py
make verify
```

The first command verifies K4 and cube instances exhaustively for the stated finite properties and checks an articulation counterexample to unconditional minimality. The published expansion, criticality and regular-resolution results are cited black boxes; the all-size composition has not been independently reviewed.
