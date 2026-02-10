import numpy as np


class EntrainmentMetrics:
    """Calculate phase-locking and entrainment between oscillators."""

    def __init__(
        self,
        fs: float = 250.0,
        bias_correction: bool = True,
        n_shuffles: int = 100,
        random_state: int | None = 0,
    ) -> None:
        self.fs = fs
        self.bias_correction = bias_correction
        self.n_shuffles = n_shuffles
        if random_state is None:
            self._rng = np.random.default_rng()
        else:
            self._rng = np.random.default_rng(random_state)

    def phase_lock_value(
        self, phase1: np.ndarray, phase2: np.ndarray, corrected: bool | None = None
    ) -> float:
        if len(phase1) == 0 or len(phase2) == 0:
            return float("nan")

        use_correction = corrected if corrected is not None else self.bias_correction
        phase_diff = phase1 - phase2
        complex_avg = np.mean(np.exp(1j * phase_diff))
        raw_plv = float(np.abs(complex_avg))

        if not use_correction or len(phase1) < 100:
            return raw_plv

        corrected_plv = self._bias_correct_plv(phase1, phase2, raw_plv)
        return max(corrected_plv, 0.0)

    def _bias_correct_plv(
        self, phase1: np.ndarray, phase2: np.ndarray, raw_plv: float
    ) -> float:
        if self.n_shuffles <= 0:
            return raw_plv

        n_samples = len(phase2)
        shuffled_plvs = []

        for _ in range(self.n_shuffles):
            shift = int(self._rng.integers(n_samples))
            phase2_shuffled = np.roll(phase2, shift)
            phase_diff_shuffled = phase1 - phase2_shuffled
            complex_avg_shuffled = np.mean(np.exp(1j * phase_diff_shuffled))
            shuffled_plvs.append(float(np.abs(complex_avg_shuffled)))

        bias_estimate = float(np.mean(shuffled_plvs))
        return raw_plv - bias_estimate

    def sliding_plv(
        self,
        phase1: np.ndarray,
        phase2: np.ndarray,
        window_sec: float = 30.0,
        step_sec: float = 1.0,
        corrected: bool | None = None,
    ) -> tuple[np.ndarray, np.ndarray]:
        window_samples = int(window_sec * self.fs)
        step_samples = int(step_sec * self.fs)
        n_windows = (len(phase1) - window_samples) // step_samples + 1

        plv_values = np.zeros(n_windows)
        time_points = np.zeros(n_windows)

        for i in range(n_windows):
            start = i * step_samples
            end = start + window_samples
            plv_values[i] = self.phase_lock_value(
                phase1[start:end], phase2[start:end], corrected=corrected
            )
            time_points[i] = start / self.fs

        return time_points, plv_values

    def arnold_tongue_boundary(self, freq1: float, freq2: float, K_eff: float) -> tuple[bool, float]:
        omega1 = 2.0 * np.pi * freq1
        omega2 = 2.0 * np.pi * freq2
        delta_omega = abs(omega1 - omega2)
        return delta_omega < K_eff, delta_omega

    def effective_coupling(
        self,
        K0: float,
        coherence: float,
        distance: float | None = None,
        r0: float = 1.0,
        falloff_exp: float = 3.0,
    ) -> float:
        K_eff = K0 * coherence
        if distance is not None and distance > 0:
            K_eff *= (r0 / distance) ** falloff_exp
        return K_eff

    def kuramoto_order_parameter(self, phases: np.ndarray) -> np.ndarray:
        complex_phasors = np.exp(1j * phases)
        mean_phasor = np.mean(complex_phasors, axis=0)
        return np.abs(mean_phasor)

    def consent_gate(
        self,
        K_eff: float,
        delta_omega: float,
        consent_threshold: float = 0.1,
        max_permissible_lock: float = 0.95,
    ) -> tuple[bool, float]:
        can_lock = delta_omega < K_eff
        if not can_lock or K_eff < consent_threshold:
            return False, 0.0

        lock_strength = 1.0 - (delta_omega / K_eff)
        lock_strength = min(lock_strength, max_permissible_lock)
        return lock_strength > 0, lock_strength

    def dynamic_consent_threshold(
        self,
        stress_level: float,
        baseline_threshold: float = 0.1,
        stress_sensitivity: float = 0.5,
    ) -> float:
        adjusted = baseline_threshold * (1.0 + stress_sensitivity * stress_level)
        return min(adjusted, baseline_threshold * 3.0)

    def revocable_entrainment(
        self,
        phase_source: np.ndarray,
        phase_receiver: np.ndarray,
        stress_receiver: float = 0.0,
        history_length: int = 10,
    ) -> dict[str, float | bool]:
        if len(phase_source) > history_length:
            omega_source = float(np.mean(np.diff(phase_source[-history_length:])) * self.fs)
        else:
            omega_source = float(
                np.mean(np.diff(phase_source)) * self.fs if len(phase_source) > 1 else 1.0
            )

        if len(phase_receiver) > history_length:
            omega_receiver = float(np.mean(np.diff(phase_receiver[-history_length:])) * self.fs)
        else:
            omega_receiver = float(
                np.mean(np.diff(phase_receiver)) * self.fs if len(phase_receiver) > 1 else 1.0
            )

        delta_omega = abs(omega_source - omega_receiver)

        plv = self.phase_lock_value(phase_source, phase_receiver)
        K_eff = plv

        consent_threshold = self.dynamic_consent_threshold(stress_receiver)
        consent_granted, lock_strength = self.consent_gate(
            K_eff, delta_omega, consent_threshold=consent_threshold
        )

        respectful_influence = lock_strength * plv if consent_granted else 0.0

        return {
            "consent_granted": consent_granted,
            "lock_strength": float(lock_strength),
            "plv": float(plv),
            "delta_omega": float(delta_omega),
            "K_eff": float(K_eff),
            "consent_threshold": float(consent_threshold),
            "respectful_influence": float(respectful_influence),
            "omega_source": float(omega_source),
            "omega_receiver": float(omega_receiver),
        }
