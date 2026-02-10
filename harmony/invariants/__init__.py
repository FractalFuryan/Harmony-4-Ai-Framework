"""Generalized ethical invariants for HarmonyO4."""

from .non_coercion import NonCoercionInvariant
from .consent_locking import ConsentLockingInvariant
from .growth_bounds import GrowthBoundsInvariant
from .loves_proof import LovesProofInvariant

__all__ = [
    "NonCoercionInvariant",
    "ConsentLockingInvariant",
    "GrowthBoundsInvariant",
    "LovesProofInvariant",
]
