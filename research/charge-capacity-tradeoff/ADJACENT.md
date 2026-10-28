# Adjacent-shift spectrum

This is an author-checked continuation of [PROOF.md](PROOF.md). It concerns
one raw charged piece, one label pair, one charge coefficient and the
unprojected grade-h output space. It does not settle weighted combinations,
other label pairs, output compression or SAT complexity.

For h>=2 put a=(1^h), s=h-1, and let m_j be part multiplicities in an
output partition of grade E<=h. Exact normal ordering gives

    [q^(2h-2)] Q_(h-1)(a,a)
     = -4h^2(h-1)E + h^2[1 + c_1 m_1
         + sum_(j=2)^E (-1)^(j+1) j B_j m_j],                 (1)
    B_j=binom(2h,j+1),   c_1=B_1+1.

The operator is diagonal. To derive (1), two nonzero currents in one
factor force alternating index i=1 and contribute
`-binom(2h,1)*2h(h-1)E`. With one nonzero current in each factor, index
0 yields `h^2(m_1+1)`, index 2 yields `h^2 B_1 m_1`, and index j+1 for
j>=2 yields `h^2 (-1)^(j+1) j B_j m_j`. No other terms have the stated
charge degree. The same expression follows from the other operator order.

## Simple spectrum except grade four

For every h>=5, the eigenvalues of (1) on partitions of h are distinct.
Consequently every output subspace on which this one operator acts as a
scalar has dimension at most one. The proof also works for h=2,3 by direct
inspection. At h=4 the exact collision `(4)` and `(2,2)` is real, as
shown in [PROOF.md](PROOF.md).

For the all-size argument, write `c_j=B_j` for j>=2, and consider the
nonconstant eigenvalue `sum_j (-1)^(j+1) j c_j m_j`. For h>=5 the
numbers c_j are strictly increasing for 1<=j<=h-1, and `c_h=c_(h-2)`.
Let mu and nu be distinct partitions of h, and let i be the largest part
size at which their multiplicities differ. Cancel their common parts and
orient them so mu has at least one i and nu has none. Their remaining
weights are equal and at most h; the contribution of size i has magnitude
at least i c_i. To cancel it, only opposite-parity parts of mu and
same-parity parts of nu can contribute. The total weight in the former is
at most h-i; that in the latter is at most h.

* If i=1, there are no smaller parts to cancel it.
* If i=2, cancellation is at most `(h-2)c_1`, strictly smaller than
  `2B_2`: since `2B_2=4(h-1)B_1/3`, the difference from
  `(h-2)(B_1+1)` is `(h+2)B_1/3-(h-2)>0`.
* If i=3<h, cancellation is at most `(h-3)B_2+h(B_1+1)`, and

      3B_3 - (h-3)B_2 - h(B_1+1)
        = h[(2h-1)(h-3)(2h+1)/6 - 1] > 0.

* If 4<=i<h, monotonicity bounds the opposing contribution by
  `(h-i)B_(i-1)+h B_(i-2)`. Binomial ratios give

      i B_i - (h-i)B_(i-1) - h B_(i-2)
      = B_(i-1) (i-1)(h-i)(2h+1) /
        [(i+1)(2h-i+1)] > 0.

* If i=h, mu is the single part (h). All same-parity parts of nu have
  sizes at most h-2 and c_j<=c_h, with equality only at j=h-2. Opposite
  parity can only reduce their signed contribution. Equality with
  `h c_h` would require all of nu's weight to consist of parts h-2,
  impossible for h>=5 because h-2 does not divide h. Thus cancellation
  is again strict.

So no two partitions of h have the same eigenvalue. This is a property of
the specified single operator; it does not rule out a suitable codebook for
other weights or a joint scalar pairing without this operator.

## Checks

`adjacent_spectrum.py` interpolates the charged operator exactly on every
output partition at grades E=0,...,h for h=2,...,5, in both operator
orders. It then checks the predicted spectra on all 540,633 partitions
of h=2,...,45: the sole collision is the grade-four pair above. Output
and source hashes are in `adjacent-spectrum-verification.json`. The finite
checks do not prove the all-size dominance argument.
