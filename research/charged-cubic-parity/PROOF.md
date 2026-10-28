# Cubic moments on fixed partition-length parity

This is an author-checked, AI-assisted component argument, not an independent
review or a faster SAT theorem. It uses the charged normal-ordering setup of
[PR #11](../charged-operator-moments/PROOF.md) and the weight-at-most-j
moment argument of the uncharged `operator-moment-recovery` branch, commit
`8191d2e2813615e4941216c012b151c96c5d7ce5`. The latter argument extends here
because the charge only adds a regular central zero mode and does not change
the nonzero-mode commutators or field weights.

## Statement

Let V_E be the weight-E partition space over Q, with a basis indexed by
partitions and length equal to the number of parts. Fix integer charge q,
source labels a,b indexed at grade h (including the inhomogeneous dual
labels of PR #19), and define

```math
 M_3(a,b)=\sum_s \frac{s^3-s}{6}Q_s^{(q)}(a,b).
```

The shifts are finite by the predecessor's energy bound. For either parity
p, let P_p project onto the span of length-p partitions of E. Then there is
a scalar G_{h,E,q}(a,b), independent of p, such that

```math
 P_p M_3(a,b) P_p=G_{h,E,q}(a,b)P_p.                 \tag{1}
```

This is a compression identity. Neither parity subspace is asserted to be
invariant. The scalar depends on the labels, energy and charge. In
particular, (1) does not assert a nonsingular label-pairing matrix.

## Proof

The common charged Laurent polynomial in PR #11 is a sum of terms whose
uncontracted fields of total weight r carry a factor `(z_1-z_2)^r`. Each
application of the logarithmic derivative can remove a zero or differentiate
a remaining field; the final coincident uncontracted field has weight at
most the derivative order. The source's mode-coefficient identity, extended termwise over the
inhomogeneous dual label, therefore
places each moment `sum_s s^j Q_s`, for j<=3, in the linear span of zero
modes of fields of weights at most 3 on V_E. The regular charged zero mode
does not alter this weight count. Thus M_3 is in that span as well. This is
the predecessor moment argument, applied to the charged fields; it is not an
assumption that higher moments are scalar.

For a homogeneous state c of weight d write o(c) for its energy-preserving
zero mode and T for the translation operator. The derivative identity
`Y(Tc,z)=partial_z Y(c,z)` gives `o(Tc)=-d o(c)`. With the predecessor's
polynomial convention `T(t_j)=j t_(j+1)`, the weight-at-most-three space is
spanned by

```text
1; t1; t2, t1^2; t3, t2 t1, t1^3.
```

The translation identity reduces their zero modes to the span of
`o(1), o(t1), o(t1^2), o(t1^3)`. Specifically,
`o(t2)=-o(t1)`, `o(t3)=o(t1)`, and
`o(t2 t1)=-o(t1^2)`.

In charge q, the Heisenberg modes are D_0=q, D_-k=t_k and
D_k=k partial_(t_k), k>0. Normal ordering yields, on V_E,

```math
 o(t_1)=qI,\qquad o(t_1^2)=(q^2+2E)I,
```

and

```math
 o(t_1^3)=(q^3+6qE)I+3\sum_{r,s\ge1}
   ((r+s)t_rt_s\partial_{t_{r+s}}
     +rs t_{r+s}\partial_{t_r}\partial_{t_s}).       \tag{2}
```

Every non-scalar term in (2) replaces one part by two or two by one;
it therefore changes partition length by exactly one. Its compression
to either fixed parity space is zero. All remaining terms are scalars on
all of V_E, with the same value in both parity sectors. Equation (1)
follows for every a,b, E and q, including the zero or empty sectors.

## Affine dependence on output energy

The scalar G is affine in E for fixed source labels and charge. Indeed,
the Laurent contraction coefficients and their reduction to low-weight
zero modes are independent of the representation V_E, while (2) and the
other scalar zero modes depend on E at most linearly. Consequently

```math
 G_{h,E,q}=(1-E)G_{h,0,q}+E G_{h,1,q}.             \tag{3}
```

The two values on the right are the diagonal coefficients on the vacuum
and the single-part state `(1)`, respectively. Thus a uniform exact
construction of the input pairing can evaluate only these two output
energies, rather than constructing all grade-E output tensors. This is a
construction identity, not a proof of invertibility or a smaller asymptotic
rank envelope.

## Output capacity and limitations

For E>=2, each partition except `1^E` can be mapped to the opposite length
parity by splitting a largest part into `1` and the remainder. A resulting
partition has at most E squared possible preimages: each is obtained by
merging a pair of its parts. For either parity class B this gives

```math
 |B|\ge (p(E)-1)/(E^2+1).
```

The standard partition asymptotic implies each class has
`exp(pi sqrt(2E/3)-O(log E))` states. Thus the parity restriction loses
only polynomial output capacity, uniformly in E. Enumerating partitions
and counting lengths supplies an explicit selection procedure, but the
input label pairing G and both rank/bit-cost contracts still require work.

For q=1 and h=E, exact full-label checks at h=3,4,5,6 have scalar pairing
ranks 2,4,5,8, respectively. These match `p(h)-p(h-3)` in those grades;
that formula is a finite observation, not an all-grade theorem. Further,
M_3 removes only s=-1,0,1: shifts ±2 remain and approach the center as
h grows. Even a uniform invertible pairing at leading capacity would not
improve PR #19's supplied asymptotic rho. No new SAT bound follows.
