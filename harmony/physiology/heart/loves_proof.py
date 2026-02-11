"""Physiology-specific adapter for Love's Proof."""

from __future__ import annotations

from typing import Any

import numpy as np

from harmony.invariants.loves_proof import LovesProofInvariant


class PhysiologyLovesProof:
    """Apply Love's Proof to physiological dynamics."""

    def __init__(self, fs: float = 250.0, **kwargs: object) -> None:
        self.fs = fs
        self.invariant = LovesProofInvariant(**kwargs)

    def check_heart_field(
        self,
        t: np.ndarray,
        heart_coherence: np.ndarray,
        stress_proxy: np.ndarray,
        influence_carrier: np.ndarray | None = None,
        heart_amplitude: np.ndarray | None = None,
    ) -> dict[str, Any]:
        if influence_carrier is None:
            if heart_amplitude is not None:
                amplitude_norm = (heart_amplitude - np.min(heart_amplitude)) / (
                    np.max(heart_amplitude) - np.min(heart_amplitude) + 1e-6
                )
                influence_carrier = amplitude_norm
            else:
                influence_carrier = stress_proxy

        return self.invariant.check(t, heart_coherence, stress_proxy, influence_carrier)

    def check_continuous_heart_field(
        self,
        t: np.ndarray,
        heart_coherence: np.ndarray,
        stress_proxy: np.ndarray,
        window_sec: float = 30.0,
        step_sec: float = 5.0,
        **kwargs: object,
    ) -> dict[str, Any]:
        return self.invariant.check_continuous(
            t=t,
            c=heart_coherence,
            s=stress_proxy,
            x=stress_proxy,
            window_sec=window_sec,
            step_sec=step_sec,
        )
