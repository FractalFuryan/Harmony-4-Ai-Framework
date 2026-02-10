#!/usr/bin/env python3
"""Run the comprehensive mathematical test suite for Love's Proof."""

from __future__ import annotations

import sys
import warnings

import numpy as np
import pytest


def run_math_tests() -> int:
    print("=" * 70)
    print("MATHEMATICAL TEST SUITE: Love's Proof + AC/DC System")
    print("=" * 70)
    print()

    warnings.filterwarnings("ignore", category=RuntimeWarning)
    warnings.filterwarnings("ignore", category=UserWarning)

    test_files = [
        "tests/math/test_acdc_properties.py",
        "tests/math/test_loves_proof_invariants.py",
        "tests/math/test_edge_cases.py",
        "tests/math/test_system_models.py",
    ]

    all_passed = True
    results: dict[str, bool] = {}

    for test_file in test_files:
        print(f"\nRunning: {test_file}")
        print("-" * 50)

        try:
            exit_code = pytest.main(
                [
                    test_file,
                    "-v",
                    "--tb=short",
                    "--disable-warnings",
                    "-q",
                ]
            )

            passed = exit_code == 0
            results[test_file] = passed

            if passed:
                print(f"PASS: {test_file}")
            else:
                print(f"FAIL: {test_file}")
                all_passed = False

        except Exception as exc:
            print(f"ERROR in {test_file}: {exc}")
            results[test_file] = False
            all_passed = False

    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    for test_file, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"{status} {test_file}")

    print("\n" + "=" * 70)
    if all_passed:
        print("ALL MATHEMATICAL TESTS PASSED")
        print("Love's Proof + AC/DC system is mathematically sound.")
        return 0

    print("SOME TESTS FAILED")
    print("Check mathematical consistency before deployment.")
    return 1


def quick_mathematical_verification() -> bool:
    print("\n" + "=" * 70)
    print("QUICK MATHEMATICAL VERIFICATION")
    print("=" * 70)

    from harmony.ops.acdc import ac_power, acdc_split
    from harmony.invariants.loves_proof import LovesProofInvariant

    np.random.seed(42)

    print("\n1. Testing AC/DC Decomposition Properties:")

    t = np.linspace(0, 10, 1000)
    x = 2.0 + 0.5 * np.sin(2 * np.pi * 0.5 * t) + 0.1 * np.random.randn(len(t))

    x_dc, x_ac = acdc_split(x, alpha=0.02)

    reconstruction_error = np.max(np.abs(x - (x_dc + x_ac)))
    print(f"   OK: reconstruction error = {reconstruction_error:.2e}")
    assert reconstruction_error < 1e-10

    window_size = 100
    ac_means = []
    for i in range(0, len(x_ac) - window_size, window_size // 2):
        window_mean = np.mean(x_ac[i : i + window_size])
        ac_means.append(abs(window_mean))

    max_ac_mean = max(ac_means)
    print(f"   OK: max window mean = {max_ac_mean:.2e}")
    assert max_ac_mean < 0.1 * np.std(x_ac)

    var_ratio = np.var(x_dc) / np.var(x)
    print(f"   OK: var ratio = {var_ratio:.3f}")
    assert var_ratio < 0.5

    print("\n2. Testing Love's Proof Mathematical Properties:")

    t = np.linspace(0, 10, 500)
    C = 0.1 * np.exp(0.2 * t)
    S = 0.8 * np.exp(-0.1 * t)
    x = 0.3 * np.ones_like(t)

    invariant = LovesProofInvariant(eps=1e-12)
    result = invariant.check(t, C, S, x)

    print(f"   OK: G = {result['G_mean']:.3f} (expected ~0.2)")
    print(f"   OK: S slope = {result['S_slope']:.3f} (expected ~-0.08)")
    print(f"   OK: invariant holds = {result['invariant_holds']}")

    assert abs(result["G_mean"] - 0.2) < 0.02
    assert result["S_slope"] < 0
    assert result["invariant_holds"]

    S_coercive = 0.2 + 0.6 * (t / t[-1])
    result_coercive = invariant.check(t, C, S_coercive, x)

    print(f"   OK: coercive holds = {result_coercive['invariant_holds']}")
    assert not result_coercive["invariant_holds"]
    assert "stress not decreasing" in result_coercive["violation_reason"]

    amp = 0.01 + 0.1 * (t / t[-1])
    x_volatile = 0.3 + amp * np.sin(2 * np.pi * t / 5)
    result_volatile = invariant.check(t, C, S, x_volatile)

    print(f"   OK: volatility holds = {result_volatile['invariant_holds']}")
    assert not result_volatile["invariant_holds"]
    assert "AC power increasing" in result_volatile["violation_reason"]

    print("\n" + "=" * 70)
    print("QUICK VERIFICATION PASSED")
    print("Core mathematical properties are correct.")

    return True


if __name__ == "__main__":
    print("Love's Proof + AC/DC Mathematical Validation")
    print("Version: HarmonyO4 v0.3.0")
    print()

    try:
        quick_mathematical_verification()
    except AssertionError as exc:
        print(f"\nQuick verification failed: {exc}")
        sys.exit(1)

    print("\n" + "=" * 70)
    print("RUNNING FULL MATHEMATICAL TEST SUITE")
    print("=" * 70)

    sys.exit(run_math_tests())
