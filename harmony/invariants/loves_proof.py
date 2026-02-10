"""
Universal non-coercive growth invariant.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from harmony.ops.acdc import ac_power, acdc_split, dc_slope


class LovesProofInvariant:
    """Enforce non-coercive growth with coherence and stress dynamics."""

    def __init__(
        self,
        eps: float = 1e-6,
        alpha: float = 0.02,
        min_window: int = 30,
        require_dc_trend: bool = True,
    ) -> None:
        self.eps = eps
        self.alpha = alpha
        self.min_window = min_window
        self.require_dc_trend = require_dc_trend

    def check(
        self,
        t: np.ndarray,
        C: np.ndarray,
        S: np.ndarray,
        x: np.ndarray,
    ) -> dict[str, Any]:
        t = np.asarray(t, dtype=float)
        C = np.asarray(C, dtype=float)
        S = np.asarray(S, dtype=float)
        x = np.asarray(x, dtype=float)

        n = min(len(t), len(C), len(S), len(x))
        if n < self.min_window:
            return self._insufficient_data_result()

        t_win = t[-n:]
        C_win = C[-n:]
        S_win = S[-n:]
        x_win = x[-n:]

        logC = np.log(C_win + self.eps)
        G = np.gradient(logC, t_win)
        G_mean = float(np.mean(G))

        S_slope = self._linear_slope(t_win, S_win)
        S_decreasing = S_slope < 0

        x_dc, x_ac = acdc_split(x_win, alpha=self.alpha)
        Pac_trend = self._ac_power_trend(x_ac, t_win)
        Pac_not_increasing = Pac_trend <= 0

        if self.require_dc_trend:
            S_dc, _ = acdc_split(S_win, alpha=self.alpha)
            S_dc_slope = self._linear_slope(t_win, S_dc)
            S_dc_decreasing = S_dc_slope < 0
        else:
            S_dc_slope = 0.0
            S_dc_decreasing = True

        invariant_holds = (
            G_mean > 0
            and S_decreasing
            and Pac_not_increasing
            and (not self.require_dc_trend or S_dc_decreasing)
        )

        return {
            "G_mean": G_mean,
            "S_slope": S_slope,
            "Pac_trend": Pac_trend,
            "S_dc_slope": S_dc_slope,
            "coherence_growing": G_mean > 0,
            "stress_decreasing": S_decreasing,
            "pac_not_increasing": Pac_not_increasing,
            "dc_stress_decreasing": S_dc_decreasing,
            "invariant_holds": invariant_holds,
            "window_samples": n,
            "violation_reason": self._analyze_violation(
                G_mean, S_slope, Pac_trend, S_dc_slope
            ),
        }

    def check_continuous(
        self,
        t: np.ndarray,
        C: np.ndarray,
        S: np.ndarray,
        x: np.ndarray,
        window_sec: float = 30.0,
        step_sec: float = 5.0,
    ) -> dict[str, list[Any]]:
        if len(t) > 1:
            fs = 1.0 / float(np.mean(np.diff(t)))
        else:
            fs = 1.0

        window_samples = int(window_sec * fs)
        step_samples = int(step_sec * fs)
        n_windows = (len(t) - window_samples) // step_samples + 1

        results: dict[str, list[Any]] = {
            "timestamps": [],
            "invariant_holds": [],
            "G_mean": [],
            "S_slope": [],
            "Pac_trend": [],
            "violation_reasons": [],
        }

        for i in range(n_windows):
            start = i * step_samples
            end = start + window_samples
            window_check = self.check(
                t=t[start:end],
                C=C[start:end],
                S=S[start:end],
                x=x[start:end],
            )
            results["timestamps"].append(float(t[start]))
            results["invariant_holds"].append(window_check["invariant_holds"])
            results["G_mean"].append(window_check["G_mean"])
            results["S_slope"].append(window_check["S_slope"])
            results["Pac_trend"].append(window_check["Pac_trend"])
            results["violation_reasons"].append(window_check["violation_reason"])

        return results

    def _linear_slope(self, t: np.ndarray, y: np.ndarray) -> float:
        if len(t) < 2:
            return 0.0

        t_mean = np.mean(t)
        y_mean = np.mean(y)
        numerator = np.sum((t - t_mean) * (y - y_mean))
        denominator = np.sum((t - t_mean) ** 2)
        return float(numerator / denominator) if denominator != 0 else 0.0

    def _ac_power_trend(self, x_ac: np.ndarray, t: np.ndarray) -> float:
        if len(x_ac) < 4:
            return 0.0

        mid = len(x_ac) // 2
        Pac1 = ac_power(x_ac[:mid]) if mid > 2 else ac_power(x_ac)
        Pac2 = ac_power(x_ac[mid:]) if len(x_ac) - mid > 2 else Pac1

        t_mid = t[mid] if mid < len(t) else t[-1]
        t_start = t[0]
        return float((Pac2 - Pac1) / (t_mid - t_start)) if t_mid > t_start else float(Pac2 - Pac1)

    def _analyze_violation(
        self, G_mean: float, S_slope: float, Pac_trend: float, S_dc_slope: float
    ) -> str:
        if G_mean > 0 and S_slope < 0 and Pac_trend <= 0 and S_dc_slope < 0:
            return "All conditions satisfied"

        violations = []
        if G_mean <= 0:
            violations.append("coherence not growing")
        if S_slope >= 0:
            violations.append("stress not decreasing")
        if Pac_trend > 0:
            violations.append("AC power increasing")
        if self.require_dc_trend and S_dc_slope >= 0:
            violations.append("DC stress not decreasing")

        return f"Violation: {'; '.join(violations)}" if violations else "No violations detected"

    def _insufficient_data_result(self) -> dict[str, Any]:
        return {
            "G_mean": 0.0,
            "S_slope": 0.0,
            "Pac_trend": 0.0,
            "S_dc_slope": 0.0,
            "coherence_growing": False,
            "stress_decreasing": False,
            "pac_not_increasing": False,
            "dc_stress_decreasing": False,
            "invariant_holds": False,
            "window_samples": 0,
            "violation_reason": "Insufficient data for analysis",
        }
