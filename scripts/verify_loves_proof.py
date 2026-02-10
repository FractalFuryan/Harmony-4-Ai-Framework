#!/usr/bin/env python3
"""Verification script for Love's Proof integration."""

from __future__ import annotations

import sys

import numpy as np

from harmony import (
    CouplingLovesProof,
    DialogueLovesProof,
    LovesProofInvariant,
    PhysiologyLovesProof,
    ac_power,
    acdc_split,
)


def test_acdc_operator() -> bool:
    print("Testing AC/DC operator...")

    t = np.linspace(0, 10, 100)
    x = 2.0 + 0.5 * np.sin(2 * np.pi * t) + 0.1 * np.random.randn(100)

    x_dc, x_ac = acdc_split(x, alpha=0.1)
    pac = ac_power(x_ac)

    assert np.allclose(x, x_dc + x_ac, rtol=1e-5)
    assert pac >= 0
    assert pac < 10

    print("  OK: AC/DC decomposition works")
    print(f"  OK: max error = {np.max(np.abs(x - (x_dc + x_ac))):.2e}")
    print(f"  OK: AC power = {pac:.4f}")

    return True


def test_loves_proof_kernel() -> bool:
    print("\nTesting Love's Proof kernel...")

    invariant = LovesProofInvariant()

    t = np.linspace(0, 60, 300)
    C = 0.2 + 0.6 * (1 - np.exp(-t / 20))
    S = 1.0 - 0.5 * (t / t[-1])
    x = 0.2 + 0.02 * np.sin(2 * np.pi * t / 5)

    result1 = invariant.check(t, C, S, x)
    assert result1["invariant_holds"] is True
    print(
        f"  OK: healthy growth passes (G={result1['G_mean']:.4f}, S={result1['S_slope']:.4f})"
    )

    S_coercive = 0.2 + 0.8 * (t / t[-1])
    result2 = invariant.check(t, C, S_coercive, x)
    assert result2["invariant_holds"] is False
    print(f"  OK: coercive growth fails ({result2['violation_reason']})")

    amp = 0.01 + 0.06 * (t / t[-1])
    x_volatile = 0.2 + amp * np.sin(2 * np.pi * t / 5)
    result3 = invariant.check(t, C, S, x_volatile)
    assert result3["invariant_holds"] is False
    print(f"  OK: volatile growth fails ({result3['violation_reason']})")

    return True


def test_domain_adapters() -> bool:
    print("\nTesting domain adapters...")

    t = np.linspace(0, 300, 1500)

    physio = PhysiologyLovesProof(fs=5.0)
    heart_coherence = 0.3 + 0.4 * (1 - np.exp(-t / 100))
    stress = 0.8 - 0.6 * (t / t[-1])
    amplitude = 1.0 + 0.1 * np.sin(2 * np.pi * t / 10)

    physio_result = physio.check_heart_field(t, heart_coherence, stress, heart_amplitude=amplitude)
    print(f"  OK: physiology adapter = {physio_result['invariant_holds']}")

    coupling = CouplingLovesProof()
    order_param = 0.1 + 0.7 * (1 - np.exp(-t / 20))
    mismatch = 2.0 - 1.5 * (t / t[-1])
    coupling_strength = 1.5 + 0.1 * np.sin(2 * np.pi * t / 10)

    coupling_result = coupling.check_entrainment(t, order_param, mismatch, coupling_strength)
    print(f"  OK: coupling adapter = {coupling_result['invariant_holds']}")

    dialogue = DialogueLovesProof()
    dialogue_coherence = 0.2 + 0.6 * (t / t[-1])
    resistance = 0.9 - 0.7 * (t / t[-1])
    push = 0.1 + 0.05 * np.sin(2 * np.pi * t / 5)

    dialogue_result = dialogue.check_influence(
        t[:20], dialogue_coherence[:20], resistance[:20], push[:20]
    )
    print(f"  OK: dialogue adapter = {dialogue_result['invariant_holds']}")

    return True


def main() -> int:
    print("=" * 60)
    print("Love's Proof + AC/DC System Verification")
    print("=" * 60)

    tests = [
        ("AC/DC Operator", test_acdc_operator),
        ("Love's Proof Kernel", test_loves_proof_kernel),
        ("Domain Adapters", test_domain_adapters),
    ]

    all_passed = True

    for test_name, test_func in tests:
        try:
            passed = test_func()
            if passed:
                print(f"\nPASS: {test_name}\n")
            else:
                print(f"\nFAIL: {test_name}\n")
                all_passed = False
        except Exception as exc:
            print(f"\nERROR: {test_name} - {exc}\n")
            all_passed = False

    print("=" * 60)
    if all_passed:
        print("PASS: all verification tests passed")
        return 0

    print("FAIL: some tests failed")
    return 1


if __name__ == "__main__":
    sys.exit(main())
