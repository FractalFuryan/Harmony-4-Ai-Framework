import unittest

import numpy as np

from heart_field.core.entrainment import EntrainmentMetrics


class TestPLVBiasCorrection(unittest.TestCase):
    def setUp(self) -> None:
        self.fs = 250.0
        self.duration = 30.0
        self.t = np.arange(0, self.duration, 1 / self.fs)

    def test_bias_correction_reduces_inflation(self) -> None:
        np.random.seed(42)
        phase1 = np.cumsum(np.random.randn(len(self.t)) * 0.1)
        phase2 = np.cumsum(np.random.randn(len(self.t)) * 0.1)

        entrainment_raw = EntrainmentMetrics(self.fs, bias_correction=False)
        entrainment_corrected = EntrainmentMetrics(self.fs, bias_correction=True)

        window_sec = 5.0
        phase1_short = phase1[: int(window_sec * self.fs)]
        phase2_short = phase2[: int(window_sec * self.fs)]

        plv_raw = entrainment_raw.phase_lock_value(phase1_short, phase2_short)
        plv_corrected = entrainment_corrected.phase_lock_value(phase1_short, phase2_short)

        self.assertLessEqual(plv_corrected, plv_raw)
        self.assertLess(plv_corrected, 0.2)

    def test_correction_preserves_true_synchrony(self) -> None:
        common_phase = np.cumsum(np.random.randn(len(self.t)) * 0.1)
        phase1 = common_phase
        phase2 = common_phase + 0.1

        entrainment = EntrainmentMetrics(self.fs, bias_correction=True)
        plv = entrainment.phase_lock_value(phase1, phase2)

        self.assertGreater(plv, 0.7)

    def test_shuffle_consistency(self) -> None:
        np.random.seed(42)
        phase1 = np.cumsum(np.random.randn(1000) * 0.1)
        phase2 = np.cumsum(np.random.randn(1000) * 0.1)

        entrainment1 = EntrainmentMetrics(self.fs, bias_correction=True, n_shuffles=50)
        entrainment2 = EntrainmentMetrics(self.fs, bias_correction=True, n_shuffles=50)

        plv1 = entrainment1.phase_lock_value(phase1, phase2)
        plv2 = entrainment2.phase_lock_value(phase1, phase2)

        self.assertAlmostEqual(plv1, plv2, places=5)

    def test_edge_cases(self) -> None:
        entrainment = EntrainmentMetrics(self.fs)
        plv_empty = entrainment.phase_lock_value(np.array([]), np.array([]))
        self.assertTrue(np.isnan(plv_empty))

        plv_single = entrainment.phase_lock_value(np.array([0.0]), np.array([0.0]))
        self.assertEqual(plv_single, 1.0)

        phase_short = np.array([0.0, 1.0])
        plv_short = entrainment.phase_lock_value(phase_short, phase_short, corrected=True)
        self.assertEqual(plv_short, 1.0)


if __name__ == "__main__":
    unittest.main()
