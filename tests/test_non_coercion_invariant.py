import numpy as np

from harmony.invariants.non_coercion import NonCoercionInvariant


def test_non_coercion_insufficient_data() -> None:
    invariant = NonCoercionInvariant()
    result = invariant.check(np.array([0.1]), np.array([0.2]))
    assert result["invariant_holds"] is None
    assert result["violation_reason"] == "Insufficient data"


def test_non_coercion_holds_for_growth_and_falling_stress() -> None:
    t = np.linspace(0, 10, 100)
    coherence = 0.1 * np.exp(0.2 * t)
    stress = 1.0 - 0.5 * (t / t[-1])

    invariant = NonCoercionInvariant(window_size=10)
    result = invariant.check(coherence, stress, t)

    assert bool(result["invariant_holds"]) is True
    assert bool(result["stress_decreasing"]) is True


def test_non_coercion_violation() -> None:
    t = np.linspace(0, 10, 100)
    coherence = np.ones_like(t) * 0.5
    stress = 0.2 + 0.3 * (t / t[-1])

    invariant = NonCoercionInvariant(window_size=10)
    result = invariant.check(coherence, stress, t)

    assert result["invariant_holds"] is False
    assert "Violation" in result["violation_reason"]


def test_non_coercion_continuous() -> None:
    t = np.linspace(0, 50, 500)
    coherence = 0.2 + 0.3 * (1 - np.exp(-t / 10))
    stress = 1.0 - 0.4 * (t / t[-1])

    invariant = NonCoercionInvariant(window_size=20)
    results = invariant.check_continuous(coherence, stress, window_sec=10.0, step_sec=5.0, fs=10.0)

    assert len(results["timestamps"]) == len(results["invariant_holds"])
    assert len(results["timestamps"]) > 0
