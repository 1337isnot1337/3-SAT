# Critical maximum-deficiency examples

Status: `scoped_checked`, substantially AI-assisted, without independent review. Base `f64e1babba809276639257f37cd218ee18824257`; task `decision-only`.

[PROOF.md](PROOF.md) gives a connected, bounded-occurrence exact-width-three family with n=3r, maximum deficiency 2r, exact variable-side expansion surplus 3, and equality in the earlier width/occurrence defect bound. Every literal appears at least twice, and the family has no nonempty matching autarky. A cited published lemma implies every one-variable restriction lowers maximum deficiency. All-true satisfies the formulas, so the construction is only a limitation of these structural tests, not a SAT lower bound.

Run:

```sh
python3 -I -B research/critical-deficiency-examples/verify.py
make verify
```

The first command checks the stated finite properties at r=3,4,5. It does not verify the all-size proof or the cited lemma. A useful next question is whether a paid reduction using polarity or other information can lower the actual deficiency uniformly; easy examples with large deficiency do not rule that out.
