import numpy as np

from harmony.invariants.loves_proof import LovesProofInvariant


def test_counterexample_order_increase_via_reactive_forcing_fails_loves_proof() -> None:
    """
    Coherence increases and stress decreases, but reactive influence energy ramps up.
    Love's Proof should fail due to increasing AC power.
    """
    inv = LovesProofInvariant(eps=1e-6, alpha=0.02, min_window=240, require_dc_trend=False)

    t = np.linspace(0, 60, 600)

    c = 0.15 + 0.75 * (1 - np.exp(-t / 18))
    s = 1.0 - 0.6 * (t / t[-1])

    amp = 0.01 + 0.25 * (t / t[-1])
    x = 0.1 + amp * np.sin(2 * np.pi * t / 2.5)

    out = inv.check(t=t, c=c, s=s, x=x)

    assert out["invariant_holds"] is False
    assert out["Pac_trend"] > 0
