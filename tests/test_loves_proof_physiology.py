"""Test physiology-specific Love's Proof adapter."""

import numpy as np

from harmony.physiology.heart.loves_proof import PhysiologyLovesProof


class TestPhysiologyLovesProof:
    def test_heart_field_healthy(self) -> None:
        t = np.linspace(0, 300, 1500)

        heart_coherence = 0.3 + 0.4 * (1 - np.exp(-t / 100))
        stress_proxy = 0.8 - 0.6 * (t / t[-1])
        heart_amplitude = 1.0 + 0.1 * np.sin(2 * np.pi * t / 10)

        checker = PhysiologyLovesProof(fs=5.0)
        result = checker.check_heart_field(
            t, heart_coherence, stress_proxy, heart_amplitude=heart_amplitude
        )

        assert "invariant_holds" in result

    def test_heart_field_coercive(self) -> None:
        t = np.linspace(0, 300, 1500)

        heart_coherence = 0.2 + 0.5 * (1 - np.exp(-t / 50))
        stress_proxy = 0.3 + 0.5 * (t / t[-1])
        heart_amplitude = 1.0 + 0.3 * np.sin(2 * np.pi * t / 5)

        checker = PhysiologyLovesProof(fs=5.0)
        result = checker.check_heart_field(
            t, heart_coherence, stress_proxy, heart_amplitude=heart_amplitude
        )

        assert result["invariant_holds"] is False
        assert result["stress_decreasing"] is False

    def test_continuous_monitoring(self) -> None:
        t = np.linspace(0, 600, 3000)

        heart_coherence = 0.2 + 0.5 * np.sin(2 * np.pi * t / 200)
        stress_proxy = 0.7 - 0.4 * (t / t[-1]) + 0.1 * np.sin(2 * np.pi * t / 50)

        checker = PhysiologyLovesProof(fs=5.0)
        results = checker.check_continuous_heart_field(
            t, heart_coherence, stress_proxy, window_sec=60, step_sec=15
        )

        assert "timestamps" in results
        assert "invariant_holds" in results
        assert len(results["timestamps"]) == len(results["invariant_holds"])
