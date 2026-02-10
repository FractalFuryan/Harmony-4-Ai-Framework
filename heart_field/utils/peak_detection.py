import numpy as np
from scipy import signal


def detect_r_peaks(ecg_signal: np.ndarray, fs: float) -> np.ndarray:
    peaks, _ = signal.find_peaks(
        ecg_signal,
        distance=int(0.5 * fs),
        height=np.percentile(ecg_signal, 75),
    )
    return peaks


def detect_breath_peaks(resp_signal: np.ndarray, fs: float) -> np.ndarray:
    peaks, _ = signal.find_peaks(
        resp_signal,
        distance=int(1.0 * fs),
        height=np.percentile(resp_signal, 60),
    )
    return peaks
