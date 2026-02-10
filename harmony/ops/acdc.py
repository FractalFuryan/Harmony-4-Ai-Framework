"""
AC/DC signal decomposition operator.
"""

from __future__ import annotations

from typing import Tuple

import numpy as np


def ema_lpf(x: np.ndarray, alpha: float = 0.02) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    if x.size == 0:
        return x.copy()

    y = np.empty_like(x, dtype=float)
    y[0] = x[0]

    for i in range(1, len(x)):
        y[i] = alpha * x[i] + (1.0 - alpha) * y[i - 1]

    return y


def acdc_split(x: np.ndarray, alpha: float = 0.02) -> Tuple[np.ndarray, np.ndarray]:
    x = np.asarray(x, dtype=float)
    x_dc = ema_lpf(x, alpha=alpha)
    x_ac = x - x_dc
    return x_dc, x_ac


def ac_power(x_ac: np.ndarray) -> float:
    x_ac = np.asarray(x_ac, dtype=float)
    return float(np.mean(x_ac**2)) if x_ac.size else 0.0


def dc_slope(x_dc: np.ndarray, t: np.ndarray) -> float:
    if len(x_dc) < 2:
        return 0.0

    t = np.asarray(t, dtype=float)
    x_dc = np.asarray(x_dc, dtype=float)

    t_mean = np.mean(t)
    x_mean = np.mean(x_dc)

    numerator = np.sum((t - t_mean) * (x_dc - x_mean))
    denominator = np.sum((t - t_mean) ** 2)

    return float(numerator / denominator) if denominator != 0 else 0.0


def ac_power_trend(x_ac: np.ndarray, t: np.ndarray) -> float:
    if len(x_ac) < 4:
        return 0.0

    window_size = max(4, len(x_ac) // 10)
    step = max(1, window_size // 2)
    power_values = []
    power_times = []

    for i in range(0, len(x_ac) - window_size + 1, step):
        window_ac = x_ac[i : i + window_size]
        window_t = t[i : i + window_size]
        if len(window_ac) >= 2:
            power_values.append(ac_power(window_ac))
            power_times.append(float(np.mean(window_t)))

    if len(power_values) < 2:
        return 0.0

    return dc_slope(np.array(power_values), np.array(power_times))
