import numpy as np

from harmony.safeguards.boundary import BoundaryEnforcer, BoundaryGuard
from harmony.safeguards.drift_detection import (
    BoundaryDriftDetector,
    DriftDetector,
    DriftEvent,
    PhaseDriftDetector,
    RoleDriftDetector,
)
from harmony.safeguards.witness import WitnessProjection, WitnessRegistry


def test_boundary_guard_and_enforcer() -> None:
    guard = BoundaryGuard(min_integrity=0.8, alert_threshold=0.85)

    valid, message = guard.check_boundary(0.9)
    assert valid is True
    assert message is None

    valid, message = guard.check_boundary(0.84, previous_integrity=0.9, consent_for_change=True)
    assert valid is True
    assert message is not None and "WARNING" in message

    valid, message = guard.check_boundary(0.7, previous_integrity=0.8, consent_for_change=False)
    assert valid is False
    assert message is not None and "CRITICAL" in message

    trend = guard.get_boundary_trend(window=3)
    assert trend in {"stable", "improving", "degrading", "insufficient_data"}

    guard.clear_violations()
    assert guard.get_violations() == []

    enforcer = BoundaryEnforcer(min_boundary=0.8)
    can_share, reason = enforcer.can_share_state(0.75, num_current_shares=0)
    assert can_share is False
    assert "below minimum" in reason

    can_share, reason = enforcer.can_share_state(0.9, num_current_shares=5, max_shares=5)
    assert can_share is False
    assert "Maximum shares" in reason

    can_share, reason = enforcer.can_share_state(0.81, num_current_shares=4, max_shares=5)
    assert can_share is False

    can_share, reason = enforcer.can_share_state(0.9, num_current_shares=1, max_shares=5)
    assert can_share is True

    can_couple, reason = enforcer.can_accept_coupling(0.75, coupling_strength=0.2)
    assert can_couple is False

    can_couple, reason = enforcer.can_accept_coupling(0.9, coupling_strength=0.8, max_coupling=0.5)
    assert can_couple is False

    can_couple, reason = enforcer.can_accept_coupling(0.9, coupling_strength=0.4, max_coupling=0.5)
    assert can_couple is False
    assert "Coupling would violate" in reason


def test_witness_projection_and_registry() -> None:
    projection = WitnessProjection(source_dim=4, target_dim=2, seed=1)
    state = np.ones(4)

    assert projection.project(state, consent=False) is None
    projected = projection.project(state, consent=True)
    assert projected is not None
    assert projected.shape == (2,)

    assert projection.is_invertible() is False
    assert projection.information_loss() == 0.5

    registry = WitnessRegistry()
    registry.register_projection("alice", "bob", projection, consent=False)

    assert registry.witness("alice", "bob", state) is None
    assert registry.grant_witness_consent("alice", "bob") is True

    witnessed = registry.witness("alice", "bob", state)
    assert witnessed is not None

    assert registry.get_consented_witnesses("alice") == ["bob"]
    assert registry.revoke_witness_consent("alice", "bob") is True


def test_drift_detectors() -> None:
    detector = DriftDetector(threshold=0.1)
    event = DriftEvent(
        timestamp=__import__("datetime").datetime.now(),
        drift_type="phase",
        magnitude=0.2,
        threshold=0.1,
        source="unit",
    )
    detector.record_event(event)
    assert detector.get_events(drift_type="phase")
    detector.clear_events()
    assert detector.get_events() == []

    phase_detector = PhaseDriftDetector(threshold=0.05, window_size=3)
    phase_detector.set_baseline(0.9)
    drifted, magnitude = phase_detector.check_drift(0.7, source="x")
    assert drifted is True
    assert magnitude > 0
    assert phase_detector.get_coherence_trend() in {
        "stable",
        "improving",
        "degrading",
        "insufficient_data",
    }

    boundary_detector = BoundaryDriftDetector(threshold=0.05)
    drifted, magnitude = boundary_detector.check_drift(0.8, previous_boundary=0.9, source="y")
    assert drifted is True
    assert magnitude > 0

    role_detector = RoleDriftDetector(threshold=0.2)
    baseline = np.zeros(3)
    role_detector.set_baseline(baseline)
    drifted, magnitude = role_detector.check_drift(np.ones(3), source="z")
    assert drifted is True
    assert magnitude > 0
