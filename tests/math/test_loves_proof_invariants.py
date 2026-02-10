"""
Mathematical invariants of Love's Proof.
Tests the core inequality: G > 0, S down, Pac <= 0.
"""

import numpy as np

from harmony.invariants.loves_proof import LovesProofInvariant


class TestLovesProofMathematical:
    def test_growth_rate_definition(self) -> None:
        t = np.linspace(0, 10, 1000)
        C_exp = 0.1 * np.exp(0.3 * t)

        invariant = LovesProofInvariant(eps=1e-12, require_dc_trend=False)
        result = invariant.check(t, C_exp, np.zeros_like(t), np.zeros_like(t))

        assert abs(result["G_mean"] - 0.3) < 0.01, (
            f"Exponential growth G incorrect: {result['G_mean']} vs 0.3"
        )

        t_long = np.linspace(0, 50, 2000)
        K = 1.0
        r = 0.5
        C0 = 0.01
        C_logistic = K / (1 + ((K - C0) / C0) * np.exp(-r * t_long))

        result = invariant.check(
            t_long, C_logistic, np.zeros_like(t_long), np.zeros_like(t_long)
        )

        early_G = np.gradient(
            np.log(C_logistic[:100] + 1e-12), t_long[:100]
        ).mean()
        assert abs(early_G - r) < 0.1, f"Logistic early G incorrect: {early_G} vs {r}"

        late_G = np.gradient(
            np.log(C_logistic[-100:] + 1e-12), t_long[-100:]
        ).mean()
        assert abs(late_G) < 0.1, f"Logistic late G near 0: {late_G}"

    def test_inequality_symmetry(self) -> None:
        t = np.linspace(0, 10, 100)

        C_base = 0.2 + 0.6 * (1 - np.exp(-t / 3))
        S = 0.8 - 0.5 * (t / t[-1])
        x = 0.1 * np.ones_like(t)

        invariant = LovesProofInvariant(require_dc_trend=False)
        base_result = invariant.check(t, C_base, S, x)

        for scale in [0.5, 2.0, 10.0]:
            C_scaled = scale * C_base
            scaled_result = invariant.check(t, C_scaled, S, x)

            G_error = abs(scaled_result["G_mean"] - base_result["G_mean"])
            assert G_error < 1e-3, (
                f"G not invariant to scaling by {scale}: "
                f"{scaled_result['G_mean']} vs {base_result['G_mean']}"
            )

            assert scaled_result["invariant_holds"] == base_result["invariant_holds"], (
                f"Invariant result changed with scaling by {scale}"
            )

    def test_stress_monotonicity_requirement(self) -> None:
        t = np.linspace(0, 10, 100)

        C = 0.1 + 0.7 * (1 - np.exp(-t / 2))
        S = 0.2 + 0.6 * (t / t[-1])
        x = 0.3 + 0.01 * np.sin(2 * np.pi * t / 5)

        invariant = LovesProofInvariant(require_dc_trend=False)
        result = invariant.check(t, C, S, x)

        assert result["invariant_holds"] is False
        assert result["stress_decreasing"] is False
        assert "stress not decreasing" in result["violation_reason"]

    def test_ac_power_inequality(self) -> None:
        t = np.linspace(0, 10, 100)
        C = 0.3 + 0.5 * (1 - np.exp(-t / 3))
        S = 0.9 - 0.7 * (t / t[-1])
        x_stable = 0.2 + 0.05 * np.sin(2 * np.pi * t / 4)

        invariant = LovesProofInvariant(require_dc_trend=False)
        result_stable = invariant.check(t, C, S, x_stable)

        assert abs(result_stable["Pac_trend"]) < 0.01, (
            f"Stable AC Pac_trend not near 0: {result_stable['Pac_trend']}"
        )

        C_growing = 0.1 + 0.8 * (1 - np.exp(-t / 2))
        amp = 0.01 + 0.1 * (t / t[-1])
        x_increasing = 0.2 + amp * np.sin(2 * np.pi * t / 4)

        result_increasing = invariant.check(t, C_growing, S, x_increasing)

        assert result_increasing["pac_not_increasing"] is False
        assert result_increasing["Pac_trend"] > 0

    def test_necessary_and_sufficient_conditions(self) -> None:
        t = np.linspace(0, 10, 100)

        C_good = 0.2 + 0.6 * (1 - np.exp(-t / 3))
        S_good = 0.8 - 0.5 * (t / t[-1])
        amp_good = 0.02 * (1 - 0.5 * (t / t[-1]))
        x_good = 0.3 + amp_good * np.sin(2 * np.pi * t / 5)

        invariant = LovesProofInvariant(require_dc_trend=False)
        base_result = invariant.check(t, C_good, S_good, x_good)
        assert base_result["invariant_holds"] is True

        C_flat = 0.5 * np.ones_like(t)
        result1 = invariant.check(t, C_flat, S_good, x_good)
        assert result1["invariant_holds"] is False
        assert result1["coherence_growing"] is False

        S_bad = 0.2 + 0.6 * (t / t[-1])
        result2 = invariant.check(t, C_good, S_bad, x_good)
        assert result2["invariant_holds"] is False
        assert result2["stress_decreasing"] is False

        amp = 0.01 + 0.08 * (t / t[-1])
        x_bad = 0.3 + amp * np.sin(2 * np.pi * t / 5)
        result3 = invariant.check(t, C_good, S_good, x_bad)
        assert result3["invariant_holds"] is False
        assert result3["pac_not_increasing"] is False

    def test_time_translation_invariance(self) -> None:
        t = np.linspace(0, 20, 200)

        def make_series(t_series: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
            t_rel = t_series - t_series[0]
            C_series = 0.1 + 0.7 * (1 - np.exp(-t_rel / 4))
            S_series = 0.8 - 0.6 * (t_rel / t_rel[-1])
            amp_series = 0.03 * (1 - 0.2 * (t_rel / t_rel[-1]))
            x_series = 0.2 + amp_series * np.sin(2 * np.pi * t_rel / 6)
            return C_series, S_series, x_series

        C, S, x = make_series(t)

        invariant = LovesProofInvariant(require_dc_trend=False)
        result_original = invariant.check(t, C, S, x)

        for shift in [0, 5, -3]:
            t_shifted = t + shift
            C_shifted, S_shifted, x_shifted = make_series(t_shifted)

            result_shifted = invariant.check(t_shifted, C_shifted, S_shifted, x_shifted)

            assert result_original["invariant_holds"] == result_shifted["invariant_holds"]

            G_error = abs(result_original["G_mean"] - result_shifted["G_mean"])
            S_error = abs(result_original["S_slope"] - result_shifted["S_slope"])

            assert G_error < 0.01, f"G changed with time shift {shift}: {G_error}"
            assert S_error < 0.01, f"S slope changed with time shift {shift}: {S_error}"

    def test_continuity_properties(self) -> None:
        np.random.seed(42)
        t = np.linspace(0, 10, 100)

        C_base = 0.2 + 0.6 * (1 - np.exp(-t / 3))
        S_base = 0.8 - 0.5 * (t / t[-1])
        x_base = 0.3 + 0.02 * np.sin(2 * np.pi * t / 5)

        invariant = LovesProofInvariant(require_dc_trend=False)
        base_result = invariant.check(t, C_base, S_base, x_base)

        for noise_scale in [1e-6, 1e-4, 1e-2]:
            C_noisy = C_base + noise_scale * np.random.randn(len(t))
            S_noisy = S_base + noise_scale * np.random.randn(len(t))
            x_noisy = x_base + noise_scale * np.random.randn(len(t))

            noisy_result = invariant.check(t, C_noisy, S_noisy, x_noisy)

            G_change = abs(noisy_result["G_mean"] - base_result["G_mean"])
            S_change = abs(noisy_result["S_slope"] - base_result["S_slope"])
            Pac_change = abs(noisy_result["Pac_trend"] - base_result["Pac_trend"])

            assert G_change < 10 * noise_scale, (
                f"G too sensitive to noise {noise_scale}: change={G_change}"
            )
            assert S_change < 10 * noise_scale, (
                f"S slope too sensitive to noise {noise_scale}: change={S_change}"
            )
            assert Pac_change < 100 * noise_scale, (
                f"Pac trend too sensitive to noise {noise_scale}: change={Pac_change}"
            )

    def test_window_size_independence(self) -> None:
        t = np.linspace(0, 100, 1000)

        C = 0.1 + 0.7 * (1 - np.exp(-t / 30)) + 0.1 * np.sin(2 * np.pi * t / 20)
        S = 0.8 - 0.6 * (t / t[-1]) + 0.05 * np.sin(2 * np.pi * t / 15)
        x = 0.3 + 0.05 * np.sin(2 * np.pi * t / 10)

        window_sizes = [30, 50, 100, 200]
        results = []

        for k in window_sizes:
            invariant = LovesProofInvariant(min_window=k, require_dc_trend=False)
            result = invariant.check(t, C, S, x)
            results.append((k, result))

        G_values = [r["G_mean"] for _, r in results]
        S_slopes = [r["S_slope"] for _, r in results]

        G_std = np.std(G_values)
        assert G_std < 0.1, f"G varies too much with window size: std={G_std}"

        S_std = np.std(S_slopes)
        assert S_std < 0.05, f"S slope varies too much with window size: std={S_std}"

        invariant_results = [r["invariant_holds"] for _, r in results]
        unique_results = set(invariant_results)
        assert len(unique_results) <= 2, (
            f"Inconsistent results across window sizes: {invariant_results}"
        )
