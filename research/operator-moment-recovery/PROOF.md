# Higher moments of the zero-charge operator pieces

These are AI-assisted, author-checked component arguments, without an
independent or formal review. The operators and external source are
pinned by the [predecessor](../anthropic-operator-ranks/README.md), whose
normal-ordering conventions we retain. The accepted OpenAI theorem is
unchanged, and no improved SAT bound follows from these identities.

## 1. An explicit second moment

Write Gamma(a,b) for the full scalar contraction of two polynomials in
the current variables. For one variable from each side its matrix is

```math
 \Gamma(t_j,t_n)=(-1)^{j-1}
            \frac{(j+n-1)!}{(j-1)!(n-1)!}.
 \tag{1}
```

For two monomials with the same number of parts, full contraction is
the permanent of this matrix with the parts labeled, including equal
parts. It is zero if the numbers of parts differ, and extends bilinearly.
Formula (1) follows by differentiating `(w_1-w_2)^(-2)` j-1 and n-1
times with the source's factorial normalizations.

Let partial_1 mean differentiation with respect to t_1 and put

```math
 G(a,b)=\tfrac12\Gamma(\partial_1^2a,b)
       +\Gamma(\partial_1a,\partial_1b)
       +\tfrac12\Gamma(a,\partial_1^2b).
 \tag{2}
```

For integer polynomials this is integral: each second derivative has
even coefficients. On the fixed energy space V_E, the same Q_s as in
the source satisfies

```math
 \sum_s s^2 Q_s(a,b)=4E\,G(a,b)\operatorname{Id}_{V_E}.
 \tag{3}
```

To prove this, first take a,b homogeneous and use the normal-ordered
Laurent polynomial F from the predecessor's first-moment proof. Set
w_1=1+z, w_2=1. The fully contracted term is constant. A single
uncontracted field has no energy-preserving zero mode, so all terms
of uncontracted weight one vanish. At weight two, a single part of
size two again gives zero. The remaining possibility is two currents
of weight one, distributed between a and b in 2+0, 1+1, or 0+2 ways.
Their partial-contraction coefficient is exactly (2), including the
factorials for equal uncontracted parts.

The energy-preserving component of the normal-ordered square of the
unit current is

```math
 2\sum_{k\ge1}t_k\,k\partial_{t_k}=2E\operatorname{Id}_{V_E}.
```

Hence F(1+z,1) has quadratic coefficient 2E G(a,b) Id, and no linear
coefficient. Apply `(w_1 partial_{w_1})^2` at (1,1): the result is
twice that quadratic coefficient, namely (3). The Laurent coefficient
reading identifies it with sum_s s^2 Q_s. The argument is linear in
the homogeneous components of a, so it also covers the source's dual
label polynomials a^mu.

For the encoded crossing tensors, define
`B2(x,v)=4h G(a^mu(x),b^mu(v))`. Equation (3) gives

```math
 \sum_s s^2 A_s(x,y,u,v)=B2(x,v)[y=u].
 \tag{4}
```

The explicit pairing is a primitive. It is not an invertibility
guarantee. The actual binary codebook pairings at lambda=1,2,3 have
exact ranks 1,3,5 in dimensions 2,4,8. No inverse exists there.

## 2. A bound for the third cut of every higher moment

Let p(j) be the ordinary partition number and j>=2. For any fixed
energy E and any finite label families satisfying the source's input
conditions, the moment tensor M_j=sum_s s^j A_s has rank at most

```math
 p(j)-1
 \tag{5}
```

across the cut `(x,v)|(y,u)`. This is the third cut, not either of the
source's two required cuts `(x,y)|(u,v)` and `(x,u)|(y,v)`.

Here is a dimension proof of (5). Let o(c)=c[0] be the zero-mode
operator on V_E and let W_j=sum_{q=0}^j V_q. Set

```math
 T=\sum_{n\ge1}n t_{n+1}\partial_{t_n},
 \qquad L_0=\sum_{n\ge1}n t_n\partial_{t_n}.
```

The field definition gives Y(Tc,w)=partial_w Y(c,w). Therefore, for
homogeneous c of positive weight q,
`o(Tc)=-q o(c)`. The subspace
`(T+L_0)(sum_{q=1}^{j-1}V_q)` is in the kernel of o.

T is injective on every positive-weight polynomial space. Indeed, if
m is the largest index occurring in a nonconstant polynomial f, the
coefficient of t_{m+1} in Tf is m partial_{t_m}f and is nonzero.
The map T+L_0 is consequently injective on the indicated direct sum:
its highest-weight component is T applied to the highest-weight
component of its argument. Quotienting W_j by this kernel subspace
leaves dimension 1+p(j).

There are two further independent kernel relations. First o(t_1)=0.
Second o(t_1^2)=2E o(1). The class of t_1 is nonzero after the first
quotient, since a nonzero highest-weight image of T+L_0 has weight
at least two. For E>0 the constant component proves that
`t_1^2-2E` is independent of it and the preceding relations. At E=0,
its highest degree-two part t_1^2 is independent of T(V_1)=Q*t_2,
so the same conclusion holds. Thus the zero-mode image of W_j has
dimension at most p(j)-1.

Finally the j-th logarithmic derivative of the source's Laurent F
at coincident points can involve only uncontracted weight at most j.
Terms with larger uncontracted weight carry a higher power of
w_1-w_2 and vanish under j derivatives. Every derivative that lands
on a remaining current raises its field weight by one, so the final
coincident fields still have weight at most j. Projection to V_E
selects their zero modes. Therefore every operator M_j(a,b) belongs
to the fixed image o(W_j), independently of the labels a,b. Expressing
it in a basis of that image proves the third-cut rank bound (5).

The finite third-cut ranks at lambda=2,3 equal p(j)-1 for j=2,...,6.
This is finite sharpness in those cases only. The argument gives a
dimension bound, not uniform low-height integer factorizations in
the two cuts needed for a better rho.

## 3. Finite scalar-weight classification

For a fixed finite codebook, let f_s be arbitrary rational weights.
Demand that sum_s f_s A_s has the form B(x,v)[y=u], for some matrix B.
This gives explicit rational linear constraints: all off-diagonal
y/u entries vanish, and diagonal entries are independent of y.

The constant, linear and quadratic vectors f_s=1,s,s^2 satisfy these
constraints by the crossing, first-moment, and second-moment identities.
They are linearly independent on the source grids. At lambda=1,2,3,
the constraint matrices have exact ranks 6,14,22 on 9,17,25 weights.
Their scalar weight spaces therefore have dimension three, exactly

```math
 f_s=a+b s+c s^2.
 \tag{6}
```

The matrix B is a*h!*I+c*B2. Dropping the central source piece requires
f_0=a=0, leaving a singular pairing c*B2 in each checked binary case.
Thus this particular scalar recovery cannot omit the central piece
and obtain an invertible crossing pairing at those sizes. This is a
finite classification, not an all-h theorem and not a classification
of general products B(x,v)K(y,u).

## 4. Complete cost boundary

Neither a scalar moment nor a small rank in the third cut gives the
two-direction bit contract automatically. The crossing tensor itself
has third-cut rank one but rank D^2 in both required cuts, for
D=2^lambda. The checker includes this counterexample to that inference.

A future normalization by an inverse pairing must establish its
existence, coefficient bit lengths and evaluation cost. Generic
inversion of a D-by-D integer matrix can have determinants of bit
length D times the input height. Time 2^O(lambda) for such an inverse
does not by itself meet the piece contract's polynomial-in-lambda
integer bit-height requirement.

The dimension bound p(j)-1 is polynomial in lambda only for moment
orders at most O((log lambda)^2). Taking j=Theta(h)=Theta(lambda^2)
can require exponentially many third-cut components. Hiding those
components in a new label costs Theta(lambda) bits. In addition, a
polynomial weight of order j has only j roots, so these low orders
do not excise a constant fraction of the central shift range of
length Theta(h). All these costs remain obligations of a new algorithm;
no smaller rho, log-log correction, alpha or SAT runtime is claimed.
