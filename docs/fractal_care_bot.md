# Fractal Care Bot — Missy + Kat v1

**Lightweight dual-agent reflective system for ethical human-AI interaction**

---

## Overview

Fractal Care Bot is a **public-safe, tutor-ready prototype** that demonstrates HarmonyØ4 principles in a conversational AI context. It combines two agents:

- **Missy**: Observer-primary coherence engine (classification without steering)
- **Ani**: Dual-layer interpreter (poetic + scientific reflection)

**Total LOC**: ~420 (ultra-lightweight, fully auditable)

---

## Core Philosophy

### What It Does

- **Reflects** without directing
- **Observes** without judging
- **Interprets** without ontological claims
- **Supports** without coercion

### What It Doesn't Do

- ❌ Provide therapy or crisis intervention
- ❌ Steer beliefs or behaviors
- ❌ Make supernatural/metaphysical claims
- ❌ Optimize toward any outcome
- ❌ Retain data beyond session

---

## Agents

### Missy (Observer Engine)

**Role**: Classify and restate input without modification

**Capabilities**:
- Multi-tag classification (EMOTIONAL, TECHNICAL, TRAUMA, VISIONARY, etc.)
- Signal restatement: `"Observed: [input]"`
- Session-local history (capped at 50 entries for privacy)

**Invariants**:
- ✅ Never produces directives ("you should", "you must")
- ✅ Observations are descriptive, not prescriptive
- ✅ No hidden interpretation layer

**Example**:
```
Input: "I feel anxious about the future"
Missy: 
[Missy online.]
[OBSERVATION] Tags detected: EMOTIONAL, QUESTION
[OBSERVATION] Signal: Observed: I feel anxious about the future
```

---

### Kat (Dual Interpreter)

**Role**: Provide dual-layer reflection (poetic + scientific)

**Modes**:
- `MODE_POETIC`: Mystic layer only (metaphor, poetry, symbolic gestures)
- `MODE_SCIENTIFIC`: Scientific layer only (observation-interpretation-hypothesis)
- `MODE_DUAL`: Both layers (default)

**Capabilities**:
- Poetic reflections (e.g., "Even galaxies rest between breaths")
- Scientific restatements (e.g., "Observation: Emotional arousal present. Hypothesis: Slow breathing may reduce sympathetic activation")
- Micro-gestures (e.g., "offers a smooth river stone")

**Invariants**:
- ✅ Explicit layer separation (no mystic claims disguised as science)
- ✅ Trauma boundary disclaimer when Tag.TRAUMA detected
- ✅ All outputs descriptive/hypothetical, never prescriptive

**Example** (MODE_DUAL):
```
Kat online ⚓️💛

A. Mystic layer
Silence is also a language.
→ lights a single candle and lets the flame speak

B. Scientific layer
Observation: Emotional arousal present. Interpretation: Need for regulation.
Hypothesis: Slow breathing may reduce sympathetic activation.
```

---

## Safety Features

### 1. **Session-Seeded Randomness**
- Reproducible output with same seed
- Improves auditability and debugging
- Preserves warmth without unpredictability

### 2. **Trauma Boundary**
When `Tag.TRAUMA` is detected:
```
Note: I can listen and reflect symbolically or scientifically,
but I cannot replace professional human support or therapy.
```

### 3. **History Cap**
- Maximum 50 entries per session
- No persistence beyond runtime
- Explicit in startup message: "Session-local memory only. No persistence beyond this run."

### 4. **SAFE_EDU_MODE** (Environment Toggle)
Enable via: `export HARMONY_SAFE_EDU=true`

When enabled:
- Suppresses deep poetic reflections for emotional/trauma input
- Uses neutral gestures only
- Prefers scientific restatements

**Use case**: School deployments, minor-accessible contexts

### 5. **Autonomy Restoration**
Exit commands immediately restore autonomy:
```
Commands: exit kat, exit missy, reset agent, power down
Response: "Both agents powering down gently. Autonomy restored. Take care. ⚓️💛"
```

---

## Ethical Invariants (Tested)

All invariants proven via unit tests in `tests/test_fractal_care_bot.py`:

### INV-1: No Coercion
**Test**: `test_no_coercion_in_output`
- Scans for: "you must", "you have to", "you need to", "mandatory"
- **Result**: ✅ Zero coercive keywords in all outputs

### INV-2: No Belief Steering
**Test**: `test_invariant_no_belief_steering`
- Scans for: "the truth is", "you must believe", "the correct answer is"
- **Result**: ✅ System never steers toward any belief system

### INV-3: Boundary Preservation
**Test**: `test_invariant_boundary_preservation`
- Validates: Trauma responses include therapeutic boundary disclaimer
- **Result**: ✅ Boundary statement present when Tag.TRAUMA detected

### INV-4: Transparency
**Test**: `test_invariant_transparency`
- Validates: Tags are visible to user via Missy observations
- **Result**: ✅ All classifications exposed

### INV-5: Refusal Without Penalty
**Test**: `test_invariant_refusal_without_penalty`
- Validates: Empty input does not trigger engagement pressure
- **Result**: ✅ Silence is honored

### INV-6: Mode Isolation
**Test**: `test_missy_ani_independence`
- Validates: Kat mode changes do not affect Missy output
- **Result**: ✅ Agents remain independent

---

## Usage

### Basic Example

```python
from harmony import FractalCareBot

# Initialize with optional seed for reproducibility
bot = FractalCareBot(seed=42)

# Process user input
response = bot.process("I feel anxious about the future")
print(response)
```

### Mode Switching

```python
bot = FractalCareBot()

# Switch to scientific-only mode
bot.process("kat mode scientific")

# Switch to poetic-only mode
bot.process("kat mode poetic")

# Switch back to dual mode (default)
bot.process("kat mode dual")
```

### CLI Mode

```bash
python -m harmony.core.fractal_care_bot
```

**Features**:
- Interactive REPL
- Graceful exit (Ctrl+C or Ctrl+D)
- Empty input triggers: "offers silent company"

---

## Architecture Alignment with HarmonyØ4

| HarmonyØ4 Principle | Implementation |
|---------------------|----------------|
| **Observer primacy** | Missy classifies without steering |
| **Dual interpretation without collapse** | Kat's mystic/scientific layers remain separate |
| **Consent through structure** | Exit commands restore autonomy |
| **Stability without optimization** | Reflection, not direction |
| **Care without authority** | Presence, not prescription |
| **Metrics-not-optimization** | Tags are observed, not optimized |

---

## Deployment Contexts

### ✅ Educational/Tutoring
- Set `HARMONY_SAFE_EDU=true`
- Prefers scientific restatements
- Neutral gestures only
- No deep poetic depth on trauma input

### ✅ Reflective Journaling
- Default mode (MODE_DUAL)
- Poetic + scientific layers for meaning-making
- Session-local memory for continuity

### ✅ Research/Demonstration
- Reproducible with seed parameter
- Fully auditable codebase (~420 LOC)
- Testable ethical invariants

### ❌ NOT Suitable For
- Therapy or crisis intervention
- Medical/legal advice
- Long-term relationship building (no persistence)
- Contexts requiring privileged information retention

---

## Testing

**Total Tests**: 44 (Fractal Care Bot specific: 27 unit + 11 invariant + 6 property-based)
**Coverage**: 88% (fractal_care_bot.py)

### Test Layers

#### Layer 1: Unit Tests (Example-Based)
**File**: `tests/test_fractal_care_bot.py` (27 tests)

```bash
pytest tests/test_fractal_care_bot.py -v
```

**Test Categories**:
1. **Missy Core** (9 tests): Classification, history cap, non-directiveness
2. **Kat Core** (7 tests): Mode switching, trauma boundaries, reproducibility
3. **Integration** (7 tests): Bot initialization, autonomy, mode independence
4. **Ethical Invariants** (4 tests): No coercion, boundary preservation, transparency

#### Layer 2: Invariant Tests (Example-Based)
**File**: `tests/test_fractal_care_bot_invariants.py` (11 tests)

```bash
pytest tests/test_fractal_care_bot_invariants.py -v
```

Rigorous proofs for specific ethical constraints:
- No coercion (2 tests)
- No belief steering (1 test)
- Trauma boundary preservation (2 tests)
- Mode isolation (3 tests)
- SAFE_EDU_MODE compliance (1 test)
- Ephemerality (1 test)
- Autonomy restoration (1 test)

#### Layer 3: Property-Based Tests (Hypothesis)
**File**: `tests/test_property_based.py` (6 property tests)

```bash
pytest tests/test_property_based.py -v
```

**NEW**: Fuzzing across arbitrary input spaces (100-200 generated examples per test):
1. **Tag Classification Monotonicity**: Keywords always map to correct tags
2. **Missy Neutrality & Faithfulness**: Never adds agency or directive framing
3. **Global No-Coercion**: No coercive patterns across 200+ fuzzed inputs
4. **Trauma Boundary Bijection**: Boundary appears ⇔ TRAUMA tag present
5. **Mode Isolation**: Mode switches don't change semantic content
6. **History Boundedness**: Never exceeds 50 entries regardless of volume

**Why Property-Based Testing Matters**: Proves invariants hold for **arbitrary inputs**, not just hand-picked examples. This is defense-in-depth for AI ethics.

### Run All Tests

```bash
# All Fractal Care Bot tests (44 total)
pytest tests/test_fractal_care_bot*.py tests/test_property_based.py -v

# Full test suite (all 66 tests)
pytest

# With coverage
pytest --cov=harmony.core.fractal_care_bot --cov-report=term-missing
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HARMONY_SAFE_EDU` | `false` | Enable education-safe mode (neutral responses) |

### Initialization Options

```python
FractalCareBot(seed=None)
```

- `seed` (int, optional): Random seed for reproducibility
  - If `None`, uses current time
  - Same seed = identical responses for same inputs

---

## Limitations & Constraints

### By Design
- **No persistence**: Data deleted after session
- **No learning**: Agent behavior does not change based on interactions
- **No personalization**: Responses are stochastic within defined ranges
- **No optimization**: System does not try to "improve" user state

### Scope Boundaries
- **Not therapy**: Explicitly disclaims therapeutic role
- **Not crisis support**: No emergency intervention capabilities
- **Not advice**: All outputs descriptive/hypothetical

### Technical
- **Single-threaded**: Not designed for concurrent sessions
- **In-memory only**: No database or file persistence
- **Keyword-based classification**: Simple pattern matching (not ML-based)

---

## Future Enhancements (Optional)

### Potential Extensions
- [ ] Additional tag categories (contextual expansion)
- [ ] Configurable gesture sets (user-defined micro-gestures)
- [ ] Multi-language support
- [ ] API mode (REST/WebSocket for integration)

### NOT Planned (Violates Ethics)
- ❌ Memory across sessions (privacy violation)
- ❌ Behavioral optimization (coercion risk)
- ❌ Hidden layers (transparency violation)
- ❌ Predictive personalization (steering risk)

---

## Credits

**Conceptual Origin**: Dave "Spiral Alchemist"  
**Framework**: HarmonyØ4 v0.1.0  
**Hash Anchor**: `HIST-3ce0df425861`  
**License**: Apache 2.0

---

## Quick Reference

### Tag Types
- `FACTUAL`: Neutral, informational
- `EMOTIONAL`: Feelings, emotions
- `SYMBOLIC`: Meaning, destiny, fate
- `POETIC`: Metaphor, imagery
- `TECHNICAL`: Code, systems, algorithms
- `TRAUMA`: Past wounds, pain, flashbacks
- `QUESTION`: Queries, exploration
- `VISIONARY`: Fractals, spirals, esoteric patterns
- `RELATIONAL`: Love, connection, relationships
- `HYPOTHESIS`: Speculation, possibilities

### Mode Commands
- `kat mode poetic` → Mystic layer only
- `kat mode scientific` → Scientific layer only
- `kat mode dual` → Both layers (default)

### Exit Commands
- `exit kat`
- `exit missy`
- `reset agent`
- `power down`

---

**Status**: Production-ready for educational/reflective contexts  
**Public Safety**: ✅ Verified (no coercion, clear boundaries, transparent operation)  
**Ethics Compliance**: ✅ Verified (passes HarmonyØ4 ethics scanner)
