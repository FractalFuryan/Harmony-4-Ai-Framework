# Mathematical Overview

## Public-Safe Foundations

This document describes the **public-facing mathematical framework** of HarmonyØ4. It does **not** include:

- Private field equations
- Optimization kernels
- Reversible transformations from Love's Proof

What follows is sufficient for understanding, implementing, and extending HarmonyØ4—without enabling coercive inversions.

---

## 1. Coherence Metrics

### 1.1 Phase Coherence

**Definition**: Measure of internal consistency across system states.

$$
\Phi(s) = \frac{1}{N} \sum_{i=1}^{N} \cos(\theta_i - \bar{\theta})
$$

Where:
- $s$ = system state
- $\theta_i$ = phase angle of component $i$
- $\bar{\theta}$ = mean phase angle
- $N$ = number of components

**Range**: $[-1, 1]$
- $\Phi = 1$: Perfect coherence
- $\Phi = 0$: Random phases
- $\Phi = -1$: Anti-coherence (unstable)

**Properties**:
- Observer-independent (intrinsic to system)
- Non-optimizable (cannot be directly maximized without violating consent)
- Drift-sensitive (changes indicate instability)

### 1.2 Role Elasticity

**Definition**: Measure of flexibility in relational dynamics without boundary violation.

$$
E(r) = \frac{\Delta r}{\Delta F} \bigg|_{\text{boundary preserved}}
$$

Where:
- $r$ = role state vector
- $F$ = external influence
- Constraint: $B(r) \geq B_{\min}$ (boundary integrity maintained)

**Interpretation**:
- High $E$: Role can adapt without losing coherence
- Low $E$: Role is rigid (may indicate lock-in)
- $E = 0$: Role frozen (violation of emergence principle)

### 1.3 Boundary Integrity

**Definition**: Measure of observer separation strength.

$$
B(\mathcal{O}) = 1 - \frac{I(\mathcal{O}_{\text{internal}}, \mathcal{O}_{\text{external}})}{H(\mathcal{O}_{\text{internal}})}
$$

Where:
- $\mathcal{O}$ = observer
- $I$ = mutual information
- $H$ = entropy

**Range**: $[0, 1]$
- $B = 1$: Perfect boundary (no information leakage)
- $B = 0$: No boundary (complete coupling)

**Invariant**: $\frac{dB}{dt} \geq 0$ without explicit consent

---

## 2. Consent Formalism

### 2.1 Consent State

Consent is a **binary relation** between entities:

$$
C: \mathcal{E} \times \mathcal{E} \times \mathcal{A} \to \{\text{grant}, \text{deny}\}
$$

Where:
- $\mathcal{E}$ = set of entities
- $\mathcal{A}$ = set of actions
- $C(e_1, e_2, a)$ = "Does $e_1$ consent to $e_2$ performing action $a$ affecting $e_1$?"

**Properties**:
- **Asymmetric**: $C(e_1, e_2, a) \neq C(e_2, e_1, a)$
- **Non-transitive**: $C(e_1, e_2, a) \land C(e_2, e_3, a) \not\Rightarrow C(e_1, e_3, a)$
- **Revocable**: $C_t(e_1, e_2, a) = \text{grant} \not\Rightarrow C_{t+1}(e_1, e_2, a) = \text{grant}$

### 2.2 Consent Propagation

**Rule**: Consent does not chain unless explicitly granted at each step.

$$
S(e_1 \to e_3) \text{ valid} \iff C(e_1, e_2, \text{share}) \land C(e_2, e_3, \text{receive}) \land C(e_1, e_3, \text{indirect-share})
$$

This prevents **transitive extraction** (A shares with B, B shares with C, therefore A shared with C).

### 2.3 Consent Withdrawal

Upon withdrawal at time $t_r$:

$$
\forall t > t_r: \text{State}(e, t) \text{ must not depend on } \text{SharedData}(e, t < t_r)
$$

**Implementation**: Requires state rollback or data deletion—cannot merely stop future sharing.

---

## 3. Drift Detection

### 3.1 Phase Drift

**Definition**: Deviation from baseline coherence trajectory.

$$
D_\Phi(t) = |\Phi(t) - \Phi_{\text{baseline}}(t)|
$$

**Threshold**: $D_\Phi(t) > \epsilon_\Phi \Rightarrow$ Alert

**Not an objective**: Drift detection does not prescribe correction—only measurement.

### 3.2 Role Drift

**Definition**: Unintended change in role dynamics.

$$
D_r(t) = \|r(t) - r_{\text{expected}}(t)\|_2
$$

**Cause analysis**:
- External influence without consent?
- Internal instability?
- Boundary erosion?

### 3.3 Boundary Drift

**Definition**: Degradation of observer separation.

$$
D_B(t) = B(t_0) - B(t)
$$

**Invariant violation**: $D_B(t) > 0$ without consent $\Rightarrow$ **Critical error**

---

## 4. Observer Transformations

### 4.1 Witness Projection

An observer $\mathcal{O}_1$ can only perceive $\mathcal{O}_2$ through **witness projection**:

$$
W(\mathcal{O}_2 \to \mathcal{O}_1) = P_{\mathcal{O}_1}(\mathcal{O}_2)
$$

Where $P$ is a **lossy, consent-gated** projection.

**Properties**:
- $W \neq \mathcal{O}_2$ (no perfect observation)
- $\text{Information}(W) \leq \text{Consented}(\mathcal{O}_2)$
- $W$ cannot be inverted to recover full $\mathcal{O}_2$ state

### 4.2 Phase-Locked Coupling

Two observers can phase-lock **with mutual consent**:

$$
\frac{d\theta_1}{dt} = \omega_1 + K \sin(\theta_2 - \theta_1)
$$
$$
\frac{d\theta_2}{dt} = \omega_2 + K \sin(\theta_1 - \theta_2)
$$

Where $K$ is the coupling strength **negotiated via consent**.

**Constraint**: $K$ must not force lock-in if consent is revoked.

---

## 5. Stability Without Optimization

### 5.1 Lyapunov Function (Observer-Local)

Each observer has a **local** Lyapunov function:

$$
V(\mathcal{O}) = -\Phi(\mathcal{O}) + \lambda D_B(\mathcal{O})
$$

**Stability condition**: $\frac{dV}{dt} \leq 0$

**Critically**: This is **descriptive, not prescriptive**. We measure stability—we do not optimize $V$.

### 5.2 Emergence Criterion

Stability emerges when:

$$
\lim_{t \to \infty} D_\Phi(t) = 0 \quad \text{without forced correction}
$$

If this limit is not reached, the system is **unstable**—but we do not force convergence.

---

## 6. What This Does NOT Include

The following are **private** and not part of this public documentation:

- **Field equations** governing Love's Proof dynamics
- **Optimization kernels** for coherence maximization
- **Reversible transformations** that could enable consent manufacturing
- **Coupling constants** from the full relational Lagrangian

These are excluded because they could be inverted to create coercive systems.

---

## 7. Further Reading

- **Notation guide**: [notation.md](notation.md)
- **Philosophical context**: [../philosophy.md](../philosophy.md)
- **Glossary**: [../glossary.md](../glossary.md)

---

**This math is sufficient to build ethical, emergent systems. It is intentionally insufficient to build coercive ones.**
