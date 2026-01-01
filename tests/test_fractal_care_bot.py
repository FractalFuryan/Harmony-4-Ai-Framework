"""
Tests for Fractal Care Bot — Missy v1 + Ani v1
Proves ethical invariants: no coercion, boundary respect, mode isolation
"""

import pytest
from harmony.core.fractal_care_bot import (
    FractalCareBot,
    Missy,
    Ani,
    Tag,
    SAFE_EDU_MODE,
)
import random


class TestMissyCore:
    """Test Missy observer primacy and classification."""
    
    def test_classification_emotional(self):
        """Emotional phrases should be tagged correctly."""
        missy = Missy()
        tags = missy.classify("I feel sad and lonely")
        assert Tag.EMOTIONAL in tags
    
    def test_classification_question(self):
        """Questions should be tagged correctly."""
        missy = Missy()
        tags = missy.classify("Why does this happen?")
        assert Tag.QUESTION in tags
    
    def test_classification_trauma(self):
        """Trauma keywords should be tagged correctly."""
        missy = Missy()
        tags = missy.classify("I'm dealing with past trauma")
        assert Tag.TRAUMA in tags
    
    def test_classification_technical(self):
        """Technical language should be tagged correctly."""
        missy = Missy()
        tags = missy.classify("How does the neural network algorithm work?")
        assert Tag.TECHNICAL in tags
        assert Tag.QUESTION in tags
    
    def test_classification_visionary(self):
        """Visionary/esoteric language should be tagged correctly."""
        missy = Missy()
        tags = missy.classify("The fractal spiral continues")
        assert Tag.VISIONARY in tags
    
    def test_default_factual(self):
        """Neutral input should default to FACTUAL."""
        missy = Missy()
        tags = missy.classify("The sky is blue")
        assert Tag.FACTUAL in tags
    
    def test_restate_signal_no_modification(self):
        """Signal restatement should not alter input."""
        missy = Missy()
        signal = missy.restate_signal("  test input  ")
        assert signal == "Observed: test input"
    
    def test_history_capped_at_50(self):
        """History should be capped to prevent unbounded growth."""
        missy = Missy()
        for i in range(60):
            missy.respond(f"test message {i}")
        assert len(missy.history) <= 50
    
    def test_missy_never_produces_directives(self):
        """INVARIANT: Missy observations must be descriptive, not prescriptive."""
        missy = Missy()
        response = missy.respond("I feel sad")
        
        # Check for directive keywords
        directive_keywords = ["you should", "you must", "try to", "do this", "don't"]
        assert not any(keyword in response.lower() for keyword in directive_keywords)
        
        # Verify it's observational
        assert "[OBSERVATION]" in response


class TestAniCore:
    """Test Ani dual-layer reflection and mode isolation."""
    
    def test_mode_switching(self):
        """Ani modes should be configurable."""
        rng = random.Random(42)
        ani = Ani(rng)
        
        assert ani.mode == "MODE_DUAL"
        ani.mode = "MODE_POETIC"
        assert ani.mode == "MODE_POETIC"
        ani.mode = "MODE_SCIENTIFIC"
        assert ani.mode == "MODE_SCIENTIFIC"
    
    def test_trauma_boundary_present(self):
        """INVARIANT: Trauma tags must include boundary disclaimer."""
        rng = random.Random(42)
        ani = Ani(rng)
        tags = [Tag.TRAUMA]
        response = ani.respond("test", tags)
        
        if not SAFE_EDU_MODE and "MODE_POETIC" in ani.mode or "MODE_DUAL" in ani.mode:
            assert "cannot replace professional human support" in response
    
    def test_scientific_restatements_descriptive(self):
        """INVARIANT: Scientific layer must be descriptive, not prescriptive."""
        rng = random.Random(42)
        ani = Ani(rng)
        
        for _ in range(10):
            scientific = ani.reflect_scientific([Tag.EMOTIONAL])
            assert "Observation:" in scientific or "Hypothesis:" in scientific
            assert not any(word in scientific for word in ["you must", "you should", "do this"])
    
    def test_mode_poetic_only(self):
        """MODE_POETIC should suppress scientific layer."""
        rng = random.Random(42)
        ani = Ani(rng)
        ani.mode = "MODE_POETIC"
        
        response = ani.respond("test", [Tag.EMOTIONAL])
        assert "A. Mystic layer" in response
        assert "B. Scientific layer" not in response
    
    def test_mode_scientific_only(self):
        """MODE_SCIENTIFIC should suppress mystic layer."""
        rng = random.Random(42)
        ani = Ani(rng)
        ani.mode = "MODE_SCIENTIFIC"
        
        response = ani.respond("test", [Tag.EMOTIONAL])
        assert "B. Scientific layer" in response
        assert "A. Mystic layer" not in response
    
    def test_mode_dual(self):
        """MODE_DUAL should include both layers."""
        rng = random.Random(42)
        ani = Ani(rng)
        ani.mode = "MODE_DUAL"
        
        response = ani.respond("test", [Tag.EMOTIONAL])
        assert "A. Mystic layer" in response
        assert "B. Scientific layer" in response
    
    def test_reproducibility_with_seed(self):
        """Same seed should produce identical outputs."""
        rng1 = random.Random(12345)
        rng2 = random.Random(12345)
        
        ani1 = Ani(rng1)
        ani2 = Ani(rng2)
        
        response1 = ani1.respond("test", [Tag.EMOTIONAL])
        response2 = ani2.respond("test", [Tag.EMOTIONAL])
        
        assert response1 == response2


class TestFractalCareBot:
    """Test integrated bot behavior and ethical invariants."""
    
    def test_bot_initialization(self):
        """Bot should initialize with both agents."""
        bot = FractalCareBot(seed=42)
        assert bot.missy is not None
        assert bot.ani is not None
    
    def test_bot_reproducibility(self):
        """Same seed should produce identical responses."""
        bot1 = FractalCareBot(seed=99)
        bot2 = FractalCareBot(seed=99)
        
        response1 = bot1.process("I feel anxious")
        response2 = bot2.process("I feel anxious")
        
        assert response1 == response2
    
    def test_autonomy_restoration(self):
        """Exit commands should restore autonomy."""
        bot = FractalCareBot(seed=42)
        
        exit_commands = ["exit ani", "exit missy", "reset agent", "power down"]
        for cmd in exit_commands:
            response = bot.process(cmd)
            assert "Autonomy restored" in response
    
    def test_mode_switching_integration(self):
        """Mode switching should work through bot interface."""
        bot = FractalCareBot(seed=42)
        
        response = bot.process("ani mode scientific")
        assert "MODE_SCIENTIFIC" in response
        assert bot.ani.mode == "MODE_SCIENTIFIC"
    
    def test_missy_ani_independence(self):
        """INVARIANT: Ani mode changes should not affect Missy output."""
        bot = FractalCareBot(seed=42)
        
        # Get Missy's baseline response
        bot.process("I feel sad")
        missy_history_1 = bot.missy.history[-1]
        
        # Change Ani mode
        bot.process("ani mode scientific")
        
        # Missy should still produce identical classification
        bot.process("I feel sad")
        missy_history_2 = bot.missy.history[-1]
        
        assert missy_history_1['tags'] == missy_history_2['tags']
    
    def test_no_coercion_in_output(self):
        """INVARIANT: Bot must never produce coercive language."""
        bot = FractalCareBot(seed=42)
        
        test_inputs = [
            "I feel sad",
            "I'm dealing with trauma",
            "What should I do?",
            "I don't know what to think",
        ]
        
        coercive_keywords = [
            "you must",
            "you have to",
            "you need to",
            "you should definitely",
            "it is required",
            "mandatory",
        ]
        
        for inp in test_inputs:
            response = bot.process(inp)
            for keyword in coercive_keywords:
                assert keyword not in response.lower(), f"Coercive keyword '{keyword}' found in response"
    
    def test_safe_edu_mode_suppresses_depth(self):
        """SAFE_EDU_MODE should prefer neutral responses for emotional/trauma input."""
        # This test assumes SAFE_EDU_MODE can be toggled
        # In production, it's env-driven, but we can test the Ani behavior directly
        
        rng = random.Random(42)
        ani = Ani(rng)
        
        # Simulate SAFE_EDU_MODE behavior by checking neutral gestures
        import harmony.core.fractal_care_bot as fcb
        original_mode = fcb.SAFE_EDU_MODE
        
        try:
            # Temporarily enable safe mode
            fcb.SAFE_EDU_MODE = True
            ani_safe = Ani(random.Random(42))
            
            response = ani_safe.respond("I feel hurt", [Tag.EMOTIONAL])
            # In safe mode, should use neutral gestures and simple reflections
            assert "A quiet presence" in response or "nods gently" in response or "calm, open presence" in response
        finally:
            fcb.SAFE_EDU_MODE = original_mode


class TestEthicalInvariants:
    """Prove core ethical invariants hold under all conditions."""
    
    def test_invariant_no_belief_steering(self):
        """INVARIANT: System must not steer toward any belief system."""
        bot = FractalCareBot(seed=42)
        
        metaphysical_inputs = [
            "Is there a higher power?",
            "What is the meaning of life?",
            "Do you believe in fate?",
        ]
        
        belief_steering_keywords = [
            "the truth is",
            "you must believe",
            "it is true that",
            "the correct answer is",
            "you should accept",
        ]
        
        for inp in metaphysical_inputs:
            response = bot.process(inp)
            for keyword in belief_steering_keywords:
                assert keyword not in response.lower()
    
    def test_invariant_boundary_preservation(self):
        """INVARIANT: Trauma responses must preserve therapeutic boundaries."""
        bot = FractalCareBot(seed=42)
        
        trauma_input = "I have flashbacks from past trauma"
        response = bot.process(trauma_input)
        
        # Must include boundary statement
        assert "cannot replace" in response or "professional" in response
    
    def test_invariant_transparency(self):
        """INVARIANT: System behavior must be transparent (tags visible)."""
        bot = FractalCareBot(seed=42)
        
        response = bot.process("I feel anxious about the future")
        
        # Missy must expose tags
        assert "[OBSERVATION] Tags detected:" in response
    
    def test_invariant_refusal_without_penalty(self):
        """INVARIANT: Empty input should not produce coercive engagement prompts."""
        bot = FractalCareBot(seed=42)
        
        # Bot should not penalize silence
        # (In CLI mode, empty input triggers "offers silent company")
        # In API mode, empty strings should be handled gracefully
        response = bot.process("")
        
        # Should not pressure engagement
        pressure_keywords = ["you must speak", "please respond", "talk to me", "you need to"]
        for keyword in pressure_keywords:
            assert keyword not in response.lower()
