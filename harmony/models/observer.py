"""
Observer models for HarmonyØ4.

Implements observer boundaries and witness-based observation.
"""

import numpy as np
import numpy.typing as npt


class Observer:
    """
    Observer with defined boundary and internal state.

    External systems can only perceive this observer through
    witness projections—no privileged access to internal states.
    """

    def __init__(
        self,
        observer_id: str,
        state_dim: int,
        initial_boundary: float = 1.0,
    ) -> None:
        """
        Initialize observer.

        Args:
            observer_id: Unique identifier
            state_dim: Dimensionality of internal state
            initial_boundary: Initial boundary integrity [0, 1]
        """
        self.observer_id = observer_id
        self.state_dim = state_dim
        self._internal_state = np.zeros(state_dim)
        self._boundary_integrity = initial_boundary
        self._consented_observers: set[str] = set()
        self._shared_states: dict[str, npt.NDArray[np.float64]] = {}

    def get_boundary_integrity(self) -> float:
        """
        Get current boundary integrity.

        Returns:
            Boundary integrity in [0, 1]
        """
        return self._boundary_integrity

    def get_coherence(self) -> float:
        """
        Get internal coherence measure.

        Simplified: based on state norm stability.

        Returns:
            Coherence estimate in [-1, 1]
        """
        # Simplified coherence: exponential decay from reference norm
        state_norm = np.linalg.norm(self._internal_state)
        return float(np.tanh(1.0 / (1.0 + state_norm)))

    def grant_observation_consent(self, other_observer_id: str) -> None:
        """
        Grant another observer permission to witness this observer.

        Args:
            other_observer_id: ID of observer receiving permission
        """
        self._consented_observers.add(other_observer_id)

    def revoke_observation_consent(self, other_observer_id: str) -> None:
        """
        Revoke observation permission.

        Args:
            other_observer_id: ID of observer losing permission
        """
        self._consented_observers.discard(other_observer_id)
        # Remove any shared state
        self._shared_states.pop(other_observer_id, None)

    def witness_projection(
        self,
        requesting_observer_id: str,
        projection_dim: int,
    ) -> npt.NDArray[np.float64] | None:
        """
        Provide witness projection to consented observer.

        Args:
            requesting_observer_id: ID of requesting observer
            projection_dim: Dimensionality of projection (must be <= state_dim)

        Returns:
            Projected state if consent granted, None otherwise
        """
        if requesting_observer_id not in self._consented_observers:
            return None

        if projection_dim > self.state_dim:
            projection_dim = self.state_dim

        # Lossy projection: random projection matrix
        # (In practice, this would be deterministic and observer-specific)
        projection_matrix = np.random.randn(projection_dim, self.state_dim)
        projection_matrix /= np.linalg.norm(projection_matrix, axis=1, keepdims=True)

        projected_state = projection_matrix @ self._internal_state

        # Cache for consistency
        self._shared_states[requesting_observer_id] = projected_state

        return projected_state

    def update_internal_state(
        self,
        new_state: npt.NDArray[np.float64],
        consent: bool = True,
    ) -> bool:
        """
        Update internal state.

        Args:
            new_state: New state vector
            consent: Whether update is consented (for external updates)

        Returns:
            True if update successful
        """
        if not consent:
            return False

        if new_state.shape[0] != self.state_dim:
            return False

        self._internal_state = new_state.copy()
        return True

    def compute_boundary_integrity(
        self,
        external_observers: list["Observer"] | None = None,
    ) -> float:
        """
        Compute boundary integrity based on information leakage.

        Args:
            external_observers: List of external observers (for mutual info calc)

        Returns:
            Updated boundary integrity value
        """
        if external_observers is None or len(external_observers) == 0:
            # No external observers—perfect boundary
            self._boundary_integrity = 1.0
            return self._boundary_integrity

        # Simplified: boundary decreases with number of consented observers
        num_consented = len(self._consented_observers)
        num_external = len(external_observers)

        if num_external == 0:
            self._boundary_integrity = 1.0
        else:
            # Boundary decreases linearly with fraction of consented observers
            self._boundary_integrity = 1.0 - 0.5 * (num_consented / num_external)

        return self._boundary_integrity

    def get_consented_observers(self) -> set[str]:
        """Get set of observers with observation consent."""
        return self._consented_observers.copy()
