from __future__ import annotations

import numpy as np
from scipy import signal, stats


class StressIndexBuilder:
    """Build a canonical stress composite index."""

    def __init__(self, fs: float = 250.0, method: str = "standard") -> None:
        self.fs = fs
        self.method = method
        self.weights = self._get_weights(method)

    def _get_weights(self, method: str) -> dict[str, float]:
        if method == "minimal":
            return {
                "lf_hf_ratio": 0.6,
                "eda_phasic": 0.4,
                "rmssd": -0.3,
                "hr_mean": 0.3,
            }
        if method == "robust":
            return {
                "lf_hf_ratio": 0.4,
                "eda_phasic": 0.3,
                "rmssd": -0.4,
                "hr_mean": 0.2,
                "hr_std": 0.3,
                "respiration_rate": 0.2,
            }
        return {
            "lf_hf_ratio": 0.5,
            "eda_phasic": 0.3,
            "rmssd": -0.4,
            "hr_mean": 0.3,
        }

    def compute_lf_hf_ratio(
        self,
        heart_rate: np.ndarray,
        f_low: tuple[float, float] = (0.04, 0.15),
        f_high: tuple[float, float] = (0.15, 0.4),
    ) -> float:
        if len(heart_rate) < 10 * self.fs:
            return 1.0

        t = np.arange(len(heart_rate)) / self.fs
        slope, intercept, _, _, _ = stats.linregress(t, heart_rate)
        detrended = heart_rate - (intercept + slope * t)

        freqs, psd = signal.welch(detrended, fs=self.fs, nperseg=min(256, len(detrended)))

        mask_lf = (freqs >= f_low[0]) & (freqs <= f_low[1])
        mask_hf = (freqs >= f_high[0]) & (freqs <= f_high[1])

        if np.any(mask_lf) and np.any(mask_hf):
            power_lf = np.trapezoid(psd[mask_lf], freqs[mask_lf])
            power_hf = np.trapezoid(psd[mask_hf], freqs[mask_hf])
            if power_hf > 0:
                return float(power_lf / power_hf)

        return 1.0

    def compute_eda_phasic(self, eda_signal: np.ndarray, cutoff: float = 0.05) -> float:
        if len(eda_signal) < 10:
            return 0.0

        nyquist = self.fs / 2.0
        b, a = signal.butter(2, cutoff / nyquist, btype="high")
        eda_filtered = signal.filtfilt(b, a, eda_signal)
        return float(np.std(eda_filtered) / (np.std(eda_signal) + 1e-6))

    def compute_rmssd(self, rr_intervals: np.ndarray) -> float:
        if len(rr_intervals) < 2:
            return 0.0
        differences = np.diff(rr_intervals)
        return float(np.sqrt(np.mean(differences**2)))

    def compute_stress_index(
        self,
        heart_rate: np.ndarray | None = None,
        eda_signal: np.ndarray | None = None,
        rr_intervals: np.ndarray | None = None,
        respiration_signal: np.ndarray | None = None,
        components: dict[str, float] | None = None,
    ) -> dict[str, object]:
        results: dict[str, object] = {
            "stress_index": 0.0,
            "components": {},
            "weights_used": self.weights,
            "method": self.method,
        }
        components_dict: dict[str, dict[str, float]] = {}
        results["components"] = components_dict

        comp = components.copy() if components else {}

        if "lf_hf_ratio" not in comp and heart_rate is not None:
            comp["lf_hf_ratio"] = self.compute_lf_hf_ratio(heart_rate)

        if "eda_phasic" not in comp and eda_signal is not None:
            comp["eda_phasic"] = self.compute_eda_phasic(eda_signal)

        if "rmssd" not in comp and rr_intervals is not None:
            comp["rmssd"] = self.compute_rmssd(rr_intervals)

        if "hr_mean" not in comp and heart_rate is not None:
            comp["hr_mean"] = float(np.mean(heart_rate))

        if "hr_std" not in comp and heart_rate is not None:
            comp["hr_std"] = float(np.std(heart_rate))

        if "respiration_rate" not in comp and respiration_signal is not None:
            comp["respiration_rate"] = float(np.mean(respiration_signal))

        weighted_sum = 0.0
        total_weight = 0.0

        for name, weight in self.weights.items():
            if name in comp:
                value = comp[name]
                if np.isfinite(value):
                    weighted_sum += weight * value
                    total_weight += abs(weight)
                    components_dict[name] = {
                        "value": float(value),
                        "weight": float(weight),
                        "contribution": float(weight * value),
                    }

        results["stress_index"] = weighted_sum / total_weight if total_weight > 0 else 0.0
        return results

    def compute_stress_timeseries(
        self, signals_dict: dict[str, np.ndarray], window_sec: float = 30.0, step_sec: float = 5.0
    ) -> tuple[np.ndarray, np.ndarray, dict[str, list[float]]]:
        window_samples = int(window_sec * self.fs)
        step_samples = int(step_sec * self.fs)

        sample_counts = [len(sig) for sig in signals_dict.values() if sig is not None]
        if not sample_counts:
            return np.array([]), np.array([]), {}

        min_samples = min(sample_counts)
        n_windows = (min_samples - window_samples) // step_samples + 1
        if n_windows <= 0:
            return np.array([]), np.array([]), {}

        time_points = np.zeros(n_windows)
        stress_values = np.zeros(n_windows)
        component_history: dict[str, list[float]] = {name: [] for name in self.weights.keys()}

        for i in range(n_windows):
            start = i * step_samples
            end = start + window_samples

            windowed_signals = {}
            for name, signal_data in signals_dict.items():
                if signal_data is not None and len(signal_data) >= end:
                    windowed_signals[name] = signal_data[start:end]

            result = self.compute_stress_index(**windowed_signals)  # type: ignore[arg-type]

            time_points[i] = start / self.fs
            stress_values[i] = float(result["stress_index"])  # type: ignore[arg-type]

            components = result["components"]  # type: ignore[assignment]
            for name in self.weights.keys():
                if name in components:  # type: ignore[operator]
                    component_history[name].append(float(components[name]["value"]))  # type: ignore[index]
                else:
                    component_history[name].append(float("nan"))

        return time_points, stress_values, component_history
