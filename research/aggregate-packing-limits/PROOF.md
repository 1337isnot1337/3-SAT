# Aggregate codes and the persistent-degree barrier

Status: research proof, AI assisted, not independently reviewed. The accepted
OpenAI theorem is used as a theorem. This note studies a proposed successor
encoding; it does not audit the accepted proof or establish a general lower
bound on SAT algorithms.

## 1. Question and representation

The proposed change is to aggregate sparse equations before indexing their
incidence monomials. This can reduce the number of code wires, but it creates
vertices of large degree. We ask whether those vertices can nevertheless pass
through the accepted balanced-packing recursion while retaining direct
summation at the leaves.

We use the following conventions from `thm:tensor-contraction` and
`lem:tensor-packets`: `r=64`, `L=2^a`, a leaf is evaluated by enumerating all
Boolean edge assignments, and a child retains every old vertex in one group
with its degree unchanged. The relevant packing guarantee states that, on
either side and at every coordinate and symbol, at most `3M/r` **real** ports
belong to vertices carrying that symbol. Here `M` is the current number of
edges.

The obstruction below applies to this balanced-packing/direct-leaf
architecture. It does not rule out a new tensor decomposition, an unbalanced
recursion with a new cost proof, or a different leaf algorithm.

## 2. A necessary degree condition for balanced packing

**Lemma 1.** If a network with `M` edges and maximum degree `Delta` admits a
labeling and packet embedding with the stated real-port balance, then

```math
 \Delta\le 3M/r.
```

**Proof.** Choose a vertex `v` of degree `Delta` and fix any coordinate. The
vertex has one symbol at that coordinate. All of its `Delta` real ports belong
to vertices carrying that symbol on its side of the network. The packing
guarantee bounds that number by `3M/r`. ∎

Thus this is not merely a failure of the sufficient inequality
`M>=2D_arr^2 Delta` used in the accepted packing proof. For example, a star
with `M>3M/r` has no labeling at all satisfying the conclusion of that lemma.
The center has one symbol per coordinate, and every one of its ports occurs at
that symbol.

**Lemma 2 (persistence).** Suppose a vertex of degree `Delta` is never split.
Every active descendant containing it must still satisfy `M>=r Delta/3`.
Every leaf containing it has at least `Delta` edges and therefore costs at
least `2^Delta` Boolean edge assignments under direct summation. If instead a
modified implementation stops when balanced packing first becomes impossible,
the direct leaf has at least `r Delta/3` edges.

**Proof.** Old vertices and their ports are retained in the child networks, so
the degree cannot decrease. Any network containing the vertex has at least
`Delta` edges. Lemma 1 gives the active-call bound, and direct summation over
`M` edges examines `2^M` assignments. ∎

Consequently, a persistent degree `Delta` asymptotically larger than the
accepted leaf threshold cannot be accommodated just by finding a more clever
root packing. Either the balanced recursion cannot continue, or direct leaf
work has exponent `Omega(Delta)`. A new construction must split the tensor,
change the recursion and its cost analysis, or supply a faster leaf method.

## 3. Exact aggregate support and degree

We next recall and make precise the local aggregate family from the
characteristic-two follow-up. Let `h>=1` and `J>=2`, and take `hJ` variables in
`h` disjoint blocks of size `J`. Over characteristic two define

```math
 P_i=\sum_{j=1}^J x_{ij}\qquad(1\le i\le h),
 \qquad
 G=\prod_{i=1}^h(1+P_i).
```

The degree-`h` part of `G` is

```math
 \prod_{i=1}^h P_i.
```

It has exactly `J^h` nonzero multilinear monomials: choose one variable from
each block. These supports are distinct and each coefficient is one.

Partition the variables into `R` groups. A degree array records only the
selected degree in each group. There are at most `(h+1)^R` such arrays, so one
array retains at least

```math
 \frac{J^h}{(h+1)^R}
```

of these actual nonzero monomials. In a one-monomial-per-code aggregate
network, every wire incident to the aggregate test vertex belongs to its local
code. Two distinct local monomials must therefore have distinct projections
to those wires; otherwise their test-side entries and all their incident edge
bits are identical. Hence that vertex needs at least

```math
 \Delta\ \ge\ h\log_2J-R\log_2(h+1)
   \tag{1}
```

incident Boolean wires in some degree array. This is an information bound on
the stated code, not on an arbitrary compressed tensor representation.

The scoped checker enumerates these supports for small `h,J,R`, verifies the
exact array count, and compares the rational information bound with an exact
ceiling-of-logarithm calculation.

## 4. The wire/leaf tradeoff

Use the parameterization in the aggregate proposal: `h=n/J`, `R=ceil(n^(1/4))`,
and nominal aggregate wire count and contraction size

```math
 M=\Theta(n\log J),\qquad s=\Theta(n\log J).
```

All logarithms may be taken base two for this order calculation. Write
`lambda=log n`, `nu=log lambda`, and `H=Theta(s/sqrt(log s))` for the accepted
leaf-scale exponent. Consider `2<=J<=lambda^O(1)`. The degree-array correction
in (1) satisfies

```math
 R\log(h+1)=O(n^{1/4}\lambda)
            =o\!\left(\frac{n\log J}{J}\right).
```

Thus (1) gives

```math
 \Delta\ge(1-o(1))\frac{n\log_2J}{J}
       =\Theta\!\left(\frac{n\log J}{J}\right).
```

Since `log s=Theta(lambda)`, comparison with `H` yields

```math
 \frac{\Delta}{H}
   =\Omega\!\left(\frac{\sqrt{\lambda}}{J}\right).
   \tag{2}
```

**Theorem 3 (aggregate packing tradeoff).** In the above
one-monomial-per-code aggregate model, if the nominal wire order improves to
`o(n nu)`, then the persistent-degree/direct-leaf obstruction is asymptotically
larger than the accepted leaf exponent. More precisely,

```math
 M=o(n\nu)\quad\Longrightarrow\quad J=o(\sqrt{\lambda})
 \quad\Longrightarrow\quad \Delta/H\to\infty.
```

Equivalently, keeping `Delta=O(H)` in this model requires
`J=Omega(sqrt(lambda))`, hence `log J=Omega(nu)` and no improvement in the
`Theta(n log log n)` wire order.

**Proof.** The aggregate wire formula gives `M=Theta(n log J)`. If
`M=o(n nu)`, then `log J=o(nu)`. This implies `J=o(sqrt(lambda))`; otherwise
`log J=Omega(nu)`. Equation (2) proves the divergence. For the equivalent
statement, `Delta=O(H)` and (2) force `J=Omega(sqrt(lambda))`. ∎

This closes the specific attempt to obtain an asymptotic wire improvement by
aggregating these codes and then using the accepted balanced recursion
unchanged. It does not show that the displayed linear system is hard: its
disjoint linear equations are easy by elimination and admit other networks.
The example refutes a blanket interface assertion for the proposed code, not
a special algorithm for the example or a different uniform algorithm.

## 5. Complete cost interpretation and reopening conditions

No new algorithm is asserted, so there is no new reduction, query, precision,
mode, recovery, randomness, or amplification budget to hide. The accepted
outer reduction and complete time envelope remain unchanged:

```math
 (n+m)^{O_k(1)}2^{O_k(n\log\log n/\sqrt{\log n})},
 \qquad \alpha=1/2.
```

The fixed-density bound and selected result are also unchanged. The result is
a stopping condition for one representation, not a selected improvement or a
runtime lower bound.

Reopening this route requires at least one changed premise:

1. a degree-bounded tensor decomposition that preserves the aggregate wire
   saving throughout recursion, with entry costs charged;
2. an unbalanced packing/recursion theorem whose non-geometric child costs and
   leaf costs are proved; or
3. a faster leaf algorithm for the persistent high-degree tensors.

A root-only packing improvement is insufficient by Lemma 2. A construction
that works only for the disjoint linear example does not settle the uniform
sparse-query interface.
