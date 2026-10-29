# What the finite recovery computation certifies

This is a finite test of a possible full-bound mechanism. It does not assert
an all-size recovery theorem or a running-time improvement.

Let f_(X,S)(T)=product_(x in S) sum_(y:X_y=1) W_xy(T), where W is the
accepted L-slot Cauchy kernel. The row monomials form an integral basis for
all row tables (Boolean subset inversion is unimodular). A COMMON linear
functional recovering origin parity for every column input and every row
table must therefore work on all 4^L generators f_(X,S).

For a set of nodes, the data matrix A has one column per generator and one
row per shifted Taylor coefficient. The target vector t records f_(X,S)(0).
At modulus 2^p, target parity is determined for arbitrary integer linear
combinations precisely when every x in ker(A mod 2^p) satisfies t.x=0 mod 2.
This universal linear-functional question is stronger than recovery for one
fixed X. A lower certificate for the linear span is NOT automatically a pair
of legal Boolean rank-one row/column tables indistinguishable by every
nonlinear recovery method.

The standard-library solver computes U A V diagonal modulo 2^P with entries
2^d_j using invertible row and column operations; it updates t to t V.
The minimum p<=P is one more than the largest d_j whose transformed target
is odd. If an unresolved zero-pivot coordinate has odd target, the result
is only failure at the chosen cutoff P. For a claimed threshold p, the
implementation constructs a row combination satisfying

    dual A = 2^(p-1) t modulo 2^p,

and independently checks it against the original matrix. It also constructs
a kernel vector at p-1 with odd target. Cutoff failures similarly include a
kernel check at P. Exhaustive small-ring enumeration checks the solver
separately from the packet constructor. The zero target needs no data.

## Exact polynomial-lattice compression

Put c=C'(0), d=L(2L-1), and g_(X,S)=c^L f_(X,S). Each g is an integer
polynomial of degree at most d. To retain data modulo 2^P, put
v=v2(c^L), Q=P+v, and adjoin the artificial generators 2^Q e_j in the
coefficient basis 1,T,...,T^d. Their shifted coefficients and origin values
vanish modulo 2^P after division by c^L, so adjoining them changes no data.

Exact integer row Hermite forms of the g coefficient vectors together with
these artificial generators give a lattice basis of d+1 rows. Shifting each
basis polynomial by T=t+2Lz, dividing out 2^v, and multiplying by the inverse
of the odd part of c^L gives the compressed data. All divisions by 2^v are
checked to be exact. Equality of the generated coefficient lattices means
a common recovery identity holds on the original generators iff it holds
on this basis, at the declared modulus. For L=2,4, the program checks the
explicit Hermite transformation H=U A and compares every reported threshold
with the uncompressed constructor. The larger screen uses FLINT's exact
integer Hermite implementation and processes every generator; its basis
hash, precision and generator count are recorded. No floating ranks occur.

## The precision profile relevant to mode cost

At node valuation i, the source charges D_i=L/2^i. A uniform precision
threshold alone does not describe its mode budget. To test p_i=q D_i,
choose P>=max p_i and multiply each node's rows by 2^(P-p_i). These scaled
rows modulo 2^P carry exactly the original data modulo their specified
p_i. Binary search over integer q, with a dual at the accepting endpoint
and a kernel witness at the preceding endpoint, gives the exact threshold
within this one-parameter finite profile. This is not an optimization over
all possible recovery schemes or input-aware methods.

## Full-bound obligations

An improved packet identity is insufficient without global composition.
The accepted grouping uses one coordinate i across the call; independent
per-packet choices of valuation can destroy that grouping. A proposal must
pay all node choices or preserve a common grouping, provide uniform
coefficients with affordable bit lengths, retain valid child degrees and
entry routines, account for inherited precision, and then compose every
outer reduction. The current screen establishes none of those new facts.
The unrestricted target and the selected baseline remain unchanged.
