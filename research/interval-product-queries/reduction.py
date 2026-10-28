#!/usr/bin/env python3
"""Bounded checks for the 3-CNF to affine adjacent-product reduction."""
import importlib.util
from itertools import product
from pathlib import Path

spec = importlib.util.spec_from_file_location('check', Path(__file__).with_name('verify.py'))
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


def encode(nvars, clauses):
    # Each reference bit and each 3-bit clause gadget is followed by 00.
    refs, rows, size = [], [], 0
    for _ in range(nvars):
        refs.append(size)
        rows.extend(((1 << (size+1), 0), (1 << (size+2), 0)))
        size += 3
    for clause in clauses:
        assert len(clause) == 3
        for k, lit in enumerate(clause):
            assert 1 <= abs(lit) <= nvars
            # m_k = literal truth on the middle edge, its complement on
            # the outer edges. False clause -> 101.
            offset = (lit < 0) ^ (k != 1)
            rows.append(((1 << (size+k)) | (1 << refs[abs(lit)-1]), int(offset)))
        rows.extend(((1 << (size+3), 0), (1 << (size+4), 0)))
        size += 5
    if size == 0:
        size = 3
        rows.extend(((1 << j, 0) for j in range(size)))
    return size, rows, refs


def sat(assignment, clauses):
    return all(any(((assignment >> (abs(lit)-1)) & 1) == (lit > 0)
                   for lit in clause) for clause in clauses)


def make_word(n, rows, refs, assignment):
    solution = check.affine_space(n, rows)
    assert solution is not None
    origin, basis = solution
    # Exhaust affine words in these tiny tests to independently confirm the
    # unique one matching the original variable references.
    words = []
    for selector in range(1 << len(basis)):
        m = origin
        for i, v in enumerate(basis):
            if (selector >> i) & 1:
                m ^= v
        if all(((m >> ref) & 1) == ((assignment >> j) & 1)
               for j, ref in enumerate(refs)):
            words.append(m)
    assert len(words) == 1
    return words[0]


def main():
    cases = checked_assignments = 0
    clauses = list(product((1, -1, 2, -2), repeat=3))
    for formula in [(clause,) for clause in clauses] + list(product(clauses, repeat=2)):
        n, rows, refs = encode(2, formula)
        assert n == 6 + 5 * len(formula)
        assert all(row.bit_count() <= 2 for row, _ in rows)
        assert len(check.affine_space(n, rows)[1]) == 2
        for assignment in range(4):
            m = make_word(n, rows, refs, assignment)
            assert check.avoids(n, m) == sat(assignment, formula)
            checked_assignments += 1
        result = check.count(n, rows)[0]
        assert (result > 0) == any(sat(assignment, formula) for assignment in range(4))
        cases += 1
    # Directly enumerate original x, not only candidate product words.
    direct = 0
    for clause in product((1, -1), repeat=3):
        n, rows, refs = encode(1, (clause,))
        assert (check.brute(n, rows) > 0) == any(sat(x, (clause,)) for x in range(2))
        direct += 1
    for formula in (((1,1,1),(-1,-1,-1)), ((1,2,1),(-1,-2,-2))):
        n, rows, refs = encode(2, formula)
        assert (check.brute(n, rows) > 0) == any(sat(x, formula) for x in range(4))
        direct += 1
    n, rows, refs = encode(0, ())
    assert (n, check.brute(n, rows)) == (3, 4)
    n, rows, refs = encode(1, ())
    assert (n, check.brute(n, rows)) == (3, 5)
    print('formulas', cases, 'assignment_controls', checked_assignments,
          'direct_x_formulas', direct, 'empty_formula_count', 4, 'one_free_variable_count', 5)
    print('All checks passed.')


if __name__ == '__main__':
    main()
