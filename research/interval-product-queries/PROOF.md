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
