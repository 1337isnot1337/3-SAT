# Registered asymmetric normalization

Base: PR 11 merge `b91287aa1361fa49d68afe5cc94c23077dce93db`.
The source charged checker replayed byte-for-byte on its merge candidate;
the candidate tree `11f5e90afa5b8febde532a2e18fc9017a779a185` equals the
actual merge tree. `make verify` passed. This was an author-side AI replay,
not a promotion to independently reviewed status. Preserve that package.

User goal remains ACTIVE and INCOMPLETE: work indefinitely toward a real
mathematical improvement, commit/push often, merge checked scoped work.
Owner has explicitly authorized merges. No subagents. Upstream and selected
alpha=1/2 remain unchanged. Refresh main, all advertised branches and PRs
before a pivot/submission. Current other open work: PR 18 aggregate packing
limits and PR 12 README docs; existing moment-recovery branch has a distinct
scalar-weight/interface screen and must be credited.

Question: can the charged first-moment image be turned into a uniform
actual rational crossing family with no central s=0 piece, preserving the
source's two directional ranks? PR 11 proved rank r_h=p(h)-p(h-1) and
left asymmetric coordinates/normalization unpaid. PR 17 now permits
uniform rational normalization of exponential height via exact integer
query recovery over a boundedly sampled prime.

Construction to test: let h be least with r_h>=N=2^lambda. Build the full
first-moment pairing G on partitions of h, charge one. Select a nondegenerate
N-by-N minor using different row/column labels. For output labels choose
any N partitions of h, the same on the output y,u axes. Define

    A_s'(x,y,u,v)=s sum_a (G_minor^-1)[x,a]
                   Q_s(a_mu[row_a], b_nu[col_v])[out_u,out_y].

Then the first-moment identity predicts sum_s A_s'=crossing; s=0 vanishes.
The inverse acts only on x, so it preserves both required flattening rank
bounds. Generic exact rational generation costs `2^O(lambda)` because
h=Theta(lambda^2), p(h)<=poly(h)*2^lambda and determinant heights are
`2^O(lambda)` bits. This fits PR 17 but is not presumed to fit a
polynomial-height integer contract.

Registered finite screen: lambda=1,2, with h=4,6; verify the full exact
crossing, source-order equality controls at positive output grade,
normalization, both rational/field ranks and integer query recovery. Grade
selection/minor-only profiles may also cover lambda=3,4 without computing
their full operator tensors. Do not extrapolate their finite rank ratios.

Success is a uniform actual family and complete cost proof at the inherited
rho=1/sqrt(2), plus a precise changed next premise for a larger central gap.
It is NOT an alpha improvement: omitting one shift leaves nearby shifts
with the same leading envelope. Stop before claiming lower rho from the
dimension count or from a singular common principal pairing.

Next improvement target: a paid scalar higher-order filter eliminating an
entire central interval while retaining leading label capacity and both
cut ranks. General higher moments are operator-valued; an inverse mixing
the wrong axes can destroy a required rank. None of that is assumed here.
