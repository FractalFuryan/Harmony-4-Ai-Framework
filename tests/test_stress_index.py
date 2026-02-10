import unittest

import numpy as np

from heart_field.core.stress import StressIndexBuilder


class TestStressIndexBuilder(unittest.TestCase):
    def test_compute_stress_index_components(self) -> None:
        builder = StressIndexBuilder(fs=250.0, method="standard")
        heart_rate = np.ones(3000) * 60.0
        eda_signal = np.random.randn(3000) * 0.1
        rr_intervals = np.ones(100) * 1.0

        result = builder.compute_stress_index(
            heart_rate=heart_rate, eda_signal=eda_signal, rr_intervals=rr_intervals
        )

        self.assertIn("stress_index", result)
        self.assertIn("components", result)
        self.assertTrue(np.isfinite(result["stress_index"]))

    def test_compute_stress_timeseries(self) -> None:
        builder = StressIndexBuilder(fs=250.0, method="minimal")
        heart_rate = np.ones(5000) * 60.0
        eda_signal = np.random.randn(5000) * 0.1
        rr_intervals = np.ones(5000) * 1.0

        time_points, stress_values, component_history = builder.compute_stress_timeseries(
            {
                "heart_rate": heart_rate,
                "eda_signal": eda_signal,
                "rr_intervals": rr_intervals,
            },
            window_sec=10.0,
            step_sec=5.0,
        )

        self.assertEqual(len(time_points), len(stress_values))
        self.assertIsInstance(component_history, dict)


if __name__ == "__main__":
    unittest.main()
