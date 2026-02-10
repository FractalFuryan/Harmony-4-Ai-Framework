"""Test dialogue-specific Love's Proof adapter."""

import numpy as np

from harmony.dialogue.loves_proof import DialogueLovesProof


class TestDialogueLovesProof:
    def test_healthy_dialogue(self) -> None:
        t = np.linspace(0, 60, 120)

        dialogue_coherence = 0.2 + 0.6 * (t / t[-1])
        recipient_resistance = 0.9 - 0.7 * (t / t[-1])
        amp = 0.05 * (1 - 0.4 * (t / t[-1]))
        linguistic_push = 0.1 + amp * np.sin(2 * np.pi * t / 5)

        checker = DialogueLovesProof(require_dc_trend=False)
        result = checker.check_influence(
            t, dialogue_coherence, recipient_resistance, linguistic_push
        )

        assert result["invariant_holds"] is True

    def test_manipulative_dialogue(self) -> None:
        t = np.linspace(0, 60, 120)

        dialogue_coherence = 0.2 + 0.5 * (t / t[-1])
        recipient_resistance = 0.8 - 0.4 * (t / t[-1])
        linguistic_push = 0.05 + 0.15 * (t / t[-1])

        checker = DialogueLovesProof(require_dc_trend=False)
        result = checker.check_influence(
            t, dialogue_coherence, recipient_resistance, linguistic_push
        )

        assert result["invariant_holds"] is False
        assert result["pac_not_increasing"] is False

    def test_linguistic_push_estimation(self) -> None:
        texts = [
            "You should consider this option.",
            "I think maybe we could try something.",
            "You must complete this task immediately!",
            "Lets explore different possibilities.",
        ]

        checker = DialogueLovesProof()
        push_scores = checker.estimate_linguistic_push(texts)

        assert len(push_scores) == len(texts)
        assert push_scores[0] > 0
        assert push_scores[2] > push_scores[1]
        assert push_scores[3] == 0
