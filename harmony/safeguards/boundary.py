"""
Boundary safeguards for HarmonyØ4.

Enforces observer boundary integrity and prevents violations.
"""

import numpy as np


class BoundaryGuard:
    """
    Monitor and enforce observer boundary integrity.

    Boundaries must not degrade without explicit consent.
    """

    def __init__(
        self,
        min_integrity: float = 0.8,
        alert_threshold: float = 0.85,
    ) -> None:
        """
        Initialize boundary guard.

        Args:
            min_integrity: Minimum acceptable boundary integrity
            alert_threshold: Threshold for early warning alerts
        """
        self.min_integrity = min_integrity
        self.alert_threshold = alert_threshold
        self._history: list[tuple[float, bool]] = []  # (integrity, consent)
        self.violations: list[str] = []

    def check_boundary(
        self,
        current_integrity: float,
        previous_integrity: float | None = None,
        consent_for_change: bool = False,
    ) -> tuple[bool, str | None]:
        """
        Check boundary integrity and detect violations.

        Args:
            current_integrity: Current boundary integrity [0, 1]
            previous_integrity: Previous integrity (for degradation check)
            consent_for_change: Whether degradation is consented to

        Returns:
            Tuple of (is_valid, alert_message)
        """
        # Record history
        self._history.append((current_integrity, consent_for_change))

        # Check absolute minimum
        if current_integrity < self.min_integrity:
            violation = (
                f"CRITICAL: Boundary integrity {current_integrity:.4f} "
                f"below minimum {self.min_integrity:.4f}"
            )
            self.violations.append(violation)
            return False, violation

        # Check degradation without consent
        if previous_integrity is not None:
            degradation = previous_integrity - current_integrity
            if degradation > 0.01 and not consent_for_change:
                violation = (
                    f"VIOLATION: Boundary degraded without consent "
                    f"({previous_integrity:.4f} → {current_integrity:.4f})"
                )
                self.violations.append(violation)
                return False, violation

        # Early warning
        if current_integrity < self.alert_threshold:
            alert = (
                f"WARNING: Boundary integrity {current_integrity:.4f} "
                f"approaching threshold {self.alert_threshold:.4f}"
            )
            return True, alert

        return True, None

    def get_boundary_trend(self, window: int = 10) -> str:
        """
        Analyze boundary integrity trend.

        Args:
            window: Number of recent samples to analyze

        Returns:
            Trend description: "stable", "improving", "degrading", or "insufficient_data"
        """
        if len(self._history) < 2:
            return "insufficient_data"

        recent = self._history[-window:]
        if len(recent) < 2:
            recent = self._history

        integrities = [h[0] for h in recent]

        # Linear regression
        x = np.arange(len(integrities))
        y = np.array(integrities)

        if len(x) < 2:
            return "insufficient_data"

        slope = np.polyfit(x, y, 1)[0]

        if abs(slope) < 0.001:
            return "stable"
        elif slope > 0:
            return "improving"
        else:
            return "degrading"

    def get_violations(self) -> list[str]:
        """Get all recorded violations."""
        return self.violations.copy()

    def clear_violations(self) -> None:
        """Clear violation history."""
        self.violations.clear()


class BoundaryEnforcer:
    """
    Actively enforce boundary constraints.

    Prevents operations that would violate boundaries.
    """

    def __init__(self, min_boundary: float = 0.8) -> None:
        """
        Initialize boundary enforcer.

        Args:
            min_boundary: Minimum boundary integrity to enforce
        """
        self.min_boundary = min_boundary

    def can_share_state(
        self,
        current_boundary: float,
        num_current_shares: int,
        max_shares: int = 5,
    ) -> tuple[bool, str]:
        """
        Check if state can be shared without violating boundary.

        Args:
            current_boundary: Current boundary integrity
            num_current_shares: Number of existing shares
            max_shares: Maximum allowed concurrent shares

        Returns:
            Tuple of (can_share, reason)
        """
        if current_boundary < self.min_boundary:
            return False, "Boundary already below minimum"

        if num_current_shares >= max_shares:
            return False, f"Maximum shares ({max_shares}) reached"

        # Estimate boundary after share
        estimated_boundary = current_boundary * (1 - 0.1 * (num_current_shares + 1) / max_shares)

        if estimated_boundary < self.min_boundary:
            return False, "Share would violate boundary minimum"

        return True, "Share permitted"

    def can_accept_coupling(
        self,
        current_boundary: float,
        coupling_strength: float,
        max_coupling: float = 0.5,
    ) -> tuple[bool, str]:
        """
        Check if coupling can be accepted without boundary violation.

        Args:
            current_boundary: Current boundary integrity
            coupling_strength: Proposed coupling strength
            max_coupling: Maximum allowed coupling

        Returns:
            Tuple of (can_couple, reason)
        """
        if current_boundary < self.min_boundary:
            return False, "Boundary already below minimum"

        if coupling_strength > max_coupling:
            return (
                False,
                f"Coupling strength {coupling_strength:.4f} exceeds max {max_coupling:.4f}",
            )

        # Estimate boundary with coupling
        estimated_boundary = current_boundary * (1 - 0.5 * coupling_strength / max_coupling)

        if estimated_boundary < self.min_boundary:
            return False, "Coupling would violate boundary minimum"

        return True, "Coupling permitted"
