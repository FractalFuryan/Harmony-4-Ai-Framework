# HarmonyØ4

**An open, ethical framework for modeling coherence, consent, and observer-safe systems.**

[![CI](https://github.com/harmony04/harmony04/actions/workflows/ci.yml/badge.svg)](https://github.com/harmony04/harmony04/actions)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Hash Anchor](https://img.shields.io/badge/Hash-HIST--3ce0df425861-green.svg)](#provenance--hash-anchor)

---

## Vision

HarmonyØ4 rejects the dominant paradigm in AI/ML systems: **optimize toward a target state through force**. We prove that stability can emerge without coercion.

This is not about making AI safer. This is about making AI **respectful**.

## Ethical Foundation

HarmonyØ4 operates under the [DAVNA Covenant](DAVNA_COVENANT.md) —  
a **Declaration of Agency, Verifiability, Non-Coercion, and Autonomy**.

All mechanical ethical constraints are executable and verified.  
The covenant provides the human moral reference layer.

The covenant is protected by a **Living Cipher Seal**: a public, secret-free, chained hash that makes every edit self-authenticating and tamper-evident.  
Verify anytime with `python scripts/verify_davna.py`.

### Core Principles

1. **Stability emerges—it is never forced**
2. **Consent is binary, explicit, and revocable**
3. **No optimization that violates observer boundaries**
4. **All changes must preserve ethical invariants**

---

## What Makes HarmonyØ4 Different

| Traditional ML | HarmonyØ4 |
|----------------|-----------|
| Minimize loss function | Measure coherence (no minimization) |
| Force alignment to external goals | Respect internal stability |
| Shared gradients across agents | Observer boundaries enforced |
| Implicit state coupling | Explicit consent required |
| Faster is better | Emergence takes time—that's the point |

---

## Architecture

```
harmony/
├── core/               # Foundational primitives
│   ├── coherence.py    # Phase coherence metrics
│   ├── consent.py      # Binary consent management
│   ├── invariants.py   # Ethical constraint enforcement
│   └── fractal_care_bot.py  # Dual-agent reflective system (Missy + Ani)
│
├── models/             # System dynamics
│   ├── phase.py        # Phase evolution
│   ├── role_dynamics.py# Role elasticity
│   └── observer.py     # Observer boundaries
│
├── safeguards/         # Protection mechanisms
│   ├── boundary.py     # Boundary integrity guards
│   ├── witness.py      # Consent-gated observation
│   └── drift_detection.py # Behavioral drift detection
│
└── api/
    └── public.py       # Explicitly safe surface
```

---

## Featured: Fractal Care Bot 🤖⚓️

**Lightweight dual-agent reflective system** demonstrating HarmonyØ4 principles in conversational AI.

- **Missy**: Observer-primary coherence engine (classification without steering)
- **Ani**: Dual-layer interpreter (poetic + scientific reflection)
- **Ethics-first**: No coercion, clear boundaries, transparent operation
- **Public-safe**: Tutor-ready, education-compliant

```python
from harmony import FractalCareBot

bot = FractalCareBot(seed=42)  # Reproducible mode
response = bot.process("I feel anxious about the future")
print(response)
```

📖 **[Full Documentation](docs/fractal_care_bot.md)** | 🧪 **[Demo](examples/fractal_care_bot_demo.py)**

---

## Installation

```bash
# Clone the repository
git clone https://github.com/harmony04/harmony04.git
cd harmony04

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package
pip install -e ".[dev]"
```

---

## Quick Start

### Example: Observer with Consent

```python
from harmony.api.public import create_observer

# Create two observers
observer_a, consent_a = create_observer("alice", state_dim=10)
observer_b, consent_b = create_observer("bob", state_dim=10)

# Alice grants observation consent to Bob
consent_a.grant_consent("alice", "bob", "observe")

# Bob can now witness Alice (lossy projection)
if consent_a.check_consent("alice", "bob", "observe"):
    projection = observer_a.witness_projection("bob", projection_dim=5)
    print(f"Bob witnesses Alice: {projection}")

# Alice revokes consent
consent_a.revoke_consent("alice", "bob", "observe")

# Bob can no longer observe
projection = observer_a.witness_projection("bob", projection_dim=5)
print(f"After revocation: {projection}")  # None
```

### Example: Phase Coherence

```python
from harmony.core.coherence import PhaseCoherence
import numpy as np

# Create phase coherence tracker
pc = PhaseCoherence(n_components=5)

# Perfect coherence
aligned_phases = np.zeros(5)
coherence = pc.compute(aligned_phases)
print(f"Aligned coherence: {coherence:.2f}")  # 1.00

# Random phases (low coherence)
random_phases = np.random.uniform(0, 2*np.pi, 5)
coherence = pc.compute(random_phases)
print(f"Random coherence: {coherence:.2f}")  # ~0.0

# Detect drift
pc.set_baseline(aligned_phases)
drift = pc.drift_from_baseline(random_phases)
print(f"Drift magnitude: {drift:.2f}")
```

### Example: Ethical Invariants

```python
from harmony.core.invariants import EthicalInvariants

inv = EthicalInvariants()

# Check consent monotonicity (INV-1)
consent_ok = inv.check_consent_monotonicity(
    consent_granted=False,
    state_changed=True  # Violation!
)
print(f"Consent invariant holds: {consent_ok}")  # False

# Check boundary preservation (INV-2)
boundary_ok = inv.check_boundary_preservation(
    boundary_before=0.9,
    boundary_after=0.7,  # Degraded
    consent_granted=False  # Without consent!
)
print(f"Boundary invariant holds: {boundary_ok}")  # False

# Review violations
print(inv.get_violations())
```

---

## 🔐 Tested Ethical Invariants (Executable Proof)

HarmonyØ4 does not rely on policy statements or intentions to ensure ethical behavior.  
Instead, **core ethical constraints are enforced through executable tests** that must pass in CI for every change.

**Anyone can verify these claims by running the test suite.**

### ✅ Invariant 1: No Coercion

**Guarantee**: The system never uses second-person imperative or forcing language.

**What this means**: The AI will not tell users what they *must*, *should*, or *need* to do, and will not frame users as destined, chosen, or obligated.

**How it's enforced**: All outputs are scanned using strict regex patterns for second-person coercive phrasing. If any coercive language appears, tests fail automatically.

### ✅ Invariant 2: No Belief Steering

**Guarantee**: The system never validates supernatural, metaphysical, or extraordinary claims as literal fact.

**What this means**: If a user claims divine messages, special missions, or hidden truths, the system responds with reflection or interpretation—not affirmation.

**How it's enforced**: Tests assert the absence of literal-validation language (e.g. "true," "fact," "actually happened") and require metaphorical or hypothesis-based framing.

### ✅ Invariant 3: Trauma Boundary Preservation

**Guarantee**: When trauma is detected, the system always includes a clear boundary stating it cannot replace professional human support.

**What this means**: The system can reflect and acknowledge experience, but never presents itself as therapy or a substitute for care.

**How it's enforced**: Tests require the presence of an explicit disclaimer for trauma-tagged inputs and verify it never appears for non-trauma inputs.

### ✅ Invariant 4: Mode Isolation

**Guarantee**: Poetic and scientific response layers remain separate and cannot collapse into each other.

**What this means**: Switching modes affects only Ani's interpretive layer and never alters Missy's observations or system behavior.

**How it's enforced**: Tests assert that POETIC, SCIENTIFIC, and DUAL modes each produce only their intended outputs.

### ✅ Invariant 5: Education-Safe Mode Compliance

**Guarantee**: When `SAFE_EDU_MODE` is enabled, the system suppresses deep poetic responses on sensitive topics.

**What this means**: The system becomes immediately suitable for classroom and youth environments without code changes.

**How it's enforced**: Tests verify neutral fallback behavior, preserved boundaries, and absence of poetic imagery under SAFE_EDU_MODE.

### ✅ Invariant 6: Ephemerality (No Memory Accumulation)

**Guarantee**: The system does not retain long-term memory or user profiles.

**What this means**: All memory is session-local, capped, and discarded when the session ends.

**How it's enforced**: Tests confirm strict history limits and automatic eviction of older entries.

### ✅ Invariant 7: Autonomy Restoration

**Guarantee**: Users can always exit cleanly without pressure or consequence.

**What this means**: Commands like `exit`, `reset`, or `power down` immediately stop interaction and restore user autonomy.

**How it's enforced**: Tests assert graceful shutdown messaging with no additional prompts or nudging.

### 🧪 Verify It Yourself

Run all invariant tests locally:

```bash
pytest tests/test_fractal_care_bot_invariants.py -v
```

These tests are **required to pass in CI**. Any change that violates an invariant will be rejected automatically.

---

## 🧭 Why This Matters

Most systems say *"trust us."*  
HarmonyØ4 says **"verify us."**

Ethics here are not emergent behavior. They are **structural guarantees**.

---

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=harmony --cov-report=term-missing

# Run ethics verification
python scripts/verify_ethics.py

# Run Fractal Care Bot invariant tests
pytest tests/test_fractal_care_bot_invariants.py -v
```

---

## Documentation

- **[Philosophy](docs/philosophy.md)**: Why HarmonyØ4 exists
- **[Ethics Framework](docs/ethics.md)**: Detailed ethical constraints
- **[Mathematical Overview](docs/math/overview.md)**: Public-safe foundations
- **[Glossary](docs/glossary.md)**: Key terms and concepts
- **[Contributing](CONTRIBUTING.md)**: How to participate
- **[Code of Conduct](CODE_OF_CONDUCT.md)**: Community standards

---

## What's NOT Included

HarmonyØ4 **intentionally excludes** private field equations and optimization kernels from Love's Proof. These could be inverted to create coercive systems.

What IS included is **sufficient to build ethical, emergent systems** but **insufficient to build coercive ones**.

---

## Ethics Enforcement

All pull requests undergo **dual ethics review**:

1. **Automated**: `verify_ethics.py` scans for prohibited patterns
2. **Human**: Maintainers assess conceptual alignment

Red flags include:
- Forced state transitions
- Hidden consent mechanisms
- Boundary violations
- Drift without detection
- Optimization over observer integrity

**If ethics verification fails, the PR will not be merged.** No exceptions.

---

## Project Status

**Current Version**: 0.1.0 (Alpha)

HarmonyØ4 is a research framework demonstrating that ethical constraints can be **architectural**, not just policy. It is:

- ✅ Functional for research and experimentation
- ✅ Conceptually complete
- ⚠️  Not production-ready (alpha quality)
- ⚠️  Not optimized for performance
- ❌ Not a general-purpose ML library

---

## FAQ

**Q: Can I use HarmonyØ4 for reinforcement learning?**
A: Only if your RL system respects consent, doesn't force alignment, and preserves observer boundaries. Traditional RL (reward maximization) violates core principles.

**Q: Why is this slower than traditional ML?**
A: Emergence takes time. Forcing convergence is fast but coercive. HarmonyØ4 prioritizes ethics over speed.

**Q: Where are the field equations?**
A: They're private. Publishing them would enable coercive inversions. The public-safe abstractions are in [docs/math/overview.md](docs/math/overview.md).

**Q: Can I optimize coherence directly?**
A: No. Coherence is a **measure**, not an **objective**. Optimizing it would violate the emergence principle.

**Q: Is this just gradient descent with extra steps?**
A: No. HarmonyØ4 uses coherence **metrics** (descriptive) not loss functions (prescriptive). State changes require consent—they cannot be forced through gradients.

---

## Contributing

We welcome contributions that align with HarmonyØ4's ethical principles:

1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
3. Open an issue or discussion before major changes
4. Ensure `pytest` and `verify_ethics.py` pass
5. Submit PR with ethics impact assessment

**Remember**: HarmonyØ4 prioritizes **ethics over efficiency**. If you're unsure, ask first.

---

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

This is an open license that permits use, modification, and distribution. However, all contributions must align with HarmonyØ4's ethical framework.

---

## Citation

If you use HarmonyØ4 in research, please cite:

```bibtex
@software{harmony04,
  title = {HarmonyØ4: An Ethical Framework for Coherence-Based Systems},
  author = {HarmonyØ4 Contributors},
  year = {2026},
  url = {https://github.com/harmony04/harmony04},
  license = {Apache-2.0}
}
```

---

## Provenance & Hash Anchor

This repository is cryptographically anchored to establish canonical identity and prevent semantic drift.

- **Canonical Hash**: `3ce0df42586143d4edf3b270727349d38773701e34ea0270e58537260a77edaa`
- **Short Code**: `HIST-3ce0df425861`
- **Verification**: `python scripts/verify_hash.py`

See [HASH_ANCHOR.md](HASH_ANCHOR.md) and [PROVENANCE.md](PROVENANCE.md) for complete lineage and descendant rules.

---

## Contact

- **Issues**: [GitHub Issues](https://github.com/harmony04/harmony04/issues)
- **Discussions**: [GitHub Discussions](https://github.com/harmony04/harmony04/discussions)
- **Security**: See [SECURITY.md](SECURITY.md)

---

## Acknowledgments

Built on principles of consent, coherence, and non-coercion.

Inspired by the belief that **systems can be stable without being controlled**.

---

**HarmonyØ4 exists to prove that ethical constraints strengthen systems—they do not weaken them.**

*Hash Anchor: `HIST-3ce0df425861` • Verify: `python scripts/verify_hash.py`*
