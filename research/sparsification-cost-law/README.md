# Sparsification and width: a conditional cost law

Status: author-checked model calculation, pending independent review. Base `572a226` (full base in CLAIM.json); coordination [issue #102](https://github.com/1337isnot1337/3-SAT/issues/102). Contributor: Cinna Davis with substantial OpenAI Codex assistance.

[PROOF.md](PROOF.md) optimizes a named positive-coefficient envelope combining a sparsification branching term and a logarithmic density-width term. For fixed model coefficients the unique minimizer is asymptotic to a constant times `1/sqrt(lambda)`, and the minimum retains a `(log lambda)/sqrt(lambda)` term. This is an obstruction to an improvement **within the specified envelope**. It is neither a lower bound on SAT algorithms nor evidence that actual leaf density or contraction times attain those upper bounds. No alpha or selected result changes.

Run `python3 -I -B research/sparsification-cost-law/verify.py` and `make verify`. The numerical controls verify the derivative equation and bracket the optimizer for specified fixed coefficients and finite lambda; the all-size result is the written calculus argument. The controls do not prove the source algorithm meets this model with particular constants.

Credit: accepted upstream source commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`, `lem:sparsify`, `eq:sharp-wire-budget`, and `lem:tensor-sparse-query`. PR #78 supplies the optional retuned-width proxy; PR #51 separately compresses candidate enumeration. No novelty is claimed for the calculus. Open: identify a changed source-wide mechanism that reduces the branch, width or contraction term with a uniform all-input proof and a paid full cost ledger.
