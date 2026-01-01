"""
Witness-based observation system for HarmonyØ4.

Implements lossy, consent-gated observation between observers.
"""

from typing import Optional, Dict
import numpy as np
import numpy.typing as npt


class WitnessProjection:
    """
    Create consent-gated, lossy projections of observer states.
    
    Witness projections:
    - Are lossy (cannot be inverted)
    - Require consent
    - Are observer-specific
    - Preserve boundary integrity
    """
    
    def __init__(
        self,
        source_dim: int,
        target_dim: int,
        seed: Optional[int] = None,
    ) -> None:
        """
        Initialize witness projection.
        
        Args:
            source_dim: Dimensionality of source observer state
            target_dim: Dimensionality of projection (target_dim <= source_dim)
            seed: Random seed for deterministic projections
        """
        if target_dim > source_dim:
            raise ValueError(
                f"Target dimension ({target_dim}) cannot exceed source ({source_dim})"
            )
        
        self.source_dim = source_dim
        self.target_dim = target_dim
        
        # Create deterministic projection matrix
        rng = np.random.default_rng(seed)
        self.projection_matrix = rng.standard_normal((target_dim, source_dim))
        
        # Normalize rows
        norms = np.linalg.norm(self.projection_matrix, axis=1, keepdims=True)
        self.projection_matrix /= norms
    
    def project(
        self,
        state: npt.NDArray[np.float64],
        consent: bool,
    ) -> Optional[npt.NDArray[np.float64]]:
        """
        Project observer state through witness projection.
        
        Args:
            state: Source observer state
            consent: Whether projection is consented to
        
        Returns:
            Projected state if consented, None otherwise
        """
        if not consent:
            return None
        
        if state.shape[0] != self.source_dim:
            raise ValueError(
                f"State dimension ({state.shape[0]}) does not match source ({self.source_dim})"
            )
        
        return self.projection_matrix @ state
    
    def is_invertible(self) -> bool:
        """
        Check if projection is invertible (it shouldn't be).
        
        Returns:
            False (projections are intentionally lossy)
        """
        return self.target_dim == self.source_dim and np.linalg.matrix_rank(
            self.projection_matrix
        ) == self.source_dim
    
    def information_loss(self) -> float:
        """
        Estimate information loss from projection.
        
        Returns:
            Fraction of dimensions lost [0, 1]
        """
        return 1.0 - (self.target_dim / self.source_dim)


class WitnessRegistry:
    """
    Manage witness projections between multiple observers.
    
    Tracks consent and provides projection lookup.
    """
    
    def __init__(self) -> None:
        """Initialize witness registry."""
        self._projections: Dict[tuple[str, str], WitnessProjection] = {}
        self._consent_map: Dict[tuple[str, str], bool] = {}
    
    def register_projection(
        self,
        source_id: str,
        target_id: str,
        projection: WitnessProjection,
        consent: bool = False,
    ) -> None:
        """
        Register a witness projection between observers.
        
        Args:
            source_id: ID of source observer (being witnessed)
            target_id: ID of target observer (witnessing)
            projection: WitnessProjection object
            consent: Initial consent state
        """
        key = (source_id, target_id)
        self._projections[key] = projection
        self._consent_map[key] = consent
    
    def grant_witness_consent(
        self,
        source_id: str,
        target_id: str,
    ) -> bool:
        """
        Grant witness consent.
        
        Args:
            source_id: ID of source observer
            target_id: ID of target observer
        
        Returns:
            True if projection exists and consent granted
        """
        key = (source_id, target_id)
        if key not in self._projections:
            return False
        
        self._consent_map[key] = True
        return True
    
    def revoke_witness_consent(
        self,
        source_id: str,
        target_id: str,
    ) -> bool:
        """
        Revoke witness consent.
        
        Args:
            source_id: ID of source observer
            target_id: ID of target observer
        
        Returns:
            True if projection exists and consent revoked
        """
        key = (source_id, target_id)
        if key not in self._projections:
            return False
        
        self._consent_map[key] = False
        return True
    
    def witness(
        self,
        source_id: str,
        target_id: str,
        source_state: npt.NDArray[np.float64],
    ) -> Optional[npt.NDArray[np.float64]]:
        """
        Perform witness projection with consent check.
        
        Args:
            source_id: ID of source observer
            target_id: ID of target observer
            source_state: State of source observer
        
        Returns:
            Projected state if consented, None otherwise
        """
        key = (source_id, target_id)
        
        if key not in self._projections:
            return None
        
        consent = self._consent_map.get(key, False)
        projection = self._projections[key]
        
        return projection.project(source_state, consent)
    
    def get_consented_witnesses(self, source_id: str) -> list[str]:
        """
        Get list of observers with witness consent from source.
        
        Args:
            source_id: ID of source observer
        
        Returns:
            List of target observer IDs with consent
        """
        consented = []
        for (src, tgt), consent in self._consent_map.items():
            if src == source_id and consent:
                consented.append(tgt)
        return consented
