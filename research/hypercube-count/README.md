# Exact count for a bipartite hypercube quadratic system

Status: `scoped_checked` for the finite controls below. The all-size proof is
author-checked with substantial OpenAI Codex assistance and awaits independent
review. The accepted theorem and selected result are unchanged.

Task: `dense-encoding`. Base: `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`.
Contributor: Cinna Davis, with substantial OpenAI Codex assistance.

## Result

For d>=1, let m=2^d, with 2m Boolean variables x_v,y_v and m equations
`x_v sum_j y_(v xor e_j)=0` over F2. This system has private quadratic
monomials and a hypercube co-occurrence component; its SAT decision is
trivial, but its exact count is a separate question. The [proof](PROOF.md)
shows that for odd d its count is exactly `3^m`. For even d it gives the
exact weight-enumerator formula

    2^(m/2) sum_(w in F2^(m/2)) 2^(m-wt(w)-wt(A_(d-1)w)),

where A_(d-1) is the binary hypercube adjacency matrix. The formula gives a
uniform polynomial-space `poly(m) 2^(m/2)` bit-time counter for even d.
The count for d=1,2,3,4 is 9, 100, 6,561, and 59,228,416 respectively.
For odd d, an exact character-sum formula also counts any prescribed fixed-bit
branch in `poly(m) 2^b` bit time and polynomial space, where b is the number
of fixed y variables. For even d, linear elimination extends the same
`poly(m) 2^(m/2)` bound to every prescribed fixed-bit branch. It remains open
here whether even d has a simpler closed form or faster count. The even-d
image is a self-dual binary code, giving a second weight-enumerator identity
and count congruences `C_d=1 mod 9`, strengthened to `C_d=1 mod 81` when
4 divides d. Applying the published cube-code minimum-distance theorem
strengthens this to `C_d=1 mod 3^d` for every even d; that external
dependency and earlier credit are recorded in [SOURCES.md](SOURCES.md).

This is a computation for one family, not a general SAT time improvement.
It illustrates that coefficientwise support entropy or a large supplied
circular span does not by itself imply a counting-time lower bound. The
branch algorithms handle all fixed x and y bits for this family.

## Evidence and reproduction

```sh
python3 -I -B research/hypercube-count/verify.py > /tmp/hypercube-count.json
cmp /tmp/hypercube-count.json research/hypercube-count/verification.json
make verify
```

Standard-library checks cover the adjacency-square identity on 2,046 basis
vectors for d=1,...,10, 1,364 block-image controls, all 65,808 x/y pairs for
d=1,2,3, all 65,812 y assignments for d=1,2,3,4, 881 odd-d branch
cases, and 6,661 even-d branch cases; 1,915 of the branch cases are
contradictory. There are also 34,782 column-overlap checks, 4,000 seeded
codeword-weight controls and two dual-enumerator and minimum-distance comparisons. The independently
computed direct sums agree with the formulas. The [saved output](verification.json)
hash-binds proof and verifier; bounded controls do not constitute an independent
review or a proof of the asymptotic algorithm.

## Sources and limits

The double-cover example was recorded in
[issue #29](https://github.com/1337isnot1337/3-SAT/issues/29#issuecomment-6459412498)
and discussed with [issue #67](https://github.com/1337isnot1337/3-SAT/issues/67).
[PR #44](https://github.com/1337isnot1337/3-SAT/pull/44) contains the earlier
row-basis support mechanism; [PR #73](https://github.com/1337isnot1337/3-SAT/pull/73)
studies a different oriented single-cube system. The self-dual hypercube-code facts were established in prior work by Fish,
Key, Seneviratne and collaborators, as detailed in [SOURCES.md](SOURCES.md).
The accepted upstream source is pinned by [SOURCES.json](../../SOURCES.json) at
`7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`.

The proof does not claim anything about general
query aggregation, selected alpha, human review, formal verification, or
scientific priority. Future generalizations must charge all reduction queries,
branches, descriptions, entry generation, recursion, precision and space.
