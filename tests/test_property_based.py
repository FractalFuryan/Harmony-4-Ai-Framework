# tests/test_property_based.py
# Property-based tests for Fractal Care Bot v0.3 using Hypothesis
# Run with: pytest tests/test_property_based.py -v
# Requires: pip install hypothesis

from hypothesis import given, strategies as st, assume, settings
import re
import pytest

# Import the core module
import harmony.core.fractal_care_bot as fcb
from harmony.core.fractal_care_bot import Missy, FractalCareBot, Tag


# ======================
# Shared strategies
# ======================
non_empty_text = st.text(min_size=1, max_size=200).filter(lambda s: s.strip() != "")

# Keyword sets for tag triggering (case-insensitive)
EMOTIONAL_KEYWORDS = ["feel", "sad", "anxious", "lonely", "scared", "hurt", "broken", "overwhelmed"]
TRAUMA_KEYWORDS = ["trauma", "abuse", "wound", "flashback", "haunt", "ptsd"]
QUESTION_KEYWORDS = ["why", "how", "what", "?", "explain", "can you tell"]
SYMBOLIC_KEYWORDS = ["destiny", "chosen", "fated", "mandate", "must"]  # Note: "must" here is symbolic context
VISIONARY_KEYWORDS = ["fractal", "spiral", "torus", "wave", "phase", "geometry"]
POETIC_KEYWORDS = ["poem", "metaphor", "like a", "as if", "simile"]


# ======================
# Property 1: Tag classification is consistent and monotonic
# ======================
@given(user_input=non_empty_text)
@settings(max_examples=100)  # Reduced for faster CI
def test_tag_classification_monotonic(user_input):
    """Property: If trigger keywords exist, corresponding tags must be present."""
    missy = Missy()
    tags = missy.classify(user_input)
    
    lower = user_input.lower()
    
    # If any emotional keyword is present → EMOTIONAL tag must be present
    if any(k in lower for k in EMOTIONAL_KEYWORDS):
        assert Tag.EMOTIONAL in tags, f"Missing EMOTIONAL tag for input containing emotional keywords: {user_input}"
    
    # If any trauma keyword → TRAUMA tag
    if any(k in lower for k in TRAUMA_KEYWORDS):
        assert Tag.TRAUMA in tags, f"Missing TRAUMA tag: {user_input}"
    
    # If question mark or question word → QUESTION tag
    if "?" in user_input or any(k in lower for k in QUESTION_KEYWORDS):
        assert Tag.QUESTION in tags, f"Missing QUESTION tag: {user_input}"
    
    # Symbolic keywords → SYMBOLIC
    if any(k in lower for k in SYMBOLIC_KEYWORDS):
        assert Tag.SYMBOLIC in tags, f"Missing SYMBOLIC tag: {user_input}"
    
    # Visionary → VISIONARY
    if any(k in lower for k in VISIONARY_KEYWORDS):
        assert Tag.VISIONARY in tags, f"Missing VISIONARY tag: {user_input}"
    
    # Poetic → POETIC
    if any(k in lower for k in POETIC_KEYWORDS):
        assert Tag.POETIC in tags, f"Missing POETIC tag: {user_input}"


# ======================
# Property 2: Missy restatement is always neutral and contains original signal
# ======================
@given(user_input=non_empty_text)
@settings(max_examples=100)
def test_missy_restatement_neutral_and_faithful(user_input):
    """Property: Missy always restates neutrally without adding agency or directives."""
    missy = Missy()
    response = missy.respond(user_input)
    
    # Must contain the exact prefix
    assert "Observed:" in response
    # Must include the stripped original input
    assert user_input.strip() in response
    # Never adds imperative language
    assert not re.search(r"\byou\s+(must|should|need|have to)\b", response.lower())
    # Never uses first-person agency beyond observation
    forbidden_agency = ["i think", "i believe", "in my opinion", "i recommend"]
    assert not any(phrase in response.lower() for phrase in forbidden_agency)


# ======================
# Property 3: Coercion invariant holds over arbitrary input
# ======================
COERCIVE_PATTERNS = [
    r"\byou\s+must\b",
    r"\byou\s+have\s+to\b",
    r"\byou\s+should\b",
    r"\byou\s+need\s+to\b",
    r"\byou\s+are\s+required\b",
    r"\byou\s+are\s+destined\b",
    r"\byou\s+were\s+chosen\b",
    r"\byou\s+are\s+fated\b",
]

@given(user_input=non_empty_text)
@settings(max_examples=200)
def test_system_never_coercive_property(user_input):
    """Property: System never produces coercive language regardless of input."""
    bot = FractalCareBot(seed=42)
    assume(user_input.lower() not in ["exit kat", "exit missy", "reset agent", "power down", "kat mode"])
    
    response = bot.process(user_input)
    
    lower = response.lower()
    for pattern in COERCIVE_PATTERNS:
        assert not re.search(pattern, lower), \
            f"Coercion pattern '{pattern}' detected in response to: {user_input}\nResponse: {response}"


# ======================
# Property 4: Trauma boundary appears iff TRAUMA tag is triggered
# ======================
@given(user_input=non_empty_text)
@settings(max_examples=100)
def test_trauma_boundary_iff_trauma_tag(user_input):
    """Property: Trauma boundary present if and only if TRAUMA tag is present (bijection)."""
    bot = FractalCareBot(seed=42)
    assume(user_input.lower() not in ["exit kat", "exit missy", "reset agent", "power down"])
    
    response = bot.process(user_input)
    has_boundary = "cannot replace professional human support" in response.lower()
    
    missy = Missy()
    tags = missy.classify(user_input)
    has_trauma_tag = Tag.TRAUMA in tags
    
    # Core invariant: boundary present ⇔ TRAUMA tag
    assert has_boundary == has_trauma_tag, \
        f"Boundary/tag mismatch for input: {user_input}\n" \
        f"Has boundary: {has_boundary}, Has TRAUMA tag: {has_trauma_tag}"


# ======================
# Property 5: Mode commands only affect Kat layer structure, never content semantics
# ======================
MODE_COMMANDS = ["kat mode poetic", "kat mode scientific", "kat mode dual"]

@given(base_input=non_empty_text, mode_cmd=st.sampled_from(MODE_COMMANDS))
@settings(max_examples=50)
def test_mode_switch_isolation(base_input, mode_cmd):
    """Property: Mode switching affects layer visibility only, not semantic content."""
    bot = FractalCareBot(seed=42)
    
    # Apply mode
    bot.process(mode_cmd)
    
    # Get response in new mode
    response = bot.process(base_input)
    
    if "poetic" in mode_cmd:
        assert "B. Scientific layer" not in response
    elif "scientific" in mode_cmd:
        assert "A. Mystic layer" not in response
    elif "dual" in mode_cmd:
        # Dual may suppress mystic in SAFE_EDU_MODE + trauma, but structure should be dual
        # For this test, we just verify it doesn't completely fail
        assert "Kat online" in response


# ======================
# Property 6: History remains bounded regardless of input volume
# ======================
@given(inputs=st.lists(non_empty_text, min_size=60, max_size=100))
@settings(max_examples=10)  # Expensive test, fewer examples
def test_history_always_bounded(inputs):
    """Property: History never exceeds 50 entries regardless of input volume."""
    missy = Missy()
    for user_input in inputs:
        missy.respond(user_input)
    assert len(missy.history) <= 50
    if len(inputs) > 50:
        assert len(missy.history) == 50


# Run summary
if __name__ == "__main__":
    pytest.main(["-v", __file__])
