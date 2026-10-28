"""Exact generator and orbit controls for two quadratic-isometric frames."""
from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ref = ROOT / 'research/three-bit-macro-walsh/schemes.py'
spec = importlib.util.spec_from_file_location('f8_scheme', ref)
f = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f)


def dual(b):
    return next(B for B in range(8) if all(
        f.trace(f.multiply(a, B)) == (a & b).bit_count() % 2 for a in range(8)))


d = [dual(b) for b in range(8)]
inv_d = {B: b for b, B in enumerate(d)}
u = 2
u_inv = next(x for x in range(1, 8) if f.multiply(u, x) == 1)
assert len({1, u, f.multiply(u, u), f.multiply(f.multiply(u, u), u),
            f.multiply(f.multiply(f.multiply(u, u), u), u),
            f.multiply(f.multiply(f.multiply(f.multiply(u, u), u), u), u), u_inv}) == 7
scale = [(f.multiply(u, a) << 3) | inv_d[f.multiply(u_inv, d[b])]
         for a in range(8) for b in range(8)]
assert len(set(scale)) == 64


def frame(x):
    # Involutory CNOT between bit 0 of two distinct three-bit macro axes.
    a0, b1 = (x >> 3) & 1, (x >> 6) & 1
    return x ^ (a0 << 9) ^ b1


def quadratic(x, macros):
    return sum(((((x >> (6 * i + 3)) & 7) & ((x >> (6 * i)) & 7)).bit_count())
               for i in range(macros)) % 2


def elementary(x, target, source):
    return x ^ (((x >> source) & 1) << target)


def local_a(x, source, target):
    a, b = x & 7, x >> 3
    return f.multiply(source, a) | (f.multiply(target, b) << 3)


def frame_a(x):
    return elementary(x, 3, 0)


def seed_transvection(x):
    # L S L^-1 S^-1; L is involutory and S scales the target macro.
    return frame_a(local_a(frame_a(local_a(x, 1, u_inv)), 1, u))


def coefficients(op):
    values = [op(1 << i) ^ (1 << i) for i in range(6)]
    assert all(v == 0 for v in values[3:])
    nonzero = {v >> 3 for v in values[:3] if v}
    assert len(nonzero) == 1
    vec = next(iter(nonzero))
    phi = sum((1 << i) for i, v in enumerate(values[:3]) if v)
    assert vec and phi
    assert all(op(x) == x ^ (vec << 3 if (x & phi).bit_count() % 2 else 0)
               for x in range(64))
    return vec, phi


pairs = set()
for a in range(1, 8):
    ai = next(v for v in range(1, 8) if f.multiply(a, v) == 1)
    for b in range(1, 8):
        bi = next(v for v in range(1, 8) if f.multiply(b, v) == 1)
        pairs.add(coefficients(lambda x, a=a, b=b, ai=ai, bi=bi:
                               local_a(seed_transvection(local_a(x, ai, bi)), a, b)))
assert pairs == {(v, phi) for v in range(1, 8) for phi in range(1, 8)}

# Elementary cross-block maps and their commutators give all within-block maps.
for target in range(6):
    for source in range(6):
        if target == source or target // 3 != source // 3:
            continue
        middle = 3 if target < 3 else 0
        for x in range(64):
            y = elementary(x, middle, source)
            y = elementary(y, target, middle)
            y = elementary(y, middle, source)
            y = elementary(y, target, middle)
            assert y == elementary(x, target, source)


def orbit_screen(macros):
    def local(x, i):
        shift = 6 * i
        return (x & ~(63 << shift)) | (scale[(x >> shift) & 63] << shift)

    def swap(x, i):
        shift = 6 * i
        diff = ((x >> shift) ^ (x >> (shift + 6))) & 63
        return x ^ (diff << shift) ^ (diff << (shift + 6))

    generators = ([lambda x, i=i: local(x, i) for i in range(macros)] +
                  [lambda x, i=i: swap(x, i) for i in range(macros - 1)])
    generators += [lambda x, g=g: frame(g(frame(x))) for g in generators]
    total = 1 << (6 * macros)
    visited = bytearray(total)
    summary = Counter()
    for start in range(total):
        if visited[start]:
            continue
        visited[start] = 1
        todo = [start]
        count = 0
        q = quadratic(start, macros)
        while todo:
            x = todo.pop()
            count += 1
            for op in generators:
                y = op(x)
                assert quadratic(y, macros) == q
                if not visited[y]:
                    visited[y] = 1
                    todo.append(y)
        summary[(q, count)] += 1
    n = 3 * macros
    expected = Counter({(0, 1): 1, (0, 2 ** n - 1): 2,
                        (0, (2 ** n - 1) * (2 ** (n - 1) - 1)): 1,
                        (1, (2 ** n - 1) * 2 ** (n - 1)): 1})
    assert summary == expected
    return {'macros': macros, 'labels': total,
            'orbits': [{'q': q, 'size': size, 'count': count}
                       for (q, size), count in sorted(summary.items())]}


screens = [orbit_screen(r) for r in (2, 3)]
files = [HERE / 'verify.py', ref]
print(json.dumps({'status': 'PASS', 'scope': 'rank-one generator controls and finite frame orbits',
                  'rank_one_cross_maps': len(pairs), 'screens': screens,
                  'bindings': {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in files}}, indent=2))
