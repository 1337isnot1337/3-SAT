#!/usr/bin/env python3
"""Check the threshold-support matching formula by an independent greedy matching."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAX_H = 35
# p[n][k] is the number of partitions of n into exactly k positive parts.
p = [[0] * (MAX_H + 1) for _ in range(MAX_H + 1)]
p[0][0] = 1
for n in range(1, MAX_H + 1):
    for k in range(1, n + 1):
        p[n][k] = p[n - 1][k - 1] + (p[n - k][k] if n >= k else 0)

cases = 0
strict = 0
fixed_deficit_cases = 0
for h in range(1, MAX_H + 1):
    def long(t):
        return sum(p[h][max(0, t):]) if t <= h else 0

    for d in range(0, 2 * h + 2):
        cover = min(long(t) + long(d - t + 1) for t in range(h + 2))
        # For each row from short to long, use the longest available column.
        # Counts keep the check bounded without constructing the full graph.
        cols = p[h][:]
        j = h
        matching = 0
        for i in range(1, h + 1):
            for _ in range(p[h][i]):
                while j and not cols[j]:
                    j -= 1
                if not j or i + j < d:
                    break
                cols[j] -= 1
                matching += 1
        assert matching == cover, (h, d, matching, cover)
        k = 2 * h - d
        if 0 <= k <= h // 2:
            def cumulative(n):
                return sum(sum(p[i]) for i in range(n + 1))
            expected = cumulative(k // 2) + cumulative((k - 1) // 2)
            assert cover == expected, (h, k, cover, expected)
            fixed_deficit_cases += 1
        if 0 <= d <= 2 * h:
            lower = sum(p[h - (d + 1) // 2])
            assert cover >= lower, (h, d, cover, lower)
            if d >= 2:
                upper = 2 * (h + 1) * sum(p[h - d // 2])
                assert cover <= upper, (h, d, cover, upper)
        old = min(sum(p[h]), 2 * long((d + 1) // 2))
        assert cover <= old
        strict += cover < old
        cases += 1

result = {
    "max_grade": MAX_H,
    "threshold_cases": cases,
    "fixed_deficit_cases": fixed_deficit_cases,
    "strict_improvements_over_predecessor_cover": strict,
    "check": "exact partition counts, greedy matching versus minimum cover, capacity sandwich and fixed-deficit formula",
    "sha256": {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
               for name in ("README.md", "PROOF.md", "CLAIM.json", "verify.py")},
}
print(json.dumps(result, indent=2, sort_keys=True))
