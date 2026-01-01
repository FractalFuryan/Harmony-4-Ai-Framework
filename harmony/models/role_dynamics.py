"""
Role dynamics models for HarmonyØ4.

Tracks role elasticity and adaptation without forcing outcomes.
"""

from typing import Optional
import numpy as np
import numpy.typing as npt


class RoleState:
    """
    Represent a role state with elasticity tracking.
    
    Roles can adapt in response to influence, but only within
    boundary constraints and with consent.
    """
    
    def __init__(
        self,
        state_dim: int,
        min_boundary_integrity: float = 0.8,
    ) -> None:
        """
        Initialize role state.
        
        Args:
            state_dim: Dimensionality of role state vector
            min_boundary_integrity: Minimum boundary threshold
        """
        self.state_dim = state_dim
        self.state = np.zeros(state_dim)
        self.min_boundary = min_boundary_integrity
        self.boundary_integrity = 1.0
        self._baseline_state = self.state.copy()
    
    def apply_influence(
        self,
        influence: npt.NDArray[np.float64],
        consent: bool,
    ) -> tuple[bool, float]:
        """
        Apply external influence to role state.
        
        Args:
            influence: Influence vector to apply
            consent: Whether influence is consented to
        
        Returns:
            Tuple of (success, elasticity)
        """
        if not consent:
            return False, 0.0
        
        # Compute hypothetical new state
        new_state = self.state + influence
        
        # Check boundary preservation
        new_boundary = self._compute_boundary(new_state)
        
        if new_boundary < self.min_boundary:
            # Influence would violate boundary—reject
            return False, 0.0
        
        # Compute elasticity
        elasticity = self._compute_elasticity(influence)
        
        # Apply change
        self.state = new_state
        self.boundary_integrity = new_boundary
        
        return True, elasticity
    
    def _compute_boundary(
        self,
        state: npt.NDArray[np.float64],
    ) -> float:
        """
        Compute boundary integrity for given state.
        
        Simplified model: boundary decreases with distance from baseline.
        """
        distance = np.linalg.norm(state - self._baseline_state)
        return float(np.exp(-0.1 * distance))  # Exponential decay
    
    def _compute_elasticity(
        self,
        influence: npt.NDArray[np.float64],
    ) -> float:
        """
        Compute role elasticity.
        
        Elasticity = change / influence magnitude
        """
        influence_magnitude = np.linalg.norm(influence)
        if influence_magnitude < 1e-9:
            return 0.0
        
        # Elasticity is ratio of accepted change to influence
        return 1.0  # Simplified: full acceptance when within boundary
    
    def get_state(self) -> npt.NDArray[np.float64]:
        """Get current role state."""
        return self.state.copy()
    
    def get_boundary_integrity(self) -> float:
        """Get current boundary integrity."""
        return self.boundary_integrity
    
    def set_baseline(self, state: Optional[npt.NDArray[np.float64]] = None) -> None:
        """
        Set baseline state for boundary calculation.
        
        Args:
            state: State to use as baseline. If None, uses current state.
        """
        if state is None:
            state = self.state
        self._baseline_state = state.copy()
        self.boundary_integrity = 1.0


class RoleLockDetector:
    """
    Detect role lock-in (frozen role state).
    
    Lock-in violates emergence principle—roles must remain elastic.
    """
    
    def __init__(
        self,
        lock_threshold: float = 1e-6,
        window_size: int = 10,
    ) -> None:
        """
        Initialize lock detector.
        
        Args:
            lock_threshold: Maximum change magnitude to consider locked
            window_size: Number of samples to confirm lock
        """
        self.lock_threshold = lock_threshold
        self.window_size = window_size
        self._changes: list[float] = []
    
    def record_change(self, state_change: npt.NDArray[np.float64]) -> bool:
        """
        Record state change and check for lock-in.
        
        Args:
            state_change: Change vector applied to role
        
        Returns:
            True if role appears locked
        """
        magnitude = float(np.linalg.norm(state_change))
        self._changes.append(magnitude)
        
        # Maintain window
        if len(self._changes) > self.window_size:
            self._changes.pop(0)
        
        # Check for lock
        if len(self._changes) == self.window_size:
            return all(c < self.lock_threshold for c in self._changes)
        
        return False
    
    def is_locked(self) -> bool:
        """
        Check if role is currently locked.
        
        Returns:
            True if locked over recent window
        """
        if len(self._changes) < self.window_size:
            return False
        
        return all(c < self.lock_threshold for c in self._changes[-self.window_size:])
