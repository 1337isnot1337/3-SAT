import copy
from fractions import Fraction
import json
from pathlib import Path
import unittest

from satbounds.cost import Envelope, analyze, contraction_cost

ROOT = Path(__file__).resolve().parents[1]


class CostTests(unittest.TestCase):
    def model(self, name="general"):
        return json.loads((ROOT / f"certificates/models/{name}.json").read_text())

    def test_selected_general_and_fixed_density_envelopes(self):
        general, fixed = analyze(self.model()), analyze(self.model("fixed-density"))
        self.assertEqual(general["alpha"], "1/2")
        self.assertEqual(fixed["alpha"], "1/2")
        self.assertEqual(general["dominant_envelope"], {"n": "1", "log": "-1/2", "loglog": "1"})
        self.assertEqual(fixed["dominant_envelope"], {"n": "1", "log": "-1/2", "loglog": "0"})

    def test_removing_iterated_log_does_not_increase_alpha(self):
        model = self.model()
        before = analyze(model)
        model["network_size"]["loglog"] = "0"
        after = analyze(model)
        self.assertEqual(before["alpha"], after["alpha"])
        self.assertLess(Envelope.read(after["dominant_envelope"]), Envelope.read(before["dominant_envelope"]))

    def test_unchanged_outer_cost_blocks_a_local_alpha_gain(self):
        model = self.model()
        model["contraction_log_saving"] = "3/5"
        result = analyze(model)
        self.assertEqual(result["alpha"], "1/2")
        self.assertEqual(set(result["dominant_terms"]), {"sparsification", "high-incidence branches"})

    def test_wire_growth_can_reverse_a_better_contraction_bound(self):
        model = self.model()
        model["contraction_log_saving"] = "3/4"
        model["network_size"]["log"] = "1/3"
        result = analyze(model)
        self.assertEqual(result["alpha"], "5/12")
        self.assertLess(Fraction(result["alpha"]), Fraction(1, 2))

    def test_polynomial_entry_exponent_can_dominate_all_log_savings(self):
        model = self.model()
        model["overheads"].append({"name": "new entry routine", "scale": {"n": "11/10", "log": "-100", "loglog": "0"}})
        result = analyze(model)
        self.assertIsNone(result["alpha"])
        self.assertEqual(result["dominant_terms"], ["new entry routine"])

    def test_reject_inexact_and_out_of_contract_models(self):
        for value in (0.5, True, "1/0"):
            model = self.model()
            model["contraction_log_saving"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                analyze(model)
        for field, value in (("n", "0"), ("n", "-1")):
            model = self.model()
            model["network_size"][field] = value
            with self.assertRaises(ValueError):
                analyze(model)
        model = self.model()
        model["overheads"].append(copy.deepcopy(model["overheads"][0]))
        with self.assertRaises(ValueError):
            analyze(model)

    def test_network_composition_retains_iterated_logs(self):
        network = Envelope(Fraction(1), Fraction(2, 7), Fraction(-3, 2))
        result = contraction_cost(network, Fraction(4, 5))
        self.assertEqual(result.log, Fraction(-18, 35))
        self.assertEqual(result.loglog, Fraction(-3, 2))


if __name__ == "__main__":
    unittest.main()
