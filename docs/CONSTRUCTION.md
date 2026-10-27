# Accepted construction and improvement points

This is a navigation map for changing the accepted theorem, not a proof audit.
Labels below resolve in the frozen
[main TeX file](../upstream/openai-eth-2026/build/main_full_version.tex),
[quantitative reduction](../upstream/openai-eth-2026/build/quantitative-reduction.tex),
or [quantitative contraction](../upstream/openai-eth-2026/build/quantitative-contraction.tex).
The published statement is Theorem 1.1 (`thm:main`) in the
[PDF](../upstream/openai-eth-2026/paper.pdf).

| Component | Source labels | Accepted role | Possible improvement |
| --- | --- | --- | --- |
| Fixed-density encoding | `subsec:sharp-fixed-density` | Clause and equality tensors give `O_k(n+m)` Boolean wires; unused variables contribute their count | A changed encoding or decision interface |
| Arbitrary-density reduction | `subsec:sharp-dense`, `lem:sparsify`, `lem:greedy-hashes` | Disjoint sparsification leaves and selected sparse parity queries | Reduce total overhead or avoid exact counting where decision suffices |
| Sparse-query encoding | `lem:tensor-sparse-query`, `eq:sharp-wire-budget` | Degree-bounded monomial indexing gives `O(n log log n)` wires | Reduce wires with entry and decoding costs charged |
| Contraction interface | `thm:tensor-contraction` | `2^O(s/sqrt(log s))` time for the stated succinct tensors | A better log saving under sufficient input guarantees |
| Packet construction | `lem:tensor-packets` | Bounded collision loads and balanced group ports | Changed packing with a complete recursive budget |
| Local coordinates | `lem:tensor-integrality` | Integral deformation over the specified two-adic extension | A changed deformation or different representation |
| Recovery | `lem:tapered-hermite`, `eq:tensor-precision-bound` | Tapered multiplicities control precision passed to children | A jointly improved recovery/precision schedule |
| Weighted modes | `eq:tensor-mode-multiplicity`, `eq:tensor-mode-budget`, `eq:tensor-partition-count` | At most `6M/D` modes per weight; retained weight below `p_t`; enumeration `exp(O(sqrt(M p_t/D))) = exp(O(M/sqrt(u)))` | Use realizable mode structure or change the mode/precision tradeoff |
| Recursion | `eq:tensor-recursion-identity`, `subsec:tensor-cost` | Children have at most `M/8` wires; depth parameters make exponents sum geometrically | A different full schedule, not just a smaller geometric constant |

The main-body rational interpolation route is a separate, weaker predecessor:
`prop:general-count`, `lem:incidence-parameters`, and `prop:interpolation-bound`
give an exponent with `(log log n)^2`. Appendix D supplies the selected sharper
bound with one `log log n` factor for arbitrary density. Do not optimize the
weaker route and call it an improvement on the selected result without a full
comparison.

At depth `d`, the selected contraction has
`M = O(s 8^-d)` and `u_d = Theta((log s)/2^d)`. Thus its mode-cost exponents are
bounded by a constant times

```math
 \frac{s}{\sqrt{\log s}}\left(\frac{\sqrt2}{8}\right)^d.
```

Improving only the geometric ratio changes a constant, not the root
`1/sqrt(log s)` saving. Improving the square-root dependence requires a changed
root tradeoff or a different algorithm. The base-case threshold, entry cost,
precision, interpolation values, number of groups and description growth must
remain inside the claimed budget.

For a contraction saving `(log s)^theta` and an encoding of size
`s = Theta(n (log n)^beta (log log n)^gamma)`, the composed exponent has envelope
`n (log n)^(beta-theta) (log log n)^gamma`, under these assumptions.
The resulting alpha is `theta-beta` unless another cost dominates. The
[exact cost models](../certificates/models/general.json) encode this comparison;
they certify bookkeeping only. A realizable simultaneous choice of assumptions
needs a new proof. Removing the current `gamma=1` gives a subleading improvement
while leaving alpha at `1/2`.
