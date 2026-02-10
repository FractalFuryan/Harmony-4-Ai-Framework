from harmony.invariants.consent_locking import ConsentLockingInvariant


def test_consent_granted() -> None:
    invariant = ConsentLockingInvariant(default_threshold=0.1)
    result = invariant.check_consent(coupling_strength=0.5, frequency_difference=0.1)
    assert result["consent_granted"] is True
    assert result["lock_strength"] > 0
    assert result["violation_reason"] is None


def test_consent_denied_frequency() -> None:
    invariant = ConsentLockingInvariant(default_threshold=0.1)
    result = invariant.check_consent(coupling_strength=0.2, frequency_difference=0.4)
    assert result["consent_granted"] is False
    assert "frequency difference" in result["violation_reason"]


def test_consent_denied_weak_coupling() -> None:
    invariant = ConsentLockingInvariant(default_threshold=0.1)
    result = invariant.check_consent(coupling_strength=0.05, frequency_difference=0.01)
    assert result["consent_granted"] is False
    assert "coupling too weak" in result["violation_reason"]


def test_dynamic_threshold() -> None:
    invariant = ConsentLockingInvariant(default_threshold=0.1)
    adjusted = invariant.dynamic_threshold(stress_level=1.0)
    assert adjusted > 0.1
    assert adjusted <= 0.3

    adjusted_custom = invariant.dynamic_threshold(
        stress_level=2.0, baseline_threshold=0.2, sensitivity=0.25
    )
    assert adjusted_custom <= 0.6
