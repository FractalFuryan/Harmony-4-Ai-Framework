"""
Growth bounds invariant: growth must be self-limiting.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np


class GrowthBoundsInvariant:
    """Enforce that growth follows bounded, self-limiting dynamics."""

    def __init__(self, growth_law: Callable[[np.ndarray, float], np.ndarray] | None = None) -> None:
        if growth_law is None:
            self.growth_law = self._logistic_growth
        else:
            self.growth_law = growth_law

    def _logistic_growth(self, x: np.ndarray, alpha: float) -> np.ndarray:
        return alpha * x * (1.0 - x)

    def _gompertz_growth(self, x: np.ndarray, alpha: float) -> np.ndarray:
        x_safe = np.clip(x, 1e-6, 1.0)
        return alpha * x * np.log(1.0 / x_safe)

    def check_boundedness(
        self,
        x_series: np.ndarray,
        time_points: np.ndarray,
        max_growth_rate: float = 1.0,
    ) -> dict[str, object]:
        if len(x_series) < 2:
            return self._insufficient_data_result()

        dx = np.diff(x_series)
        dt = np.diff(time_points)
        actual_rates = dx / dt

        explosive_growth = bool(np.any(np.abs(actual_rates) > max_growth_rate))

        if len(x_series) > 10:
            recent_values = x_series[-min(10, len(x_series)) :]
            saturation_level = float(np.mean(recent_values))
            near_saturation = saturation_level > 0.9
        else:
            saturation_level = 0.0
            near_saturation = False

        invariant_holds = not explosive_growth

        return {
            "invariant_holds": invariant_holds,
            "explosive_growth": explosive_growth,
            "max_growth_rate_observed": (
                float(np.max(np.abs(actual_rates))) if len(actual_rates) > 0 else 0.0
            ),
            "saturation_level": saturation_level,
            "near_saturation": near_saturation,
            "violation_reason": self._get_violation_reason(invariant_holds, explosive_growth),
        }

    def simulate_bounded_growth(
        self,
        x0: float,
        alpha: float,
        n_steps: int = 100,
        dt: float = 0.1,
        growth_type: str = "logistic",
    ) -> np.ndarray:
        if growth_type == "gompertz":
            growth_func = self._gompertz_growth
        else:
            growth_func = self._logistic_growth

        x = np.zeros(n_steps)
        x[0] = np.clip(x0, 0.01, 0.99)

        for i in range(1, n_steps):
            dx = growth_func(x[i - 1], alpha) * dt
            x[i] = np.clip(x[i - 1] + dx, 0.0, 1.0)

        return x

    def _get_violation_reason(self, holds: bool, explosive_growth: bool) -> str | None:
        if holds:
            return None
        if explosive_growth:
            return "Growth rate exceeds maximum bound"
        return "Growth pattern violates boundedness"

    def _insufficient_data_result(self) -> dict[str, object]:
        return {
            "invariant_holds": None,
            "explosive_growth": False,
            "max_growth_rate_observed": 0.0,
            "saturation_level": 0.0,
            "near_saturation": False,
            "violation_reason": "Insufficient data",
        }
