"""
Heart-specific implementations of HarmonyO4 ethical dynamics.

These are domain-specific instantiations of the general
consent, coherence, and non-coercion principles.
"""

from .preprocessing import SignalPreprocessor
from .analytic import AnalyticSignal
from .coherence import PhaseCoherence
from .entrainment import EntrainmentMetrics
from .stress import StressIndexBuilder
from .field_score import HeartFieldScorer
from .loves_proof import PhysiologyLovesProof

__all__ = [
    "SignalPreprocessor",
    "AnalyticSignal",
    "PhaseCoherence",
    "EntrainmentMetrics",
    "StressIndexBuilder",
    "HeartFieldScorer",
    "PhysiologyLovesProof",
]
