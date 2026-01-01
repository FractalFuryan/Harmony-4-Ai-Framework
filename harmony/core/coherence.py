"""
Coherence metrics for HarmonyØ4.

This module provides public-safe implementations of coherence measurement.
Field equations and optimization kernels are NOT included.
"""

from typing import List, Optional
import numpy as np
import numpy.typing as npt


class PhaseCoherence:
    """
    Measure internal consistency across system states via phase alignment.
    
    Phase coherence quantifies how synchronized components are without
    forcing synchronization. High coherence indicates emergent stability.
    
    Range: [-1, 1]
        1.0: Perfect coherence
        0.0: Random phases
       -1.0: Anti-coherence (unstable)
    """
    
    def __init__(self, n_components: int) -> None:
        """
        Initialize phase coherence tracker.
        
        Args:
            n_components: Number of phase components to track
        """
        self.n_components = n_components
        self.phases: npt.NDArray[np.float64] = np.zeros(n_components)
        self.baseline_coherence: Optional[float] = None
    
    def compute(self, phases: npt.NDArray[np.float64]) -> float:
        """
        Compute phase coherence for given phase angles.
        
        Args:
            phases: Array of phase angles in radians, shape (n_components,)
        
        Returns:
            Phase coherence value in [-1, 1]
        
        Raises:
            ValueError: If phases array has wrong shape
        """
        if phases.shape != (self.n_components,):
            raise ValueError(
                f"Expected {self.n_components} phases, got {phases.shape[0]}"
            )
        
        # Compute mean phase
        mean_phase = np.angle(np.mean(np.exp(1j * phases)))
        
        # Compute coherence as average cosine deviation from mean
        coherence = np.mean(np.cos(phases - mean_phase))
        
        return float(coherence)
    
    def update_phases(self, phases: npt.NDArray[np.float64]) -> float:
        """
        Update internal phase state and compute coherence.
        
        Args:
            phases: New phase angles
        
        Returns:
            Current coherence value
        """
        self.phases = phases.copy()
        return self.compute(phases)
    
    def set_baseline(self, phases: Optional[npt.NDArray[np.float64]] = None) -> None:
        """
        Set baseline coherence for drift detection.
        
        Args:
            phases: Phase angles to use as baseline. If None, uses current phases.
        """
        if phases is None:
            phases = self.phases
        self.baseline_coherence = self.compute(phases)
    
    def drift_from_baseline(self, phases: npt.NDArray[np.float64]) -> float:
        """
        Measure drift from baseline coherence.
        
        Args:
            phases: Current phase angles
        
        Returns:
            Absolute drift from baseline
        
        Raises:
            RuntimeError: If baseline not set
        """
        if self.baseline_coherence is None:
            raise RuntimeError("Baseline coherence not set. Call set_baseline() first.")
        
        current = self.compute(phases)
        return abs(current - self.baseline_coherence)


class CoherenceMetrics:
    """
    Container for multiple coherence measurements.
    
    Tracks phase coherence, role elasticity, and boundary integrity
    in a unified interface.
    """
    
    def __init__(self) -> None:
        """Initialize coherence metrics container."""
        self.phase_coherence: Optional[float] = None
        self.role_elasticity: Optional[float] = None
        self.boundary_integrity: Optional[float] = None
        self._history: List[dict] = []
    
    def update(
        self,
        phase_coherence: Optional[float] = None,
        role_elasticity: Optional[float] = None,
        boundary_integrity: Optional[float] = None,
    ) -> None:
        """
        Update coherence metrics and record history.
        
        Args:
            phase_coherence: Phase coherence value in [-1, 1]
            role_elasticity: Role elasticity value >= 0
            boundary_integrity: Boundary integrity in [0, 1]
        """
        if phase_coherence is not None:
            self.phase_coherence = phase_coherence
        if role_elasticity is not None:
            self.role_elasticity = role_elasticity
        if boundary_integrity is not None:
            self.boundary_integrity = boundary_integrity
        
        # Record snapshot
        self._history.append({
            "phase_coherence": self.phase_coherence,
            "role_elasticity": self.role_elasticity,
            "boundary_integrity": self.boundary_integrity,
        })
    
    def is_stable(
        self,
        phase_threshold: float = 0.7,
        boundary_threshold: float = 0.8,
    ) -> bool:
        """
        Check if system is in stable state.
        
        Args:
            phase_threshold: Minimum phase coherence for stability
            boundary_threshold: Minimum boundary integrity for stability
        
        Returns:
            True if all metrics indicate stability
        """
        if self.phase_coherence is None or self.boundary_integrity is None:
            return False
        
        return (
            self.phase_coherence >= phase_threshold
            and self.boundary_integrity >= boundary_threshold
        )
    
    def get_history(self) -> List[dict]:
        """
        Get historical coherence measurements.
        
        Returns:
            List of metric snapshots
        """
        return self._history.copy()
