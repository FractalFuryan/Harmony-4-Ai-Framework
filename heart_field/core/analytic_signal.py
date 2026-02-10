import numpy as np
from scipy import signal, stats


class AnalyticSignal:
    """Compute analytic signal representation using a Hilbert transform."""

    def __init__(self, fs: float = 250.0) -> None:
        self.fs = fs

    def compute(self, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        analytic = signal.hilbert(x)
        amplitude_envelope = np.abs(analytic)
        instantaneous_phase = np.angle(analytic)
        return amplitude_envelope, instantaneous_phase

    def unwrap_phase(self, phase: np.ndarray) -> np.ndarray:
        return np.unwrap(phase)

    def remove_linear_trend(self, phase: np.ndarray, t: np.ndarray | None = None) -> np.ndarray:
        if len(phase) == 0:
            return phase.copy()
        if len(phase) == 1:
            return np.array([0.0])

        if t is None:
            t = np.arange(len(phase)) / self.fs

        slope, intercept, _, _, _ = stats.linregress(t, phase)
        trend = intercept + slope * t
        return phase - trend

    def instantaneous_frequency(self, phase: np.ndarray) -> np.ndarray:
        return np.gradient(phase) * self.fs / (2.0 * np.pi)
