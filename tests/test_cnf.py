import itertools
import unittest

from satbounds.cnf import CNF, count, parse_dimacs


class CNFTests(unittest.TestCase):
    def test_declared_unused_variables_and_empty_inputs(self):
        self.assertEqual(count(parse_dimacs("p cnf 0 0\n")), 1)
        self.assertEqual(count(parse_dimacs("p cnf 4 0\n")), 16)
        self.assertEqual(count(parse_dimacs("p cnf 4 1\n1 0\n")), 8)
        self.assertEqual(count(parse_dimacs("p cnf 4 1\n0\n")), 0)

    def test_repeated_literals_tautologies_and_negations(self):
        self.assertEqual(count(parse_dimacs("p cnf 3 2\n1 1 1 0 -2 2 0\n")), 4)
        self.assertEqual(count(parse_dimacs("p cnf 3 2\n1 0 -1 0\n")), 0)
        self.assertEqual(count(parse_dimacs("p cnf 3 1\n-1 -2 -3 0\n")), 7)

    def test_clauses_can_span_or_share_lines(self):
        formula = parse_dimacs("c example\np cnf 3 2\n1\n-2 0 3 0\nc end\n")
        self.assertEqual(formula.clauses, ((1, -2), (3,)))
        self.assertEqual(count(formula), 3)

    def test_reject_malformed_or_non_3cnf_inputs(self):
        invalid = ["", "1 0\np cnf 1 1", "p cnf 1 1\n1", "p cnf 1 0\n1 0",
                   "p cnf -1 0", "p cnf 1 1\n2 0", "p cnf 4 1\n1 2 3 4 0",
                   "p cnf 0 1\n1 0", "p cnf 1 0\np cnf 1 0", "p cnf 1 1\nx 0"]
        for text in invalid:
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_dimacs(text)

    def test_small_reference_is_explicitly_bounded(self):
        with self.assertRaises(ValueError):
            count(CNF(21, ()))

    def test_all_two_clause_formulas_over_two_used_variables(self):
        # Independent inclusion-exclusion oracle, with a third declared unused variable.
        # Includes empty clauses, repetitions, both signs, and tautological clauses.
        clauses = [c for width in range(4)
                   for c in itertools.product((1, -1, 2, -2), repeat=width)]

        def violation_intersection(*selected):
            forced = {}
            for clause in selected:
                for literal in clause:
                    variable, value = abs(literal), literal < 0
                    if variable in forced and forced[variable] != value:
                        return 0
                    forced[variable] = value
            return 1 << (3 - len(forced))

        checked = 0
        for left, right in itertools.combinations_with_replacement(clauses, 2):
            expected = (8 - violation_intersection(left) - violation_intersection(right)
                        + violation_intersection(left, right))
            self.assertEqual(count(CNF(3, (left, right))), expected, (left, right))
            checked += 1
        self.assertEqual(checked, 3655)


if __name__ == "__main__":
    unittest.main()
