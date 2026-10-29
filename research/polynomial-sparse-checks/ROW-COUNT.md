# A sublinear initial-check row count

This refinement uses the same matrix as PROOF.md but omits all zero padding rows, and omits any additional rows that become zero on shortening. Removing zero equations does not change the kernel, row width or distance. Let mu=floor(log2 m)+1, d=min(m,D0), q be the least power of two with qd>=m, h=ceil(d/(100 B mu))-1, and r=ceil(log2 d) for d>=2; if d=1 set r=0. There are at most 2qrh nonzero candidate rows. For h>0, r<=mu and h<d/(100B mu), while qd<2m, so

    number of rows <= 2 q r h < m r / (25 B mu) <= n/25.

For h=0 no rows are needed, so the same conclusion holds. This is stronger than the source's at-most-3n initial-check bound. It does not change the constant-fraction rejection argument for the additional rows and does not by itself give a new SAT bound.

For the source sparsification regime B<=C(log(n+2))^t with fixed C,t, the count is in fact O(n log log n / log n), uniformly over all nontrivial leaves. If m<sqrt(n), then rh<d/(100B) for h>0, so the count is less than 2qd<=4m=O(sqrt n); the case h=0 is empty. If m>=sqrt(n), then mu=Omega(log n), and because m<=Bn, mu=O(log n). Also d<=D0=320000B²mu³, hence r=O(log log n). Substitute these estimates into m r/(25B mu)<=n r/(25mu). Finite small n can be absorbed in the constant. This derivation is uniform in the leaf, not an average over leaves.

The reduction preserves the source construction and all q=1 and q>1 cases, but the numerical asymptotic improvement is only in the initial-check count. The greedy procedure still needs its own rows, and the parity lift's precision term and tensor contraction are unchanged. No improvement in alpha or total runtime exponent is claimed. The bounded source replay records the actual nonzero-row count; exhaustive scaled fixtures remain finite tests, not an independent proof.
