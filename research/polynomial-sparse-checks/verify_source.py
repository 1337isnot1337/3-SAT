#!/usr/bin/env python3
"""Bounded replay with actual source parameters in the q=1 regime."""
from pathlib import Path
import importlib.util
spec = importlib.util.spec_from_file_location('tanner', Path(__file__).with_name('tanner.py'))
tanner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tanner)
result = tanner.build(2048, 2048, 1)
assert (result['q'], result['d'], result['h']) == (1, 2048, 1)
rows = result['rows']
assert len(rows) == 2
assert all(any((row >> j) & 1 for row in rows) for j in range(2048))
assert all(all((row & ((1 << a) | (1 << b))).bit_count() % 2 == 0 for row in rows)
           for a, b in ((0, 1), (0, 2047), (100, 1500)))
assert result['P'] > 2048  # The source's guaranteed distance is then only one.
try:
    tanner.build(1, 2, 1)
except ValueError:
    pass
else:
    raise AssertionError('invalid density accepted')
try:
    tanner.build(2048, 2048, 1, max_degree=1024)
except ValueError:
    pass
else:
    raise AssertionError('execution cap ignored')
print('PASS: source parameters n=m=2048, B=1, q=1, 2 nonzero rows; all 2048 singleton words rejected; density and cap controls')
