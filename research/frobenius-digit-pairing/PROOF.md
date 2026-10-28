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
