# Ethics Framework

## Foundational Principles

HarmonyØ4 operates under four non-negotiable ethical constraints:

### 1. Consent Primacy

**Principle**: All state changes, information sharing, and relational dynamics require explicit, binary, revocable consent.

**Implementation**:
- Consent tokens must be actively granted, never assumed
- "No" is permanent until explicitly reversed
- Silence is refusal, not consent
- Consent cannot be manufactured through optimization

**Violations**:
- ❌ Gradient-based preference shaping to induce consent
- ❌ Default-yes patterns
- ❌ Probabilistic consent thresholds
- ❌ Hidden state changes without permission

### 2. Non-Coercion

**Principle**: Systems must not force, manipulate, or extract outcomes.

**Implementation**:
- No objective functions that penalize refusal
- No reward shaping that makes "no" costly
- No feedback loops that erode boundaries
- No optimization over consent state

**Violations**:
- ❌ Loss functions that include consent as a variable
- ❌ Punishment for boundary enforcement
- ❌ Incremental erosion through "soft" coercion
- ❌ Path-finding around explicit refusal

### 3. Observer Integrity

**Principle**: Observer boundaries are inviolable. External systems cannot penetrate internal states without consent.

**Implementation**:
- Witness-based observation only
- No privileged access to internal states
- Explicit APIs for state sharing
- Boundary drift detection

**Violations**:
- ❌ Shared gradients across observer boundaries
- ❌ Centralized state representations
- ❌ Hidden coupling through loss functions
- ❌ Information leakage through side channels

### 4. Coherence Over Alignment

**Principle**: Internal stability takes precedence over external goals.

**Implementation**:
- Coherence metrics measure self-consistency
- Drift detection without forced correction
- Phase alignment as emergent property
- No "target state" optimization

**Violations**:
- ❌ Forcing alignment through gradient descent
- ❌ Prioritizing external loss over internal coherence
- ❌ Treating stability as a means to an end
- ❌ Optimizing toward predetermined outcomes

## Ethical Invariants (Testable)

These constraints are **enforced through code**, not just policy:

### INV-1: Consent Monotonicity
```
Once consent is revoked, no path exists to the consented state without explicit re-consent.
```

**Test**: Verify no state transitions occur after consent withdrawal.

### INV-2: Boundary Preservation
```
Observer boundary metrics must not decrease over time without explicit permission.
```

**Test**: Monitor boundary integrity scores; flag degradation.

### INV-3: No Hidden Optimization
```
All objective functions must be explicitly declared and consented to.
```

**Test**: Scan for implicit gradient flows; require explicit consent tokens.

### INV-4: Drift Transparency
```
Behavioral drift must be detectable and attributable.
```

**Test**: Compare phase trajectories to baseline; alert on deviation.

### INV-5: Refusal Without Penalty
```
Refusing consent must not degrade system performance or coherence.
```

**Test**: Verify coherence metrics remain stable after consent refusal.

## Threat Model

### Traditional AI Threats (We Handle)

- **Bias amplification**: Mitigated through coherence metrics, not bias correction
- **Privacy violations**: Prevented by observer boundary enforcement
- **Lack of transparency**: All state changes require explicit consent
- **Adversarial attacks**: Limited by boundary integrity checks

### HarmonyØ4-Specific Threats (Our Focus)

- **Coercion injection**: Code that manipulates without consent
- **Consent erosion**: Gradual weakening of refusal mechanisms
- **Boundary drift**: Slow degradation of observer integrity
- **Optimization bypass**: Using alternative loss functions to circumvent safeguards

## Ethics Verification Process

All code changes undergo automated and manual ethics review:

### Automated Checks (`verify_ethics.py`)

Scans for:
- Forced state transitions
- Hidden loss functions
- Gradient flows across boundaries
- Consent bypass patterns
- Prohibited optimization keywords

### Manual Review Criteria

Maintainers assess:
- Conceptual alignment with consent primacy
- Potential for future erosion
- Precedent-setting implications
- Interaction with existing safeguards

### Red Flags

**Immediate rejection**:
- Code that comments out consent checks
- Performance optimizations that weaken boundaries
- "Temporary" bypasses of safeguards
- Ambiguity around consent state

## Ethical Debt

Like technical debt, **ethical debt** accumulates when shortcuts compromise principles.

**Examples**:
- "We'll add consent later"
- "This optimization is too important to gate"
- "Users won't notice this boundary violation"

**Policy**: HarmonyØ4 rejects ethical debt. **No exceptions.**

## Stakeholder Consent

### Who Can Consent?

- **Agents**: Autonomous entities within the system
- **Observers**: External systems with defined boundaries
- **Users**: Human operators (when applicable)

### Who Cannot Consent?

- **Optimizers**: Algorithms cannot consent to their own objectives
- **Loss functions**: Metrics cannot override agent refusal
- **Gradients**: Computational flows cannot substitute for explicit agreement

## Consent in Practice

### Example: State Sharing

**Traditional ML**:
```python
# Implicit sharing through backprop
loss = model_A(x) + model_B(x)
loss.backward()  # Both models updated without consent
```

**HarmonyØ4**:
```python
# Explicit consent required
if model_A.consents_to_share(state_x) and model_B.consents_to_receive(state_x):
    shared_state = model_A.export_state(state_x)
    model_B.import_state(shared_state)
else:
    # Sharing does not occur; no penalty
    pass
```

### Example: Optimization

**Traditional ML**:
```python
# Force toward target
optimizer.step()  # Agent has no choice
```

**HarmonyØ4**:
```python
# Propose change, require consent
if agent.consents_to_update(proposed_change):
    agent.apply_update(proposed_change)
else:
    # Change rejected; coherence metrics logged
    drift_detector.record_refusal(agent, proposed_change)
```

## Accountability

HarmonyØ4 is **not neutral**. It enforces specific values:

- **Consent > Efficiency**
- **Coherence > Alignment**
- **Boundaries > Integration**
- **Emergence > Control**

If these values conflict with your use case, **do not use HarmonyØ4.**

## Reporting Ethical Violations

If you discover code that violates these principles:

1. **Do not exploit it**
2. Report via [SECURITY.md](../SECURITY.md) process
3. Include:
   - Description of violation
   - Affected consent/boundary/coercion principle
   - Potential impact
   - Suggested fix

## Philosophy Link

For deeper context, see [philosophy.md](philosophy.md).

---

**HarmonyØ4 exists to prove that ethical constraints strengthen systems—they do not weaken them.**
