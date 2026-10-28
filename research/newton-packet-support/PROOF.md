# Local mode support and a child-tensor obstruction

This is an author-checked research note, not an independent proof review.
The accepted OpenAI theorem is used as a premise. The predecessor Newton
modes are those in [PR #4](https://github.com/1337isnot1337/3-SAT/pull/4).

## 1. Exact local identities

For a Boolean table `A` on `d` row ports define its multilinear extension

```
F_A(z_1,...,z_d) = sum_{y in {0,1}^d} A(y) prod_i l_{y_i}(z_i),
l_0(z)=1-z,  l_1(z)=z.
```

This identity holds over any commutative ring. For the equality table,

```
F_eq(z) = prod_i (1-z_i) + prod_i z_i.
```

Its coefficient of `prod_{i in S} z_i` is `(-1)^|S|` for proper
subsets, and `1+(-1)^d` for the full set. Thus, for odd `d>=3`, its
total degree is `d-1`; for even `d` its full coefficient is 2. In
particular, for a trivalent equality,

```
F_eq = 1-z_1-z_2-z_3+z_1z_2+z_1z_3+z_2z_3.       (1)
```

This cancellation is exact over the integral coefficient ring, not merely
modulo 2. For a clause with unique falsifying pattern `v`, its extension is
`1-prod_i l_{v_i}(z_i)` and has degree `d` with full coefficient `+1` or
`-1`. A tautology can be removed as in the source reduction.

At a deformed-contraction call, each `z_i` is an affine form in local
column bits and crossing mode variables. Substitution into (1) therefore
has total mode degree at most 2 for this single equality vertex, even if
its ports lie in different packets. This follows because a vertex belongs
to one group, so all its row bits can be summed together. The bound is
local: in a whole group, products of many such vertices can have much
larger total degree, and distinct vertices can share mode variables. It
also does not say which individual coefficients vanish, nor that the group
contraction is cheap to evaluate.

## 2. One exact packet with no additional support holes

Use `L=8`, `i=0`, `t=1`, `alpha=16`, `zeta=1`, so `T=17`. Take a
packet with unequal coordinate-0 symbols. It has real row and column ports
at slots `0,2,4` only; all row ports are in one group and all column
ports in the other. This respects the local slot/orientation rule; we do
not claim that this small packet alone satisfies all global asymptotic
packing side conditions. The three row ports are one trivalent equality
vertex or one positive 3-clause vertex. Each column is attached to a unary
`(1,1)` vertex. Thus every input table is a fixed-density reduction table.
There are no local row-to-column terms in either group.

Use the general Newton modes from PR #4. The tile has `j=0,1,2,3`, but
only `j=0,1,2` are real, hence mode `k=3` has zero source linear form.
For `k=0,1,2`, write `a_{xk}` for the row coefficient and `b_{kj}` for
the column coefficient. The checker verifies the nine identities
`W_xy=sum_k a_xk b_ky` exactly over the rationals. It substitutes the
three row affine forms into (1) and into the clause polynomial, and then
multiplies each mode coefficient by the actual source-side moment obtained
by summing all eight Boolean column assignments. Independently it sums all
64 pairs of assignments in the original deformed contraction.

The equality case has **all 10** tuples of three modes with total degree at
most two, and no others. The positive clause case has **all 19** tuples of
total degree one through three, and no others. Every corresponding source
moment is nonzero and the child sum equals the direct contraction exactly.
The checker determines nonzero values over `Q`, before reducing modulo a
precision; some may vanish at a particular two-adic precision. This is a
bounded illustration of the absence of further support holes in this one
packet, not a claim for every input, interpolation point, or packing.

## 3. A child need not retain the input table family

In the same packet, choose `beta=0` for all crossing modes. By the source
child construction, the packet vertex on the row group is the coefficient
of the mode-free part of the row factors. Since that group has no local
column ports, each row argument's local part is zero, and the packet table is

```
P(Y_1,Y_2,Y_3) = prod_i l_{Y_i}(0) = (1-Y_1)(1-Y_2)(1-Y_3).   (2)
```

Its cubic Boolean multilinear coefficient is `-1`, and it has one nonzero
Boolean entry; a ternary equality table has two and no cubic coefficient.
Thus even a network starting with a trivalent equality and unary tensors
can acquire a non-equality packet tensor in a zero-mode child. This does
not assert that the entire child contraction has a nonzero cubic mode term:
packet tensors and original vertex tensors are both present in the child,
and the child is later repacked and deformed. The statement only refutes
closure of the *individual input table family* under the specified child
construction. A successor may find a broader invariant using their joint
structure.

## 4. Cost and unresolved obligations

No new algorithm, asymptotic mode count, or SAT bound follows from (1) or
(2). The total number of group vertices can grow with the input, and the
formal weighted count includes coupled modes, recursive packet tensors,
precision and recovery. It is not valid to replace that global count by
10 per equality or to infer a smaller alpha from the small example. The
accepted reduction branches, queries, descriptions, entry computations,
recursion, precision, recovery and space bounds remain the baseline; no
changed cost is claimed.

A concrete next question is whether a joint invariant of old vertices and
packet tensors, retained through *repacking*, yields a uniform weighted
support bound. It must cover clauses as well as equalities, cancellation
modulo the actual precision, every child and every group. Alternatively,
construct admissible large packet families with sufficiently many nonzero
low-weight terms modulo the real taper to rule out a named support-only
strategy. The finite rational example does neither.

## Source references

The fixed-density network appears at `subsec:sharp-fixed-density` in the
frozen quantitative reduction. Packet orientation, deformed contraction,
mode budget and child tensors are `lem:tensor-packets`,
`eq:tensor-deformed-contraction`, `eq:tensor-mode-budget` and
`eq:tensor-recursion-identity` in the frozen quantitative contraction.
Hashes and upstream attribution are in the root `SOURCES.json`. The Newton
identity and its integral validity at source points are credited to the
local [predecessor](../cauchy-newton-modes/PROOF.md). The small-packet
support example and the child-table observation are the present scope.
