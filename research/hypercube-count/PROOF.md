# Exact count of the bipartite hypercube system

This is an exact counter for one explicit family of quadratic F2 systems,
not a bound for general SAT or sparse queries. The all-size arguments are
author-checked with substantial Codex assistance and await independent review.
The family arose in the local continuation of
[issue #29](https://github.com/1337isnot1337/3-SAT/issues/29#issuecomment-6459412498),
and is different from the oriented single-cube family in
[PR #73](https://github.com/1337isnot1337/3-SAT/pull/73). Both have an
obvious SAT solution; this package addresses exact counting.

## Statement

For d>=1 put m=2^d, with binary variables x_v,y_v indexed by v in F2^d,
and impose, for each v,

    x_v sum_(j=1)^d y_(v xor e_j) = 0 over F2.

Let A_d be the m-by-m cube adjacency matrix over F2. Its square is
(d mod 2)I: diagonal entries count d length-two returns, while every
nontrivial length-two destination appears twice. For fixed y, put z=A_d y.
The equation at v leaves x_v free if z_v=0 and forces x_v=0 otherwise.
Hence the exact number of solutions is

    C_d = sum_(y in F2^m) 2^(m-wt(A_d y)).                     (1)

When d is odd, A_d is its own inverse, so z ranges once over F2^m and

    C_d = sum_z 2^(m-wt(z)) = 3^m.                              (2)

When d is even, let q=m/2 and B=A_(d-1), so B^2=I. Ordering indices by
one coordinate gives A_d=[[B,I],[I,B]]. Its image is exactly
{(w,Bw): w in F2^q}: every output has that form, and A_d(0,w)=(w,Bw).
Its rank and nullity are both q, so every image point has 2^q preimages.
Consequently

    C_d = 2^q sum_(w in F2^q) 2^(m-wt(w)-wt(Bw)).               (3)

For example C_1=9 and C_2=100. Equation (3) is an exact weight-enumerator
identity, not a claimed closed form or polynomial-time method for even d.

## Arbitrary fixed-bit branches for odd d

Suppose d is odd. Let X0 and X1 be the sets of fixed-zero and fixed-one
x variables, F their free complement, and Y the set of fixed y variables,
with prescribed values b_i. Put b=|Y|. Because A_d=A_d^-1, the change of
variables z=A_d y makes y=A_d z. For each z_v, summing over the allowed
x_v contributes a unary weight f_v(z_v):

    x_v free:     f_v(0)=2, f_v(1)=1;
    x_v fixed 0:  f_v(0)=1, f_v(1)=1;
    x_v fixed 1:  f_v(0)=1, f_v(1)=0.

For a in F2 write H_v(a)=sum_(t in F2) f_v(t)(-1)^(at). Thus H_v is
(3,1), (2,0), or (1,1), respectively. The b constraints (A_d z)_i=b_i
for i in Y can be expanded by character orthogonality. With 1_T the m-bit
indicator of T subset Y, the branch count is exactly

    2^(-b) sum_(T subset Y) (-1)^(sum_(i in T) b_i)
                   product_v H_v((A_d 1_T)_v).                (4)

This is an integer: it was obtained from the sum of exact Boolean indicator
products, and the division is performed in the integers after summation.
It also handles contradictory branches, for which the answer is zero.
Evaluating (4) uses poly(m) 2^b bit operations and polynomial space; every
intermediate numerator has O(m+b) bits. No field inverse or randomness is
needed. When the source high-incidence step fixes B variables, b<=B, so
this gives a per-branch cost poly(m) 2^B; it does not claim that a general
sparse query has the same structure. Even d is not covered by (4).

## Arbitrary fixed-bit branches for even d

Let d be even, q=m/2 and B=A_(d-1), and split y into two q-bit halves.
For each image vector z=(w,Bw), all of its preimages are

    y=(u,w+Bu),    u in F2^q.                                 (5)

Indeed the first image half is Bu+(w+Bu)=w and the second is u+B(w+Bu)=Bw.
For prescribed y bits, the low-half restrictions are equations u_i=b_i;
the high-half restrictions are (Bu)_i=b_(q+i)+w_i. Solve this binary
linear system for u using Gaussian elimination. It has either zero or
2^(q-r) solutions, where r is its coefficient rank. The coefficient matrix
is independent of w, although recomputing elimination for each w is already
within the stated time.

For each w, reject it if any x fixed to one has corresponding z_v=1.
Otherwise each free x at a coordinate z_v=0 contributes a factor two; fixed
x=0 contributes one. Multiply this weight by the number of compatible u,
and sum over all 2^q choices of w. This handles all prescribed x/y bits,
including inconsistent branches, in poly(m) 2^(m/2) bit time and polynomial
space. With no fixed variables it reduces to (3). It does not provide a
faster even-d exponent or an algorithm for general sparse queries.

## Uniform bit complexity and scope

Read d or the explicit instance, compute m=2^d, and construct the hypercube
neighbor lists in O(md) word operations. For odd d, compute 3^m by repeated
squaring in polynomial bit time. For even d, enumerate all q-bit w and
compute Bw from the q(d-1) adjacency incidences. Each summand and the
accumulator are at most 2^(2m), so all integers have O(m) bits. The resulting
uniform algorithm uses O(poly(m) 2^(m/2)) bit operations and polynomial
space; no randomness or hidden preprocessing is needed. A finite input can
be handled directly, including d=1; there is no asymptotic parameter
fallback or precision issue.

The branch formulas cover arbitrary fixed x and y bits in this family;
other private-edge systems, arbitrary row transformations as a representation
of a different system, and general sparse queries require separate treatment.
Invertible row transformations of this exact system preserve its solution
set and therefore its count. These formulas do not refute its coefficientwise
support obstruction: an aggregate computation can avoid enumerating the
lift's nonzero incidence coefficients. No comparison establishes a new
selected SAT time bound or improvement in alpha.
