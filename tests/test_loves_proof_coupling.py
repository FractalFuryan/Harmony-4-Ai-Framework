"""Test coupling-specific Love's Proof adapter."""

import numpy as np

from harmony.coupling.loves_proof import CouplingLovesProof


class TestCouplingLovesProof:
    def test_healthy_entrainment(self) -> None:
        t = np.linspace(0, 60, 300)

        order_param = 0.1 + 0.7 * (1 - np.exp(-t / 20))
        mismatch = 2.0 - 1.5 * (t / t[-1])
        amp = 0.1 * (1 - 0.4 * (t / t[-1]))
        coupling = 1.5 + amp * np.sin(2 * np.pi * t / 10)

        checker = CouplingLovesProof(require_dc_trend=False)
        result = checker.check_entrainment(t, order_param, mismatch, coupling)

        assert result["invariant_holds"] is True
        assert result["coherence_growing"] is True
        assert result["stress_decreasing"] is True

    def test_coercive_entrainment(self) -> None:
        t = np.linspace(0, 60, 300)

        order_param = 0.1 + 0.7 * (1 - np.exp(-t / 15))
        mismatch = 2.0 - 1.0 * (t / t[-1])

        coupling_volatility = 0.1 + 0.3 * (t / t[-1])
        coupling = 1.0 + coupling_volatility * np.sin(2 * np.pi * t / 5)

        checker = CouplingLovesProof(require_dc_trend=False)
        result = checker.check_entrainment(t, order_param, mismatch, coupling)

        assert result["invariant_holds"] is False
        assert result["pac_not_increasing"] is False

    def test_consent_dynamics(self) -> None:
        t = np.linspace(0, 60, 300)

        phase_concentration = 0.3 + 0.4 * (1 - np.exp(-t / 25))
        receiver_resistance = 0.8 - 0.5 * (t / t[-1])
        applied_coupling = 1.2 + 0.05 * np.sin(2 * np.pi * t / 8)

        checker = CouplingLovesProof(require_dc_trend=False)
        result = checker.check_consent_dynamics(
            t, phase_concentration, receiver_resistance, applied_coupling
        )

        assert result["coherence_growing"] is True
        assert result["stress_decreasing"] is True
