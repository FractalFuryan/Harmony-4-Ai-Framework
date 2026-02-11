from __future__ import annotations

import numpy as np

EPS = 1e-12


def coherence_kuramoto(phases: np.ndarray) -> np.ndarray:
    """
    Kuramoto order parameter magnitude R(t) for N oscillators:
        R(t) = |(1/N) * sum_k exp(i * phi_k(t))|
    phases shape: (N, T) or (T,) for single oscillator (returns ones).
    Returns shape: (T,)
    """
    phases = np.asarray(phases, dtype=float)
    if phases.ndim == 1:
        # Single oscillator is perfectly phase-concentrated by definition.
        return np.ones_like(phases, dtype=float)
    if phases.ndim != 2:
        raise ValueError("phases must be shape (N, T) or (T,)")

    phasors = np.exp(1j * phases)
    mean_phasor = np.mean(phasors, axis=0)
    r = np.abs(mean_phasor)
    return np.clip(r, 0.0, 1.0)


def coherence_phase_concentration(phase: np.ndarray) -> float:
    """
    Phase concentration:
        C = | mean(exp(i * phase)) |
    phase shape: (T,)
    Returns scalar in [0, 1].
    """
    phase = np.asarray(phase, dtype=float)
    c_value = np.abs(np.mean(np.exp(1j * phase)))
    return float(np.clip(c_value, 0.0, 1.0))


def coherence_spectral_concentration(
    x: np.ndarray,
    fs: float,
    f0: float,
    bandwidth: float = 0.1,
) -> float:
    """
    Spectral concentration around fundamental frequency f0:
        C = power_in_band / total_power
    Returns scalar in [0, 1].
    """
    x = np.asarray(x, dtype=float)
    if x.size < 8:
        return 0.0

    spectrum = np.fft.rfft(x)
    power = np.abs(spectrum) ** 2
    freqs = np.fft.rfftfreq(x.size, d=1.0 / fs)

    mask = (freqs >= (f0 - bandwidth)) & (freqs <= (f0 + bandwidth))
    total = float(np.sum(power))
    if total <= EPS or not np.any(mask):
        return 0.0
    band = float(np.sum(power[mask]))
    return float(np.clip(band / total, 0.0, 1.0))


def coherence_compression_gain(
    loss_model: np.ndarray,
    loss_baseline: np.ndarray,
    eps: float = 1e-12,
) -> np.ndarray:
    """
    Predictive compression / structure gain:
        C = 1 - (L_model / L_baseline)
    Interpretable when losses are comparable (e.g., cross-entropy per token).
    Returns time-series clipped to [0, 1].
    """
    loss_model = np.asarray(loss_model, dtype=float)
    loss_baseline = np.asarray(loss_baseline, dtype=float)
    if loss_model.shape != loss_baseline.shape:
        raise ValueError("loss_model and loss_baseline must have same shape")

    ratio = loss_model / (loss_baseline + eps)
    c_value = 1.0 - ratio
    return np.clip(c_value, 0.0, 1.0)
