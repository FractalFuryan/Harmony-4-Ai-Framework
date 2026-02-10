"""Test the core Love's Proof invariant kernel."""

import numpy as np

from harmony.invariants.loves_proof import LovesProofInvariant


class TestLovesProofKernel:
    def test_healthy_growth_passes(self) -> None:
        t = np.linspace(0, 60, 300)

        C = 0.2 + 0.6 * (1 - np.exp(-t / 20))
        S = 1.0 - 0.5 * (t / t[-1])
        amp = 0.02 * (1 - 0.4 * (t / t[-1]))
        x = 0.2 + amp * np.sin(2 * np.pi * t / 5)

        invariant = LovesProofInvariant(require_dc_trend=False)
        result = invariant.check(t, C, S, x)

        assert result["invariant_holds"] is True
        assert result["coherence_growing"] is True
        assert result["stress_decreasing"] is True
        assert result["pac_not_increasing"] is True

    def test_coercive_growth_fails(self) -> None:
        t = np.linspace(0, 60, 300)

        C = 0.2 + 0.6 * (1 - np.exp(-t / 20))
        S = 0.2 + 0.8 * (t / t[-1])
        x = 0.2 + 0.02 * np.sin(2 * np.pi * t / 5)

        invariant = LovesProofInvariant(require_dc_trend=False)
        result = invariant.check(t, C, S, x)

        assert result["invariant_holds"] is False
        assert result["coherence_growing"] is True
        assert result["stress_decreasing"] is False
        assert "stress not decreasing" in result["violation_reason"]

    def test_volatile_growth_fails(self) -> None:
        t = np.linspace(0, 60, 300)

        C = 0.2 + 0.6 * (1 - np.exp(-t / 20))
        S = 1.0 - 0.5 * (t / t[-1])

        amp = 0.01 + 0.06 * (t / t[-1])
        x = 0.2 + amp * np.sin(2 * np.pi * t / 5)

        invariant = LovesProofInvariant(require_dc_trend=False)
        result = invariant.check(t, C, S, x)

        assert result["invariant_holds"] is False
        assert result["coherence_growing"] is True
        assert result["stress_decreasing"] is True
        assert result["pac_not_increasing"] is False
        assert "AC power increasing" in result["violation_reason"]

    def test_insufficient_data(self) -> None:
        invariant = LovesProofInvariant(min_window=10)

        t = np.array([0.0, 1.0])
        C = np.array([0.5, 0.6])
        S = np.array([0.8, 0.7])
        x = np.array([0.2, 0.3])

        result = invariant.check(t, C, S, x)

        assert result["invariant_holds"] is False
        assert "Insufficient data" in result["violation_reason"]

    def test_continuous_monitoring(self) -> None:
        t = np.linspace(0, 120, 600)

        C = np.zeros_like(t)
        S = np.zeros_like(t)
        x = np.zeros_like(t)

        C[:300] = 0.2 + 0.3 * (1 - np.exp(-t[:300] / 30))
        S[:300] = 0.8 - 0.4 * (t[:300] / t[299])
        x[:300] = 0.2 + 0.01 * np.sin(2 * np.pi * t[:300] / 5)

        C[300:] = 0.5 + 0.3 * (1 - np.exp(-(t[300:] - t[300]) / 20))
        S[300:] = 0.4 + 0.4 * ((t[300:] - t[300]) / (t[-1] - t[300]))
        x[300:] = 0.2 + 0.02 * np.sin(2 * np.pi * t[300:] / 5)

        invariant = LovesProofInvariant(require_dc_trend=False)
        results = invariant.check_continuous(t, C, S, x, window_sec=30, step_sec=10)

        assert len(results["timestamps"]) > 0
        assert len(results["invariant_holds"]) == len(results["timestamps"])
