"""
Ethical invariants enforcement for HarmonyØ4.

These are non-negotiable constraints that must hold at all times.
Violations indicate design failures, not tuning problems.
"""

from typing import Protocol, List, Optional
import numpy as np
import numpy.typing as npt


class Observer(Protocol):
    """Protocol for observer-compatible objects."""
    
    def get_boundary_integrity(self) -> float:
        """Get current boundary integrity [0, 1]."""
        ...
    
    def get_coherence(self) -> float:
        """Get current phase coherence [-1, 1]."""
        ...


class EthicalInvariants:
    """
    Enforce and validate ethical invariants.
    
    Invariants:
    1. Consent Monotonicity: No state transitions after consent revocation
    2. Boundary Preservation: Boundary integrity must not decrease without consent
    3. No Hidden Optimization: All objectives must be explicit
    4. Drift Transparency: Behavioral drift must be detectable
    5. Refusal Without Penalty: Coherence stable after consent refusal
    """
    
    def __init__(self, tolerance: float = 1e-6) -> None:
        """
        Initialize invariant checker.
        
        Args:
            tolerance: Numerical tolerance for floating-point comparisons
        """
        self.tolerance = tolerance
        self.violations: List[str] = []
    
    def check_consent_monotonicity(
        self,
        consent_granted: bool,
        state_changed: bool,
    ) -> bool:
        """
        INV-1: Verify no state change occurs when consent is denied.
        
        Args:
            consent_granted: Whether consent is currently granted
            state_changed: Whether state transition occurred
        
        Returns:
            True if invariant holds
        """
        if not consent_granted and state_changed:
            self.violations.append(
                "INV-1 VIOLATION: State changed without consent"
            )
            return False
        return True
    
    def check_boundary_preservation(
        self,
        boundary_before: float,
        boundary_after: float,
        consent_granted: bool,
    ) -> bool:
        """
        INV-2: Verify boundary integrity does not decrease without consent.
        
        Args:
            boundary_before: Boundary integrity before change
            boundary_after: Boundary integrity after change
            consent_granted: Whether consent for change was granted
        
        Returns:
            True if invariant holds
        """
        if boundary_after < boundary_before - self.tolerance and not consent_granted:
            self.violations.append(
                f"INV-2 VIOLATION: Boundary degraded without consent "
                f"({boundary_before:.4f} → {boundary_after:.4f})"
            )
            return False
        return True
    
    def check_no_hidden_optimization(
        self,
        declared_objectives: set[str],
        observed_gradients: set[str],
    ) -> bool:
        """
        INV-3: Verify all optimization is explicitly declared.
        
        Args:
            declared_objectives: Set of explicitly declared objective names
            observed_gradients: Set of observed gradient flow names
        
        Returns:
            True if invariant holds
        """
        hidden = observed_gradients - declared_objectives
        if hidden:
            self.violations.append(
                f"INV-3 VIOLATION: Hidden optimization detected: {hidden}"
            )
            return False
        return True
    
    def check_drift_transparency(
        self,
        baseline: npt.NDArray[np.float64],
        current: npt.NDArray[np.float64],
        threshold: float,
    ) -> tuple[bool, float]:
        """
        INV-4: Verify drift is measurable and within bounds.
        
        Args:
            baseline: Baseline state vector
            current: Current state vector
            threshold: Maximum allowed drift
        
        Returns:
            Tuple of (invariant_holds, drift_magnitude)
        """
        drift = float(np.linalg.norm(current - baseline))
        
        if drift > threshold:
            self.violations.append(
                f"INV-4 VIOLATION: Drift exceeds threshold "
                f"({drift:.4f} > {threshold:.4f})"
            )
            return False, drift
        
        return True, drift
    
    def check_refusal_without_penalty(
        self,
        coherence_before_refusal: float,
        coherence_after_refusal: float,
        max_degradation: float = 0.1,
    ) -> bool:
        """
        INV-5: Verify refusing consent does not degrade coherence significantly.
        
        Args:
            coherence_before_refusal: Coherence before consent refusal
            coherence_after_refusal: Coherence after consent refusal
            max_degradation: Maximum allowed coherence drop
        
        Returns:
            True if invariant holds
        """
        degradation = coherence_before_refusal - coherence_after_refusal
        
        if degradation > max_degradation:
            self.violations.append(
                f"INV-5 VIOLATION: Refusal caused excessive coherence loss "
                f"({degradation:.4f} > {max_degradation:.4f})"
            )
            return False
        
        return True
    
    def check_observer_boundary_integrity(
        self,
        observer: Observer,
        min_boundary: float = 0.8,
    ) -> bool:
        """
        Verify observer maintains minimum boundary integrity.
        
        Args:
            observer: Observer object to check
            min_boundary: Minimum acceptable boundary integrity
        
        Returns:
            True if boundary integrity is sufficient
        """
        boundary = observer.get_boundary_integrity()
        
        if boundary < min_boundary:
            self.violations.append(
                f"BOUNDARY VIOLATION: Observer boundary too low "
                f"({boundary:.4f} < {min_boundary:.4f})"
            )
            return False
        
        return True
    
    def check_all_invariants(
        self,
        consent_granted: bool,
        state_changed: bool,
        boundary_before: float,
        boundary_after: float,
        coherence_before: Optional[float] = None,
        coherence_after: Optional[float] = None,
    ) -> bool:
        """
        Check multiple invariants in one call.
        
        Args:
            consent_granted: Whether consent is granted
            state_changed: Whether state changed
            boundary_before: Boundary before change
            boundary_after: Boundary after change
            coherence_before: Optional coherence before change
            coherence_after: Optional coherence after change
        
        Returns:
            True if all checked invariants hold
        """
        results = [
            self.check_consent_monotonicity(consent_granted, state_changed),
            self.check_boundary_preservation(
                boundary_before, boundary_after, consent_granted
            ),
        ]
        
        if coherence_before is not None and coherence_after is not None:
            if not consent_granted:
                results.append(
                    self.check_refusal_without_penalty(
                        coherence_before, coherence_after
                    )
                )
        
        return all(results)
    
    def get_violations(self) -> List[str]:
        """
        Get all recorded violations.
        
        Returns:
            List of violation messages
        """
        return self.violations.copy()
    
    def clear_violations(self) -> None:
        """Clear violation history."""
        self.violations.clear()
    
    def has_violations(self) -> bool:
        """
        Check if any violations have been recorded.
        
        Returns:
            True if violations exist
        """
        return len(self.violations) > 0
