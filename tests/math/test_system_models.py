"""
Test Love's Proof with known mathematical systems.
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import hilbert

from harmony.invariants.loves_proof import LovesProofInvariant


class TestMathematicalSystems:
    def test_harmonic_oscillator(self) -> None:
        m = 1.0
        k = 100.0
        c = 2.0

        w0 = np.sqrt(k / m)
        zeta = c / (2 * np.sqrt(m * k))
        w = w0 * np.sqrt(1 - zeta**2)

        A = 1.0
        phi = 0.0

        t = np.linspace(0, 10, 1000)

        x = A * np.exp(-zeta * w0 * t) * np.cos(w * t + phi)
        v = -A * w0 * np.exp(-zeta * w0 * t) * (
            zeta * np.cos(w * t + phi) - np.sqrt(1 - zeta**2) * np.sin(w * t + phi)
        )

        analytic_signal = x + 1j * np.gradient(x, t) / w
        C = np.abs(analytic_signal) / A

        S = c * v**2
        S_normalized = S / np.max(S)

        influence = np.zeros_like(t)

        invariant = LovesProofInvariant()
        result = invariant.check(t, C, S_normalized, influence)

        assert result["coherence_growing"] is False
        assert result["G_mean"] < 0

    def test_van_der_pol_oscillator(self) -> None:
        mu = 0.5
        t_span = (0, 50)
        t_eval = np.linspace(*t_span, 2000)

        def vdp_ode(_, y):
            x, v = y
            return [v, mu * (1 - x**2) * v - x]

        y0 = [2.0, 0.0]

        sol = solve_ivp(vdp_ode, t_span, y0, t_eval=t_eval, rtol=1e-8, atol=1e-10)

        t = sol.t
        x = sol.y[0]
        v = sol.y[1]

        steady_idx = len(t) // 5
        t = t[steady_idx:]
        x = x[steady_idx:]
        v = v[steady_idx:]

        analytic = hilbert(x)
        amplitude = np.abs(analytic)
        phase = np.angle(analytic)

        phase_diff = np.diff(phase)
        phase_diff = np.unwrap(phase_diff)

        window = 100
        C = np.zeros(len(t) - window)
        for i in range(len(C)):
            window_phases = phase_diff[i : i + window]
            C[i] = np.abs(np.mean(np.exp(1j * window_phases)))

        t_C = t[window:]

        amplitude_mean = np.mean(amplitude)
        S = (amplitude - amplitude_mean) ** 2
        S = S / np.max(S)

        influence = mu * (1 - x**2) * v

        min_len = min(len(t_C), len(S), len(influence))
        t_align = t_C[:min_len]
        C_align = C[:min_len]
        S_align = S[:min_len]
        influence_align = influence[:min_len]

        invariant = LovesProofInvariant()
        result = invariant.check(t_align, C_align, S_align, influence_align)

        assert C_align.mean() > 0.8
        assert abs(result["G_mean"]) < 0.1

    def test_lotka_volterra_predator_prey(self) -> None:
        alpha = 1.1
        beta = 0.4
        delta = 0.1
        gamma = 0.4

        t_span = (0, 100)
        t_eval = np.linspace(*t_span, 2000)

        def lotka_volterra(_, z):
            x, y = z
            return [alpha * x - beta * x * y, delta * x * y - gamma * y]

        z0 = [10.0, 2.0]

        sol = solve_ivp(lotka_volterra, t_span, z0, t_eval=t_eval, rtol=1e-8)

        t = sol.t
        prey = sol.y[0]
        predator = sol.y[1]

        steady_idx = len(t) // 4
        t = t[steady_idx:]
        prey = prey[steady_idx:]
        predator = predator[steady_idx:]

        analytic_prey = hilbert(prey - np.mean(prey))
        analytic_pred = hilbert(predator - np.mean(predator))

        phase_prey = np.angle(analytic_prey)
        phase_pred = np.angle(analytic_pred)

        phase_diff = np.unwrap(phase_prey - phase_pred)

        window = 100
        C = np.zeros(len(t) - window)
        for i in range(len(C)):
            window_diff = phase_diff[i : i + window]
            C[i] = np.abs(np.mean(np.exp(1j * window_diff)))

        t_C = t[window:]

        total_pop = prey + predator
        S = np.abs(np.gradient(total_pop, t))
        S = S / np.max(S)
        S = S[window:]

        influence = beta * prey * predator
        influence = influence[window:]

        invariant = LovesProofInvariant()
        result = invariant.check(t_C, C, S, influence)

        assert C.mean() > 0.7

    def test_kuramoto_phase_oscillators(self) -> None:
        np.random.seed(42)

        N = 20
        K = 2.0

        omega = np.random.normal(0, 1, N)

        dt = 0.01
        t_max = 50
        steps = int(t_max / dt)

        theta = np.random.uniform(0, 2 * np.pi, N)

        t = np.zeros(steps)
        order_param = np.zeros(steps)
        z_series = np.zeros(steps, dtype=complex)

        for step in range(steps):
            t[step] = step * dt

            z = np.mean(np.exp(1j * theta))
            z_series[step] = z
            order_param[step] = np.abs(z)

            for i in range(N):
                coupling = 0.0
                for j in range(N):
                    if i != j:
                        coupling += np.sin(theta[j] - theta[i])

                dtheta = omega[i] + (K / N) * coupling
                theta[i] += dtheta * dt
                theta[i] %= 2 * np.pi

        transient = steps // 5
        t = t[transient:]
        order_param = order_param[transient:]
        z_series = z_series[transient:]

        C = order_param

        phase = np.unwrap(np.angle(z_series))
        freq_est = np.gradient(phase, t)
        S = np.abs(freq_est - np.mean(freq_est))
        S = S / np.max(S)

        influence = np.ones_like(t) * K

        invariant = LovesProofInvariant()
        result = invariant.check(t, C, S, influence)

        assert C[-1] > C[0]
        assert result["coherence_growing"] is True

    def test_linear_system_stability(self) -> None:
        test_matrices = [
            np.array([[-0.1, -1.0], [1.0, -0.1]]),
            np.array([[0.1, -1.0], [1.0, 0.1]]),
            np.array([[0.5, 0.0], [0.0, -0.5]]),
            np.array([[0.0, -1.0], [1.0, 0.0]]),
        ]

        for A in test_matrices:
            eigvals = np.linalg.eigvals(A)
            real_parts = eigvals.real

            t_span = (0, 20)
            t_eval = np.linspace(*t_span, 1000)

            def linear_system(_, x):
                return A @ x

            x0 = [1.0, 0.0]

            sol = solve_ivp(linear_system, t_span, x0, t_eval=t_eval, rtol=1e-8)

            t = sol.t
            x1 = sol.y[0]
            x2 = sol.y[1]

            steady_idx = len(t) // 10
            t = t[steady_idx:]
            x1 = x1[steady_idx:]
            x2 = x2[steady_idx:]

            magnitude = np.sqrt(x1**2 + x2**2)
            C = magnitude / np.max(magnitude)

            dMdt = np.gradient(magnitude, t)
            S = np.abs(dMdt)
            S = S / np.max(S)

            influence = np.linalg.norm(A) * np.ones_like(t)

            invariant = LovesProofInvariant()
            result = invariant.check(t, C, S, influence)

            max_real = np.max(real_parts)

            if max_real < 0:
                assert result["G_mean"] < 0
            elif max_real > 0:
                assert result["stress_decreasing"] is False or result["G_mean"] <= 0
            else:
                assert abs(result["G_mean"]) < 0.1
