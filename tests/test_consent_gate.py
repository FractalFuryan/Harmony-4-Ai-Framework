import unittest

import numpy as np

from heart_field.core.entrainment import EntrainmentMetrics


class TestConsentGate(unittest.TestCase):
    def setUp(self) -> None:
        self.entrainment = EntrainmentMetrics(fs=250.0)

    def test_consent_gate_basic(self) -> None:
        consent, lock = self.entrainment.consent_gate(K_eff=2.0, delta_omega=1.0)
        self.assertTrue(consent)
        self.assertGreaterEqual(lock, 0.5)

        consent, lock = self.entrainment.consent_gate(K_eff=0.05, delta_omega=0.01)
        self.assertFalse(consent)
        self.assertEqual(lock, 0.0)

        consent, lock = self.entrainment.consent_gate(K_eff=1.0, delta_omega=2.0)
        self.assertFalse(consent)
        self.assertEqual(lock, 0.0)

    def test_dynamic_consent_threshold(self) -> None:
        threshold_low = self.entrainment.dynamic_consent_threshold(
            stress_level=0.0, baseline_threshold=0.1
        )
        self.assertAlmostEqual(threshold_low, 0.1)

        threshold_high = self.entrainment.dynamic_consent_threshold(
            stress_level=0.8, baseline_threshold=0.1, stress_sensitivity=0.5
        )
        self.assertGreater(threshold_high, threshold_low)

        threshold_capped = self.entrainment.dynamic_consent_threshold(
            stress_level=10.0, baseline_threshold=0.1
        )
        self.assertLessEqual(threshold_capped, 0.3000001)

    def test_max_permissible_lock(self) -> None:
        consent, lock = self.entrainment.consent_gate(
            K_eff=10.0, delta_omega=0.001, max_permissible_lock=0.8
        )
        self.assertTrue(consent)
        self.assertLessEqual(lock, 0.8)

    def test_revocable_entrainment_integration(self) -> None:
        fs = 250.0
        t = np.arange(0, 10, 1 / fs)

        phase_source = 2 * np.pi * 1.0 * t

        phase_receiver = 2 * np.pi * 1.2 * t[: len(t) // 2]
        phase_receiver = np.concatenate(
            [phase_receiver, 2 * np.pi * 1.0 * t[len(t) // 2 :] + 0.5]
        )

        results = self.entrainment.revocable_entrainment(
            phase_source, phase_receiver, stress_receiver=0.3
        )

        expected_keys = [
            "consent_granted",
            "lock_strength",
            "plv",
            "delta_omega",
            "K_eff",
            "consent_threshold",
            "respectful_influence",
        ]
        for key in expected_keys:
            self.assertIn(key, results)

        self.assertLessEqual(results["respectful_influence"], results["plv"])


if __name__ == "__main__":
    unittest.main()
