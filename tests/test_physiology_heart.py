import numpy as np

from harmony.physiology.heart import (
    AnalyticSignal,
    EntrainmentMetrics,
    HeartFieldScorer,
    PhaseCoherence,
    PhysiologyLovesProof,
    SignalPreprocessor,
    StressIndexBuilder,
)


def test_preprocessing_and_amplitude() -> None:
    fs = 100.0
    t = np.arange(0, 2, 1 / fs)
    signal = np.sin(2 * np.pi * 1.0 * t) + 0.05 * np.random.randn(len(t))

    pre = SignalPreprocessor(fs=fs)
    cleaned = pre.preprocess_heart_signal(signal)
    assert cleaned.shape == signal.shape

    resp = pre.preprocess_resp_signal(signal)
    assert resp.shape == signal.shape

    amp_p2p = pre.robust_amplitude(signal, method="p2p", window_sec=0)
    amp_rms = pre.robust_amplitude(signal, method="rms", window_sec=0)
    assert amp_p2p > 0
    assert amp_rms > 0

    peaks = pre.detect_r_peaks(signal)
    assert isinstance(peaks, np.ndarray)


def test_analytic_and_coherence() -> None:
    fs = 100.0
    t = np.arange(0, 1, 1 / fs)
    signal = np.sin(2 * np.pi * 5 * t)

    analytic = AnalyticSignal(fs=fs)
    amp, phase = analytic.compute(signal)
    assert amp.shape == signal.shape
    assert phase.shape == signal.shape

    detrended = analytic.remove_linear_trend(phase, t)
    assert detrended.shape == phase.shape

    pc = PhaseCoherence(window_sec=0.2, fs=fs)
    coherence = pc.phase_concentration(detrended)
    assert 0 <= coherence <= 1

    times, values = pc.sliding_coherence(detrended, step_sec=0.1)
    assert len(times) == len(values)

    gains = pc.coherence_gain_rate(values, times)
    assert gains.shape[0] == values.shape[0]


def test_entrainment_and_consent() -> None:
    fs = 50.0
    t = np.arange(0, 2, 1 / fs)
    phase1 = 2 * np.pi * 1.0 * t
    phase2 = 2 * np.pi * 1.0 * t

    entrainment = EntrainmentMetrics(fs=fs, bias_correction=False)
    plv = entrainment.phase_lock_value(phase1, phase2)
    assert plv == 1.0

    times, plv_series = entrainment.sliding_plv(phase1, phase2, window_sec=1.0, step_sec=0.5)
    assert len(times) == len(plv_series)

    locked, delta = entrainment.arnold_tongue_boundary(1.0, 1.0, k_eff=0.1)
    assert locked is True
    assert delta == 0.0

    k_eff = entrainment.effective_coupling(k0=0.5, coherence=0.5, distance=2.0)
    assert k_eff > 0

    consent, lock_strength = entrainment.consent_gate(k_eff=1.0, delta_omega=0.2)
    assert consent is True
    assert lock_strength > 0

    threshold = entrainment.dynamic_consent_threshold(stress_level=0.5)
    assert threshold >= 0.1

    result = entrainment.revocable_entrainment(phase1, phase2, stress_receiver=0.1)
    assert "consent_granted" in result


def test_stress_index_builder() -> None:
    fs = 50.0
    builder = StressIndexBuilder(fs=fs)

    heart_rate = np.ones(500) * 60.0
    eda_signal = np.random.randn(500) * 0.05
    rr_intervals = np.ones(200) * 1.0

    stress = builder.compute_stress_index(
        heart_rate=heart_rate, eda_signal=eda_signal, rr_intervals=rr_intervals
    )
    assert "stress_index" in stress

    times, values, history = builder.compute_stress_timeseries(
        {
            "heart_rate": heart_rate,
            "eda_signal": eda_signal,
            "rr_intervals": rr_intervals,
        },
        window_sec=5.0,
        step_sec=2.5,
    )
    assert len(times) == len(values)
    assert isinstance(history, dict)


def test_heart_field_scoring_and_loves_proof() -> None:
    fs = 50.0
    t = np.arange(0, 10, 1 / fs)
    coherence = 0.2 + 0.6 * (t / t[-1])
    stress = 0.8 - 0.6 * (t / t[-1])
    heart_amp = np.sin(2 * np.pi * 1.0 * t)

    scorer = HeartFieldScorer(fs=fs, enable_loves_proof=True)

    field = scorer.compute_net_field(
        heart_amplitude=float(np.std(heart_amp)),
        heart_coherence=float(np.mean(coherence)),
        plv_dict={"respiration": 0.7, "ppg": 0.6},
        distance=1.0,
    )
    assert "net_field" in field

    check = scorer.compute_non_coercion_check(coherence, t, stress)
    assert "constraint_satisfied" in check

    combined = scorer.compute_with_loves_proof(
        t=t,
        heart_coherence=coherence,
        stress_proxy=stress,
        heart_amplitude=heart_amp,
        plv_dict={"respiration": 0.7},
    )
    assert "field_score" in combined
    assert "loves_proof" in combined

    adapter = PhysiologyLovesProof(fs=fs)
    result = adapter.check_heart_field(t, coherence, stress, heart_amplitude=heart_amp)
    assert "invariant_holds" in result
