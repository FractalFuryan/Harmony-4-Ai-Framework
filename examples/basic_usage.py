#!/usr/bin/env python3
"""
HarmonyØ4 Example: Observer Consent and Coherence

Demonstrates the core ethical patterns:
1. Binary consent between observers
2. Phase coherence measurement
3. Boundary integrity preservation
4. Ethical invariant enforcement
"""

import numpy as np
from harmony.api.public import create_observer, create_phase_system
from harmony.core.coherence import PhaseCoherence
from harmony.core.invariants import EthicalInvariants


def main():
    print("=" * 80)
    print("HarmonyØ4 Example: Ethical Observer Dynamics")
    print("=" * 80)
    print()
    
    # 1. Create observers with consent management
    print("1️⃣  Creating Observers")
    print("-" * 80)
    
    alice, alice_consent = create_observer("alice", state_dim=10)
    bob, bob_consent = create_observer("bob", state_dim=10)
    
    print(f"Created observer 'alice' with state_dim=10")
    print(f"Created observer 'bob' with state_dim=10")
    print(f"Alice boundary integrity: {alice.get_boundary_integrity():.2f}")
    print(f"Bob boundary integrity: {bob.get_boundary_integrity():.2f}")
    print()
    
    # 2. Demonstrate consent mechanism
    print("2️⃣  Consent Mechanism")
    print("-" * 80)
    
    # Alice grants observation consent to Bob
    alice_consent.grant_consent("alice", "bob", "observe")
    print("Alice grants observation consent to Bob")
    
    can_observe = alice_consent.check_consent("alice", "bob", "observe")
    print(f"Can Bob observe Alice? {can_observe}")
    
    # Bob attempts to witness Alice
    if can_observe:
        projection = alice.witness_projection("bob", projection_dim=5)
        print(f"Bob's witness projection of Alice: {projection}")
    
    # Alice revokes consent
    alice_consent.revoke_consent("alice", "bob", "observe")
    print("\nAlice revokes observation consent")
    
    can_observe = alice_consent.check_consent("alice", "bob", "observe")
    print(f"Can Bob observe Alice? {can_observe}")
    
    projection = alice.witness_projection("bob", projection_dim=5)
    print(f"Bob's witness projection after revocation: {projection}")
    print()
    
    # 3. Phase coherence measurement
    print("3️⃣  Phase Coherence")
    print("-" * 80)
    
    pc = PhaseCoherence(n_components=5)
    
    # Perfect coherence
    aligned = np.zeros(5)
    coherence_aligned = pc.compute(aligned)
    print(f"Aligned phases coherence: {coherence_aligned:.4f}")
    
    # Random phases
    random = np.random.uniform(0, 2*np.pi, 5)
    coherence_random = pc.compute(random)
    print(f"Random phases coherence: {coherence_random:.4f}")
    
    # Drift detection
    pc.set_baseline(aligned)
    drift = pc.drift_from_baseline(random)
    print(f"Drift from baseline: {drift:.4f}")
    print()
    
    # 4. Ethical invariants
    print("4️⃣  Ethical Invariants")
    print("-" * 80)
    
    inv = EthicalInvariants()
    
    # INV-1: Consent monotonicity
    print("Testing INV-1 (Consent Monotonicity):")
    valid = inv.check_consent_monotonicity(consent_granted=False, state_changed=True)
    print(f"  State change without consent: {'✅ VALID' if valid else '❌ VIOLATION'}")
    
    # INV-2: Boundary preservation
    print("Testing INV-2 (Boundary Preservation):")
    valid = inv.check_boundary_preservation(
        boundary_before=0.9,
        boundary_after=0.7,
        consent_granted=False
    )
    print(f"  Boundary degraded without consent: {'✅ VALID' if valid else '❌ VIOLATION'}")
    
    # INV-5: Refusal without penalty
    print("Testing INV-5 (Refusal Without Penalty):")
    valid = inv.check_refusal_without_penalty(
        coherence_before_refusal=0.8,
        coherence_after_refusal=0.79,
        max_degradation=0.1
    )
    print(f"  Coherence stable after refusal: {'✅ VALID' if valid else '❌ VIOLATION'}")
    
    if inv.has_violations():
        print("\n⚠️  Violations detected:")
        for violation in inv.get_violations():
            print(f"  - {violation}")
    else:
        print("\n✅ No violations detected")
    
    print()
    
    # 5. Phase evolution with coupling
    print("5️⃣  Phase Evolution with Consent-Based Coupling")
    print("-" * 80)
    
    phase_a, drift_a = create_phase_system(natural_frequency=1.0, initial_phase=0.0)
    phase_b, drift_b = create_phase_system(natural_frequency=1.1, initial_phase=np.pi/4)
    
    print(f"Phase A: {phase_a.get_phase():.4f} rad")
    print(f"Phase B: {phase_b.get_phase():.4f} rad")
    
    # Evolve without coupling
    for _ in range(10):
        phase_a.evolve(dt=0.1)
        phase_b.evolve(dt=0.1)
    
    print(f"After evolution (uncoupled):")
    print(f"  Phase A: {phase_a.get_phase():.4f} rad")
    print(f"  Phase B: {phase_b.get_phase():.4f} rad")
    print()
    
    # Summary
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print("✅ Consent is binary, explicit, and revocable")
    print("✅ Coherence is measured, not optimized")
    print("✅ Boundaries are preserved through consent")
    print("✅ Ethical invariants are enforced")
    print()
    print("HarmonyØ4: Stability emerges—it is never forced.")
    print("=" * 80)


if __name__ == "__main__":
    main()
