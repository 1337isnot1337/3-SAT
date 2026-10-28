# Exact scalar-weight screen for asymmetric charged codebooks

This is a finite, substantially AI-assisted research result, awaiting independent
review. It gives no asymptotic 3-SAT improvement and does not change the
selected result. The accepted OpenAI theorem is the starting assumption.

## Question and scope

PR #19's [asymmetric crossing](../charged-asymmetric-crossing/PROOF.md) asks
whether a scalar pairing can remove a whole central interval of shifts while
retaining input and output capacity. Here we fix its deterministic input
minor and output codebook, charge `q=1`, and classify *all rational shift
weights* satisfying the scalar-output equations on that finite codebook.
Unlike the first-moment construction, the weights are arbitrary and the input
pairing may be nonprincipal. Other labels, codebooks, charges, and
non-scalar constructions are outside the screen. The charge-degree route in
issue #20 is distinct.

For grade `h` and codebook dimension `N`, use the raw predecessor pieces
`C_s(x,y,u,v)` for every integer `-2h <= s <= 2h`, including zero. A weight
vector is scalar exactly when, for each input pair `x,v`, its weighted output
matrix is a scalar multiple of the identity: all off-diagonal entries vanish
and all diagonal entries agree. The resulting common diagonal entries form
an `N` by `N` pairing matrix. The linear equations are solved over `Q`.

## Results

* At `h=6`, `N=4`, the complete scalar-weight space has dimension 3 and
  consists exactly of the restrictions of polynomials of degree at most 2
  in `s`. Therefore a scalar weight vanishing at `-1,0,1` must vanish
  everywhere. This holds regardless of the resulting pairing rank.
* At `h=4`, `N=2`, the complete scalar-weight space has dimension 5. When
  `-1,0,1` are excluded, the weight space has dimension 2 and contains a
  full-rank pairing. When `-2,-1,0,1,2` are excluded, all its pairing matrices
  vanish. Thus the grade-six conclusion cannot be extrapolated to all grades
  from these experiments alone.

At `h=9`, `N=8`, five selected input pairs yield 315 necessary scalarity
equations after setting the three central weights to zero. The 315 by 34
integer matrix has rank 26 modulo 65537, so its rational rank is at least
26 and the full scalar-filter solution space has dimension **at most 8**.
This is a one-sided partial certificate: it does not show whether any of the
remaining candidates satisfy all 64 input-pair constraints, yield nonzero
pairings, or have rank 26 over the rationals. See
[grade9-verification.json](grade9-verification.json).

The full labels, exact rational weight bases and rank profiles are in
[verification.json](verification.json). A rank of every displayed basis
pairing is reported; an individual full-rank basis pairing certifies
existence. Conversely, a zero pairing for every basis vector certifies that
all pairings vanish by linearity. The code does not infer a maximum matrix
rank from the individual basis ranks in other cases.

## Certificate and reproduction

```sh
python3 -I -B research/asymmetric-scalar-filter/verify.py > /tmp/scalar-filter.json
cmp /tmp/scalar-filter.json research/asymmetric-scalar-filter/verification.json
python3 -I -B research/asymmetric-scalar-filter/grade9.py > /tmp/grade9.json
cmp /tmp/grade9.json research/asymmetric-scalar-filter/grade9-verification.json
make verify
```

The checker uses only Python's standard library and the pinned predecessor.
It constructs every required exact tensor entry, verifies that the known
zeroth and first moments solve the scalarity constraints, and computes an
exact rational nullspace. Each reported basis is checked against all its
constraints. Independent forward elimination modulo 65537 certifies a lower
bound on rational rank matching the nullspace upper bound. At grade 6 the
three basis vectors have vanishing third finite differences; since quadratic
sequences form a three-dimensional space, they classify *all* solutions.
The rank of the associated 240-by-25 scalarity matrix is 22 over both the
rationals and the stated prime field. The three-root conclusion then follows
from the elementary root bound for polynomials.

This certificate relies on the predecessor's finite operator implementation;
it is not an independent verification of that implementation or of the
accepted theorem. The existing PR #19 checker separately tests both operator
orders and full crossing tensors at these two grades. No new all-size proof,
uniform construction, runtime bound, recovery analysis, or full SAT algorithm
is claimed. In particular these finite obstruction checks do not bound other
output subspaces, other row and column labels, or label capacity as h grows.
The complete asymptotic cost obligations in the predecessor remain open:
entry generation, both flattening ranks, reduction and query counts,
precision, recursion, recovery, and space must all be paid for a new filter.

## Next step

Test whether the grade-six rigidity persists at larger grade, then seek a
representation-theoretic proof or an explicit counterexample. Alternative
grade-six output codebooks are the subject of [issue #21](https://github.com/1337isnot1337/3-SAT/issues/21).
A successful larger finite case alone is not an all-size
obstruction, and any genuine interval filter must retain leading input and
output capacity. Reopening the fixed-codebook search needs a larger grade or a
changed choice of codebook; repeating these two classifications is not progress.

## Credit and source pins

The charged operator and first-moment pairing come from
[PR #11](../charged-operator-moments/PROOF.md); the asymmetric selection and
normalization come from [PR #19](../charged-asymmetric-crossing/PROOF.md),
whose model and transitive predecessor files are hash-checked by the checker.
The researcher in [issue #21](https://github.com/1337isnot1337/3-SAT/issues/21)
independently obtained the same grade-four and grade-six exclusion outcomes
in parallel, before the overlap was identified; they subsequently took the
alternative grade-six output-codebook search. The quadratic characterization
and rank certificate here describe this package's additional finite result.
The source snapshot is main commit `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`;
the upstream baseline commit and license are recorded in the root
[SOURCES.json](../../SOURCES.json). Research and implementation were performed
with substantial OpenAI Codex assistance; no independent or formal review is
claimed.
