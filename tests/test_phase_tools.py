import numpy as np

from harmony.physiology.shared.phase_tools import (
    bias_corrected_plv,
    compute_analytic_signal,
    compute_coherence_gain_rate,
    compute_phase_concentration,
    compute_phase_lock_value,
    remove_linear_phase_trend,
)


def test_compute_analytic_signal_basic() -> None:
    fs = 100.0
    t = np.arange(0, 1.0, 1.0 / fs)
    x = np.sin(2 * np.pi * 5 * t)

    amplitude, phase = compute_analytic_signal(x, fs)

    assert amplitude.shape == x.shape
    assert phase.shape == x.shape
    assert np.mean(amplitude) > 0.5


def test_remove_linear_phase_trend_edges() -> None:
    empty = np.array([])
    assert remove_linear_phase_trend(empty).size == 0

    single = np.array([3.14])
    assert np.allclose(remove_linear_phase_trend(single), np.array([0.0]))

    t = np.arange(100)
    phase = 0.5 * t + 1.0
    detrended = remove_linear_phase_trend(phase, t)
    slope = np.polyfit(t, detrended, 1)[0]
    assert abs(slope) < 1e-12


def test_phase_concentration_and_plv() -> None:
    phase = np.zeros(100)
    assert compute_phase_concentration(phase) == 1.0

    assert np.isnan(compute_phase_concentration(np.array([])))

    phase1 = np.linspace(0, 2 * np.pi, 200)
    phase2 = phase1.copy()
    assert abs(compute_phase_lock_value(phase1, phase2) - 1.0) < 1e-12

    assert np.isnan(compute_phase_lock_value(np.array([]), np.array([])))


def test_bias_corrected_plv() -> None:
    np.random.seed(0)
    phase1 = np.random.uniform(0, 2 * np.pi, 50)
    phase2 = np.random.uniform(0, 2 * np.pi, 50)

    raw = bias_corrected_plv(phase1, phase2, n_shuffles=100)
    direct = compute_phase_lock_value(phase1, phase2)
    assert raw == direct

    phase1 = np.random.uniform(0, 2 * np.pi, 200)
    phase2 = np.random.uniform(0, 2 * np.pi, 200)
    raw = compute_phase_lock_value(phase1, phase2)
    corrected = bias_corrected_plv(phase1, phase2, n_shuffles=10)
    assert 0.0 <= corrected <= raw


def test_compute_coherence_gain_rate() -> None:
    t = np.linspace(0, 5, 200)
    C = 0.1 * np.exp(0.3 * t)
    gain = compute_coherence_gain_rate(C, t)
    assert np.mean(gain) > 0

    single_gain = compute_coherence_gain_rate(np.array([0.5]), np.array([0.0]))
    assert np.allclose(single_gain, np.array([0.0]))
