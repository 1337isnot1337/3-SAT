# A depth-first workspace bound for the field-clique recursion

This is an author-checked, Codex-assisted conditional argument, not an
independent review or a new SAT bound. It studies the recursive clique query
from Anthropic's `thm:master:b`, using the source's operation accounting and
the field identities and source pins in PR #17. It strengthens PR #84's
**per-factor-entry** workspace statement to the named clique computation,
under an explicit streamability hypothesis. It does not yet prove the entire
arbitrary-density SAT reduction runs in polynomial space.

## Contract and conclusion

Let H be a size parameter bounding the root clique's binary description,
node count, root wire budget, and field modulus bit length. The modulus is a
certified prime; all computations below are in this one field. Suppose:

* Every root table query returns its field element in polynomial(H) workspace
  and at most `tau` bit operations; `tau` is charged for every query.
* For every call size and every permitted piece/direction, piece metadata,
  both factor-entry routines, normalizer and direct piece entries are
  uniformly computable in polynomial(H) workspace. The entry time is at most
  `2^O(lambda) poly(H)` (including metadata), with the same support-bit and rho bounds assumed by
  the cited master recurrence. Enumerating a binary support code and returning
  zero for padding is included; no exponential table is materialized.
* The source's specified parameter recursion and grouping are used, and the
  maximum size of a call and every loop counter, grouping, intermediate bit
  string, and local parameter is bounded by polynomial(H). This follows for
  the source recurrence from the explicit estimate below, but is stated so
  the computational model and root description are unambiguous.

Then a depth-first, nonmemoizing executor computes the field value of the root
clique in polynomial(H) workspace while retaining the source master operation
bound, with root-query cost `tau` charged as in the source and the explicitly
charged `poly(H)` factor and `2^O(lambda)` piece-entry cost. Polynomial-space access to a root table is an
assumption; an arbitrary stored exponential root table is not included.

The factor formulas of PR #84 satisfy the factor-entry part of this hypothesis
for its named structured families with the stated indexing conditions. They
alone do not prove those families have a rho below the required threshold;
their known rate barriers are unchanged. The generic Gaussian-elimination
compiler of PR #17 does not meet this workspace hypothesis merely because its
running time is bounded.

## Size and explicit execution

Write a call's wire budget `N=K^2 lambda`. As derived in PR #16 from the
source child inequality, `N_child <= (c+3)N` for a fixed constant c. Its
parameter recurrence has depth `d=O(log log(2+H))` for a root whose parameters
are bounded by H. Therefore all call wire budgets are at most
`H(c+3)^d`, a polynomial in H. Piece indices, a full assignment of indices
for the at most `g^4/4` crossings, and a grouping of g nodes require
polynomially many bits. Parameters, flags, counters and one node setting have
polynomial bit lengths as well. The following implementation keeps only the
current item of each finite enumeration:

1. At a call, enumerate crossing piece assignments and deterministic candidate
   groupings in the source order. Keep one assignment, grouping and field
   accumulator, and select the source's first acceptable grouping.
2. Describe the grouped child tables *by a frame* containing the grouping,
   piece choices and a link to the parent-table evaluator. A child table
   query enumerates its group settings one at a time, evaluates the required
   parent entries and factor entries, multiplies their residues, and updates
   one field accumulator. Recompute entries whenever requested; do not cache
   a table. If a piece entry is needed instead of one of its two factors,
   enumerate its binary support codes, multiply factors and sum them in the
   field. This takes `2^O(lambda) poly(H)` time and polynomial workspace.
3. Run the next lower clique recursively with those table evaluators. At
   level zero enumerate the edge strings and accumulate one product at a
   time. Multiply by inverse normalizers only when they are nonzero in the
   field, as the field-transfer contract requires.

Each table evaluation and its parents use only a bounded number of active
frames per level; a child evaluation may invoke a parent evaluator, but the
link always goes toward the root and cannot form a cycle. Thus an execution
stack has O(d) recursive-level and table-evaluation frames, each of
polynomial(H) size. Loop counters represent exponentially many possibilities
in polynomially many bits. Arithmetic stays in F_p: field accumulators have
`O(log p)` bits and no integer sum of exponentially many terms is stored.
The stated root-table evaluator can itself use polynomial(H) workspace.
Hence the total is polynomial(H), including the call stack.

## Time, and what this does not establish

The source grouping proof bounds the number of table queries and charges the
cost of evaluating each queried grouped entry by enumerating group settings.
The executor performs exactly that on-demand enumeration. Recomputing a table
entry is not an uncharged extra step: each query pays for it in that bound.
Replacing direct piece lookup by the streamed support sum costs
`2^O(lambda) poly(H)`, absorbed in the source's existing entry-cost term after
increasing its constant. Polynomial-space metadata and factor routines are
likewise charged in this term. The source's grouping search, assignments,
recursion and base-case enumerations remain in its recurrence; no exponential
cache or hidden randomization is introduced. Thus its master time envelope
continues to apply under the above hypotheses, up to the stated polynomial
arithmetic cost. This is a space claim for the *field-clique query*, not a
new proof of the external theorem.

For deterministic exact integer network queries, PR #60 performs polynomially
many such field queries sequentially and CRT-reconstructs a balanced integer.
If the prime inventory, query bounds, CRT state and original root-table
routines are polynomial-space, this wrapper also uses polynomial workspace.
Applying that wrapper to a full fixed- or general-density SAT algorithm still
requires independent accounting of every reduction, profile, query,
sparsification branch and its enumeration stack; it is not claimed here.

The finite checker uses a two-layer lazy grouped contraction with signed
entries, compares each field query to independent exhaustive enumeration and
reconstructs via CRT. It verifies the finite evaluator and stack lifecycle,
not the master recurrence, its asymptotic time, or its SAT composition.
