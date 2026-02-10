import unittest

import numpy as np

from heart_field.core.field_score import HeartFieldScorer


class TestHeartFieldScorer(unittest.TestCase):
    def setUp(self) -> None:
        self.scorer = HeartFieldScorer()

    def test_compute_net_field_basic(self) -> None:
        results = self.scorer.compute_net_field(
            heart_amplitude=2.0,
            heart_coherence=0.8,
            plv_dict={"respiration": 0.7, "ppg": 0.6},
        )

        expected_eff = 1.6
        expected_plv = (0.7 ** 0.4) * (0.6 ** 0.3)
        self.assertAlmostEqual(results["effective_field"], expected_eff)
        self.assertAlmostEqual(results["net_field"], expected_eff * expected_plv, places=6)

    def test_distance_scaling(self) -> None:
        results = self.scorer.compute_net_field(
            heart_amplitude=2.0,
            heart_coherence=0.8,
            plv_dict={"respiration": 0.7},
            distance=2.0,
        )

        self.assertAlmostEqual(results["distance_scaling"], 0.125)

    def test_zero_plv_handling(self) -> None:
        results = self.scorer.compute_net_field(
            heart_amplitude=1.0,
            heart_coherence=1.0,
            plv_dict={"respiration": 0.0},
        )

        self.assertGreater(results["net_field"], 0)

    def test_custom_weights(self) -> None:
        custom_weights = {"respiration": 0.8, "ppg": 0.2}

        results = self.scorer.compute_net_field(
            heart_amplitude=1.0,
            heart_coherence=1.0,
            plv_dict={"respiration": 0.5, "ppg": 0.5},
            weights=custom_weights,
        )

        self.assertIn("respiration", results["plv_contributions"])
        self.assertEqual(results["plv_contributions"]["respiration"]["weight"], 0.8)


if __name__ == "__main__":
    unittest.main()
