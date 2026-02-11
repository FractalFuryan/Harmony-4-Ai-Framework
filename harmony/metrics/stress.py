from __future__ import annotations

import numpy as np

EPS = 1e-12


def stress_composite_physio(
    heart_rate: np.ndarray,
    eda: np.ndarray | None = None,
    hrv: np.ndarray | None = None,
) -> np.ndarray:
    """
    Composite physiological stress metric combining multiple signals.
    
    Combines heart rate elevation, electrodermal activity (EDA), and heart rate
    variability (HRV) reduction into a unified stress metric. When only heart rate
    is provided, returns normalized heart rate stress.
    
    Args:
        heart_rate: Heart rate signal (bpm), shape (T,)
        eda: Optional electrodermal activity signal, shape (T,)
        hrv: Optional heart rate variability signal (e.g., RMSSD), shape (T,)
    
    Returns:
        Composite stress values in [0, 1], shape (T,)
        Higher values indicate higher stress.
    """
    heart_rate = np.asarray(heart_rate, dtype=float)
    
    # Normalize heart rate to [0, 1] assuming typical range [40, 180] bpm
    hr_min, hr_max = 40.0, 180.0
    hr_stress = np.clip((heart_rate - hr_min) / (hr_max - hr_min), 0.0, 1.0)
    
    components = [hr_stress]
    
    if eda is not None:
        eda = np.asarray(eda, dtype=float)
        # Normalize EDA by its range in the signal
        eda_min, eda_max = np.min(eda), np.max(eda)
        if eda_max - eda_min > EPS:
            eda_stress = (eda - eda_min) / (eda_max - eda_min)
        else:
            eda_stress = np.zeros_like(eda)
        components.append(eda_stress)
    
    if hrv is not None:
        hrv = np.asarray(hrv, dtype=float)
        # Normalize HRV (inverse: lower HRV = higher stress)
        hrv_min, hrv_max = np.min(hrv), np.max(hrv)
        if hrv_max - hrv_min > EPS:
            hrv_stress = 1.0 - (hrv - hrv_min) / (hrv_max - hrv_min)
        else:
            hrv_stress = np.zeros_like(hrv)
        components.append(hrv_stress)
    
    # Average all components
    composite = np.mean(components, axis=0)
    return np.clip(composite, 0.0, 1.0)


def stress_prediction_error(
    predictions: np.ndarray,
    targets: np.ndarray,
    baseline_error: float | None = None,
) -> np.ndarray:
    """
    Stress derived from prediction error / surprise.
    
    Measures stress as the magnitude of prediction errors, normalized to [0, 1].
    Higher prediction errors indicate higher surprise/stress. Can be compared
    against a baseline error level.
    
    Args:
        predictions: Predicted values, shape (T,)
        targets: Target/actual values, shape (T,)
        baseline_error: Optional baseline error for normalization. If None,
                       uses the maximum error in the signal.
    
    Returns:
        Stress values in [0, 1], shape (T,)
        Higher values indicate higher prediction error/surprise.
    """
    predictions = np.asarray(predictions, dtype=float)
    targets = np.asarray(targets, dtype=float)
    
    if predictions.shape != targets.shape:
        raise ValueError("predictions and targets must have same shape")
    
    # Compute absolute prediction error
    error = np.abs(predictions - targets)
    
    # Normalize by baseline or maximum error
    if baseline_error is None:
        baseline_error = np.max(error)
    
    if baseline_error > EPS:
        stress = error / baseline_error
    else:
        stress = np.zeros_like(error)
    
    return np.clip(stress, 0.0, 1.0)


def stress_velocity_energy(
    signal: np.ndarray,
    window_size: int = 10,
) -> np.ndarray:
    """
    Stress derived from rate of change / kinetic energy.
    
    Measures stress as the magnitude of velocity (rate of change) in a signal.
    Higher rates of change indicate higher arousal/stress. Uses a sliding window
    to compute local velocity energy.
    
    Args:
        signal: Input signal, shape (T,)
        window_size: Window size for computing velocity energy (default: 10)
    
    Returns:
        Stress values in [0, 1], shape (T,)
        Higher values indicate higher rate of change/energy.
    """
    signal = np.asarray(signal, dtype=float)
    
    if signal.size < 2:
        return np.zeros_like(signal)
    
    # Compute first-order differences (velocity)
    velocity = np.diff(signal, prepend=signal[0])
    
    # Compute velocity energy (squared velocity) in sliding windows
    velocity_sq = velocity ** 2
    
    if window_size <= 1:
        energy = velocity_sq
    else:
        # Convolve with uniform window for smoothing
        window = np.ones(window_size) / window_size
        energy = np.convolve(velocity_sq, window, mode='same')
    
    # Normalize to [0, 1] by maximum energy
    max_energy = np.max(energy)
    if max_energy > EPS:
        stress = energy / max_energy
    else:
        stress = np.zeros_like(energy)
    
    return np.clip(stress, 0.0, 1.0)
