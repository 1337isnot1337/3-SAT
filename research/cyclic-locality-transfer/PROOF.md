# Locality bypass of an incidence-support barrier

## Statement

Let `n >= 1` Boolean variables be given in a specified cyclic order. Suppose
`a` Boolean polynomial equations `P_i(x)=0` over F2 are explicitly listed
as monomials, and every equation is accompanied by a cyclic interval of at
most `L` consecutive variables containing all its variables, where
`1 <= L <= n`. Put `w=L-1`, and let `B` denote the total input length,
including the intervals and polynomial descriptions. Their common zeros can
be counted exactly in `poly(n+B) 2^(2w)` bit operations and
`poly(n+B) 2^w` bits of space. These bounds include evaluating all equations,
not just enumerating abstract states. This elementary bounded-band transfer
argument is not claimed as a new algorithmic technique.

## Transfer construction

Number the variables `0,...,n-1` in cyclic order, cut just before zero, and
fix the first `w` bits in all `2^w` possible ways. Sweep the rest from left
to right. The state is the last `w` assigned bits, with a nonnegative integer
count of partial assignments for each state. Before retaining the newest `w`
bits, the old state and the new bit expose the last `L` bits. For every
nonwrapping interval, evaluate its equation when its right endpoint has been
assigned; equations whose endpoints lie within the prefix are evaluated
directly from the fixed prefix. If an equation fails, discard the transition.
Empty monomials and zero polynomials are evaluated by their ordinary Boolean
semantics. This also works for `w=0`.

Postpone every interval crossing the cut until the sweep ends. Its variables
lie among the first `w` and last `w` variables: if the interval contains `r`
variables before the cut and `s` after, then `r,s >= 1` and
`r+s <= w+1`, so `r,s <= w`. Its equation is therefore determined by the
fixed prefix and final state. Filter the final states accordingly and sum
their counts. Prefix and suffix may overlap; their values agree because both
come from the same partial assignment. With no equations the same procedure
returns `2^n`, including unused variables.

Induction on the sweep position shows that each surviving state count is
exactly the number of partial assignments with that suffix satisfying all
nonwrapping equations scheduled so far. The final filter adds all remaining
equations. Each full assignment has exactly one prefix and one path, so it is
counted once. No division, randomness, or modular recovery is needed.

There are `2^w` prefixes, at most `2^w` states per prefix, and at most two
transitions per state at each step. A straightforward evaluation of the
listed monomials costs `poly(n+B)` per transition; the integer counts have at
most `n+1` bits. Process prefixes serially, keeping only two state tables,
the input, and the current prefix. The claimed bit-operation and space bounds
follow. For fixed `L=O(log n)` and polynomially sized input both are polynomial;
for arbitrary `L` no polynomial-time claim follows. The supplied checker
implements this algorithm directly as an auditable reference, not the accepted
contraction algorithm.

## Application to the existing witness

In `research/newton-parity-compression/PROOF.md`, section 4, fix `k >= 2`,
`t=floor(log_2 n)`, and `kt<n`. The equation at position `i` is

```
P_i = XOR_{j=0}^{t-1} product_{u=0}^{k-1} x_{i+kj+u mod n}.
```

It has an explicitly given cyclic interval of length `L=kt` and `t`
monomials of degree `k`. Therefore the transfer algorithm counts its common
zeros exactly in `poly(n) 2^(2(kt-1)) = n^O(k)` bit operations and polynomial
space for fixed `k`. The separate predecessor establishes that `t^n`
incidence monomials survive its scalar expansion and yield an
`Omega(n log log n)` wire lower bound within its specified injective
one-monomial-per-code architecture. Both statements can hold: transfer sums
assignments through shared boundary states and does not assign a distinct wire
code to each incidence monomial. This is a concrete bypass on that *family*,
not a refutation of the predecessor's scoped information bound.

## Locality is not automatic

For every `h >= 1` take the complete binary tree of height `h` with
`n=2^(h+1)-1` vertices. For each edge `uv`, use one sparse quadratic equation
`x_u x_v = 0`. There are `n-1` equations, each has one degree-two monomial,
and every variable belongs to at most three scopes. Consider any cyclic
ordering of the vertices and any choice of intervals of length at most `L`
containing the two ends of each edge. The circular distance between the ends
of each edge is at most `L-1`. Two vertices at circular distance `floor(n/2)`
exist in every such ordering. Their tree path has at most `2h` edges. The
triangle inequality for circular distance implies

```
floor(n/2) <= 2h(L-1),
L >= 1 + floor(n/2)/(2h) = Omega(n/log n).
```

Thus no reordering can put every equation of this permitted sparse family
into logarithmic cyclic span. This is a limitation of the circular-band
interface, not a hardness result: these tree instances also admit simple
linear-time tree dynamic programming. More general separators, sparse-query
structure, or hybrid algorithms might help, but require separate proofs.

## Cost and scope in the SAT reduction

The result supplies a conditional exact-counting subroutine when a locality
certificate is given for the *entire* system. Given a claimed order and arcs,
their containment can be verified in polynomial input time. It does not show
that all sparse queries, high-incidence branches, or rejected candidates of
the accepted greedy reduction have this locality. It does not bound the
number of reductions or queries, nor provide a new general-density encoding,
contraction, decision guarantee, or faster complete SAT algorithm. Hence no
change to either accepted SAT bound or alpha is claimed. A hybrid using this
subroutine with a safe fallback could exploit verified local cases, but its
worst case remains governed by the fallback; no unproved improvement in the
number or cost of outer branches is assumed.

The proof is author-checked, substantially AI assisted, and has no independent
human or formal review. The finite checker provides regression evidence only.
