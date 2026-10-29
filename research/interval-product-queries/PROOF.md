# Consecutive information sets for adjacent-product queries

## The result

Let n>=3, let A be an a-by-n binary matrix, and let b be a binary
vector of length a. On cyclically indexed Boolean variables set
`m_i=x_i x_(i+1)`. We give a deterministic exact algorithm for

    A m = b over F_2.

If the linear system is inconsistent it returns zero in polynomial
time. Otherwise let d be its nullity. Let r be the greatest length of
a cyclically consecutive interval of coordinate functionals that are
linearly independent when restricted to ker A. Equivalently, r is the
largest interval on which the kernel projection is onto all binary
words. Then the count is computed in

    poly(n+a) 2^(d-r) lambda^r bit operations

and polynomial space, where lambda=1.754877666... is the Perron root
of `z^3-2z^2+z-1`. Both d and r, and the interval, are found in
polynomial time. The estimate includes r=0; then lambda^0=1. It applies
to arbitrary explicit A, sparse or dense. No structural guarantee makes
r a positive fraction of d, and this class is not all sparse polynomial
systems or all SAT instances.

## Proof and algorithm

First solve A m=b by Gaussian elimination, obtaining an origin m_0 and
basis vectors B_1,...,B_d for the kernel. If inconsistent, no Boolean x
can satisfy the equations. Otherwise write every solution uniquely as
`m=m_0+sum_j z_j B_j`, z in F_2^d. The coefficient row w_i for
coordinate m_i is the vector of the ith bits of the B_j. It is a
coordinate functional on the kernel.

For every cyclic start position, scan consecutive w_i until dependence,
maintaining an exact binary linear basis. Once dependent, longer
intervals from that start remain dependent. This finds a longest block
I, of length r<=d, in polynomial time. Greedily append other coordinate
functionals to I until a basis of the dual kernel space is obtained.
That is always possible: the coordinate functionals of any subspace
separate its vectors. The resulting d positions form an information
set. Precompute the inverse of their d-by-d coefficient matrix, including
the affine offset from m_0; any values on these coordinates then specify
exactly one kernel vector. For d=0 the information set and inverse are
empty, with the unique linear solution m_0.

Any adjacent-product vector m avoids cyclic 101: two 1 edges around a
0 edge would force both ends of the zero edge to 1. Conversely, if a
cyclic word contains at least one 1 and avoids 101, its 0 runs have
length at least two and each can be filled independently. A 0 run of
r_i edges between forced-1 endpoints has `F_(r_i-1)` valid assignments,
where F_0=0, F_1=1. Thus its total preimage weight is the product of
these Fibonacci numbers; the empty product for the all-one word is 1.
The all-zero word has `F_(n-1)+F_(n+1)` preimages, the cycle independent
set count. This proves necessity, sufficiency, and the exact weight.

Enumerate every binary r-word avoiding 101 as the actual values of m on
I, and every assignment to the other d-r information coordinates. The
values are actual affine m bits, not the z bits: subtract m_0 before
applying the precomputed inverse. Reconstruct m, test the entire cyclic
word for 101 including both ends of I and the cyclic boundary, and sum
its exact preimage weight. A realizable m has a 101-free I, so it appears
in this enumeration exactly once. Unrealisable candidates contribute
zero. The total is the exact number of x.

The count a_r of length-r words avoiding 101 is bounded by
O(lambda^r): the three-state automaton for suffixes of 101 has primitive
transition matrix `[[1,1,0],[0,1,1],[1,0,0]]` and that characteristic
polynomial. Thus there are O(2^(d-r) lambda^r) candidates. The scan,
linear algebra, decoding, cyclic test and Fibonacci weights have
polynomial bit cost per candidate, including output and accumulator
lengths at most n+1 bits. A depth-first prefix generator and one
candidate at a time give polynomial space and the stated worst-run
time. There is no randomness or amplification. This is a direct exact
count for the specified query; it does not implement the source's
sparsification, greedy candidate selection, contraction, or recovery.
An all-input SAT composition would need to account for all of them.

## A barrier to unconditional savings

For every d>=2 take n=2d and constraints m_(2j)=m_(2j+1),
0<=j<d. The kernel has dimension d. Its coordinate functionals are
`e_0,e_0,e_1,e_1,...,e_(d-1),e_(d-1)` in cyclic order. Every cyclic
interval of length three contains a duplicate, while some interval of
length two is independent, so r=2. These equations also have the zero
product vector, so their affine system is consistent. Consequently the
bound above alone gives only a constant-factor saving over 2^d for this
family. This is not a lower bound on other algorithms; a different
representation may exploit the duplicated structure.

## Evidence and attribution

`python3 -I -B research/interval-product-queries/verify.py` exhausts all
4,096 affine 3-by-3 systems and tests 1,200 seeded systems with n=4..9
against direct enumeration of every Boolean x, for 5,296 comparisons in
all; 1,766 systems have an inconsistent linear relaxation. The checker
also validates the duplicated-coordinate control at n=8, d=4, r=2.
It does not mechanically prove the all-size cost or correctness.

The adjacent-product kernel-prefix method and Fibonacci run criterion
were first worked out for cyclic operators in the concurrent
[PR #54](https://github.com/1337isnot1337/3-SAT/pull/54), at head
`1f647600ac7eecf4663dc940c17275cc3a0619fc`. The argument here is
self-contained, generalizes that approach to arbitrary matrices and
includes a concrete information-set limitation. It does not use that
unmerged branch as a code dependency. OpenAI's owner-accepted baseline
is fixed by `certificates/selected-result.json`; source labels include
`lem:tensor-sparse-query` and `thm:tensor-contraction`. The present
work neither audits nor changes that theorem. Substantial AI assistance;
no independent or formal review claimed.

## Several independent intervals

The same algorithm permits information scattered across disjoint cyclic
intervals I_1,...,I_t, provided that **all** their coordinate functionals
together are linearly independent. Let their lengths be ell_j and put
s=sum ell_j. Extend their ordered coordinates to an information set,
enumerate a 101-free word on each interval, and enumerate the remaining
d-s bits. After reconstructing m, test all cyclic adjacencies, including
boundaries between intervals and their complements. No realizable word
is lost, and each is counted once. This gives

    poly(n+a) 2^(d-s) product_j a_(ell_j)

bit operations and polynomial space. The product counts candidates,
not a claim that local constraints alone guarantee realizability.
When one interval of maximum length is used, this recovers the earlier
bound. Given any supplied intervals, joint independence and disjointness
can be checked in polynomial time.

A simple uniform choice needs no optimization oracle: scan the
nonwrapping consecutive triples in order, accepting a triple if it is
disjoint from all accepted ones and its three functionals extend their
joint linear independence. This takes polynomial time. For t accepted
triples, s=3t and a_3=7, giving `2^(d-3t) 7^t` candidates. Compute this
integer and the single-block count `2^(d-r) a_r` in polynomial bit time,
then use the smaller enumeration; a_r is obtained from its three-term
recurrence, not by enumerating all prefixes. This construction does not
claim the greedy choice is optimal.

The two approaches can differ exponentially. For any t>=2, take n=4t
and impose `m_(4j+2)=m_(4j+3)` for all j. The kernel dimension is 3t;
its coordinate functionals are t blocks of four, with the last two in
each block equal and all others distinct. The largest independent
consecutive interval has length 4, while the first three coordinates in
each four-block form t disjoint, jointly independent triples. The
single-interval count is `12*2^(3t-4)`, while the triple count is `7^t`.
Their ratio tends to zero exponentially as t grows. This compares the
two candidate enumerations, not the underlying counting problem or SAT
complexity. At t=3, the checker confirms 343 versus 384 candidates and
verifies the resulting exact count by all 4,096 original assignments.
All 5,296 earlier systems are also evaluated using the triple method.

## Exact count of the short-interval control

The duplicate-pair family above is easy for a different representation.
More generally impose `m_(2j)+m_(2j+1)=b_j` for j=0,...,d-1, with
n=2d and d>=2. Put y_j=x_(2j) and z_j=x_(2j+1). The jth equation is
`z_j (y_j+y_(j+1))=b_j` over F_2. After summing z_j, its transfer
matrix on successive y bits is

    T_0 = [[2,1],[1,2]],       T_1 = [[0,1],[1,0]].

The count is the trace of their cyclic product. Both matrices have the
common eigenvectors (1,1) and (1,-1), with respective eigenvalues
(3,1) for T_0 and (1,-1) for T_1. Writing w=|b| gives the exact count

    3^(d-w) + (-1)^w.

This is computable in polynomial bit time and space, and for b=0 yields
`3^d+1` (82 when d=4). Thus the small-r example limits the information
set bound, not the complexity of the instance. This is a direct
application of the bounded-span transfer idea in
[PR #48](https://github.com/1337isnot1337/3-SAT/pull/48); no novelty or
priority is claimed for the technique. The checker exhausts all 124
right-hand sides for d=2,...,6 against the original Boolean equations.

## The general class can encode 3-SAT decision

Deciding whether `A m=b` has a Boolean preimage `m_i=x_i x_(i+1)` is
NP-complete, even when every row of A has at most two nonzero entries.
This is a polynomial-time decision reduction, not an exponential-time
lower bound and not a parsimonious counting reduction. It explains why
the arbitrary-A class should not be treated as uniformly easy.

Take a 3-CNF formula with v declared variables and c clauses, each
listed with exactly three literals; repetitions and both signs are
allowed. If v+c>0, create a cyclic product word with the following
blocks, in order:

- for each original variable, a reference coordinate u followed by 00;
- for each clause with literal truth values L_1,L_2,L_3, the three
  coordinates `(1+L_1,L_2,1+L_3)` followed by 00.

All additions here are in F_2. Each reference coordinate is free. Fix
every separator to zero by a one-coordinate equation. Express each
clause coordinate as its reference variable or its complement by a
two-coordinate affine equation. The resulting matrix has n=3v+5c
columns and a=2v+5c rows, each of weight at most two. Its affine
solution space is nonempty and has nullity exactly v: every assignment
to the references determines every other coordinate uniquely. If v=c=0,
use a three-coordinate all-zero product word as a fixed special case.

The only possible 101 occurrences lie entirely inside a clause gadget:
every block ends in 00, including the last block across the cyclic
boundary, and a reference block has only one nonseparator coordinate.
Inside a clause gadget the pattern is 101 exactly when all three
literals are false. Hence an original assignment satisfies all clauses
if and only if its unique affine product word avoids cyclic 101. By the
preimage characterization above, a cyclic word avoids 101 if and only
if it equals the adjacent-product word of at least one Boolean x. Thus
the source formula is satisfiable precisely when the constructed query
is. The mapping and sparse matrix are built in polynomial time; an x
witness verifies a query in polynomial time, establishing membership in
NP and hence NP-completeness under the usual polynomial reductions.
Unused declared variables are retained as free references. Any ordinary
width-at-most-three clause can be padded by repeating a literal; empty
clauses are immediate unsatisfiable inputs.

The reduction does not preserve the number of solutions: a product
word can have several x-preimages. For example, the empty formula with
one declared variable has two assignments, while its constructed query
has five x-solutions (the product words 000 and 100 have four and one
preimages). No #P-hardness or counting-preserving reduction is claimed.
An NP-completeness statement alone says nothing about whether an
algorithm has a particular exponential or subexponential time bound.

`reduction.py` checks all 4,160 one- and two-clause formulas over two
variables, including repeated and negated literals, for all 16,640
source assignments. It verifies affine nullity and row weight, compares
the candidate product word's 101 predicate to source satisfaction,
and checks the exact query counter's decision. It also enumerates x
directly for ten selected formulas, including a contradictory pair,
and tests both empty-formula controls. This finite evidence is not a
substitute for the all-size reduction above.
