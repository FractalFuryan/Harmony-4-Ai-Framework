"""Generalized ethical invariants for HarmonyO4."""

from .consent_locking import ConsentLockingInvariant
from .growth_bounds import GrowthBoundsInvariant
from .loves_proof import LovesProofInvariant
from .non_coercion import NonCoercionInvariant

__all__ = [
    "NonCoercionInvariant",
    "ConsentLockingInvariant",
    "GrowthBoundsInvariant",
    "LovesProofInvariant",
]
