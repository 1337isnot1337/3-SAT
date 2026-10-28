# Clause-width and occurrence defects

Status: `scoped_checked`; author-checked and substantially AI-assisted, without independent review. Task `decision-only`; base `4ce0cb947bdb6837718c7061e45d3a723219d703`.

[PROOF.md](PROOF.md) shows that maximum clause deficiency is at most one third of the sum of width shortfalls below three and variable occurrence excess above three. Combined with Szeider's existing decision theorem, this gives an efficiently checkable input-class bound, with no unrestricted alpha improvement. Measuring maximum deficiency directly by matching is always at least as strong. The proof gives sharpness and slack examples and pays for a possible defect increase under branching.

Run:

```sh
python3 -I -B research/occurrence-defect-interface/verify.py
make verify
```

The first command checks 1,200 small formulas, 8,400 restrictions and three sharpness controls. It is finite evidence only. The accepted algorithm and Szeider's solver are black boxes. A useful continuation would need a paid reduction that makes this defect small on every relevant branch, or a stronger directly measured parameter; bounded occurrence alone does not establish either.
