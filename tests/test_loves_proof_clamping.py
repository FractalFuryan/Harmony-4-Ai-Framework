import numpy as np

from harmony.invariants.loves_proof import LovesProofInvariant


def test_clamped_C_flag_triggers_on_nonpositive_coherence() -> None:
    """Nonpositive coherence values should clamp and raise the audit flag."""
    t = np.linspace(0, 30, 120)

    C = np.linspace(-0.1, 0.5, t.size)
    S = 1.0 - 0.5 * (t / t[-1])
    x = 0.1 + 0.01 * np.sin(2 * np.pi * t / 5)

    invariant = LovesProofInvariant(require_dc_trend=False)
    out = invariant.check(t, C, S, x)

    assert "clamped_C" in out
    assert out["clamped_C"] is True
    assert np.isfinite(out["G_mean"])
    assert np.isfinite(out["S_slope"])
    assert np.isfinite(out["Pac_trend"])
