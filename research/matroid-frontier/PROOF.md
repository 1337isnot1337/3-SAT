# A frontier network for the binary-matroid predicate

This is an author-checked component argument, awaiting independent review. It
builds on the shared-code identity in
[characteristic-two-decision/FOLLOWUPS.md](../characteristic-two-decision/FOLLOWUPS.md).
No SAT time improvement is asserted.

## The exact state invariant

Let A have columns v_1,...,v_m in F_2^a, in a fixed specified order. At cut i,
write U_i=span(v_1,...,v_i), F_i=span(v_{i+1},...,v_m), and
E_i=U_i intersect F_i. Its width is b_i=dim E_i; let b=max_i b_i.
Given previously chosen columns, let P_i denote their span. Keep the state
X_i=P_i intersect F_i, provided the chosen prefix is independent. Thus
X_i is a subspace of E_i and X_0=0. Reject dependent prefixes permanently.

At column v=v_{i+1}, if its selection bit is 0, set X_{i+1}=X_i intersect
F_{i+1}. If the bit is 1, reject exactly when v belongs to X_i; otherwise set
X_{i+1}=(X_i+span(v)) intersect F_{i+1}. These operations are in the ambient
space F_2^a. The test is correct because v is in F_i, so v in P_i iff
v in P_i intersect F_i. For either choice of bit e, the state update is exact:

    (P_i + span(e v)) intersect F_{i+1}
      = ((P_i intersect F_i) + span(e v)) intersect F_{i+1}.

Indeed the right side is contained in the left. Conversely, if p+e'v is in
F_{i+1} subset F_i, then p is in F_i, since v is in F_i. Here e' is zero
when e=0, and otherwise ranges over F_2. This proves the invariant by
induction, including zero columns and an empty matrix. At i=m, F_m=0, so
every surviving run has the unique final state 0. There is exactly one run
for an independent selected set and none for a dependent one.

## State count, construction and cost

Every state is a subspace of an at-most b-dimensional space. A k-dimensional
subspace has a unique reduced row-echelon basis. For any fixed pivot set its
free entries number at most k(b-k), and there are binom(b,k) pivot sets.
Consequently the total number of states in any layer is at most

    sum_k binom(b,k) 2^(k(b-k)) <= 2^(floor(b^2/4)+b).

The bound need not be tight; the zero and full subspaces are included. Prefix,
suffix and intersection bases are computable by Gaussian elimination over
F_2 in time polynomial in a and m. Fix a canonical basis for each E_i and
encode a state by its unique reduced row-echelon basis in a zero-padded
b-by-b binary matrix; reject malformed encodings. State transitions and
membership are decidable by polynomial-time binary linear algebra. Thus a
layered deterministic branching program has at most the stated number of
live states per layer, with polynomial-time generated transitions. Explicitly
listing all possible states costs up to 2^O(b^2) per layer; the succinct
transition predicate does not require such enumeration.

Equivalently, over any field, use one 0/1 transition tensor per column, with
the input selection bit and the two b^2-bit state encodings as ports; fix the
first and final encodings to zero. Summing internal state bits yields exactly
the independence indicator: each selection has either one valid path or
none. The m transitions introduce O(m b^2) state-bit incidences and have
arity at most 2b^2+1, with polynomial-time entry evaluation and polynomial
length descriptions. At b=0, the state is the unique empty encoding. A
straight scan using the actual reachable subspaces takes at most
poly(a,m) times 2^O(b^2) state operations per layer. It is not claimed that
this describes the full SAT input or solves its remaining costs.

## Shared-hash identity and what the construction does not establish

For any Boolean selection vector z, the predecessor identity is

    1[A z = 0] = sum_{S independent} product_{j in S} z_j   (over F_2).

This follows by Boolean subset inversion: the coefficient for S is the
parity of 2^(|S|-rank(A_S)). The transition network computes its independent
set coefficient predicate. To evaluate the entire polynomial one can sum
selection bits, weighting selected j by z_j, in characteristic two. This
network is exact; it is a circuit/interface construction, not a complete
contraction theorem or bound on general-density 3-SAT.

After substituting the actual clause-violation polynomials, one must still
supply all external consistency and multiplication tensors, bound m and b
for the actual hash matrices and a uniformly computable ordering, and pay
wire count, maximum degree, descriptions, entry time, all queries, branching,
precision, recursion, recovery, and randomized amplification. The state
network uses characteristic two; a transfer to the accepted two-adic interface
must specify an appropriate embedding and output semantics. No unproved
small-width assumption is made. Exhaustive ordering search can itself be
expensive. Even O(m b^2) auxiliary incidences alone need not improve the
existing O(n log log n) wire envelope. These gaps preclude any change to the
selected result or alpha.

## Sparse cut-rank control

Take A=[I_b | I_b], ordered with the first copy before the second. Each
column has one nonzero and each row has two. The middle frontier is all of
F_2^b, hence width b. At that cut, indexing the two sides by subsets S,T of
[b], their union is independent exactly when S intersect T is empty. Its
flattening matrix is the b-fold Kronecker power of

    [[1, 1], [1, 0]],

whose determinant is -1. It therefore has rank 2^b over every field, including
F_2. Any exact sum of separable functions across this fixed cut needs at least
2^b terms, by the matrix rank bound. This applies to any exact path-state
factorization across that cut, regardless of cancellation or state encoding.
It is not a lower bound on arbitrary orderings: interleaving the two copies
has width at most one and a constant-state representation. It is also not a
SAT lower bound, nor a matching lower bound for the general 2^O(b^2) upper
bound. It shows that column sparsity alone does not control the width or
rank of a prescribed cut.
