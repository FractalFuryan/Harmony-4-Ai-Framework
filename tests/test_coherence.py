"""Tests for coherence module."""

import pytest
import numpy as np
from harmony.core.coherence import PhaseCoherence, CoherenceMetrics


def test_phase_coherence_initialization():
    """Test PhaseCoherence initialization."""
    pc = PhaseCoherence(n_components=5)
    assert pc.n_components == 5
    assert pc.baseline_coherence is None


def test_phase_coherence_perfect_alignment():
    """Test coherence with perfectly aligned phases."""
    pc = PhaseCoherence(n_components=5)
    phases = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
    coherence = pc.compute(phases)
    assert coherence == pytest.approx(1.0, abs=1e-6)


def test_phase_coherence_random_phases():
    """Test coherence with random phases."""
    pc = PhaseCoherence(n_components=100)
    phases = np.random.uniform(0, 2 * np.pi, 100)
    coherence = pc.compute(phases)
    # Random phases should have low coherence
    assert -0.2 < coherence < 0.2


def test_phase_coherence_drift_detection():
    """Test drift detection from baseline."""
    pc = PhaseCoherence(n_components=5)
    
    baseline_phases = np.zeros(5)
    pc.set_baseline(baseline_phases)
    
    # Drifted phases (significantly different to ensure detection)
    drifted_phases = np.array([1.0, 1.5, 1.0, 1.5, 1.0])
    drift = pc.drift_from_baseline(drifted_phases)
    
    assert drift > 0.0


def test_coherence_metrics_update():
    """Test CoherenceMetrics update mechanism."""
    metrics = CoherenceMetrics()
    
    metrics.update(phase_coherence=0.8, boundary_integrity=0.9)
    
    assert metrics.phase_coherence == 0.8
    assert metrics.boundary_integrity == 0.9
    assert len(metrics.get_history()) == 1


def test_coherence_metrics_stability():
    """Test stability detection."""
    metrics = CoherenceMetrics()
    
    # Unstable system
    metrics.update(phase_coherence=0.5, boundary_integrity=0.7)
    assert not metrics.is_stable()
    
    # Stable system
    metrics.update(phase_coherence=0.9, boundary_integrity=0.95)
    assert metrics.is_stable()
