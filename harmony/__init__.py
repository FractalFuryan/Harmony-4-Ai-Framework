"""HarmonyO4: An open, ethical framework for modeling coherence and consent."""

__version__ = "0.3.0"

from harmony.core import coherence, consent, fractal_care_bot, invariants as core_invariants
from harmony import invariants
from harmony.core.coherence import PhaseCoherence, CoherenceMetrics
from harmony.core.consent import ConsentManager, ConsentState
from harmony.core.invariants import EthicalInvariants
from harmony.core.fractal_care_bot import FractalCareBot, Missy, Kat, Tag

from harmony.ops.acdc import ac_power, ac_power_trend, acdc_split, dc_slope, ema_lpf

from harmony.invariants import ConsentLockingInvariant, GrowthBoundsInvariant, NonCoercionInvariant
from harmony.invariants.loves_proof import LovesProofInvariant

from harmony.physiology.heart import (
    AnalyticSignal,
    EntrainmentMetrics,
    HeartFieldScorer,
    PhaseCoherence as HeartPhaseCoherence,
    SignalPreprocessor,
    StressIndexBuilder,
)
from harmony.physiology.heart.loves_proof import PhysiologyLovesProof
from harmony.physiology.shared import phase_tools

from harmony.coupling.loves_proof import CouplingLovesProof
from harmony.dialogue.loves_proof import DialogueLovesProof

HASH_ANCHOR = "HIST-3ce0df425861-lovesproof-v0.3.0"

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
    "coherence",
    "consent",
    "fractal_care_bot",
    "core_invariants",
    "invariants",
    "ema_lpf",
    "acdc_split",
    "ac_power",
    "dc_slope",
    "ac_power_trend",
    "SignalPreprocessor",
    "AnalyticSignal",
    "HeartPhaseCoherence",
    "EntrainmentMetrics",
    "StressIndexBuilder",
    "HeartFieldScorer",
    "phase_tools",
    "NonCoercionInvariant",
    "ConsentLockingInvariant",
    "GrowthBoundsInvariant",
    "LovesProofInvariant",
    "PhysiologyLovesProof",
    "CouplingLovesProof",
    "DialogueLovesProof",
]
