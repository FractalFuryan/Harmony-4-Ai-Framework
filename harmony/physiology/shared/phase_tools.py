"""
General phase dynamics tools usable across domains.
These are mathematical primitives, not physiological models.
"""

from __future__ import annotations

import numpy as np
from scipy import signal, stats


def compute_analytic_signal(x: np.ndarray, fs: float) -> tuple[np.ndarray, np.ndarray]:
    """Compute analytic signal z(t) = x(t) + i*H[x(t)]."""
    analytic = signal.hilbert(x)
    amplitude = np.abs(analytic)
    phase = np.angle(analytic)
    return amplitude, phase


def remove_linear_phase_trend(phase: np.ndarray, t: np.ndarray | None = None) -> np.ndarray:
    """Remove linear trend from phase using regression."""
    if len(phase) == 0:
        return phase.copy()
    if len(phase) == 1:
        return np.array([0.0])

    if t is None:
        t = np.arange(len(phase))

    slope, intercept, _, _, _ = stats.linregress(t, phase)
    trend = intercept + slope * t
    return phase - trend


def compute_phase_concentration(phase: np.ndarray) -> float:
    """Compute phase concentration C = |<exp(i*phi)>|."""
    if len(phase) == 0:
        return float("nan")
    complex_mean = np.mean(np.exp(1j * phase))
    return float(np.abs(complex_mean))


def compute_phase_lock_value(phase1: np.ndarray, phase2: np.ndarray) -> float:
    """Compute phase-locking value between two phase sequences."""
    if len(phase1) == 0 or len(phase2) == 0:
        return float("nan")
    phase_diff = phase1 - phase2
    complex_avg = np.mean(np.exp(1j * phase_diff))
    return float(np.abs(complex_avg))


def bias_corrected_plv(phase1: np.ndarray, phase2: np.ndarray, n_shuffles: int = 100) -> float:
    """Bias-correct PLV using circular shuffling."""
    raw_plv = compute_phase_lock_value(phase1, phase2)

    if n_shuffles <= 0 or len(phase1) < 100:
        return raw_plv

    shuffled_plvs = []
    n_samples = len(phase2)

    for _ in range(n_shuffles):
        shift = np.random.randint(n_samples)
        phase2_shuffled = np.roll(phase2, shift)
        shuffled_plvs.append(compute_phase_lock_value(phase1, phase2_shuffled))

    bias_estimate = float(np.mean(shuffled_plvs))
    return max(raw_plv - bias_estimate, 0.0)


def compute_coherence_gain_rate(coherence: np.ndarray, time_points: np.ndarray) -> np.ndarray:
    """Compute coherence gain rate G = d/dt log(C + eps)."""
    epsilon = 1e-6
    log_coherence = np.log(coherence + epsilon)
    if len(time_points) > 1:
        return np.gradient(log_coherence, time_points)
    return np.array([0.0])
