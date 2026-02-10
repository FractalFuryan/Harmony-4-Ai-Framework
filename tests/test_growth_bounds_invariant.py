import numpy as np

from harmony.invariants.growth_bounds import GrowthBoundsInvariant


def test_growth_bounds_insufficient_data() -> None:
    invariant = GrowthBoundsInvariant()
    result = invariant.check_boundedness(np.array([0.1]), np.array([0.0]))
    assert result["invariant_holds"] is None
    assert result["violation_reason"] == "Insufficient data"


def test_growth_bounds_detects_explosive_growth() -> None:
    invariant = GrowthBoundsInvariant()
    x = np.array([0.0, 2.0, 4.0])
    t = np.array([0.0, 1.0, 2.0])
    result = invariant.check_boundedness(x, t, max_growth_rate=1.0)
    assert result["explosive_growth"] is True
    assert result["invariant_holds"] is False


def test_growth_bounds_near_saturation() -> None:
    invariant = GrowthBoundsInvariant()
    x = invariant.simulate_bounded_growth(x0=0.05, alpha=2.0, n_steps=200, dt=0.1)
    t = np.arange(len(x)) * 0.1
    result = invariant.check_boundedness(x, t, max_growth_rate=2.0)
    assert result["invariant_holds"] is True
    assert result["near_saturation"] is True


def test_growth_bounds_gompertz_simulation() -> None:
    invariant = GrowthBoundsInvariant()
    x = invariant.simulate_bounded_growth(
        x0=0.2, alpha=1.0, n_steps=50, dt=0.1, growth_type="gompertz"
    )
    assert np.all(x >= 0.0)
    assert np.all(x <= 1.0)
