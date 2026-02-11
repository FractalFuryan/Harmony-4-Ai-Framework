"""
Mathematical properties of AC/DC decomposition.
Pure mathematical tests, no domain-specific assumptions.
"""

import numpy as np
from scipy import fft

from harmony.ops.acdc import ac_power, acdc_split, dc_slope, ema_lpf


class TestACDCDecomposition:
    def test_decomposition_linearity(self) -> None:
        np.random.seed(42)

        x = np.random.randn(1000)
        y = np.random.randn(1000)
        a = 2.5
        b = -1.3

        x_dc, x_ac = acdc_split(x, alpha=0.05)
        y_dc, y_ac = acdc_split(y, alpha=0.05)
        xy = a * x + b * y
        xy_dc, xy_ac = acdc_split(xy, alpha=0.05)

        linear_combination_dc = a * x_dc + b * y_dc
        dc_error = np.max(np.abs(xy_dc - linear_combination_dc))
        assert dc_error < 1e-10, f"DC linearity violated: max error = {dc_error}"

        linear_combination_ac = a * x_ac + b * y_ac
        ac_error = np.max(np.abs(xy_ac - linear_combination_ac))
        assert ac_error < 1e-10, f"AC linearity violated: max error = {ac_error}"

    def test_dc_low_pass_property(self) -> None:
        fs = 1000
        t = np.arange(0, 1, 1 / fs)

        x = (
            np.sin(2 * np.pi * 2 * t)
            + 0.5 * np.sin(2 * np.pi * 10 * t)
            + 0.2 * np.sin(2 * np.pi * 50 * t)
        )

        x_dc, _ = acdc_split(x, alpha=0.01)

        def power_spectrum(sig: np.ndarray):
            freqs = fft.rfftfreq(len(sig), 1 / fs)
            power = np.abs(fft.rfft(sig)) ** 2
            return freqs, power

        freqs_x, power_x = power_spectrum(x)
        freqs_dc, power_dc = power_spectrum(x_dc)

        high_freq_mask = freqs_x > 5

        total_power_x = np.sum(power_x)
        total_power_dc = np.sum(power_dc)

        high_freq_ratio_x = np.sum(power_x[high_freq_mask]) / total_power_x
        high_freq_ratio_dc = np.sum(power_dc[high_freq_mask]) / total_power_dc

        assert high_freq_ratio_dc < 0.5 * high_freq_ratio_x, (
            "DC has too much high frequency: "
            f"{high_freq_ratio_dc:.3f} vs {high_freq_ratio_x:.3f}"
        )

    def test_ac_zero_mean_property(self) -> None:
        np.random.seed(42)

        test_signals = [
            np.random.randn(1000),
            np.sin(2 * np.pi * 0.1 * np.arange(1000)) + 0.5 * np.random.randn(1000),
        ]

        for x in test_signals:
            _, x_ac = acdc_split(x, alpha=0.02)

            window_size = 100
            warmup = 3 * window_size
            for i in range(warmup, len(x_ac) - window_size, window_size // 2):
                window_ac = x_ac[i : i + window_size]
                window_mean = np.mean(window_ac)

                assert abs(window_mean) < 0.7 * np.std(window_ac), (
                    f"AC mean not zero in window {i}: "
                    f"mean={window_mean:.3f}, std={np.std(window_ac):.3f}"
                )

    def test_energy_conservation(self) -> None:
        np.random.seed(42)

        for _ in range(10):
            x = np.random.randn(1000)
            x_dc, x_ac = acdc_split(x, alpha=0.03)

            e_total = np.sum(x**2)
            e_dc = np.sum(x_dc**2)
            e_ac = np.sum(x_ac**2)
            e_cross = 2 * np.sum(x_dc * x_ac)

            energy_error = abs(e_total - (e_dc + e_ac + e_cross))

            assert (
                energy_error < 1e-8 * e_total
            ), f"Energy not conserved: error={energy_error}, E_total={e_total}"

            dot_product = np.abs(np.sum(x_dc * x_ac))
            assert dot_product < 0.6 * np.sqrt(
                e_dc * e_ac
            ), f"DC and AC not sufficiently orthogonal: dot={dot_product}"

    def test_ema_impulse_response(self) -> None:
        x = np.zeros(100)
        x[0] = 1.0

        for alpha in [0.01, 0.1, 0.5]:
            y = ema_lpf(x, alpha=alpha)

            for i in range(1, len(y)):
                expected = (1 - alpha) * y[i - 1] if i > 0 else alpha
                actual = y[i]
                error = abs(actual - expected)
                assert error < 1e-10, f"EMA recurrence violated at i={i}, alpha={alpha}"

            final_value = y[-1]
            theoretical_final = (1 - alpha) ** (len(x) - 1)
            error = abs(final_value - theoretical_final)

            assert error < 1e-8, f"EMA final value incorrect: {final_value} vs {theoretical_final}"

    def test_ac_power_invariance(self) -> None:
        np.random.seed(42)

        base_signal = np.random.randn(500)
        _, base_ac = acdc_split(base_signal, alpha=0.02)
        base_power = ac_power(base_ac)

        for offset in [-10.0, 0.0, 5.0, 100.0]:
            shifted_signal = base_signal + offset
            _, shifted_ac = acdc_split(shifted_signal, alpha=0.02)
            shifted_power = ac_power(shifted_ac)

            power_error = abs(shifted_power - base_power)
            assert power_error < 1e-10, (
                f"AC power not invariant to DC shift {offset}: " f"{shifted_power} vs {base_power}"
            )

    def test_dc_slope_mathematical(self) -> None:
        t = np.linspace(0, 10, 100)

        test_cases = [
            (2.0 * t + 3.0, 2.0, True),
            (-1.5 * t + 0.0, -1.5, True),
            (0.0 * t + 5.0, 0.0, True),
            (0.1 * t**2, 0.1 * 2 * t.mean(), False),
        ]

        for y, expected_slope, exact in test_cases:
            computed_slope = dc_slope(y, t)
            error = abs(computed_slope - expected_slope)

            if exact:
                assert error < 1e-10, f"DC slope incorrect: {computed_slope} vs {expected_slope}"
            else:
                assert error < 0.1, f"DC slope too inaccurate: {computed_slope} vs {expected_slope}"

        np.random.seed(42)
        noise = np.random.randn(1000)
        t_noise = np.arange(len(noise))
        noise_slope = dc_slope(noise, t_noise)

        assert abs(noise_slope) < 0.1, f"Noise slope too large: {noise_slope}"
