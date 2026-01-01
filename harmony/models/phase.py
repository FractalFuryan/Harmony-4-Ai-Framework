"""
Phase dynamics models for HarmonyØ4.

Tracks phase evolution and synchronization without forcing convergence.
"""

from typing import Optional
import numpy as np
import numpy.typing as npt


class PhaseModel:
    """
    Model phase evolution for individual observers.
    
    Phase represents internal oscillatory state. Evolution follows
    natural frequency unless coupled with consent.
    """
    
    def __init__(
        self,
        natural_frequency: float,
        initial_phase: float = 0.0,
    ) -> None:
        """
        Initialize phase model.
        
        Args:
            natural_frequency: Intrinsic oscillation frequency (rad/s)
            initial_phase: Starting phase angle (radians)
        """
        self.natural_frequency = natural_frequency
        self.phase = initial_phase
        self.coupling_strength: Optional[float] = None
        self.coupled_phase: Optional[float] = None
    
    def evolve(self, dt: float) -> float:
        """
        Evolve phase forward in time.
        
        Args:
            dt: Time step
        
        Returns:
            New phase value
        """
        # Natural evolution
        dphase = self.natural_frequency * dt
        
        # Add coupling if consented
        if self.coupling_strength is not None and self.coupled_phase is not None:
            dphase += self.coupling_strength * np.sin(self.coupled_phase - self.phase) * dt
        
        self.phase += dphase
        self.phase = self.phase % (2 * np.pi)  # Wrap to [0, 2π)
        
        return self.phase
    
    def set_coupling(
        self,
        coupling_strength: float,
        coupled_phase: float,
    ) -> None:
        """
        Set coupling to another phase (requires consent).
        
        Args:
            coupling_strength: Strength of coupling (K parameter)
            coupled_phase: Phase of coupled observer
        """
        self.coupling_strength = coupling_strength
        self.coupled_phase = coupled_phase
    
    def remove_coupling(self) -> None:
        """Remove coupling (consent revoked)."""
        self.coupling_strength = None
        self.coupled_phase = None
    
    def get_phase(self) -> float:
        """Get current phase value."""
        return self.phase


class PhaseLockDetector:
    """
    Detect phase-locking between observers.
    
    Does not force phase-locking—only detects when it emerges naturally.
    """
    
    def __init__(
        self,
        lock_threshold: float = 0.1,
        window_size: int = 10,
    ) -> None:
        """
        Initialize phase-lock detector.
        
        Args:
            lock_threshold: Maximum phase difference for lock detection (radians)
            window_size: Number of samples to confirm lock
        """
        self.lock_threshold = lock_threshold
        self.window_size = window_size
        self._history: list[float] = []
    
    def check_lock(
        self,
        phase1: float,
        phase2: float,
    ) -> bool:
        """
        Check if two phases are currently locked.
        
        Args:
            phase1: First phase
            phase2: Second phase
        
        Returns:
            True if phases are locked
        """
        diff = abs((phase1 - phase2 + np.pi) % (2 * np.pi) - np.pi)
        self._history.append(diff)
        
        # Keep window size
        if len(self._history) > self.window_size:
            self._history.pop(0)
        
        # Check if locked over window
        if len(self._history) == self.window_size:
            return all(d < self.lock_threshold for d in self._history)
        
        return False
    
    def get_phase_difference_history(self) -> list[float]:
        """Get history of phase differences."""
        return self._history.copy()
