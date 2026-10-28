# Row-basis support with nonlocal original variables

This is a scoped extension of the private-edge construction in
[PR #44](https://github.com/1337isnot1337/3-SAT/pull/44), head
`93dd174db3c354d3548bce4b291af30a6964977f`. It combines that support
mechanism with an obstruction to the bounded-cyclic-span interface in
[PR #48](https://github.com/1337isnot1337/3-SAT/pull/48). The argument is
about a specified representation and is not a SAT lower bound.

## Explicit sparse systems

Let `d >= 2` be even, `n=2^d`, `L=d/2`, and label the variables by vertices
of the d-dimensional hypercube. Pair the coordinate positions as
`(0,1),(2,3),...`. In every square corresponding to a coordinate pair,
orient its four edges cyclically `00 -> 10 -> 11 -> 01 -> 00` with the
other coordinates held fixed. These squares partition all edges: each edge
belongs to the unique pair containing its flipped coordinate. Consequently
this gives an explicit, deterministic orientation with exactly `L` outgoing
and `L` incoming edges at each vertex. It is constructible in `O(nd)` steps.

For each vertex v define a polynomial equation

```
P_v(x) = XOR_{v -> u} x_v x_u = 0.
```

Each row has exactly `L` distinct quadratic monomials and `L+1` variables.
Every undirected cube edge occurs in exactly one row. Each variable occurs
in its own row and in exactly `L` incoming neighbors' rows, so its scope load
is `L+1`, and `N0=n(L+1)`. With `lambda=ceil(log2 n)=d`, the accepted
sparse-query high-incidence threshold `(L+1) ceil(sqrt(d))` is no smaller
than this load, so this original presentation triggers no such branch.
There are `n` equations, `L <= lambda` monomials per row, and degree 2;
these satisfy the source's sparse-query interface. The all-zero assignment
satisfies every equation, so the family has a trivial decision witness.

## Row-basis-resistant support

Write `E_v` for the set of edges assigned to row v. The sets `E_v` are
pairwise disjoint. For a nonzero binary row vector `a`, the normalized
polynomial `Q_a = XOR_v a_v P_v` contains exactly `L wt(a)` distinct
quadratic monomials. Hence the original polynomials are linearly independent,
and every row of every invertible binary basis change has at least `L`
monomials. This count is exact and there are no linear or constant terms.
A dense basis change can exceed the sparse-query input length or trigger
subsequent high-incidence preprocessing; the following is a pre-branch
statement about its scalar-lift representation, not a claim that the
transformed query remains inside the original sparse-query promise.

Give each transformed row its own incidence variables. In the integer
zero-indicator lift `E_Q(z)=1-(Q(z) mod 2)` on Boolean inputs, the coefficient
of a present degree-two monomial `z_u z_v` equals `-1`: its subset Mobius
formula has values 1 at the empty and two singleton inputs and 0 at `{u,v}`.
Selecting independently one of at least `L` such monomials in each row gives
at least `L^n` distinct incidence monomials of degree `2n` and coefficient
`(-1)^n` in the product lift. They survive modulo `2^(n+1)` and fit the
scalar predecessor's degree cutoff `2(a+p-1)=4n` at `a=n`, `p=n+1`.
Different incidence monomials can still cancel after identifying variables
or summing; no claim is made that their total contribution is nonzero.

For the predecessor's `J=ceil(n^(1/4))` groups per side, there are at most
`(2n+1)^(J^2)` degree arrays relevant to these degree-`2n` choices. Some
array therefore contains at least `L^n/(2n+1)^(J^2)` such monomials. Any
injective binary code for each of them within that array has at least

```
n log2 L - J^2 log2(2n+1) = Omega(n log log n)
```

bits for the growing even-d sequence. This extends the mechanism of PR #44
to this graph; it is not a lower bound for an aggregate or alternative code.

## Every circular ordering has large span

Consider any cyclic order of the variables and any invertible row basis.
Suppose every transformed equation's variable scope is contained in a cyclic
interval of at most `s` variables. Since every original edge belongs to a
unique original row and the basis matrix is invertible, the corresponding
column of that matrix is nonzero: the edge appears in at least one
transformed equation. Its two endpoints therefore have circular distance
at most `s-1`.

Choose two vertices at opposite locations in the order, circular distance
`n/2`. Their hypercube graph distance is at most its diameter `d`. Apply
the circular metric triangle inequality along a cube path between them:

```
n/2 <= d(s-1),  so  s >= 1 + n/(2d) = Omega(n/log n).
```

Thus neither the original equations nor any invertible row basis admits
the logarithmic cyclic span needed for the polynomial-time transfer in
PR #48. This is an ordering-interface obstruction only. Other decompositions,
nonlinear transformations, variable elimination, tree decompositions,
problem-specific algorithms, or changes of coefficient representation are
not excluded. Large circular span alone does not establish computational
hardness.

## Span after a limited number of substitutions

Fix any `B` variables to arbitrary bits and let `f=n-B >= 2` be the number
of remaining variables. Every cube edge with both endpoints free remains a
quadratic monomial in its original row; those monomials are still private.
Consequently every collection of residual polynomials spanning the restricted
row space, including a basis chosen after arbitrary invertible row changes,
must contain each surviving edge in some row. Lower-degree terms and
constants caused by substitution cannot cancel these quadratic coefficients.

Put the free variables in any cyclic order, and let `S` be its first
`q=floor(f/2)` vertices. For any cube vertex set `S`, its edge boundary
obeys

```
|boundary(S)| >= 2 q (n-q)/n.
```

For completeness, take normalized inner product on functions on the cube.
The characters `(-1)^(T dot x)` form an orthonormal basis, and the cube
Laplacian has eigenvalue `2|T|` on character T. For `1_S`, the Laplacian
quadratic form is `|boundary(S)|/n`, while the nonconstant Fourier mass is
`q/n*(1-q/n)`. Every nonconstant eigenvalue is at least two, proving the
inequality. At most `dB` boundary edges touch deleted vertices. Thus at
least `2q(n-q)/n - dB` edges join the two free halves.

If every residual row scope lies in a cyclic interval of at most `s`
free variables, each surviving edge has circular distance at most `s-1`.
An edge crossing between the two consecutive halves has its endpoint in S
within `s-1` positions of one of the two cuts. There are at most `2(s-1)`
such vertices, each of degree at most `d`. Therefore

```
2d(s-1) >= 2q(n-q)/n - dB.
```

For `B=o(n/d)` the right side is `n/2-o(n)`, so every such residual spanning
collection and cyclic order still has `s=Omega(n/d)=Omega(n/log n)`.
This applies even to an inconsistent fixed branch, and is an interface
statement, not a lower bound on work a solver must perform. It does **not**
cover the source's full single-step allowance `B=O(n/sqrt(d))`; for that
larger regime the displayed right-hand side may be nonpositive. No claim
about repeated preprocessing or a coefficientwise support bound after
substitution is made here.

The proof method has a concrete obstruction at the source allowance scale.
For even d, delete all `binom(d,d/2)` vertices of middle Hamming weight.
The lower and upper weight classes have equal size `(n-B)/2`, and no cube
edge joins them: an edge changes Hamming weight by exactly one. Ordering the
lower class consecutively and then the upper class gives zero edges across
the two halves. By the central binomial asymptotic,

```
B = (sqrt(2/pi)+o(1)) n/sqrt(d)
    < n/ceil(sqrt(d))
```

for sufficiently large even d. Thus this arbitrary deletion set satisfies
the *numerical* single-step cardinality allowance, yet the proof cannot
obtain a positive crossing-edge bound for its half cut. This does not show
that the source high-incidence procedure selects exactly those vertices,
nor that the remaining equations admit small cyclic span: it only shows
that this particular cut argument cannot establish span at that scale.

## A different exact count by bipartite linear algebra

The cube is bipartite, with color classes `A` and `B` of size `n/2`.
More generally, let any bipartite graph be oriented arbitrarily and use
one equation `x_v * (XOR_{v->u} x_u) = 0` at each vertex. Fix an assignment on
`A`. For each `a in A` with `x_a=1`, its equation is the homogeneous linear
condition `XOR_{a->b} x_b=0`; if `x_a=0`, it is automatically satisfied.
For each `b in B`, its equation is `x_b c_b=0`, where
`c_b=XOR_{b->a} x_a` is now known. If `c_b=1`, add the linear condition
`x_b=0`; otherwise there is no condition. Thus all remaining constraints are
a linear system over F2 in the `B` variables. Gaussian elimination gives
zero if inconsistent and otherwise `2^(|B|-rank)` solutions.

Enumerate all `2^|A|` assignments and add those counts. For a prescribed
fixed-bit branch, enumerate only compatible assignments on `A` and add the
corresponding affine unary equations on `B`; the same elimination handles
conflicting conditions exactly. Both variants run in `2^(n/2) poly(n)` bit
operations and polynomial space, using serial enumeration and counts of at
most `n+1` bits. This exact count works for the oriented cube and any one
fixed-bit branch without any cyclic order. It is asymptotically slower than
the accepted general counting theorem and is not a SAT improvement. It also
illustrates why the cyclic-span obstruction cannot be interpreted as a
counting lower bound.

As a simple separate control, every assignment supported entirely in `A`
or entirely in `B` satisfies all equations. There are at least
`2^(n/2+1)-1` satisfying assignments, including all-zero only once. Neither
this lower bound nor the linear-algebra count establishes the exact formula
count without the stated summation.

## Costs and evidence boundary

The bipartite enumeration is a scoped exact-counting algorithm for this
family, not a faster general SAT algorithm. Neither the coefficientwise obstruction
nor the circular-span bound establishes the cost of the entire dense
reduction, its branches and queries, tensor entries, contractions,
precision, recovery, or space. The accepted bound and alpha remain unchanged.
In particular, a coefficient-support post-branch observation from PR #44
is not imported here as a proved claim; the span-after-substitution argument
has its own explicit smaller branch-size restriction.

`verify.py` checks explicit small cubes, all invertible four-row bases,
seeded larger bases, exact integer subset-Mobius coefficients, and circular
orderings. The saved finite output supports regression testing, not the
all-size claims. Those arguments are author-checked, substantially AI-assisted,
and have not received independent human or formal review.
