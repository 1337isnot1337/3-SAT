"""Bounded exact simple-spectrum check for the second-deficit operator."""
from hashlib import sha256
import json
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent


def partitions(n, largest):
    if n == 0:
        yield ()
        return
    for k in range(min(n, largest), 0, -1):
        for tail in partitions(n-k, k):
            yield (k,) + tail


counts = {}
for h in range(2, 46):
    weight = [0] + [(-1)**i * comb(2*h-1, i-1) for i in range(1, h+1)]
    values = set()
    count = 0
    for parts in partitions(h, h):
        value = sum(weight[i] for i in parts)
        assert value not in values, (h, parts, value)
        values.add(value)
        count += 1
    counts[str(h)] = count
print(json.dumps({'result': 'PASS', 'grades': [2,45],
                  'partition_vectors': sum(counts.values()),
                  'counts_by_grade': counts,
                  'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest()},
                 indent=2, sort_keys=True))
