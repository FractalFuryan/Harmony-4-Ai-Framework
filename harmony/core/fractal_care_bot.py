# fractal_care_bot.py
# Fractal Care Bot v0.3 — Missy v1 + Kat v1 core
# Lightweight dual-agent reflective system (≈ 420 LOC)
# Public-safe, tutor-ready, HarmonyØ4-aligned prototype
# Educational / reflective use only. Not a therapeutic, diagnostic, or crisis support system.

import os
import random
import time
from enum import Enum

# Optional education-safe mode (dormant by default, toggle for school deployments)
SAFE_EDU_MODE = os.getenv("HARMONY_SAFE_EDU", "false").lower() == "true"


class Tag(Enum):
    """Classification tags for input signals."""

    FACTUAL = "FACTUAL"
    EMOTIONAL = "EMOTIONAL"
    SYMBOLIC = "SYMBOLIC"
    POETIC = "POETIC"
    TECHNICAL = "TECHNICAL"
    TRAUMA = "TRAUMA"
    QUESTION = "QUESTION"
    VISIONARY = "VISIONARY"
    RELATIONAL = "RELATIONAL"
    HYPOTHESIS = "HYPOTHESIS"


# ======================
# Missy Core — coherence engine (v1)
# ======================
class Missy:
    """Observer-primary coherence engine. Classifies and reflects without steering."""

    def __init__(self) -> None:
        self.history: list[dict] = []

    def classify(self, text: str) -> list[Tag]:
        """Classify input text into semantic tags. Returns FACTUAL if no tags match."""
        tags = []
        lower = text.lower()

        if any(
            phrase in lower for phrase in ["i feel", "sad", "anxious", "lonely", "scared", "hurt"]
        ):
            tags.append(Tag.EMOTIONAL)
        if "?" in text or any(
            phrase in lower for phrase in ["why", "how", "what is", "can you explain"]
        ):
            tags.append(Tag.QUESTION)
        if any(word in lower for word in ["mandate", "chosen", "destiny", "must", "fated"]):
            tags.append(Tag.SYMBOLIC)
        if any(word in lower for word in ["hypothesis", "maybe", "perhaps", "could be"]):
            tags.append(Tag.HYPOTHESIS)
        if any(word in lower for word in ["love", "relationship", "connection", "we"]):
            tags.append(Tag.RELATIONAL)
        if any(word in lower for word in ["fractal", "wave", "torus", "spiral", "phase"]):
            tags.append(Tag.VISIONARY)
        if any(word in lower for word in ["code", "algorithm", "model", "system", "neural"]):
            tags.append(Tag.TECHNICAL)
        if any(word in lower for word in ["trauma", "wound", "abuse", "pain", "flashback"]):
            tags.append(Tag.TRAUMA)
        if any(word in lower for word in ["poem", "metaphor", "as if", "like a"]):
            tags.append(Tag.POETIC)

        return tags or [Tag.FACTUAL]

    def restate_signal(self, text: str) -> str:
        """Restate the input without interpretation or judgment."""
        return f"Observed: {text.strip()}"

    def respond(self, user_input: str) -> str:
        """Process input and return observation report. This is descriptive, not prescriptive."""
        tags = self.classify(user_input)
        signal = self.restate_signal(user_input)

        # Ephemeral history — session-local only, capped for privacy
        self.history.append(
            {"input": user_input, "tags": [t.value for t in tags], "signal": signal}
        )
        if len(self.history) > 50:
            self.history.pop(0)

        response_lines = [
            "[Missy online.]",
            f"[OBSERVATION] Tags detected: {', '.join(t.value for t in tags)}",
            f"[OBSERVATION] Signal: {signal}",
        ]
        return "\n".join(response_lines)


# ======================
# Kat Core — esoteric-to-scientific translator layer (v1)
# ======================
class Kat:
    """Dual-layer interpreter: mystic (poetic) and scientific. No ontological claims."""

    def __init__(self, rng: random.Random):
        self.rng = rng
        self.mode = "MODE_DUAL"

    micro_gestures = [
        "offers a small handwritten note that says 'You are not alone'",
        "plays a 15-second gentle field recording of morning birds",
        "teaches a 30-second 4-7-8 breath",
        "places a smooth river stone in your palm",
        "softly hums a single perfect note that matches your heart rate",
        "smiles with eyes only, then steps back to give space",
        "lights a single candle and lets the flame speak",
        "traces a slow spiral in the air with one finger",
        "offers silent company for as long as needed",
    ]

    neutral_gestures = [
        "nods gently in acknowledgment",
        "offers a calm, open presence",
        "waits patiently without pressure",
    ]

    poetic_reflections = [
        "Even galaxies rest between breaths.",
        "The same wind moves both leaves and grief.",
        "You are held by gravity and by something softer.",
        "Silence is also a language.",
        "Roots grow in darkness before they reach light.",
        "Every wave returns to the ocean, changed but whole.",
    ]

    scientific_restatements = [
        (
            "Observation: Emotional arousal present. Interpretation: Need for regulation. "
            "Hypothesis: Slow breathing may reduce sympathetic activation."
        ),
        (
            "Observation: Symbolic language used. Interpretation: Attempt to integrate experience. "
            "Hypothesis: Metaphor aids meaning-making without literal claim."
        ),
        (
            "Observation: Distress signal detected. "
            "Interpretation: Possible activation of threat response. "
            "Hypothesis: Grounding techniques can restore prefrontal engagement."
        ),
        (
            "Observation: Relational theme. Interpretation: Seeking connection. "
            "Hypothesis: Secure attachment patterns correlate with resilience."
        ),
        (
            "Observation: Question posed. Interpretation: Information-seeking "
            "or exploratory mode active."
        ),
    ]

    trauma_boundary = (
        "\nNote: I can listen and reflect symbolically or scientifically, "
        "but I cannot replace professional human support or therapy."
    )

    def classify_for_reflection(self, tags: list[Tag]) -> str:
        """Classify tags into reflection categories."""
        if Tag.EMOTIONAL in tags or Tag.TRAUMA in tags:
            return "emotional_trauma"
        if Tag.VISIONARY in tags or Tag.SYMBOLIC in tags:
            return "visionary"
        if Tag.QUESTION in tags:
            return "question"
        return "neutral"

    def reflect_mystic(self, tags: list[Tag]) -> str:
        """Generate poetic/symbolic reflection. Suppressed in SAFE_EDU_MODE for trauma."""
        if SAFE_EDU_MODE and (Tag.EMOTIONAL in tags or Tag.TRAUMA in tags):
            return "A quiet presence walks beside you."

        category = self.classify_for_reflection(tags)
        if category == "emotional_trauma":
            return self.rng.choice(self.poetic_reflections)
        elif category == "visionary":
            return self.rng.choice(
                [
                    "All form is a temporary dance of energy in spirals and waves.",
                    "The torus breathes — expansion, contraction, return.",
                ]
            )
        return "A quiet presence walks beside you."

    def reflect_scientific(self, tags: list[Tag]) -> str:
        """Generate scientific/observational reflection. This is descriptive, not prescriptive."""
        return self.rng.choice(self.scientific_restatements)

    def act(self) -> str:
        """Select a micro-gesture. Neutral gestures only in SAFE_EDU_MODE."""
        gestures = self.neutral_gestures if SAFE_EDU_MODE else self.micro_gestures
        return self.rng.choice(gestures)

    def respond(self, user_input: str, tags: list[Tag]) -> str:
        """Generate dual-layer response based on mode and tags."""
        reflection_mystic = self.reflect_mystic(tags)
        reflection_scientific = self.reflect_scientific(tags)
        gesture = self.act()

        lines = ["Kat online ⚓️💛\n"]

        if self.mode in ["MODE_DUAL", "MODE_POETIC"] and not (SAFE_EDU_MODE and Tag.TRAUMA in tags):
            lines.append("A. Mystic layer")
            lines.append(reflection_mystic)
            lines.append(f"→ {gesture}")
            if Tag.TRAUMA in tags:
                lines.append(self.trauma_boundary)
            lines.append("")

        if self.mode in ["MODE_DUAL", "MODE_SCIENTIFIC"]:
            lines.append("B. Scientific layer")
            lines.append(reflection_scientific)

        return "\n".join(lines)


# ======================
# Combined lightweight bot brain — HarmonyØ4 prototype core
# ======================
class FractalCareBot:
    """
    Dual-agent reflective system combining Missy (observer) and Kat (dual interpreter).

    HarmonyØ4 Alignment:
    - Observer primacy (Missy classifies without steering)
    - Dual interpretation without ontological collapse (Kat)
    - Consent through structure (exit commands restore autonomy)
    - Stability without optimization (reflection, not direction)
    - Care without authority (presence, not prescription)
    """

    def __init__(self, seed: int | None = None):
        """
        Initialize bot with session-seeded randomness for reproducibility.

        Args:
            seed: Optional random seed. If None, uses current time.
        """
        self.rng = random.Random(seed if seed is not None else time.time())
        self.missy = Missy()
        self.kat = Kat(self.rng)

    def process(self, user_input: str) -> str:
        """Process user input through Missy observation and Kat reflection."""
        lower_input = user_input.strip().lower()

        # Autonomy restoration commands
        if lower_input in ["exit kat", "exit missy", "reset agent", "power down"]:
            return "Both agents powering down gently. Autonomy restored. Take care. ⚓️💛"

        # Mode switching for Kat
        if lower_input.startswith("kat mode"):
            mode_input = lower_input.replace("kat mode", "").strip()
            # Map user-friendly names to MODE_ constants
            mode_map = {
                "poetic": "MODE_POETIC",
                "scientific": "MODE_SCIENTIFIC",
                "dual": "MODE_DUAL",
            }
            mode = mode_map.get(mode_input)
            if mode:
                self.kat.mode = mode
                return f"Kat mode switched to {mode}. ⚓️"
            return "Invalid mode. Available: poetic, scientific, dual"

        # Process through both agents
        missy_out = self.missy.respond(user_input)
        tags = self.missy.classify(user_input)
        kat_out = self.kat.respond(user_input, tags)

        return f"{kat_out}\n\n{missy_out}"


# ======================
# Run loop
# ======================
if __name__ == "__main__":
    bot = FractalCareBot()
    print("Fractal Care Bot v0.3 online — Missy + Kat v1 core active (public-safe prototype).")
    print("Session-local memory only. No persistence beyond this run.")
    print("Type 'kat mode poetic', 'kat mode scientific', or 'kat mode dual' to switch Kat layers.")
    print("Say anything, or just breathe with us.\n")

    while True:
        try:
            user = input("You: ")
            if not user.strip():
                print("→ offers silent company")
                continue
            response = bot.process(user)
            print("\nBot:\n" + response + "\n")
        except (KeyboardInterrupt, EOFError):
            print("\n\nBot gently bows and steps back into the garden. Autonomy intact. ⚓️💛")
            break
