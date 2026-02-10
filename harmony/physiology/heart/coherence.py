import numpy as np
from scipy import fft, stats


class PhaseCoherence:
    """Calculate phase coherence and concentration metrics."""

    def __init__(self, window_sec: float = 30.0, fs: float = 250.0) -> None:
        self.window_sec = window_sec
        self.fs = fs
        self.window_samples = int(window_sec * fs)

    def phase_concentration(self, phase: np.ndarray, detrend: bool = True) -> float:
        if detrend:
            phase = self._detrend_within_window(phase)
        complex_mean = np.mean(np.exp(1j * phase))
        return float(np.abs(complex_mean))

    def spectral_concentration(
        self, signal_data: np.ndarray, fundamental_freq: float, bandwidth: float = 0.1
    ) -> float:
        n = len(signal_data)
        freqs = fft.rfftfreq(n, 1 / self.fs)
        power = np.abs(fft.rfft(signal_data)) ** 2

        mask = (freqs >= fundamental_freq - bandwidth) & (freqs <= fundamental_freq + bandwidth)
        if not np.any(mask):
            return 0.0

        power_in_band = np.sum(power[mask])
        total_power = np.sum(power)
        if total_power == 0:
            return 0.0
        return float(power_in_band / total_power)

    def sliding_coherence(self, phase: np.ndarray, step_sec: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
        step_samples = int(step_sec * self.fs)
        n_windows = (len(phase) - self.window_samples) // step_samples + 1

        coherence = np.zeros(n_windows)
        time_points = np.zeros(n_windows)

        for i in range(n_windows):
            start = i * step_samples
            end = start + self.window_samples
            window_phase = phase[start:end]
            coherence[i] = self.phase_concentration(window_phase, detrend=True)
            time_points[i] = start / self.fs

        return time_points, coherence

    def _detrend_within_window(self, phase: np.ndarray) -> np.ndarray:
        if len(phase) == 0:
            return phase.copy()
        if len(phase) == 1:
            return np.array([0.0])

        n = len(phase)
        t = np.arange(n) / self.fs
        slope, intercept, _, _, _ = stats.linregress(t, phase)
        trend = intercept + slope * t
        return phase - trend

    def coherence_gain_rate(self, coherence_values: np.ndarray, time_points: np.ndarray) -> np.ndarray:
        epsilon = 1e-6
        log_coherence = np.log(coherence_values + epsilon)
        if len(time_points) > 1:
            return np.gradient(log_coherence, time_points)
        return np.array([0.0])
