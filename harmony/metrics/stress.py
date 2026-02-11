from __future__ import annotations

import numpy as np

EPS = 1e-12

def zscore(x: np.ndarray, eps: float = 1e-9) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    mean = np.mean(x)
    std = np.std(x)
    result: np.ndarray = (x - mean) / (std + eps)
    return result

def stress_composite_physio(
    eda_phasic: np.ndarray,
    lf_hf_ratio: np.ndarray,
    rmssd: np.ndarray,
    w_eda: float = 1.0,
    w_lfhf: float = 1.0,
    w_rmssd: float = 1.0,
) -> np.ndarray:
    """
    Physiological stress proxy (higher = worse):
        S = w_eda*z(EDA_phasic) + w_lfhf*z(LF/HF) - w_rmssd*z(RMSSD)
    """
    eda = zscore(eda_phasic)
    lfhf = zscore(lf_hf_ratio)
    rmssd_z = zscore(rmssd)
    stress = w_eda * eda + w_lfhf * lfhf - w_rmssd * rmssd_z
    result: np.ndarray = np.maximum(stress, 0.0)
    return result

def stress_velocity_energy(x: np.ndarray, dt: float) -> np.ndarray:
    """
    Dynamics stress proxy: squared velocity energy ||dx/dt||^2.
    """
    x = np.asarray(x, dtype=float)
    if x.size < 3:
        return np.zeros_like(x)
    dx = np.gradient(x, dt)
    stress = dx**2
    result: np.ndarray = np.maximum(stress, 0.0)
    return result

def stress_prediction_error(err: np.ndarray) -> np.ndarray:
    """
    Surprise / prediction error proxy: squared error.
    """
    err = np.asarray(err, dtype=float)
    result: np.ndarray = np.maximum(err**2, 0.0)
    return result
