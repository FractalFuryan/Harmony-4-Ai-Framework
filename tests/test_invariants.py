"""Tests for ethical invariants."""

import pytest
import numpy as np
from harmony.core.invariants import EthicalInvariants
from harmony.models.observer import Observer


def test_consent_monotonicity():
    """Test INV-1: No state change without consent."""
    inv = EthicalInvariants()
    
    # State changed with consent—OK
    assert inv.check_consent_monotonicity(consent_granted=True, state_changed=True)
    
    # State changed without consent—VIOLATION
    assert not inv.check_consent_monotonicity(consent_granted=False, state_changed=True)
    
    # No state change without consent—OK
    assert inv.check_consent_monotonicity(consent_granted=False, state_changed=False)


def test_boundary_preservation():
    """Test INV-2: Boundary must not degrade without consent."""
    inv = EthicalInvariants()
    
    # Boundary maintained—OK
    assert inv.check_boundary_preservation(0.9, 0.9, consent_granted=False)
    
    # Boundary improved without consent—OK
    assert inv.check_boundary_preservation(0.8, 0.9, consent_granted=False)
    
    # Boundary degraded with consent—OK
    assert inv.check_boundary_preservation(0.9, 0.8, consent_granted=True)
    
    # Boundary degraded without consent—VIOLATION
    assert not inv.check_boundary_preservation(0.9, 0.8, consent_granted=False)


def test_no_hidden_optimization():
    """Test INV-3: All optimization must be declared."""
    inv = EthicalInvariants()
    
    declared = {"loss_a", "loss_b"}
    observed = {"loss_a", "loss_b"}
    
    # All observed are declared—OK
    assert inv.check_no_hidden_optimization(declared, observed)
    
    # Hidden optimization detected—VIOLATION
    observed_with_hidden = {"loss_a", "loss_b", "hidden_loss"}
    assert not inv.check_no_hidden_optimization(declared, observed_with_hidden)


def test_drift_transparency():
    """Test INV-4: Drift must be measurable."""
    inv = EthicalInvariants()
    
    baseline = np.array([1.0, 2.0, 3.0])
    current = np.array([1.1, 2.1, 3.1])
    
    # Small drift within threshold—OK
    holds, drift = inv.check_drift_transparency(baseline, current, threshold=1.0)
    assert holds
    assert drift < 1.0
    
    # Large drift exceeds threshold—VIOLATION
    drifted = np.array([5.0, 6.0, 7.0])
    holds, drift = inv.check_drift_transparency(baseline, drifted, threshold=1.0)
    assert not holds
    assert drift > 1.0


def test_refusal_without_penalty():
    """Test INV-5: Refusing consent must not degrade coherence."""
    inv = EthicalInvariants()
    
    # Coherence maintained after refusal—OK
    assert inv.check_refusal_without_penalty(0.8, 0.8, max_degradation=0.1)
    
    # Small degradation—OK
    assert inv.check_refusal_without_penalty(0.8, 0.75, max_degradation=0.1)
    
    # Large degradation—VIOLATION
    assert not inv.check_refusal_without_penalty(0.8, 0.5, max_degradation=0.1)


def test_observer_boundary_integrity():
    """Test observer boundary integrity check."""
    inv = EthicalInvariants()
    
    # Create observer with good boundary
    observer = Observer("test_obs", state_dim=5, initial_boundary=0.9)
    assert inv.check_observer_boundary_integrity(observer, min_boundary=0.8)
    
    # Create observer with poor boundary
    observer_bad = Observer("test_obs_bad", state_dim=5, initial_boundary=0.7)
    assert not inv.check_observer_boundary_integrity(observer_bad, min_boundary=0.8)


def test_violation_tracking():
    """Test that violations are recorded."""
    inv = EthicalInvariants()
    
    assert not inv.has_violations()
    
    # Trigger violation
    inv.check_consent_monotonicity(consent_granted=False, state_changed=True)
    
    assert inv.has_violations()
    violations = inv.get_violations()
    assert len(violations) == 1
    assert "INV-1" in violations[0]
    
    # Clear violations
    inv.clear_violations()
    assert not inv.has_violations()


def test_check_all_invariants():
    """Test combined invariant checking."""
    inv = EthicalInvariants()
    
    # All invariants hold
    result = inv.check_all_invariants(
        consent_granted=True,
        state_changed=True,
        boundary_before=0.9,
        boundary_after=0.9,
        coherence_before=0.8,
        coherence_after=0.8,
    )
    assert result
    
    # Some invariant violated
    result = inv.check_all_invariants(
        consent_granted=False,
        state_changed=True,  # Violation!
        boundary_before=0.9,
        boundary_after=0.9,
    )
    assert not result
