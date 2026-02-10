"""Dialogue-specific adapter for Love's Proof."""

from __future__ import annotations

from typing import Any

import numpy as np

from harmony.invariants.loves_proof import LovesProofInvariant


class DialogueLovesProof:
    """Apply Love's Proof to dialogue influence dynamics."""

    def __init__(self, **kwargs: object) -> None:
        self.invariant = LovesProofInvariant(**kwargs)

    def check_influence(
        self,
        t: np.ndarray,
        dialogue_coherence: np.ndarray,
        recipient_resistance: np.ndarray,
        linguistic_push: np.ndarray,
    ) -> dict[str, Any]:
        return self.invariant.check(t, dialogue_coherence, recipient_resistance, linguistic_push)

    def estimate_linguistic_push(
        self, texts: list[str], directive_keywords: list[str] | None = None
    ) -> np.ndarray:
        if directive_keywords is None:
            directive_keywords = ["should", "must", "need to", "have to", "ought to"]

        push_scores = []
        for text in texts:
            text_lower = text.lower()
            directive_count = sum(text_lower.count(keyword) for keyword in directive_keywords)
            word_count = max(len(text.split()), 1)
            push_scores.append(directive_count / word_count)

        return np.array(push_scores, dtype=float)
