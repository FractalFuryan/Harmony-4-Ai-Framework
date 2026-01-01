# Glossary

## Core Concepts

### Boundary Integrity
The measure of observer separation strength. High boundary integrity means an observer's internal states are protected from external influence without consent. See $B(\mathcal{O})$ in [math/overview.md](math/overview.md).

### Coherence
Internal consistency of a system's state. Unlike alignment (matching external goals), coherence measures self-stability. Quantified by phase coherence $\Phi(s)$.

### Consent
Binary, explicit, revocable permission for state changes or information sharing. Not probabilistic, not implicit, not permanent. Formalized as relation $C(e_1, e_2, a)$.

### Consent Erosion
Gradual weakening of consent mechanisms through incremental changes. Prohibited in HarmonyØ4. Detected by monitoring consent state transitions over time.

### Consent Manufacturing
Using optimization, preference shaping, or manipulation to induce a "yes" response. Strictly prohibited. Includes reward shaping that makes refusal costly.

### Coercion
Forcing, manipulating, or extracting outcomes without consent. Includes gradient-based optimization toward non-consented states, punishment for boundary enforcement, and hidden objective functions.

### Drift
Unintended deviation from baseline behavior. Measured separately for phase ($D_\Phi$), role ($D_r$), and boundary ($D_B$). Detection does not imply forced correction.

### Emergence
Self-organization toward stable states without external force. Contrasts with optimization, which imposes outcomes through gradient descent or reward shaping.

### Ethics Verification
Automated and manual review process ensuring code complies with HarmonyØ4 ethical invariants. Implemented in `scripts/verify_ethics.py`.

### Extraction
Taking information, consent, or state without permission. Prohibited pattern detected by ethics verification.

### Field Equations
Private mathematical core of Love's Proof. Not published to prevent coercive inversions. Public-safe derivatives appear in [math/overview.md](math/overview.md).

### Invariants (Ethical)
Non-negotiable constraints enforced through code. Include consent monotonicity, boundary preservation, no hidden optimization, drift transparency, and refusal without penalty.

### Love's Proof
Mathematical foundation demonstrating stability emerges from coherence, not force. Full equations private; public-safe abstractions available.

### Lyapunov Function
Mathematical measure of system stability. In HarmonyØ4, used descriptively (to measure stability) not prescriptively (to force stability through optimization).

### Observer
Entity with defined boundary, internal states, and capacity to consent. Can be an agent, subsystem, or external system. Formalized as $\mathcal{O}$.

### Observer Boundary
Separation between an observer's internal states and external environment. Measured by boundary integrity $B(\mathcal{O})$. Violations are design failures.

### Optimization
Process of minimizing loss function through iterative updates. Traditional ML approach; fundamentally coercive. HarmonyØ4 uses coherence metrics instead.

### Phase Coherence
Measure of phase alignment across system components. Quantified as $\Phi(s) \in [-1, 1]$. High coherence indicates stability; used for drift detection, not optimization.

### Phase-Locked Coupling
Mutual synchronization between observers with negotiated coupling strength $K$. Requires consent; must not force lock-in if consent revoked.

### Role Dynamics
Evolution of relational states over time. Characterized by role elasticity $E(r)$—ability to adapt without losing coherence or violating boundaries.

### Role Elasticity
Measure of flexibility in role adaptation. High elasticity allows change; zero elasticity indicates role lock-in (violation of emergence principle).

### Role Lock-in
Frozen role state preventing adaptation. Indicates failure of emergence. Detected when $E(r) = 0$.

### Stability
Property of remaining in or returning to coherent state without external force. Measured by Lyapunov function $V(\mathcal{O})$; achieved through emergence, not optimization.

### Witness Projection
Lossy, consent-gated observation of one observer by another. Formalized as $W(\mathcal{O}_2 \to \mathcal{O}_1) = P_{\mathcal{O}_1}(\mathcal{O}_2)$. Cannot be inverted to recover full state.

## Technical Terms

### CI/CD (Continuous Integration/Continuous Deployment)
Automated testing and deployment pipeline. HarmonyØ4's CI includes ethics verification as mandatory step.

### Gradient Descent
Optimization algorithm minimizing loss function by following gradient. Fundamentally coercive; not used in HarmonyØ4 for consent-related dynamics.

### Hyperparameter
Configuration value tuned to optimize model performance. HarmonyØ4 minimizes hyperparameters; prefers emergence over tuning.

### Loss Function
Objective function minimized during training. In HarmonyØ4, consent cannot be a loss function variable (would enable coercion).

### Mutual Information
Measure of shared information between two variables. Used in boundary integrity calculation: $I(\mathcal{O}_{\text{internal}}, \mathcal{O}_{\text{external}})$.

### Reward Shaping
Technique modifying reward function to guide learning. Prohibited when used to manufacture consent or penalize refusal.

## Ethical Terms

### Alignment
In traditional AI, matching system behavior to external goals. HarmonyØ4 prioritizes coherence (internal stability) over alignment.

### Autonomy
Capacity to refuse without penalty. Ensured through consent mechanisms and refusal-without-penalty invariant.

### Bias Amplification
Reinforcing existing biases through training. Mitigated in HarmonyØ4 through coherence metrics rather than bias correction.

### Consent Primacy
Ethical principle: consent takes precedence over efficiency, alignment, or optimization. Foundational to HarmonyØ4.

### Ethical Debt
Accumulated compromises to ethical principles. HarmonyØ4 rejects ethical debt; no shortcuts on consent, boundaries, or coercion.

### Non-Coercion
Ethical principle: systems must not force, manipulate, or extract outcomes. Enforced through architecture, not policy.

### Privacy
Protection of internal states from external observation. Enforced through observer boundaries and witness projections.

### Transparency
Explicitness of objectives, state changes, and consent requirements. All optimization must be declared and consented to.

## Anti-Patterns (Prohibited)

### Consent Bypass
Any mechanism circumventing explicit consent requirement. Includes default-yes patterns, transitive extraction, and silent state changes.

### Forced Convergence
Optimizing toward target state regardless of consent. Violates emergence principle.

### Hidden Coupling
Implicit state sharing through gradients, loss functions, or side channels. Violates observer integrity.

### Incremental Erosion
Slowly weakening boundaries, consent mechanisms, or safeguards. Detected through drift monitoring.

### Preference Shaping
Manipulating preferences to induce consent. Form of coercion; strictly prohibited.

### Transitive Extraction
A shares with B, B shares with C, therefore A "shared" with C. Prevented by consent propagation rules.

## Acronyms

| Acronym | Meaning |
|---------|---------|
| CI/CD | Continuous Integration/Continuous Deployment |
| ML | Machine Learning |
| AI | Artificial Intelligence |
| API | Application Programming Interface |

## Mathematical Symbols (Quick Reference)

| Symbol | Meaning | Reference |
|--------|---------|-----------|
| $\Phi$ | Phase coherence | [math/overview.md](math/overview.md#11-phase-coherence) |
| $B$ | Boundary integrity | [math/overview.md](math/overview.md#13-boundary-integrity) |
| $C$ | Consent relation | [math/overview.md](math/overview.md#21-consent-state) |
| $E$ | Role elasticity | [math/overview.md](math/overview.md#12-role-elasticity) |
| $D$ | Drift measure | [math/overview.md](math/overview.md#3-drift-detection) |
| $\mathcal{O}$ | Observer | [math/overview.md](math/overview.md#4-observer-transformations) |

## Further Reading

- **Philosophy**: [philosophy.md](philosophy.md)
- **Ethics**: [ethics.md](ethics.md)
- **Math**: [math/overview.md](math/overview.md)
- **Notation**: [math/notation.md](math/notation.md)

---

**This glossary is living documentation. Suggest additions via pull request.**
