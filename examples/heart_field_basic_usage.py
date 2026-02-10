#!/usr/bin/env python3
"""Basic example of using the heart field scaling model."""

import numpy as np

from heart_field import (
    AnalyticSignal,
    EntrainmentMetrics,
    HeartFieldScorer,
    PhaseCoherence,
    SignalPreprocessor,
)


def simulate_signals(duration_sec: int = 300, fs: float = 250.0):
    t = np.arange(0, duration_sec, 1 / fs)
    n_samples = len(t)

    heart_rate = 1.2
    heart_signal = np.sin(2 * np.pi * heart_rate * t)

    resp_rate = 0.25
    heart_signal *= 1 + 0.1 * np.sin(2 * np.pi * resp_rate * t)

    resp_signal = 0.5 * np.sin(2 * np.pi * resp_rate * t)
    ppg_signal = 0.7 * np.sin(2 * np.pi * heart_rate * (t - 0.1))

    heart_signal += 0.05 * np.random.randn(n_samples)
    resp_signal += 0.02 * np.random.randn(n_samples)
    ppg_signal += 0.03 * np.random.randn(n_samples)

    return t, {"ecg": heart_signal, "resp": resp_signal, "ppg": ppg_signal}


def main() -> dict[str, object]:
    fs = 250.0
    duration_sec = 300

    print("Simulating physiological signals...")
    t, signals = simulate_signals(duration_sec, fs)

    preprocessor = SignalPreprocessor(fs=fs)
    analytic = AnalyticSignal(fs=fs)
    coherence = PhaseCoherence(window_sec=30, fs=fs)
    entrainment = EntrainmentMetrics(fs=fs)
    scorer = HeartFieldScorer(fs=fs)

    print("Preprocessing signals...")
    ecg_clean = preprocessor.preprocess_heart_signal(signals["ecg"])
    resp_clean = preprocessor.preprocess_resp_signal(signals["resp"])
    ppg_clean = preprocessor.preprocess_heart_signal(signals["ppg"])

    print("Computing analytic signals...")
    _, ecg_phase = analytic.compute(ecg_clean)
    _, resp_phase = analytic.compute(resp_clean)
    _, ppg_phase = analytic.compute(ppg_clean)

    ecg_phase_detrended = analytic.remove_linear_trend(ecg_phase, t)

    heart_amplitude = preprocessor.robust_amplitude(ecg_clean, method="p2p")
    print(f"Heart amplitude (A_h): {heart_amplitude:.4f}")

    heart_coherence = coherence.phase_concentration(ecg_phase_detrended)
    print(f"Heart coherence (C_h): {heart_coherence:.4f}")

    plv_resp = entrainment.phase_lock_value(ecg_phase_detrended, resp_phase)
    plv_ppg = entrainment.phase_lock_value(ecg_phase_detrended, ppg_phase)

    print(f"Heart-Resp PLV: {plv_resp:.4f}")
    print(f"Heart-PPG PLV: {plv_ppg:.4f}")

    results = scorer.compute_net_field(
        heart_amplitude=heart_amplitude,
        heart_coherence=heart_coherence,
        plv_dict={"respiration": plv_resp, "ppg": plv_ppg},
        distance=1.0,
    )

    print("\n=== Heart Field Scorecard ===")
    print(f"Effective field (A_eff): {results['effective_field']:.4f}")
    print(f"Net field (A_net): {results['net_field']:.4f}")
    print(f"Distance scaled: {results['net_field_scaled']:.4f}")

    print("\n=== Non-Coercion Constraint Check ===")
    time_points, coherence_series = coherence.sliding_coherence(ecg_phase_detrended)
    stress_proxy = 1.0 - 0.5 * time_points / time_points[-1] + 0.1 * np.random.randn(
        len(time_points)
    )

    constraint_check = scorer.compute_non_coercion_check(
        coherence_series, time_points, stress_proxy
    )

    print(constraint_check["message"])

    return results


if __name__ == "__main__":
    main()
