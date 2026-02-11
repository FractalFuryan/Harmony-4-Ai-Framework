import numpy as np
from scipy import signal


class SignalPreprocessor:
    """Clean and prepare physiological signals."""

    def __init__(
        self,
        fs: float = 250.0,
        notch_freq: float = 50.0,
        heart_band: tuple[float, float] = (0.5, 40.0),
        resp_band: tuple[float, float] = (0.05, 0.5),
    ) -> None:
        self.fs = fs
        self.notch_freq = notch_freq
        self.heart_band = heart_band
        self.resp_band = resp_band

    def apply_notch_filter(self, x: np.ndarray, q: float = 30.0) -> np.ndarray:
        b, a = signal.iirnotch(self.notch_freq, q, self.fs)  # type: ignore[misc]
        return signal.filtfilt(b, a, x)  # type: ignore[no-any-return]

    def apply_bandpass(
        self, x: np.ndarray, band: tuple[float, float], order: int = 4
    ) -> np.ndarray:
        nyquist = self.fs / 2.0
        low = band[0] / nyquist
        high = band[1] / nyquist
        b, a = signal.butter(order, [low, high], btype="band")  # type: ignore[misc]
        return signal.filtfilt(b, a, x)  # type: ignore[no-any-return]

    def remove_baseline_drift(
        self, x: np.ndarray, cutoff: float = 0.5, order: int = 2
    ) -> np.ndarray:
        nyquist = self.fs / 2.0
        high = cutoff / nyquist
        b, a = signal.butter(order, high, btype="high")  # type: ignore[misc]
        return signal.filtfilt(b, a, x)  # type: ignore[no-any-return]

    def preprocess_heart_signal(self, x: np.ndarray, remove_drift: bool = True) -> np.ndarray:
        x_clean = x.copy()
        x_clean = self.apply_notch_filter(x_clean)
        if remove_drift:
            x_clean = self.remove_baseline_drift(x_clean)
        x_clean = self.apply_bandpass(x_clean, self.heart_band)
        return x_clean

    def preprocess_resp_signal(self, x: np.ndarray) -> np.ndarray:
        x_clean = x.copy()
        x_clean = self.apply_bandpass(x_clean, self.resp_band)
        return x_clean

    def robust_amplitude(
        self, x: np.ndarray, method: str = "p2p", window_sec: float = 30.0
    ) -> float:
        if window_sec <= 0:
            return self._amplitude_from_segment(x, method)

        window_samples = max(1, int(window_sec * self.fs))
        if len(x) <= window_samples:
            return self._amplitude_from_segment(x, method)

        n_windows = len(x) // window_samples
        estimates = []
        for i in range(n_windows):
            start = i * window_samples
            end = start + window_samples
            estimates.append(self._amplitude_from_segment(x[start:end], method))
        return float(np.mean(estimates))

    def _amplitude_from_segment(self, x: np.ndarray, method: str) -> float:
        if method == "p2p":
            q5 = np.percentile(x, 5)
            q95 = np.percentile(x, 95)
            return float((q95 - q5) / 2.0)
        if method == "rms":
            return float(np.sqrt(np.mean(x**2)))
        raise ValueError(f"Unknown method: {method}")

    def detect_r_peaks(self, ecg_signal: np.ndarray) -> np.ndarray:
        peaks, _ = signal.find_peaks(  # type: ignore[misc]
            ecg_signal,
            distance=int(0.5 * self.fs),
            height=np.percentile(ecg_signal, 75),
        )
        return peaks  # type: ignore[no-any-return]
