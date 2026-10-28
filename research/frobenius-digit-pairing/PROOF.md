# Base-p digit oscillators: pairing repair and local obstruction

Fix a prime p. For every original positive grade k and every j>=0, introduce
an independent variable `y_{k,j}` of grade `k p^j`, with relation
`y_{k,j}^p=0`. Work over F_p in the tensor product of these truncated
polynomial algebras. Each finite grade has finitely many variables and basis
monomials. The ordinary derivative `d/dy_{k,j}` descends to this quotient,
since the derivative of `y_{k,j}^p` is zero in F_p.

Let multiplication by y be creation and its ordinary derivative be
annihilation. Their commutator is the identity, including at the top degree:
when m=p-1 the product y*y^m vanishes, and `-(p-1)=1` in F_p. The vacuum
pairing between digit monomials is diagonal, and the diagonal entry at
occupations `d_{k,j}` is `product d_{k,j}!`, nonzero for all `0<=d<p`.
Consequently the pairing is nondegenerate grade by grade.

Map each original occupation n_k to its unique base-p digits d_{k,j}:

    n_k = sum_j d_{k,j} p^j,       0<=d_{k,j}<p.

This gives a grade-preserving bijection between ordinary partition monomials
`product t_k^n_k` and the digit monomials `product y_{k,j}^d_{k,j}`. Hence
for every grade E the dimension is exactly the ordinary partition number
P(E), not merely an asymptotic upper bound. Equivalently,

    product_{k,j>=0} (1-z^(k p^(j+1)))/(1-z^(k p^j))
      = product_{k>=1} 1/(1-z^k),

where the left product has k>=1, j>=0 and the telescoping is formal in z.
Thus this label-pairing repair alone makes no improvement to the graded
state count. It is a new representation, not a proof that Anthropic's dual
label recovery or crossing pieces survive.

## A direct crossing-interface obstruction

The most immediate choice of one degree-k oscillator is
`D_-k = y_{k,0}` and `D_k = d/dy_{k,0}`. Its commutator is 1 for each
positive k, -1 for negative k, and 0 at k=0. In the source's existing h=1
three-term two-order test, the difference is minus the second difference of
this sequence. At s=1, it is `-(0-2+1)=1`, a nonzero identity operator
in every characteristic. The defect is witnessed on the vacuum. Therefore
the nondegenerate digit pairing does not by itself give the required
operator identity. Weighting the chosen annihilator by k restores that
particular commutator but makes it zero at p-divisible k; no recovery of the
full crossing identity is claimed from such reweighting.

## Costs and scope

At grade at most E, only digit variables with `k p^j<=E` can appear. Their
count is `sum_{j>=0} floor(E/p^j) <= 2E` for every prime p. An occupation
vector, its digit encoding, grade, and any single creation/annihilation
entry can be computed in polynomial time in E and log p using standard field
arithmetic. Enumerating the whole grade still takes P(E) entries. These
facts are local representation costs, not a uniform two-direction crossing
construction, a global recursive algorithm, or a claimed SAT bound. Source
pieces, dual label identity, denominators, output recovery, field choice,
recursion, bit cost and space remain open. The exact source convention for
the h=1 test is documented in the merged scalar predecessor
`research/sparse-oscillator-locality/PROOF.md`; the finite-characteristic
pairing radical appears in `research/weighted-oscillator-rigidity/PROOF.md`.

## Carry-aware source commutator and its vacuum radical

The digit labels also permit a different operator choice. For each k, write
`|n>_k` for the digit monomial encoding the ordinary occupation n, and set

    R_k |n>_k = |n+1>_k,
    L_k |n>_k = k(n mod p) |n-1>_k,  with L_k |0>_k = 0.

R performs base-p carry; L performs borrow followed by the indicated field
coefficient. These are linear operators on the digit-basis vector space,
not the preceding multiplication/derivative operators. Their grade shifts
are +k and -k, and, for every n,

    (L_k R_k - R_k L_k)|n>_k = k |n>_k.

Operators associated with distinct original k commute. Thus their h=1
commutator sequence is the original linear `g(k)=k` over F_p, and the
three-term second differences vanish at every shift. The action on the
ordinary occupation basis is the standard creation/derivative action
reduced modulo p, so implementing one such operator requires only a
base-p increment or decrement and field multiplication.

However, the vacuum pairing generated specifically by these operators is

    <0| L_k^m R_k^n |0> = [m=n] k^n n!  (in F_p).

It vanishes for every n>=p and also for positive n when p divides k. Thus
the original source commutator and a nondegenerate digit pairing coexist on
the same graded vector space only as **different operator interfaces**: the
carry-based annihilators do not generate the full nondegenerate digit
vacuum pairing. This is an exact component identity and does not rule out
another operator construction linking them. It also does not establish the
remaining source crossing, factorization, or cost contracts.

## General vacuum-pairing obstruction

The preceding factorial radical is not special to base-p carries. Let V be
a vector space over a field of characteristic p, with operators L,R and a
nonzero vacuum v satisfying `L v=0` and `[L,R]=c Id`. Let a linear vacuum
functional omega obey `omega(v)=1` and `omega(R w)=0` for every w; a
projection to degree zero has this property when R raises a positive grade.
The elementary commutator induction gives

    L R^n v = n c R^(n-1) v,
    omega(L^m R^n v) = [m=n] c^n n!.

These formulas hold in every characteristic. At n=p the second expression
vanishes for every m. Consequently either `R^p v=0`, losing that state in
the R-generated sector, or the nonzero state `R^p v` lies in the right
radical of its pairing with the L-generated vacuum functionals. In
particular, a nondegenerate pairing between all distinct R-generated states
and the L-generated dual states cannot coexist with the scalar commutator
in characteristic p. If c=0, the defect occurs already at n=1.

This theorem applies to arbitrary representations with these stated vacuum
and commutator conditions, not only the carry example. It does not prevent
additional annihilators or a different functional from detecting `R^p v`,
nor does it rule out an altered commutator or a different crossing identity.
The nondegenerate digit pairing uses exactly such extra digit operators, and
there is no claimed full source identity tying them to the carry operators.
