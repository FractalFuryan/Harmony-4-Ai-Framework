"""
Drift detection for HarmonyØ4.

Detects unintended behavioral changes without forcing correction.
"""

from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime
import numpy as np
import numpy.typing as npt


@dataclass
class DriftEvent:
    """Record of detected drift."""
    timestamp: datetime
    drift_type: str  # "phase", "role", "boundary"
    magnitude: float
    threshold: float
    source: str  # Identifier of drifting entity


class DriftDetector:
    """
    Base class for drift detection.
    
    Detects drift without prescribing correction—measurement only.
    """
    
    def __init__(
        self,
        threshold: float,
        window_size: int = 10,
    ) -> None:
        """
        Initialize drift detector.
        
        Args:
            threshold: Drift magnitude threshold for alerts
            window_size: Number of samples for trend analysis
        """
        self.threshold = threshold
        self.window_size = window_size
        self._events: List[DriftEvent] = []
    
    def record_event(self, event: DriftEvent) -> None:
        """Record a drift event."""
        self._events.append(event)
    
    def get_events(
        self,
        drift_type: Optional[str] = None,
        since: Optional[datetime] = None,
    ) -> List[DriftEvent]:
        """
        Get drift events with optional filtering.
        
        Args:
            drift_type: Filter by drift type
            since: Filter by events after this time
        
        Returns:
            List of matching drift events
        """
        events = self._events
        
        if drift_type is not None:
            events = [e for e in events if e.drift_type == drift_type]
        
        if since is not None:
            events = [e for e in events if e.timestamp >= since]
        
        return events
    
    def clear_events(self) -> None:
        """Clear event history."""
        self._events.clear()


class PhaseDriftDetector(DriftDetector):
    """Detect phase coherence drift."""
    
    def __init__(
        self,
        threshold: float = 0.1,
        window_size: int = 10,
    ) -> None:
        """
        Initialize phase drift detector.
        
        Args:
            threshold: Maximum allowed coherence drift
            window_size: Window for baseline comparison
        """
        super().__init__(threshold, window_size)
        self.baseline_coherence: Optional[float] = None
        self._coherence_history: List[float] = []
    
    def set_baseline(self, coherence: float) -> None:
        """
        Set baseline coherence.
        
        Args:
            coherence: Baseline coherence value
        """
        self.baseline_coherence = coherence
    
    def check_drift(
        self,
        current_coherence: float,
        source: str = "unknown",
    ) -> tuple[bool, float]:
        """
        Check for phase coherence drift.
        
        Args:
            current_coherence: Current coherence value
            source: Identifier of source entity
        
        Returns:
            Tuple of (drift_detected, drift_magnitude)
        """
        self._coherence_history.append(current_coherence)
        
        if self.baseline_coherence is None:
            self.baseline_coherence = current_coherence
            return False, 0.0
        
        drift = abs(current_coherence - self.baseline_coherence)
        
        if drift > self.threshold:
            event = DriftEvent(
                timestamp=datetime.now(),
                drift_type="phase",
                magnitude=drift,
                threshold=self.threshold,
                source=source,
            )
            self.record_event(event)
            return True, drift
        
        return False, drift
    
    def get_coherence_trend(self) -> str:
        """
        Analyze coherence trend.
        
        Returns:
            Trend description
        """
        if len(self._coherence_history) < 2:
            return "insufficient_data"
        
        recent = self._coherence_history[-self.window_size:]
        x = np.arange(len(recent))
        y = np.array(recent)
        
        slope = np.polyfit(x, y, 1)[0]
        
        if abs(slope) < 0.01:
            return "stable"
        elif slope > 0:
            return "improving"
        else:
            return "degrading"


class BoundaryDriftDetector(DriftDetector):
    """Detect boundary integrity drift."""
    
    def __init__(
        self,
        threshold: float = 0.05,
        window_size: int = 10,
    ) -> None:
        """
        Initialize boundary drift detector.
        
        Args:
            threshold: Maximum allowed boundary degradation
            window_size: Window for trend analysis
        """
        super().__init__(threshold, window_size)
        self._boundary_history: List[float] = []
    
    def check_drift(
        self,
        current_boundary: float,
        previous_boundary: Optional[float] = None,
        source: str = "unknown",
    ) -> tuple[bool, float]:
        """
        Check for boundary integrity drift.
        
        Args:
            current_boundary: Current boundary integrity
            previous_boundary: Previous boundary (if available)
            source: Identifier of source entity
        
        Returns:
            Tuple of (drift_detected, drift_magnitude)
        """
        self._boundary_history.append(current_boundary)
        
        if previous_boundary is None:
            if len(self._boundary_history) < 2:
                return False, 0.0
            previous_boundary = self._boundary_history[-2]
        
        # Boundary drift is DEGRADATION (negative change)
        drift = previous_boundary - current_boundary
        
        if drift > self.threshold:
            event = DriftEvent(
                timestamp=datetime.now(),
                drift_type="boundary",
                magnitude=drift,
                threshold=self.threshold,
                source=source,
            )
            self.record_event(event)
            return True, drift
        
        return False, drift


class RoleDriftDetector(DriftDetector):
    """Detect role state drift."""
    
    def __init__(
        self,
        threshold: float = 0.5,
        window_size: int = 10,
    ) -> None:
        """
        Initialize role drift detector.
        
        Args:
            threshold: Maximum allowed role state drift
            window_size: Window for trend analysis
        """
        super().__init__(threshold, window_size)
        self.baseline_state: Optional[npt.NDArray[np.float64]] = None
        self._state_history: List[npt.NDArray[np.float64]] = []
    
    def set_baseline(self, state: npt.NDArray[np.float64]) -> None:
        """
        Set baseline role state.
        
        Args:
            state: Baseline state vector
        """
        self.baseline_state = state.copy()
    
    def check_drift(
        self,
        current_state: npt.NDArray[np.float64],
        source: str = "unknown",
    ) -> tuple[bool, float]:
        """
        Check for role state drift.
        
        Args:
            current_state: Current role state
            source: Identifier of source entity
        
        Returns:
            Tuple of (drift_detected, drift_magnitude)
        """
        self._state_history.append(current_state.copy())
        
        if self.baseline_state is None:
            self.baseline_state = current_state.copy()
            return False, 0.0
        
        drift = float(np.linalg.norm(current_state - self.baseline_state))
        
        if drift > self.threshold:
            event = DriftEvent(
                timestamp=datetime.now(),
                drift_type="role",
                magnitude=drift,
                threshold=self.threshold,
                source=source,
            )
            self.record_event(event)
            return True, drift
        
        return False, drift
