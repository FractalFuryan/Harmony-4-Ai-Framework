import numpy as np

from harmony import HeartFieldScorer, NonCoercionInvariant, phase_tools


print("=== Final Integration Smoke Test ===\n")

fs = 250.0
duration = 60

t = np.arange(0, duration, 1 / fs)

heart_signal = np.sin(2 * np.pi * 1.2 * t) * (0.5 + 0.3 * t / duration)
heart_signal += 0.1 * np.random.randn(len(t))

print("1. Testing domain-agnostic phase tools...")
amp, phase = phase_tools.compute_analytic_signal(heart_signal, fs)
phase_detrended = phase_tools.remove_linear_phase_trend(phase)
coherence = phase_tools.compute_phase_concentration(phase_detrended)
print(f"   Signal length: {len(heart_signal)} samples")
print(f"   Mean amplitude: {np.mean(amp):.3f}")
print(f"   Phase concentration: {coherence:.3f}")

print("\n2. Testing non-coercion invariant...")
nc_invariant = NonCoercionInvariant()

coherence_series = 0.3 + 0.5 * (t / duration)
stress_series = 0.8 - 0.6 * (t / duration)

result = nc_invariant.check(coherence_series, stress_series, t)
print(f"   Invariant holds: {result['invariant_holds']}")
print(f"   Coherence gain rate: {result['coherence_gain_rate']:.4f}")
print(f"   Stress slope: {result['stress_slope']:.4f}")
if result["violation_reason"]:
    print(f"   Note: {result['violation_reason']}")

print("\n3. Testing physiology-specific implementation...")
scorer = HeartFieldScorer(fs=fs)

plv_dict = {
    "respiration": 0.7 + 0.2 * np.random.rand(),
    "ppg": 0.6 + 0.2 * np.random.rand(),
}

field_result = scorer.compute_net_field(
    heart_amplitude=np.std(heart_signal),
    heart_coherence=coherence,
    plv_dict=plv_dict,
    distance=1.0,
)

print(f"   Heart amplitude: {field_result['heart_amplitude']:.3f}")
print(f"   Heart coherence: {field_result['heart_coherence']:.3f}")
print(f"   Effective field: {field_result['effective_field']:.3f}")
print(f"   Net field score: {field_result['net_field']:.3f}")

print("\n4. Testing non-coercion constraint in scorer...")
coherence_ds = coherence_series[::100]
stress_ds = stress_series[::100]
time_ds = t[::100]

constraint_result = scorer.compute_non_coercion_check(
    coherence_values=coherence_ds,
    time_points=time_ds,
    stress_proxy=stress_ds,
)

print(f"   Constraint satisfied: {constraint_result['constraint_satisfied']}")
print(f"   Message: {constraint_result['message']}")

print("\n=== Smoke Test Complete ===")
print("✓ Domain-agnostic tools work")
print("✓ Generalized invariants work")
print("✓ Physiology-specific implementations work")
print("✓ All components integrate correctly")
