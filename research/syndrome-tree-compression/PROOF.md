# Tree syndrome states and the Boolean-port degree bottleneck

Author-checked argument; no independent review. This is a representation
result, not a lower bound on SAT algorithms or an improved SAT time bound.

## 1. Model and exact tree construction

Let A have m>=1 binary columns, let C=ker(A), and let k=dim(C).
Assume every nonzero codeword has weight at least D, where 1<=D<=m+1.
Assign each of the m independent input bits z_j to exactly one vertex of a
finite tree T. A vertex may hold many input bits or none. Let l_v count its
inputs. Replace each tree edge e by a bundle of w_e Boolean state wires.
A tensor at v has l_v+sum_{e incident v} w_e ports. Arbitrary entries over
any field are allowed, but contracting the state wires must give the entire
function f(z)=1[Az=0] for every z. No positivity, unique-path, linear-state
or local-code restriction is imposed on these candidate realizations.

For an edge e, deleting e partitions the coordinates into S and its
complement. Put

    E_e = span(A_S) intersect span(A_notS),    b_e = dim(E_e).

The flattening of f across this cut has rank exactly 2^b_e over every field.
Indeed, partition rows and columns by their binary syndromes. For each
syndrome in E_e there is one all-ones matching block, and all other entries
are zero. Choosing one preimage per syndrome gives an identity submatrix;
the sum of the 2^b_e block outer products gives the matching upper bound.
Thus any realization in this model has w_e>=b_e at every edge, even if its
entries have cancellations or lie in a field of characteristic two.

These lower bounds are simultaneously attainable. Choose a binary basis
of each E_e and use b_e bits to encode its syndrome s_e. At vertex v set
the tensor to one precisely when

    XOR_{e incident v} s_e = XOR_{j assigned to v} z_j A_j.       (1)

Otherwise set it to zero. On a tree, summing (1) over a component of T-e
forces s_e=A_S z_S. Hence every input has at most one state extension.
For Az=0, these forced syndromes belong to E_e and satisfy every vertex
equation. Conversely, summing all equations gives Az=0. The contraction is
therefore f as an integer identity and hence over every field.

Binary elimination constructs all state bases in polynomial time in the
listed matrix and tree. Entry evaluation, including state decoding and
(1), is polynomial time. This representation uses sum_e b_e internal wires,
and minimizes that sum and each vertex port count for the fixed tree and
coordinate placement. Finding an optimal tree is not claimed efficient.
The total port count includes the m external inputs; after attaching input
sources these are ordinary Boolean wires. Zero-dimensional bundles can be
omitted. Subdividing bundles to obtain bipartiteness does not reduce the
original vertex degrees.

This is the standard minimal tree-realization mechanism, written here in
the repository's Boolean-wire convention. Credit Kashyap's minimal tree
realizations and vertex-cut framework, and the repository's ordered
`hash-syndrome-chain` construction. No novelty is claimed for that mechanism.

## 2. A weighted tree separator with a paid number of vertices

Put weight l_v on vertex v, with total m. There is a set X of at most
floor(m/D) vertices such that every component of T-X has total weight <D.
If D>m, take X empty. Otherwise root T. Work upwards from the leaves,
maintaining the weight of each still-attached descendant subtree. Whenever
that weight is at least D, put its root v in X and pass weight zero upwards.
Before v is selected, each still-attached child subtree has weight <D,
since a child meeting the threshold would already have been selected.
Removing v therefore separates those small components from its parent.
At the end the remaining root component also has weight <D.
Each selected vertex accounts for at least D input coordinates that were
not accounted for at an earlier selection. These charged sets are disjoint,
so |X|D<=m. Zero-weight vertices and inputs placed at internal vertices need
no exceptions. This procedure is linear in the tree size once weights are known.

## 3. A dimension bound and a degree bound for every tree layout

For any separator X whose remaining components have fewer than D inputs,
map a codeword to its coordinates at X together with its canonical edge
syndromes on edges incident to X. This binary linear map is injective.
To prove it, take a word in its kernel. Its inputs at X are zero. Sum (1)
over any component Q of T-X. Internal edge syndromes cancel in pairs and
all boundary syndromes vanish. Thus A_Q z_Q=0. The restriction z_Q is a
codeword supported on fewer than D coordinates, and must be zero. This
holds in every component, so the original word is zero.

Counting dimensions in the target (overcounting an edge between two
separator vertices is harmless) gives

    k <= sum_{v in X} (l_v + sum_{e incident v} b_e).             (2)

For any exact field-valued realization on this tree, w_e>=b_e. If Delta
is its maximum Boolean-port degree, then

    k <= |X| Delta <= floor(m/D) Delta.                         (3)

For k>0 we necessarily have D<=m and obtain the explicit universal bound

    Delta >= ceil(k / floor(m/D)) >= kD/m.                     (4)

For the zero kernel k=0 the statement is simply vacuous; dividing by a
zero floor is not permitted. The bound depends on dimension as well as
distance: a repetition code has k=1 even when D=m. This argument applies
to every tree topology and every grouping of input coordinates, not merely
to ordered paths, trivalent trees or canonical linear realizations.
It is a Boolean-port statement. It must not be relabeled as a newly proved
optimal coding-theory constraint-complexity bound or a bound on cyclic
networks. General code realization and vertex-cut results predate this work.

## 4. Consequence for the accepted sparse-check interface

The source `lem:sparse-checks` has m columns, at most 3n rows, and nonzero
kernel weight at least m/P, with

    P=20000 B^2 (floor(log2 m)+1)^2,    m<=Bn.

Appending t rows preserves distance and gives
k>=K=max(0,m-3n-t). When m>P and K>0 take D=ceil(m/P). Since
floor(m/D)<=P, every free-input tree representation has

    Delta >= k / floor(m/D) >= K/P.                            (5)

Using actual rank instead of the row-count upper bound can strengthen K.
No claim is made that every sparsification leaf has positive K. In the
conditional regime K=Omega(m), m>=n and P=polylog(n), this implies
Delta=Omega(n/polylog(n)). The source tensor-contraction theorem requires
Delta<=ceil(s^(9/10)). For a proposed size parameter s=O(n log log n),
the latter is O(n^(9/10)(log log n)^(9/10)), asymptotically smaller than
(5). Merely replacing the ordered chain by a branching tree cannot meet
that contract uniformly in this parameter regime.

Padding the theorem's size parameter does not rescue this inference:
ceil(s^(9/10))>=K/P implies s>=max(0,K/P-1)^(10/9). If K=Omega(n) and
P is polylogarithmic, this parameter grows faster than n log log n.
Consequently plugging that padded parameter into the accepted upper-cost
envelope does not certify a better time bound. This is a limitation of
that invocation, not a lower bound on the actual contraction runtime.

The external bits in (5) are arbitrary independent violation coordinates.
After substituting the actual clause functions z_j=v_j(x), only a subset
of those patterns may occur. The rank and degree bounds need not survive
that restriction. Nor do they cover a cyclic network, a different hash
family, a representation that never exposes all m independent inputs, or a
changed contraction theorem. The existing individual-input wire cost m
is a separate obstruction; the degree argument still has content when
m=Theta(n) so that that simple wire count is affordable.

## 5. Cost scope and the next changed premise

For a supplied tree, the exact construction has polynomial description
and entry work, sum b_e internal wires and maximum degree
max_v(l_v+sum_{e incident v}b_e). Those are the actual parameters to charge;
this proof supplies no smaller uniform exponent for them. It does not
implement the accepted contraction algorithm. Satisfiability still requires
paying sparsification branches, construction and selection of all checks,
every query, clause wiring, weights or isolation, coefficient-ring embedding,
precision, recursive contraction, recovery and any probability amplification.
The source remains selected at alpha=1/2 with its general-density log-log
factor. Independent review of this argument is outstanding.

The next useful change is to exploit restricted clause-violation patterns
before constructing a syndrome network, or to use cyclic topology with a
provably smaller complete budget. Another tree layout alone does not change
the premise of (4). Bounded checks described in README.md test the algebra
and separator claims, not the infinite asymptotic conclusion or SAT runtime.
