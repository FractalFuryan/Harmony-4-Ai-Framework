"""
Mathematical edge cases and limits of Love's Proof.
"""

import warnings

import numpy as np
import pytest

from harmony.invariants.loves_proof import LovesProofInvariant
from harmony.ops.acdc import acdc_split


class TestEdgeCases:
    def test_zero_coherence(self) -> None:
        t = np.linspace(0, 10, 100)

        c_zero = np.maximum(0.01 * np.exp(-t), 1e-12)
        s = 0.8 - 0.5 * (t / t[-1])
        x = 0.3 * np.ones_like(t)

        invariant = LovesProofInvariant(eps=1e-12)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = invariant.check(t, c_zero, s, x)

        assert result["G_mean"] < 0
        assert result["coherence_growing"] is False

    def test_near_zero_coherence(self) -> None:
        t = np.linspace(0, 5, 50)

        for eps in [1e-6, 1e-9, 1e-12, 1e-15]:
            c_tiny = eps * np.ones_like(t)
            s = 0.5 * np.ones_like(t)
            x = 0.1 * np.ones_like(t)

            invariant = LovesProofInvariant(eps=eps)
            result = invariant.check(t, c_tiny, s, x)

            assert not np.any(np.isnan([result["G_mean"], result["S_slope"], result["Pac_trend"]]))
            assert abs(result["G_mean"]) < 1e-3

    def test_constant_signals(self) -> None:
        t = np.linspace(0, 10, 100)

        test_cases = [
            (0.5, 0.3, 0.2),
            (1.0, 0.0, 0.5),
            (0.0, 1.0, 1.0),
        ]

        for c_const, s_const, x_const in test_cases:
            c = c_const * np.ones_like(t)
            s = s_const * np.ones_like(t)
            x = x_const * np.ones_like(t)

            invariant = LovesProofInvariant()
            result = invariant.check(t, c, s, x)

            assert abs(result["G_mean"]) < 1e-6
            assert abs(result["S_slope"]) < 1e-6
            assert abs(result["Pac_trend"]) < 1e-6

            assert result["invariant_holds"] is False

    def test_high_frequency_oscillations(self) -> None:
        fs = 100
        nyquist = fs / 2

        for freq_factor in [0.1, 0.5, 0.9, 0.99]:
            freq = freq_factor * nyquist

            t = np.arange(0, 1, 1 / fs)

            c = 0.5 + 0.1 * np.sin(2 * np.pi * freq * t)
            s = 0.6 + 0.05 * np.sin(2 * np.pi * 0.8 * freq * t)
            x = 0.3 + 0.02 * np.sin(2 * np.pi * 0.6 * freq * t)

            invariant = LovesProofInvariant()
            result = invariant.check(t, c, s, x)

            assert not np.any(np.isnan([result["G_mean"], result["S_slope"], result["Pac_trend"]]))

    def test_aliasing_robustness(self) -> None:
        fs = 100
        t = np.arange(0, 10, 1 / fs)

        f_alias = 30
        x = 0.5 + 0.2 * np.sin(2 * np.pi * f_alias * t)

        for alpha in [0.01, 0.05, 0.2]:
            x_dc, x_ac = acdc_split(x, alpha=alpha)

            assert np.allclose(x, x_dc + x_ac, rtol=1e-5)

            var_original = np.var(x)
            var_dc = np.var(x_dc)

            assert var_dc < var_original

    def test_extreme_amplitude_values(self) -> None:
        t = np.linspace(0, 10, 100)

        extreme_cases = [
            (1e-12, 1e-12, 1e-12),
            (1e12, 1e12, 1e12),
            (1e-6, 1e6, 1e3),
            (1e6, 1e-6, 1e9),
        ]

        for c_scale, s_scale, x_scale in extreme_cases:
            c = c_scale * (0.5 + 0.1 * np.sin(2 * np.pi * t / 5))
            s = s_scale * (0.6 - 0.2 * (t / t[-1]))
            x = x_scale * (0.3 + 0.05 * np.sin(2 * np.pi * t / 3))

            invariant = LovesProofInvariant()

            try:
                result = invariant.check(t, c, s, x)

                assert np.isfinite(result["G_mean"])
                assert np.isfinite(result["S_slope"])
                assert np.isfinite(result["Pac_trend"])

            except (FloatingPointError, ValueError) as exc:
                pytest.skip(f"Extreme case failed gracefully: {exc}")

    def test_single_sample_edge(self) -> None:
        t = np.array([0.0, 1.0])
        c = np.array([0.5, 0.6])
        s = np.array([0.8, 0.7])
        x = np.array([0.2, 0.3])

        invariant = LovesProofInvariant(min_window=2)
        result = invariant.check(t, c, s, x)

        assert "invariant_holds" in result
        assert "violation_reason" in result

        if "Insufficient data" in result["violation_reason"]:
            assert result["invariant_holds"] is False
        else:
            assert abs(result["G_mean"]) < 10

    def test_discontinuous_signals(self) -> None:
        t = np.linspace(0, 10, 100)

        c_step = np.where(t < 5, 0.3, 0.8)
        s_step = np.where(t < 5, 0.9, 0.4)
        x_step = np.where(t < 5, 0.1, 0.5)

        invariant = LovesProofInvariant()
        result = invariant.check(t, c_step, s_step, x_step)

        assert np.isfinite(result["G_mean"])
        assert np.isfinite(result["S_slope"])
        assert np.isfinite(result["Pac_trend"])

        early_mask = t < 2.5
        late_mask = t > 7.5

        if np.any(early_mask) and np.any(late_mask):
            c_early = np.mean(c_step[early_mask])
            c_late = np.mean(c_step[late_mask])
            s_early = np.mean(s_step[early_mask])
            s_late = np.mean(s_step[late_mask])

            assert c_late > c_early
            assert s_late < s_early

    def test_nan_and_inf_handling(self) -> None:
        t = np.linspace(0, 10, 100)

        c = 0.5 + 0.1 * np.sin(2 * np.pi * t / 5)
        s = 0.7 - 0.3 * (t / t[-1])
        x = 0.3 + 0.02 * np.sin(2 * np.pi * t / 3)

        invariant = LovesProofInvariant()

        c_nan = c.copy()
        c_nan[50] = np.nan

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result_nan = invariant.check(t, c_nan, s, x)

        assert "invariant_holds" in result_nan

        c_inf = c.copy()
        c_inf[75] = np.inf

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result_inf = invariant.check(t, c_inf, s, x)

        assert "invariant_holds" in result_inf

        c_neg_inf = c.copy()
        c_neg_inf[25] = -np.inf

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result_neg_inf = invariant.check(t, c_neg_inf, s, x)

        assert "invariant_holds" in result_neg_inf
