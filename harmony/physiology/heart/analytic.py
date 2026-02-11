import numpy as np

from harmony.physiology.shared import phase_tools


class AnalyticSignal:
    """Compute analytic signal representation using a Hilbert transform."""

    def __init__(self, fs: float = 250.0) -> None:
        self.fs = fs

    def compute(self, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        return phase_tools.compute_analytic_signal(x, self.fs)

    def unwrap_phase(self, phase: np.ndarray) -> np.ndarray:
        return np.unwrap(phase)

    def remove_linear_trend(self, phase: np.ndarray, t: np.ndarray | None = None) -> np.ndarray:
        if t is None:
            t = np.arange(len(phase)) / self.fs
        return phase_tools.remove_linear_phase_trend(phase, t)

    def instantaneous_frequency(self, phase: np.ndarray) -> np.ndarray:
        return np.gradient(phase) * self.fs / (2.0 * np.pi)  # type: ignore[no-any-return]
