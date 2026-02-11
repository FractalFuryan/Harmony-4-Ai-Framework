"""Integration tests for the generalized ethical invariants."""

import unittest

import numpy as np

from harmony.invariants.consent_locking import ConsentLockingInvariant
from harmony.invariants.growth_bounds import GrowthBoundsInvariant
from harmony.invariants.non_coercion import NonCoercionInvariant


class TestInvariantsIntegration(unittest.TestCase):
    def test_non_coercion_alignment(self) -> None:
        invariant = NonCoercionInvariant()

        coherence = np.linspace(0.3, 0.8, 100)
        stress = np.linspace(0.8, 0.3, 100)
        result = invariant.check(coherence, stress)
        self.assertTrue(result["invariant_holds"])

        coherence = np.linspace(0.3, 0.8, 100)
        stress = np.linspace(0.3, 0.8, 100)
        result = invariant.check(coherence, stress)
        self.assertFalse(result["invariant_holds"])
        self.assertIn("stress not decreasing", result["violation_reason"])

        coherence = np.ones(100) * 0.5
        stress = np.linspace(0.8, 0.3, 100)
        result = invariant.check(coherence, stress)
        self.assertFalse(result["invariant_holds"])
        self.assertIn("coherence not growing", result["violation_reason"])

    def test_consent_locking_generalization(self) -> None:
        invariant = ConsentLockingInvariant()

        result = invariant.check_consent(coupling_strength=2.0, frequency_difference=1.0)
        self.assertTrue(result["consent_granted"])
        self.assertGreaterEqual(result["lock_strength"], 0.5)

        result = invariant.check_consent(coupling_strength=1.0, frequency_difference=2.0)
        self.assertFalse(result["consent_granted"])
        self.assertIn("frequency difference too large", result["violation_reason"])

        result = invariant.check_consent(coupling_strength=0.05, frequency_difference=0.01)
        self.assertFalse(result["consent_granted"])
        self.assertIn("coupling too weak", result["violation_reason"])

    def test_growth_bounds_prevent_explosion(self) -> None:
        invariant = GrowthBoundsInvariant()

        t = np.linspace(0, 10, 100)
        x = 0.5 / (1 + np.exp(-0.5 * (t - 5)))
        result = invariant.check_boundedness(x, t)
        self.assertTrue(result["invariant_holds"])

        t = np.linspace(0, 10, 100)
        x = np.exp(2 * t)
        result = invariant.check_boundedness(x, t)
        self.assertFalse(result["invariant_holds"])
        self.assertTrue(result["explosive_growth"])

    def test_invariant_composition(self) -> None:
        non_coercion = NonCoercionInvariant()
        consent = ConsentLockingInvariant()
        growth = GrowthBoundsInvariant()

        t = np.linspace(0, 20, 200)
        coherence = 0.3 / (1 + np.exp(-0.3 * (t - 10)))
        stress = 0.8 - 0.6 * (t / t[-1])

        nc_result = non_coercion.check(coherence, stress, t)
        gb_result = growth.check_boundedness(coherence, t)

        self.assertTrue(nc_result["invariant_holds"])
        self.assertTrue(gb_result["invariant_holds"])

        consent_result = consent.check_consent(
            coupling_strength=1.5, frequency_difference=0.8, receiver_threshold=0.2
        )
        self.assertTrue(consent_result["consent_granted"])


class TestPhysiologyImplementsInvariants(unittest.TestCase):
    def test_heart_field_respects_non_coercion(self) -> None:
        from harmony.physiology.heart import HeartFieldScorer

        scorer = HeartFieldScorer(fs=250.0)

        coherence = np.linspace(0.3, 0.8, 100)
        stress = np.linspace(0.3, 0.8, 100)

        result = scorer.compute_non_coercion_check(
            coherence_values=coherence,
            time_points=np.arange(100),
            stress_proxy=stress,
        )

        self.assertFalse(result["constraint_satisfied"])

    def test_entrainment_respects_consent_locking(self) -> None:
        from harmony.physiology.heart import EntrainmentMetrics

        entrainment = EntrainmentMetrics(fs=250.0)

        phase1 = np.cumsum(np.random.randn(1000) * 0.1)
        phase2 = np.cumsum(np.random.randn(1000) * 0.1)

        result = entrainment.revocable_entrainment(
            phase_source=phase1,
            phase_receiver=phase2,
            stress_receiver=0.3,
        )

        self.assertIn("consent_granted", result)
        self.assertIn("lock_strength", result)
        self.assertIn("consent_threshold", result)
        self.assertLessEqual(result["respectful_influence"], result["plv"])


if __name__ == "__main__":
    unittest.main()
