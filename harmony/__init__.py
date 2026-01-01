"""HarmonyØ4: An open, ethical framework for modeling coherence, consent, and observer-safe systems."""

__version__ = "0.1.0"

from harmony.core.coherence import PhaseCoherence, CoherenceMetrics
from harmony.core.consent import ConsentManager, ConsentState
from harmony.core.invariants import EthicalInvariants
from harmony.core.fractal_care_bot import FractalCareBot, Missy, Kat, Tag

__all__ = [
    "PhaseCoherence",
    "CoherenceMetrics",
    "ConsentManager",
    "ConsentState",
    "EthicalInvariants",
    "FractalCareBot",
    "Missy",
    "Kat",
    "Tag",
]
