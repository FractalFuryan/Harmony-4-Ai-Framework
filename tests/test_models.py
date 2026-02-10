import numpy as np

from harmony.models.observer import Observer
from harmony.models.phase import PhaseLockDetector, PhaseModel
from harmony.models.role_dynamics import RoleLockDetector, RoleState


def test_observer_consent_and_projection() -> None:
    np.random.seed(42)
    observer = Observer("alice", state_dim=4)

    assert observer.get_boundary_integrity() == 1.0
    assert observer.get_coherence() > 0.7

    projection = observer.witness_projection("bob", projection_dim=3)
    assert projection is None

    observer.grant_observation_consent("bob")
    projection = observer.witness_projection("bob", projection_dim=10)
    assert projection is not None
    assert projection.shape == (4,)

    observer.revoke_observation_consent("bob")
    projection = observer.witness_projection("bob", projection_dim=2)
    assert projection is None


def test_observer_state_updates_and_boundary() -> None:
    observer = Observer("alice", state_dim=3)

    assert observer.update_internal_state(np.ones(3), consent=False) is False
    assert observer.update_internal_state(np.ones(4), consent=True) is False
    assert observer.update_internal_state(np.ones(3), consent=True) is True

    other = Observer("bob", state_dim=3)
    observer.grant_observation_consent("bob")
    boundary = observer.compute_boundary_integrity([other, Observer("c", 3)])
    assert boundary == 0.75


def test_phase_model_and_lock_detector() -> None:
    model = PhaseModel(natural_frequency=1.0, initial_phase=0.0)
    phase = model.evolve(dt=1.0)
    assert 0.0 <= phase < 2 * np.pi

    model.set_coupling(coupling_strength=0.5, coupled_phase=np.pi / 2)
    phase_coupled = model.evolve(dt=0.1)
    assert 0.0 <= phase_coupled < 2 * np.pi

    model.remove_coupling()
    phase_uncoupled = model.evolve(dt=0.1)
    assert 0.0 <= phase_uncoupled < 2 * np.pi

    detector = PhaseLockDetector(lock_threshold=0.2, window_size=3)
    phases = [(0.0, 0.1), (0.05, 0.1), (0.1, 0.1)]
    results = [detector.check_lock(p1, p2) for p1, p2 in phases]
    assert results[-1] is True
    assert len(detector.get_phase_difference_history()) == 3


def test_role_state_and_lock_detector() -> None:
    role = RoleState(state_dim=3, min_boundary_integrity=0.8)

    success, elasticity = role.apply_influence(np.ones(3), consent=False)
    assert success is False
    assert elasticity == 0.0

    success, elasticity = role.apply_influence(np.ones(3) * 10, consent=True)
    assert success is False

    success, elasticity = role.apply_influence(np.ones(3) * 0.1, consent=True)
    assert success is True
    assert elasticity == 1.0
    assert role.get_boundary_integrity() >= 0.8

    role.set_baseline()
    assert role.get_boundary_integrity() == 1.0

    lock = RoleLockDetector(lock_threshold=1e-3, window_size=3)
    changes = [np.zeros(3), np.zeros(3), np.zeros(3)]
    locked = [lock.record_change(change) for change in changes]
    assert locked[-1] is True
    assert lock.is_locked() is True
