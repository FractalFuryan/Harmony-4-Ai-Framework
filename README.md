# HarmonyØ4 + Heart Field Dynamics

**An open, ethical framework for modeling coherence, consent, and observer-safe systems — now with biophysical extensions for non-coercive growth.**

[![CI](https://github.com/FractalFuryan/Harmony-4-Ai-Framework/actions/workflows/ci.yml/badge.svg)](https://github.com/FractalFuryan/Harmony-4-Ai-Framework/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Hash Anchor](https://img.shields.io/badge/Hash-HIST--3ce0df425861-green.svg)](#provenance--hash-anchor)

---

## What's New (v0.3.0)

This repository now includes **Love's Proof** — a mathematical invariant for non-coercive growth, implemented across multiple domains:

- **Universal AC/DC decomposition**: signal analysis operator for separating baseline from fluctuations
- **Love's Proof invariant**: $G > 0 \wedge \dot{S} < 0 \wedge \dot{P}_{ac} \le 0$ — mathematically verified non-coercion
- **Physiological extensions**: heart field dynamics with ethical constraints
- **Domain adapters**: coupling, dialogue, and system-wide applications

---

## Mathematical Foundation

### Love's Proof Invariant (Executable Non-Coercive Ordering)

HarmonyØ4 includes an invariant nicknamed "Love's Proof." It is not presented as a
universal theorem or physical law. It is an executable, domain-agnostic sufficient
condition intended to prevent a specific failure mode: increasing order by increasing
pressure, instability, volatility, or reactive forcing.

#### Definitions

The invariant evaluates three time-series over a rolling window $W$:

- **Coherence** $C(t) \in (0, 1]$, a normalized order measure selected from canonical
  definitions per domain (see harmony/metrics/coherence.py).
- **Stress / instability** $S(t) \ge 0$, a proxy for pressure or resistance selected from
  canonical definitions (see harmony/metrics/stress.py).
- **Influence carrier** $x(t)$, a domain-chosen signal representing how influence is applied
  (coupling strength, directive pressure, control effort, etc.).

We decompose $x(t)$ into DC/AC (baseline + residual) via an EMA low-pass filter:

$$
x(t) = x_{\text{DC}}(t) + x_{\text{AC}}(t), \quad x_{\text{AC}}(t) = x(t) - x_{\text{DC}}(t)
$$

Define reactive energy (AC power):

$$
P_{\text{reactive}}(t) = \langle x_{\text{AC}}(t)^2 \rangle_W
$$

Define coherence growth rate:

$$
G(t) = \frac{d}{dt} \log(C(t) + \epsilon)
$$

#### Invariant (Sufficient Condition)

Over window $W$:

$$
\langle G \rangle_W > 0 \quad \wedge \quad \langle \dot{S} \rangle_W < 0 \quad \wedge \quad
\langle \dot{P}_{\text{reactive}} \rangle_W \le 0
$$

Interpretation:

- Coherence must increase (in log-growth sense),
- while stress decreases,
- and reactive influence energy does not ramp up.

This is a sufficient filter. Passing it does not prove optimality or correctness.
Failing it is treated as a red flag that order may be rising through pressure or
volatility.

#### Explicit Metric Requirement

$C(t)$ and $S(t)$ are not free variables. Each subsystem must declare which canonical
metric definition it uses. This is enforced by code boundaries and tests to reduce
metric gaming.

#### Auditability

The implementation clamps coherence to at least $\epsilon$ for numerical stability and
returns an audit flag `clamped_C` whenever clamping occurred. Clamping is not hidden,
and downstream systems may fail runs if clamping frequency exceeds a policy threshold.

### AC/DC Decomposition Operator

Any signal $x(t)$ decomposes as:

$$
x(t) = x_{\text{DC}}(t) + x_{\text{AC}}(t)
$$

- **DC**: low-pass filtered baseline (long-term load, traits)
- **AC**: high-frequency fluctuations (reactivity, immediate state)

Implemented via EMA filter: `x_dc = ema_lpf(x, alpha)`

---

## Architecture

```
harmony/
├── core/                    # Original HarmonyØ4
├── ops/                     # Mathematical operators
│   └── acdc.py              # AC/DC decomposition
├── invariants/              # Ethical invariants
│   ├── loves_proof.py       # Universal non-coercion
│   ├── non_coercion.py      # Base non-coercion
│   ├── consent_locking.py   # Consent-as-locking invariant
│   └── growth_bounds.py     # Bounded growth laws
├── physiology/              # Biophysical extensions
│   ├── heart/               # Heart field dynamics
│   │   ├── preprocessing.py
│   │   ├── analytic.py
│   │   ├── coherence.py
│   │   ├── entrainment.py
│   │   ├── stress.py
│   │   ├── field_score.py
│   │   └── loves_proof.py   # Physiology adapter
│   └── shared/
│       └── phase_tools.py
├── coupling/                # Coupling dynamics
│   └── loves_proof.py       # Entrainment adapter
└── dialogue/                # Linguistic influence
    └── loves_proof.py       # Dialogue adapter
```

---

## Quick Start

### Installation

```bash
git clone https://github.com/FractalFuryan/Harmony-4-Ai-Framework.git
cd Harmony-4-Ai-Framework
pip install -e ".[dev]"
```

### Example: Heart Field Analysis

```python
import numpy as np
from harmony.physiology.heart import HeartFieldScorer
from harmony.invariants.loves_proof import LovesProofInvariant

# Simulated physiological data
fs = 250.0
t = np.arange(0, 300, 1 / fs)  # 5 minutes
heart_coherence = 0.3 + 0.5 * (1 - np.exp(-t / 100))
stress = 0.8 - 0.6 * (t / t[-1])
heart_amplitude = 1.0 + 0.1 * np.sin(2 * np.pi * t / 10)

# Check Love's Proof
invariant = LovesProofInvariant()
result = invariant.check(t, heart_coherence, stress, heart_amplitude)

print(f"Love's Proof holds: {result['invariant_holds']}")
print(f"Coherence growth: {result['G_mean']:.3f}")
print(f"Stress trend: {result['S_slope']:.3f}")
```

See a full walkthrough in [examples/heart_field_basic_usage.py](examples/heart_field_basic_usage.py).

### Example: AC/DC Analysis

```python
import numpy as np
from harmony.ops.acdc import acdc_split, ac_power

signal = np.random.randn(1000) + 2.0
dc_component, ac_component = acdc_split(signal, alpha=0.02)

print(f"DC mean: {np.mean(dc_component):.3f}")
print(f"AC power: {ac_power(ac_component):.3f}")
print(f"Signal = DC + AC: {np.allclose(signal, dc_component + ac_component)}")
```

---

## Research Applications

1. **Biofeedback & heart coherence training**
2. **Interpersonal physiology with consent-aware entrainment**
3. **Ethical AI & dialogue systems**
4. **System dynamics & non-coercive control**

---

## Testing & Verification

```bash
# Mathematical validation suite
python run_math_tests.py

# Full test suite with coverage gate
pytest --cov=harmony --cov-report=term-missing --cov-fail-under=85

# Verify ethical constraints
python scripts/verify_ethics.py
```

---

## Mathematical Validation

All components are mathematically verified:

1. **AC/DC properties**: linearity, reconstruction, frequency separation
2. **Love's Proof invariants**: scale invariance, time translation, continuity
3. **Edge cases**: zero coherence, constant signals, discontinuities
4. **System models**: harmonic oscillators, Lotka-Volterra, Kuramoto

See [tests/math/](tests/math/) for the complete validation suite.

---

## API Highlights

- `harmony.ops.acdc`: `acdc_split()`, `ema_lpf()`, `ac_power()`
- `harmony.invariants.loves_proof`: `LovesProofInvariant`
- `harmony.physiology.heart`: `HeartFieldScorer`, `PhysiologyLovesProof`
- `harmony.coupling.loves_proof`: `CouplingLovesProof`
- `harmony.dialogue.loves_proof`: `DialogueLovesProof`

---

## Citing This Work

### Framework Citation

```bibtex
@software{harmony04,
  title = {HarmonyØ4: An Ethical Framework for Coherence-Based Systems},
  author = {HarmonyØ4 Contributors},
  year = {2024},
  url = {https://github.com/harmony04/harmony04},
  note = {With Love's Proof extensions for non-coercive growth}
}
```

### Mathematical Extensions

```bibtex
@software{harmony04_lovesproof,
  title = {Love's Proof: A Mathematical Invariant for Non-Coercive Growth},
  author = {FractalFuryan and HarmonyØ4 Contributors},
  year = {2024},
  url = {https://github.com/FractalFuryan/Harmony-4-Ai-Framework},
  note = {AC/DC decomposition and universal non-coercion invariant}
}
```

---

## Research Status

**Current version**: 0.3.0 (Research Beta)

- **Mathematically verified**: core invariants proven
- **Ethically constrained**: DAVNA principles maintained
- **Domain extensible**: physiology, coupling, dialogue adapters
- **Experimental validation**: single-subject studies in progress
- **Performance**: research-ready, not production-optimized

---

## Contributing

We welcome contributions that align with:

1. **Mathematical rigor**: extensions must be mathematically sound
2. **Ethical alignment**: must respect DAVNA Covenant principles
3. **Test coverage**: comprehensive tests for new functionality
4. **Documentation**: clear mathematical and ethical documentation

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## Links

- **Documentation**: [docs/math/extensions.md](docs/math/extensions.md)
- **Tests**: [tests/math/](tests/math/)
- **Examples**: [examples/](examples/)
- **Ethics**: [DAVNA_COVENANT.md](DAVNA_COVENANT.md)

---

**Love's Proof**: order emerges without force, stability without coercion, growth without exploitation.

*Hash Anchor: `HIST-3ce0df425861-lovesproof-v0.3.0`*

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

**What this means**: Switching modes affects only Kat's interpretive layer and never alters Missy's observations or system behavior.

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
