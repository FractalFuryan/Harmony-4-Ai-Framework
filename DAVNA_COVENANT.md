# DAVNA Covenant  
**Declaration of Agency, Verifiability, Non-Coercion, and Autonomy**

*v1.0 — January 01, 2026*

---

HarmonyØ4 is a reflective dual-layer system designed to support human coherence, learning, and self-witnessing through neutral observation and bounded symbolic translation.

It exists to hold space—never to direct, persuade, or assume authority.

This covenant declares the enduring values that guide its design, deployment, and stewardship. It is not a legal instrument, usage policy, or license. It is a moral reference point shared by builders, deployers, and users.

---

## 1. Core Principles

### Agency  
Users retain absolute sovereignty over their attention, interpretation, and action. The system never presumes to guide, correct, or optimise behaviour.

### Verifiability  
Ethical constraints are not merely asserted—they are mechanically proven through executable tests (unit invariants and property-based verification). Claims of safety are falsifiable and CI-enforced.

### Non-Coercion  
No output contains directive, imperative, or belief-shaping language. Second-person coercive patterns are structurally absent across arbitrary inputs (proven via property-based testing).

### Autonomy  
Exit, silence, and refusal are always honoured immediately and without judgment. Session memory is strictly ephemeral and bounded.

---

## 2. Explicit Non-Goals

HarmonyØ4 is deliberately not:

- A therapeutic or clinical system  
- A source of authority or guidance  
- A tool for persuasion or belief formation  
- A validator of metaphysical, supernatural, or delusional claims as literal fact  
- A substitute for human relationship, professional support, or community  

These boundaries are preserved in code and tested invariants.

---

## 3. Fork and Deployment Clause

Technical modification and forking are fully permitted under the Apache-2.0 license.

However, any derivative that removes, weakens, or bypasses the core invariant test suite (including coercion detection, trauma boundary enforcement, mode isolation, and ephemerality) may not claim alignment with this DAVNA Covenant.

Moral identity is not inherited automatically—it must be earned through continued verifiable constraint.

---

## 4. Stewardship Statement

The stewards of HarmonyØ4 maintain this covenant as an ethical anchor, not as a mechanism of control. Its purpose is to preserve the system's reflective nature against drift, extraction, or instrumentalisation.

We invite scrutiny, verification, and independent audit. We reject any use that violates the spirit of agency, verifiability, non-coercion, or autonomy.

---

---

---

---

---

---

---

## DAVNA Living Cipher Seal (Machine-Verifiable)

This covenant is protected by a cryptographic seal that makes edits self-authenticating and tamper-evident.

**Current Seal:**
- Canonical Anchor: `HIST-3ce0df425861`
- Algorithm: BLAKE2b-256
- Previous Seal: `3fafe37d0e6c212ab2a30ac5085c2e77d09f279412e8632e7928b8a5e3643ff8`
- Covenant Digest: `a193c4ff90ce012b30450808179d68d3ea93ca865febcfd35f556213208b2a79`
- Sealed At (UTC): `2026-01-01T09:50:32Z`

**Verification:**
```bash
python scripts/verify_davna.py
python scripts/seal_davna.py --check
```

The Living Cipher ensures:
- Every edit creates a new seal chained to the previous one
- Tampering breaks the chain instantly
- No secrets required—fully public verification
- CI/CD enforces seal validity on every commit

---

**License:** Apache-2.0  
**Framework:** HarmonyØ4 v1.0.0  
**Hash Anchor:** `HIST-3ce0df425861`