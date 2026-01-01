"""
Public API for HarmonyØ4.

This module provides the explicitly safe surface for external use.
All exported functions preserve ethical invariants.
"""

from harmony.core.coherence import PhaseCoherence, CoherenceMetrics
from harmony.core.consent import ConsentManager, ConsentState
from harmony.core.invariants import EthicalInvariants
from harmony.models.observer import Observer
from harmony.models.phase import PhaseModel
from harmony.models.role_dynamics import RoleState
from harmony.safeguards.boundary import BoundaryGuard, BoundaryEnforcer
from harmony.safeguards.witness import WitnessProjection, WitnessRegistry
from harmony.safeguards.drift_detection import (
    PhaseDriftDetector,
    BoundaryDriftDetector,
    RoleDriftDetector,
)


__all__ = [
    # Core
    "PhaseCoherence",
    "CoherenceMetrics",
    "ConsentManager",
    "ConsentState",
    "EthicalInvariants",
    # Models
    "Observer",
    "PhaseModel",
    "RoleState",
    # Safeguards
    "BoundaryGuard",
    "BoundaryEnforcer",
    "WitnessProjection",
    "WitnessRegistry",
    "PhaseDriftDetector",
    "BoundaryDriftDetector",
    "RoleDriftDetector",
]


def create_observer(
    observer_id: str,
    state_dim: int,
    enable_consent_tracking: bool = True,
) -> tuple[Observer, ConsentManager]:
    """
    Factory function to create observer with consent management.
    
    Args:
        observer_id: Unique identifier for observer
        state_dim: Dimensionality of observer state
        enable_consent_tracking: Whether to create consent manager
    
    Returns:
        Tuple of (Observer, ConsentManager)
    
    Example:
        ```python
        observer, consent_mgr = create_observer("obs1", state_dim=10)
        observer.grant_observation_consent("obs2")
        ```
    """
    observer = Observer(observer_id=observer_id, state_dim=state_dim)
    consent_mgr = ConsentManager() if enable_consent_tracking else None
    return observer, consent_mgr


def create_phase_system(
    natural_frequency: float,
    initial_phase: float = 0.0,
    enable_drift_detection: bool = True,
    drift_threshold: float = 0.1,
) -> tuple[PhaseModel, PhaseDriftDetector]:
    """
    Factory function to create phase system with drift detection.
    
    Args:
        natural_frequency: Natural oscillation frequency
        initial_phase: Starting phase angle
        enable_drift_detection: Whether to enable drift detection
        drift_threshold: Threshold for drift alerts
    
    Returns:
        Tuple of (PhaseModel, PhaseDriftDetector)
    
    Example:
        ```python
        phase, drift_detector = create_phase_system(natural_frequency=1.0)
        phase.evolve(dt=0.1)
        detected, magnitude = drift_detector.check_drift(coherence)
        ```
    """
    phase_model = PhaseModel(
        natural_frequency=natural_frequency,
        initial_phase=initial_phase,
    )
    
    drift_detector = (
        PhaseDriftDetector(threshold=drift_threshold)
        if enable_drift_detection
        else None
    )
    
    return phase_model, drift_detector


def create_guarded_role(
    state_dim: int,
    min_boundary: float = 0.8,
    enable_boundary_guard: bool = True,
) -> tuple[RoleState, BoundaryGuard]:
    """
    Factory function to create role with boundary protection.
    
    Args:
        state_dim: Dimensionality of role state
        min_boundary: Minimum boundary integrity threshold
        enable_boundary_guard: Whether to enable boundary monitoring
    
    Returns:
        Tuple of (RoleState, BoundaryGuard)
    
    Example:
        ```python
        role, guard = create_guarded_role(state_dim=5)
        success, elasticity = role.apply_influence(influence, consent=True)
        is_valid, alert = guard.check_boundary(role.get_boundary_integrity())
        ```
    """
    role_state = RoleState(
        state_dim=state_dim,
        min_boundary_integrity=min_boundary,
    )
    
    boundary_guard = (
        BoundaryGuard(min_integrity=min_boundary)
        if enable_boundary_guard
        else None
    )
    
    return role_state, boundary_guard


def enforce_invariants_check(
    consent_mgr: ConsentManager,
    observer: Observer,
    invariants: EthicalInvariants,
    entity_from: str,
    entity_to: str,
    action: str,
) -> bool:
    """
    Convenience function to check consent and enforce invariants.
    
    Args:
        consent_mgr: ConsentManager instance
        observer: Observer instance
        invariants: EthicalInvariants instance
        entity_from: Entity granting consent
        entity_to: Entity receiving consent
        action: Action requiring consent
    
    Returns:
        True if consent granted and all invariants hold
    
    Example:
        ```python
        if enforce_invariants_check(consent, obs, inv, "a", "b", "share"):
            # Proceed with action
            pass
        ```
    """
    # Check consent
    consent_granted = consent_mgr.check_consent(entity_from, entity_to, action)
    
    # Check boundary invariant
    boundary_ok = invariants.check_observer_boundary_integrity(observer)
    
    return consent_granted and boundary_ok
