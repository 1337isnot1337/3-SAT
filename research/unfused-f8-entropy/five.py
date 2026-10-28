"""Check a rational row relation excluding stronger five-macro seeds."""
from contextlib import redirect_stdout
from fractions import Fraction
from hashlib import sha256
import importlib.util
import io
import json
from math import prod
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('entropy_seed', HERE / 'verify.py')
base = importlib.util.module_from_spec(spec)
with redirect_stdout(io.StringIO()):
    spec.loader.exec_module(base)


def compositions(n, k):
    if k == 1:
        yield (n,)
    else:
        for i in range(n + 1):
            for tail in compositions(n - i, k - 1):
                yield (i,) + tail


def entropy_power(a):
    return Fraction(5 ** 5 * 7 ** (5 - a[0]), prod(x ** x for x in a if x))


types = list(compositions(5, 10))
eligible = {a for a in types if entropy_power(a) ** 4 > 153664 ** 5}
assert len(types) == 2002 and len(eligible) == 1008
orbits = []
for a in types:
    if a in eligible:
        group = base.orbit(a)
        assert group <= eligible
        orbits.append(group)
        eligible.difference_update(group)
assert len(orbits) == 245
relation = json.loads((HERE / 'five-relation.json').read_text())
denominator = relation['denominator']
terms = relation['terms']
assert isinstance(denominator, int) and denominator > 0 and len(terms) == 225
assert len({i for i, _ in terms}) == len(terms)
assert all(isinstance(i, int) and 0 <= i < len(types) and isinstance(c, int) and c for i, c in terms)
row_weights = {types[i]: c for i, c in terms}

# Apply the frozen integral row functional to each independent orbit column.
for group in orbits:
    lhs = 0
    target = 0
    for a in group:
        transformed = base.transform_monomial(a)
        lhs += sum(row_weights.get(b, 0) * value for b, value in transformed.items())
        lhs -= 8 ** 5 * row_weights.get(a, 0)
        target += prod(v ** count for v, count in zip(base.q, a))
    assert lhs == denominator * target

files = [HERE / 'five.py', HERE / 'five-relation.json', HERE / 'verify.py', HERE / 'seed.json',
         ROOT / 'research/three-bit-macro-walsh/schemes.py']
print(json.dumps({'status': 'PASS', 'scope': 'five-macro stronger-entropy row relation',
                  'all_types': len(types), 'eligible_types': 1008, 'eligible_orbits': len(orbits),
                  'row_relation_terms': len(terms), 'denominator_bits': denominator.bit_length(),
                  'bindings': {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in files}}, indent=2))
