# Mathematical Notation Guide

## Symbol Reference

### Greek Letters

| Symbol | Meaning | Context |
|--------|---------|---------|
| $\Phi$ | Phase coherence | Coherence metrics |
| $\theta$ | Phase angle | Phase dynamics |
| $\omega$ | Natural frequency | Observer oscillations |
| $\lambda$ | Weighting parameter | Lyapunov functions |
| $\epsilon$ | Threshold value | Drift detection |
| $\Delta$ | Change/difference | Elasticity, drift |

### Latin Letters

| Symbol | Meaning | Context |
|--------|---------|---------|
| $B$ | Boundary integrity | Observer boundaries |
| $C$ | Consent relation | Consent formalism |
| $D$ | Drift measure | Drift detection |
| $E$ | Role elasticity | Role dynamics |
| $F$ | External influence | Elasticity calculations |
| $H$ | Entropy | Information theory |
| $I$ | Mutual information | Boundary metrics |
| $K$ | Coupling strength | Phase-locked coupling |
| $N$ | Number of components | Coherence averaging |
| $P$ | Projection operator | Witness transformations |
| $r$ | Role state vector | Role dynamics |
| $s$ | System state | General state |
| $t$ | Time | Temporal evolution |
| $V$ | Lyapunov function | Stability analysis |
| $W$ | Witness projection | Observer transformations |

### Calligraphic Letters

| Symbol | Meaning | Context |
|--------|---------|---------|
| $\mathcal{O}$ | Observer | Observer boundaries, transformations |
| $\mathcal{E}$ | Entity set | Consent relations |
| $\mathcal{A}$ | Action set | Consent formalism |

### Operators and Relations

| Symbol | Meaning | Example |
|--------|---------|---------|
| $\to$ | Maps to / transforms to | $C: \mathcal{E} \to \{\text{grant}, \text{deny}\}$ |
| $\Rightarrow$ | Implies | $D > \epsilon \Rightarrow$ Alert |
| $\not\Rightarrow$ | Does not imply | Non-transitivity |
| $\iff$ | If and only if | Logical equivalence |
| $\land$ | Logical AND | Consent chaining |
| $\lor$ | Logical OR | Alternative conditions |
| $\forall$ | For all | Universal quantification |
| $\exists$ | There exists | Existential quantification |
| $\|\cdot\|$ | Absolute value / norm | Magnitude |
| $\lim$ | Limit | Convergence analysis |
| $\frac{d}{dt}$ | Time derivative | Temporal evolution |
| $\bigg\|_{\text{constraint}}$ | Evaluated under constraint | Conditional evaluation |

### Set Notation

| Symbol | Meaning | Example |
|--------|---------|---------|
| $\in$ | Element of | $e \in \mathcal{E}$ |
| $\times$ | Cartesian product | $\mathcal{E} \times \mathcal{E}$ |
| $\{\cdot\}$ | Set builder | $\{\text{grant}, \text{deny}\}$ |

## Subscripts and Superscripts

### Subscripts

| Notation | Meaning |
|----------|---------|
| $\theta_i$ | Phase of component $i$ |
| $\bar{\theta}$ | Mean phase |
| $B_{\min}$ | Minimum boundary value |
| $\Phi_{\text{baseline}}$ | Baseline coherence |
| $t_0$ | Initial time |
| $t_r$ | Revocation time |
| $\mathcal{O}_{\text{internal}}$ | Internal observer state |
| $\mathcal{O}_{\text{external}}$ | External observer state |

### Superscripts

Generally avoided to prevent confusion with exponentiation. When used:

| Notation | Meaning |
|----------|---------|
| $C_t$ | Consent at time $t$ |

## Common Patterns

### Coherence Measurement

$$
\Phi(s) = \frac{1}{N} \sum_{i=1}^{N} \cos(\theta_i - \bar{\theta})
$$

**Read as**: "Phase coherence of state $s$ is the average cosine of deviations from mean phase."

### Consent Check

$$
C(e_1, e_2, a) = \text{grant}
$$

**Read as**: "Entity $e_1$ grants consent to entity $e_2$ for action $a$."

### Boundary Preservation

$$
\frac{dB}{dt} \geq 0
$$

**Read as**: "The time derivative of boundary integrity must be non-negative" (boundary cannot degrade without consent).

### Drift Alert

$$
D_\Phi(t) > \epsilon_\Phi \Rightarrow \text{Alert}
$$

**Read as**: "If phase drift exceeds threshold, trigger alert."

## Conventions

### Naming

- **Uppercase Greek**: Global metrics ($\Phi$, $\Delta$)
- **Lowercase Greek**: Component properties ($\theta$, $\omega$)
- **Uppercase Latin**: Operators, functions ($C$, $B$, $V$)
- **Lowercase Latin**: State variables ($r$, $s$, $t$)
- **Calligraphic**: Sets and observers ($\mathcal{O}$, $\mathcal{E}$)

### Temporal Evolution

- $x(t)$: State at time $t$
- $\frac{dx}{dt}$: Rate of change
- $x_0$: Initial state
- $x_{\text{final}}$: Terminal state

### Constraints

Constraints are written as:

$$
f(x) \bigg|_{g(x) = 0}
$$

**Read as**: "Function $f$ of $x$, subject to constraint $g(x) = 0$."

## Avoiding Ambiguity

### Absolute Value vs. Norm

- $|x|$: Absolute value (scalar)
- $\|x\|_2$: Euclidean norm (vector)
- $\|x\|_1$: Manhattan norm (vector)

### Parentheses for Clarity

- Use $\sin(\theta)$, not $\sin\theta$
- Use $\cos(\theta_i - \bar{\theta})$, not $\cos \theta_i - \bar{\theta}$

### Evaluation Order

When multiple operators appear:

$$
\frac{dV}{dt} = \frac{d}{dt}\left(-\Phi(\mathcal{O}) + \lambda D_B(\mathcal{O})\right)
$$

Parentheses make clear that the derivative applies to the entire expression.

## Further Reading

- **Mathematical overview**: [overview.md](overview.md)
- **Glossary of terms**: [../glossary.md](../glossary.md)

---

**This notation is designed for clarity and precision. When in doubt, prefer explicit notation over abbreviated forms.**
