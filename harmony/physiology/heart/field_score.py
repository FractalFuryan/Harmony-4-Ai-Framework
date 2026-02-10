from __future__ import annotations

import numpy as np
from scipy import stats

from .stress import StressIndexBuilder


class HeartFieldScorer:
    """Compute heart field scores and non-coercion checks."""

    def __init__(
        self,
        fs: float = 250.0,
        default_weights: dict[str, float] | None = None,
        r0: float = 1.0,
        falloff_exp: float = 3.0,
        stress_method: str = "standard",
        enable_loves_proof: bool = True,
        loves_proof_kwargs: dict[str, object] | None = None,
    ) -> None:
        self.fs = fs
        if default_weights is None:
            self.default_weights = {
                "respiration": 0.4,
                "ppg": 0.3,
                "eda": 0.2,
                "other": 0.1,
            }
        else:
            self.default_weights = default_weights
        self.r0 = r0
        self.falloff_exp = falloff_exp
        self.stress_builder = StressIndexBuilder(fs=fs, method=stress_method)
        self.enable_loves_proof = enable_loves_proof
        self.loves_proof_checker = None
        if enable_loves_proof:
            from .loves_proof import PhysiologyLovesProof

            self.loves_proof_checker = PhysiologyLovesProof(
                fs=fs, **(loves_proof_kwargs or {})
            )

    def compute_net_field(
        self,
        heart_amplitude: float,
        heart_coherence: float,
        plv_dict: dict[str, float],
        weights: dict[str, float] | None = None,
        distance: float | None = None,
    ) -> dict[str, object]:
        if weights is None:
            weights = self.default_weights

        A_eff = heart_amplitude * heart_coherence
        plv_product = 1.0
        plv_contributions: dict[str, dict[str, float]] = {}

        for channel, plv in plv_dict.items():
            w = weights.get(channel, weights.get("other", 0.1))
            plv_safe = max(plv, 1e-6)
            channel_contribution = plv_safe**w
            plv_product *= channel_contribution
            plv_contributions[channel] = {
                "plv": float(plv),
                "weight": float(w),
                "contribution": float(channel_contribution),
            }

        A_net = A_eff * plv_product

        distance_scaling = 1.0
        if distance is not None and distance > 0:
            distance_scaling = (self.r0 / distance) ** self.falloff_exp
        A_net_scaled = A_net * distance_scaling

        return {
            "heart_amplitude": float(heart_amplitude),
            "heart_coherence": float(heart_coherence),
            "effective_field": float(A_eff),
            "plv_contributions": plv_contributions,
            "plv_product": float(plv_product),
            "net_field": float(A_net),
            "distance_scaling": float(distance_scaling),
            "net_field_scaled": float(A_net_scaled),
            "weights_used": weights,
        }

    def compute_non_coercion_check(
        self,
        coherence_values: np.ndarray,
        time_points: np.ndarray,
        stress_proxy: np.ndarray | dict[str, float] | None = None,
        stress_signals: dict[str, np.ndarray] | None = None,
        window_sec: float = 60.0,
    ) -> dict[str, object]:
        epsilon = 1e-6
        log_coherence = np.log(coherence_values + epsilon)

        if len(time_points) <= 1:
            return {
                "coherence_gain_rate": 0.0,
                "stress_slope": None,
                "stress_decreasing": None,
                "constraint_satisfied": None,
                "gain_rate_timeseries": None,
                "stress_values": stress_proxy,
                "message": "Insufficient data for constraint check",
            }

        gain_rate = np.gradient(log_coherence, time_points)

        stress_decreasing = None
        stress_slope = None

        if stress_proxy is None and stress_signals is not None:
            stress_times, stress_values, _ = self.stress_builder.compute_stress_timeseries(
                stress_signals, window_sec=window_sec, step_sec=window_sec / 2
            )
            if len(stress_times) > 1 and len(time_points) > 1:
                stress_proxy = np.interp(time_points, stress_times, stress_values)
            else:
                stress_proxy = stress_values
        elif isinstance(stress_proxy, dict):
            stress_result = self.stress_builder.compute_stress_index(components=stress_proxy)
            stress_proxy = np.array([stress_result["stress_index"]])

        if stress_proxy is not None and not isinstance(stress_proxy, np.ndarray):
            stress_proxy = np.array(stress_proxy)

        if stress_proxy is not None and len(stress_proxy) >= 2:
            min_len = min(len(gain_rate), len(stress_proxy))
            if min_len >= 2:
                time_aligned = time_points[:min_len]
                stress_aligned = stress_proxy[:min_len]
                gain_aligned = gain_rate[:min_len]
                stress_slope, _, _, _, _ = stats.linregress(time_aligned, stress_aligned)
                stress_decreasing = stress_slope < 0
                recent_G = float(np.mean(gain_aligned[-min(10, len(gain_aligned)):]))
            else:
                recent_G = float(np.mean(gain_rate[-min(10, len(gain_rate)):]))
        else:
            recent_G = float(np.mean(gain_rate[-min(10, len(gain_rate)):]))

        if stress_decreasing is not None:
            constraint_satisfied = (recent_G > 0) and bool(stress_decreasing)
        else:
            constraint_satisfied = None

        return {
            "coherence_gain_rate": recent_G,
            "stress_slope": None if stress_slope is None else float(stress_slope),
            "stress_decreasing": stress_decreasing,
            "constraint_satisfied": constraint_satisfied,
            "gain_rate_timeseries": gain_rate,
            "stress_values": stress_proxy,
            "message": self._get_constraint_message(constraint_satisfied, recent_G, stress_slope),
        }

    def compute_with_loves_proof(
        self,
        t: np.ndarray,
        heart_coherence: np.ndarray,
        stress_proxy: np.ndarray,
        heart_amplitude: np.ndarray,
        plv_dict: dict[str, float],
        **kwargs: object,
    ) -> dict[str, object]:
        field_result = self.compute_net_field(
            heart_amplitude=float(np.std(heart_amplitude)),
            heart_coherence=float(
                np.mean(heart_coherence[-100:])
                if len(heart_coherence) > 100
                else np.mean(heart_coherence)
            ),
            plv_dict=plv_dict,
            **kwargs,
        )

        loves_proof_result = None
        if self.enable_loves_proof and self.loves_proof_checker is not None:
            loves_proof_result = self.loves_proof_checker.check_heart_field(
                t=t,
                heart_coherence=heart_coherence,
                stress_proxy=stress_proxy,
                heart_amplitude=heart_amplitude,
            )
            field_result["loves_proof_holds"] = loves_proof_result["invariant_holds"]
            field_result["loves_proof_diagnostics"] = loves_proof_result

        return {
            "field_score": field_result,
            "loves_proof": loves_proof_result,
        }

    def _get_constraint_message(
        self, satisfied: bool | None, gain_rate: float, stress_slope: float | None
    ) -> str:
        if satisfied is None:
            return "Cannot evaluate constraint"
        if satisfied:
            return (
                "OK: coherence growing "
                f"(G={gain_rate:.3f}) while stress decreasing (slope={stress_slope:.3f})"
            )
        if gain_rate <= 0:
            return f"FAIL: coherence not growing (G={gain_rate:.3f})"
        return (
            "FAIL: coherence growing "
            f"(G={gain_rate:.3f}) but stress not decreasing (slope={stress_slope:.3f})"
        )

    def batch_process(
        self,
        signals_dict: dict[str, np.ndarray],
        timestamps: np.ndarray,
        distance: float | None = None,
    ) -> dict[str, object]:
        return {
            "timestamp": float(timestamps[-1]) if len(timestamps) > 0 else 0.0,
            "signals_present": list(signals_dict.keys()),
            "distance": distance,
            "note": "Batch processing not yet implemented",
        }
