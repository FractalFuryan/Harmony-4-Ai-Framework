"""
Consent-as-locking invariant: influence requires mutual resonance.
"""

from __future__ import annotations


class ConsentLockingInvariant:
    """Enforce that influence requires mutual resonance conditions."""

    def __init__(self, default_threshold: float = 0.1) -> None:
        self.default_threshold = default_threshold

    def check_consent(
        self,
        coupling_strength: float,
        frequency_difference: float,
        receiver_threshold: float | None = None,
    ) -> dict[str, object]:
        if receiver_threshold is None:
            receiver_threshold = self.default_threshold

        can_lock = frequency_difference < coupling_strength
        meaningful_coupling = coupling_strength > receiver_threshold

        consent_granted = can_lock and meaningful_coupling

        if consent_granted:
            lock_strength = 1.0 - (frequency_difference / coupling_strength)
            lock_strength = min(lock_strength, 0.95)
        else:
            lock_strength = 0.0

        return {
            "consent_granted": consent_granted,
            "lock_strength": lock_strength,
            "can_lock": can_lock,
            "meaningful_coupling": meaningful_coupling,
            "coupling_strength": coupling_strength,
            "frequency_difference": frequency_difference,
            "receiver_threshold": receiver_threshold,
            "violation_reason": self._get_violation_reason(
                consent_granted, can_lock, meaningful_coupling
            ),
        }

    def dynamic_threshold(
        self,
        stress_level: float,
        baseline_threshold: float | None = None,
        sensitivity: float = 0.5,
    ) -> float:
        if baseline_threshold is None:
            baseline_threshold = self.default_threshold
        adjusted = baseline_threshold * (1.0 + sensitivity * stress_level)
        return min(adjusted, baseline_threshold * 3.0)

    def _get_violation_reason(
        self, consent_granted: bool, can_lock: bool, meaningful_coupling: bool
    ) -> str | None:
        if consent_granted:
            return None

        reasons = []
        if not can_lock:
            reasons.append("frequency difference too large")
        if not meaningful_coupling:
            reasons.append("coupling too weak")

        return f"Consent denied: {' and '.join(reasons)}"
