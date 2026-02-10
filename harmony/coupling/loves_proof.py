"""Coupling-specific adapter for Love's Proof."""

from __future__ import annotations

from typing import Any

import numpy as np

from harmony.invariants.loves_proof import LovesProofInvariant


class CouplingLovesProof:
    """Apply Love's Proof to coupling dynamics."""

    def __init__(self, **kwargs: object) -> None:
        self.invariant = LovesProofInvariant(**kwargs)

    def check_entrainment(
        self,
        t: np.ndarray,
        order_parameter: np.ndarray,
        mismatch_energy: np.ndarray,
        coupling_strength: np.ndarray,
    ) -> dict[str, Any]:
        return self.invariant.check(t, order_parameter, mismatch_energy, coupling_strength)

    def check_consent_dynamics(
        self,
        t: np.ndarray,
        phase_concentration: np.ndarray,
        receiver_resistance: np.ndarray,
        applied_coupling: np.ndarray,
    ) -> dict[str, Any]:
        return self.invariant.check(t, phase_concentration, receiver_resistance, applied_coupling)
