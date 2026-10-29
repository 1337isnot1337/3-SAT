# Polynomial construction of the initial sparse checks

## Result and scope

For the parameters and matrix contract of the accepted source `lem:sparse-checks`, its initial matrix A^(0) can be constructed deterministically in poly(n,m,B) bit operations and space. This changes only how the existing Cayley shifts and local check matrix are found; the graph, Tanner proof, source parameters P and D0, number of rows, row lengths and distance guarantee stay as in the source. Here B is treated as a positive integer, as in the lemma, and the polynomial is in its numeric value; in the application B is polylogarithmic in n. This uses the source's Tanner mixing argument, not a new proof of the accepted theorem.

Write mu=floor(log2 m)+1, epsilon=1/(200 B mu), delta=2 epsilon, d=min(m,D0), and q the source's least power of two satisfying qd>=m. If q=1 there are no nontrivial characters and the shift construction is vacuous. Otherwise d=D0>=2 and qd<2m, hence q<m. The source needs d shifts s_j in F_2^log2(q) such that every nonzero character sum has absolute value <=epsilon d.

## Constructing the shifts

Use conditional expectation with exact rational arithmetic. Put t=epsilon/2 and define, for each nonzero character chi, the two products

    W_chi,+ = product_{j chosen} (1+t chi(s_j)),
    W_chi,- = product_{j chosen} (1-t chi(s_j)).

The sum Phi of all these products starts at 2(q-1). At each step, averaging over a uniformly chosen next shift preserves Phi exactly, since every nontrivial character is balanced. Enumerate all q shifts and choose one that does not increase Phi. After d choices Phi<=2(q-1)<2m<2^(mu+1).

If a character sum has absolute value greater than epsilon d, choose the product with the corresponding sign. Since 0<t<=1/2 and ln(1+x)>=x-x² for |x|<=1/2, its logarithm is at least t epsilon d-t²d=epsilon²d/4. With d=D0=320000 B² mu³ this is 2mu. But exp(2mu)>2^(mu+1) for every positive integer mu, a contradiction. Thus the chosen shifts meet the source's two-sided Walsh condition.

Each factor has denominator 400 B mu. Represent every product after the same number of steps by its integer numerator over the common denominator. There are 2(q-1) products, at most q candidate next shifts per step, and d steps. Numerators have O(d log(B mu+2)) bits; updating and comparing them is polynomial in q,d,B,mu. Compute one candidate at a time; no random generator or numerical exponential is needed. The logarithms above are only a proof of correctness.

## Constructing the local code

Put c=ceil(d/(8B)), h=ceil(delta d)-1. The source needs a binary c-by-d matrix whose kernel has no nonzero word of weight <=h. When h=0 use the all-zero matrix. For h>0, d>=2. Let r=ceil(log2 d), so r<=mu because d<=m<2^mu. Construct F_(2^r) by finding an irreducible binary polynomial of degree r via trial division over all monic polynomials of degree <=r/2; enumeration and field operations take poly(2^r,r)=poly(d) time. Pick d distinct field elements a_1,...,a_d. Form the h-by-d field matrix V_(i,j)=a_j^i, i=0,...,h-1, with a_j^0=1. Expand each field entry into r binary coordinates; pad with zero rows to c rows. This defines a binary check matrix.

Any nonzero binary vector supported on s<=h coordinates cannot lie in its kernel: its first s field equations form a square Vandermonde system on distinct a_j, whose determinant is the nonzero product of their pairwise differences. The number of binary rows before padding is rh. As h<delta d=d/(100 B mu) and r<=mu, rh<d/(100B)<=c. Thus the matrix fits the source row budget. This argument needs no enumeration of local words.

## Composition and limits

Insert the shifts and local matrix into the source's bipartite Cayley-Tanner construction, shorten to m edge coordinates and retain all its inequalities. The source proves at most 3n rows of weight at most D0 and every nonzero kernel word has weight at least m/P. Construction of the qd<2m edges, their endpoint checks and all output rows is polynomial in n,m,B; handle q=1 exactly as the source does. Finite-field search and potential arithmetic are polynomial in the same numeric parameters. No bound on the total SAT exponent is improved: the greedy counts and tensor contraction still incur their original costs unless a separate result is composed. The polynomial greedy-candidate contribution is PR #51, which is independent of this construction and is not assumed here. No new selected alpha or independent review is claimed.
