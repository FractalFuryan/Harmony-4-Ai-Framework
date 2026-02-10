import unittest

import numpy as np
from scipy import stats

from heart_field.core.analytic_signal import AnalyticSignal


class TestPhaseRobustness(unittest.TestCase):
    def test_detrending_robust_to_noise(self) -> None:
        fs = 250.0
        duration = 10.0
        t = np.arange(0, duration, 1 / fs)

        linear_drift = 0.5 * t
        noise = 0.2 * np.random.randn(len(t))
        phase_jump = np.zeros(len(t))
        phase_jump[len(t) // 2 :] = 1.0

        phase = linear_drift + noise + phase_jump

        analytic = AnalyticSignal(fs=fs)
        phase_detrended = analytic.remove_linear_trend(phase, t)

        slope_resid, _, _, _, _ = stats.linregress(t, phase_detrended)

        self.assertLess(abs(slope_resid), 0.01)
        self.assertLess(abs(np.mean(phase_detrended)), 0.1)

    def test_detrending_preserves_oscillations(self) -> None:
        fs = 250.0
        duration = 10.0
        t = np.arange(0, duration, 1 / fs)

        linear_drift = 0.3 * t
        oscillation = 0.5 * np.sin(2 * np.pi * 0.5 * t)

        phase = linear_drift + oscillation

        analytic = AnalyticSignal(fs=fs)
        phase_detrended = analytic.remove_linear_trend(phase, t)

        fft_result = np.fft.rfft(phase_detrended)
        freqs = np.fft.rfftfreq(len(phase_detrended), 1 / fs)

        idx = np.where((freqs > 0.4) & (freqs < 0.6))[0]
        if len(idx) > 0:
            peak_power = np.max(np.abs(fft_result[idx]))
            self.assertGreater(peak_power, 0.1)

    def test_empty_phase_handling(self) -> None:
        analytic = AnalyticSignal(fs=250.0)

        phase_empty = np.array([])
        t_empty = np.array([])
        result = analytic.remove_linear_trend(phase_empty, t_empty)
        self.assertEqual(len(result), 0)

        phase_single = np.array([1.0])
        t_single = np.array([0.0])
        result = analytic.remove_linear_trend(phase_single, t_single)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 0.0)


if __name__ == "__main__":
    unittest.main()
