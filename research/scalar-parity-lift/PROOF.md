# Scalar parity projectors

This changes the sparse-query encoding in the owner-accepted OpenAI theorem.
It does not audit that theorem. The construction and proof below are
AI-assisted and have no independent review.

## 1. An exact local lift

Normalize an equation over F_2 on Boolean variables by multilinearizing its
monomials and canceling duplicate monomials modulo two. Write it as

```math
 P_i(x)=b_i+\sum_{j=1}^{t_i}x^{A_{ij}}\pmod2,
 \qquad b_i\in\{0,1\},\quad 1\le |A_{ij}|\le k.
```

Each test has its own incidence variables z_iv. In the integer Boolean
quotient, where z_iv^2=z_iv, define

```math
 E_i(z_i)=\frac{1+(-1)^{b_i}
                    \prod_{j=1}^{t_i}(1-2z_i^{A_{ij}})}2.
 \tag{1}
```

The numerator is coefficientwise even: its constant coefficient is
1+(-1)^b_i, and all its other expansion terms contain a factor of two.
Equation (1) therefore defines an integer multilinear polynomial. The
division is in the integers before reduction; division by two in
Z/2^p Z is neither required nor valid in general.

At every Boolean assignment, each product factor is (-1)^(x^A_ij).
Thus E_i is exactly the zero-indicator of P_i, with values zero and one.
This includes constant equations: E_i=1 for P_i=0 and E_i=0 for P_i=1.

For a nonempty support S, its coefficient is

```math
 c_i(S)=(-1)^{b_i}\sum_{\substack{\varnothing\ne R\subseteq[t_i]\\
                              \bigcup_{j\in R}A_{ij}=S}}
                            (-1)^{|R|}2^{|R|-1}.
 \tag{2}
```

Every summand has |R|>=ceil(|S|/k). Consequently

```math
 2^{w_i(S)}\mid c_i(S),\qquad
 w_i(S)=\max\{0,\lceil |S|/k\rceil-1\}.
 \tag{3}
```

For S empty set w_i(S)=0; its coefficient is (1+(-1)^b_i)/2.
Zero coefficients satisfy every divisibility assertion. Cancellation in
(2) can increase the valuation, but cannot decrease (3).

One coefficient can be evaluated directly, without constructing E_i:

```math
 c_i(S)=\sum_{T\subseteq S}(-1)^{|S|-|T|}
                       \mathbf1_{\{P_i(\mathbf1_T)=0\}}.
 \tag{4}
```

This is Boolean Mobius inversion, because E_i agrees with the indicator
at every Boolean point. Its time is 2^|S| times a polynomial in the input
length and p, and its space is polynomial. Work modulo 2^p throughout
the sum if only that residue is needed. No formal expansion table is
needed by the algorithm.

## 2. A smaller retained degree over a scalar ring

Give different tests disjoint incidence variables and take F=prod_i E_i.
For a monomial with local supports S_1,...,S_a and incidence degree
d=sum_i |S_i|, its coefficient is the product prod_i c_i(S_i). Equation
(3) implies divisibility by 2^max(0,ceil(d/k)-a): indeed, the sum of the
ceilings is at least the ceiling of the sum, and replacing a negative
individual lower bound by zero can only increase it.

Fix an integer p>=1. If d>k(a+p-1), then ceil(d/k)-a>=p. All such
coefficients vanish in Z/2^p Z. Thus **coefficientwise**, before any
variable identifications or sums, F modulo 2^p has degree at most

```math
 K_{scalar}=\min\{N,\ k(a+p-1)\},
 \tag{5}
```

where N is the number of test-variable incidences. Equivalently it is
enough to retain local supports with sum_i w_i(S_i)<p, a stronger
support-sensitive restriction that we do not need for the degree bound.

For f free Boolean variables choose p=f+1. The exact zero count is at
most 2^f<2^p, so its least nonnegative residue recovers it. The product
sum is

```math
 \#\{x:P_i(x)=0\ \forall i\}
 =\sum_{(S_i)}\left(\prod_i c_i(S_i)\right)
        2^{f-|\bigcup_i S_i|}\pmod{2^p}.
 \tag{6}
```

Here the union uses original variable names, whereas d counts their
separate incidence copies. An unused variable contributes its factor of
two. Equation (5) justifies discarding all tuples above the cutoff in
(6), including when several tests use the same original variable.

The source retains degree k(a+2n) for p=ell=n+1 using the auxiliary
algebra (Z/2^p Z)[V]/(V^ell) and the total h-order. At the same p=n+1,
the new bound is k(a+n), capped by N. The ambient algebra can have
ell=1: it is just Z/2^p Z. This is a smaller degree envelope and a
smaller coefficient representation, not yet a smaller asymptotic
running-time envelope.
