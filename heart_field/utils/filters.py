import numpy as np
from scipy import signal


def notch_filter(x: np.ndarray, fs: float, notch_freq: float = 50.0, Q: float = 30.0) -> np.ndarray:
    b, a = signal.iirnotch(notch_freq, Q, fs)
    return signal.filtfilt(b, a, x)


def bandpass_filter(
    x: np.ndarray, fs: float, low: float, high: float, order: int = 4
) -> np.ndarray:
    nyquist = fs / 2.0
    b, a = signal.butter(order, [low / nyquist, high / nyquist], btype="band")
    return signal.filtfilt(b, a, x)


def highpass_filter(x: np.ndarray, fs: float, cutoff: float, order: int = 2) -> np.ndarray:
    nyquist = fs / 2.0
    b, a = signal.butter(order, cutoff / nyquist, btype="high")
    return signal.filtfilt(b, a, x)


def lowpass_filter(x: np.ndarray, fs: float, cutoff: float, order: int = 2) -> np.ndarray:
    nyquist = fs / 2.0
    b, a = signal.butter(order, cutoff / nyquist, btype="low")
    return signal.filtfilt(b, a, x)
