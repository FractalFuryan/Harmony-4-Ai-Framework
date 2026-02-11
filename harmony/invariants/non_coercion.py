"""
Non-coercion invariant: order must grow while stress decreases.
"""

from __future__ import annotations

import numpy as np
from scipy import stats


class NonCoercionInvariant:
    """Enforce that growth emerges without force."""

    def __init__(self, window_size: int = 10, epsilon: float = 1e-6) -> None:
        self.window_size = window_size
        self.epsilon = epsilon

    def check(
        self,
        coherence: np.ndarray,
        stress: np.ndarray,
        time_points: np.ndarray | None = None,
    ) -> dict[str, object]:
        if len(coherence) < 2 or len(stress) < 2:
            return self._insufficient_data_result()

        if time_points is None:
            time_points = np.arange(len(coherence))

        log_coherence = np.log(coherence + self.epsilon)
        gain_rate = np.gradient(log_coherence, time_points)

        stress_slope, _, _, _, _ = stats.linregress(time_points, stress)
        stress_decreasing = stress_slope < 0

        recent = min(self.window_size, len(gain_rate))
        recent_g = float(np.mean(gain_rate[-recent:]))

        invariant_holds = (recent_g > 0) and stress_decreasing

        return {
            "invariant_holds": invariant_holds,
            "coherence_gain_rate": recent_g,
            "stress_slope": float(stress_slope),
            "stress_decreasing": stress_decreasing,
            "window_size": self.window_size,
            "violation_reason": self._get_violation_reason(invariant_holds, recent_g, stress_slope),
        }

    def check_continuous(
        self,
        coherence_series: np.ndarray,
        stress_series: np.ndarray,
        window_sec: float = 30.0,
        step_sec: float = 5.0,
        fs: float = 1.0,
    ) -> dict[str, list[object]]:
        window_samples = int(window_sec * fs)
        step_samples = int(step_sec * fs)
        n_windows = (len(coherence_series) - window_samples) // step_samples + 1

        results: dict[str, list[object]] = {
            "timestamps": [],
            "invariant_holds": [],
            "coherence_gain": [],
            "stress_slope": [],
        }

        for i in range(n_windows):
            start = i * step_samples
            end = start + window_samples

            window_coherence = coherence_series[start:end]
            window_stress = stress_series[start:end]
            window_time = np.arange(len(window_coherence)) / fs

            result = self.check(window_coherence, window_stress, window_time)

            results["timestamps"].append(start / fs)
            results["invariant_holds"].append(result["invariant_holds"])
            results["coherence_gain"].append(result["coherence_gain_rate"])
            results["stress_slope"].append(result["stress_slope"])

        return results

    def _get_violation_reason(
        self, holds: bool, gain_rate: float, stress_slope: float
    ) -> str | None:
        if holds:
            return None
        reasons = []
        if gain_rate <= 0:
            reasons.append("coherence not growing")
        if stress_slope >= 0:
            reasons.append("stress not decreasing")
        return f"Violation: {' and '.join(reasons)}"

    def _insufficient_data_result(self) -> dict[str, object]:
        return {
            "invariant_holds": None,
            "coherence_gain_rate": 0.0,
            "stress_slope": 0.0,
            "stress_decreasing": None,
            "window_size": self.window_size,
            "violation_reason": "Insufficient data",
        }
