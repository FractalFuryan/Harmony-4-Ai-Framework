# Mathematical Extensions to HarmonyO4

## Overview

HarmonyO4 version 0.2.0 extends the core ethical framework with:

1. Generalized ethical invariants
2. Physiological instantiations
3. Domain-agnostic tools for oscillatory systems

## New Invariants

### 1. Non-coercion Invariant

```python
from harmony.invariants.non_coercion import NonCoercionInvariant

invariant = NonCoercionInvariant()
result = invariant.check(coherence_series, stress_series, time_points)
```

Mathematical form:

$G > 0 \wedge dS/dt < 0$

where $G = d/dt \log(\text{coherence} + \epsilon)$.

### 2. Consent-as-Locking Invariant

```python
from harmony.invariants.consent_locking import ConsentLockingInvariant

invariant = ConsentLockingInvariant()
result = invariant.check_consent(
    coupling_strength=K,
    frequency_difference=delta_omega,
    receiver_threshold=theta,
)
```

Mathematical form:

$|\Delta \omega| < K \wedge K > \theta$

### 3. Growth Bounds Invariant

```python
from harmony.invariants.growth_bounds import GrowthBoundsInvariant

invariant = GrowthBoundsInvariant()
result = invariant.check_boundedness(state_series, time_points)
```

Mathematical forms:

- Logistic: $dx/dt = \alpha x(1 - x)$
- Gompertz: $dx/dt = \alpha x \log(1/x)$

## Physiological Implementations

```python
from harmony.physiology.heart import HeartFieldScorer

scorer = HeartFieldScorer(fs=250.0)
results = scorer.compute_net_field(...)
constraint_check = scorer.compute_non_coercion_check(...)
```

## Mathematical Primitives

```python
from harmony.physiology.shared import phase_tools

amplitude, phase = phase_tools.compute_analytic_signal(x, fs)
coherence = phase_tools.compute_phase_concentration(phase)
plv = phase_tools.compute_phase_lock_value(phase1, phase2)
```

## Verification

All new code is verified through unit tests and integration tests, with ethics
checks in scripts such as scripts/verify_ethics.py.

## Hash Anchor

HIST-3ce0df425861-ephys-v0.2.0
