"""
Consent management for HarmonyØ4.

Implements binary, explicit, revocable consent mechanisms.
Consent is the foundational architecture—not a feature.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Set, Tuple, Optional
from datetime import datetime


class ConsentState(Enum):
    """Binary consent states."""
    GRANT = "grant"
    DENY = "deny"


@dataclass(frozen=True)
class ConsentAction:
    """Immutable consent action record."""
    entity_from: str  # Entity granting/denying consent
    entity_to: str  # Entity receiving consent decision
    action: str  # Action being consented to
    state: ConsentState  # grant or deny
    timestamp: datetime
    scope: Optional[str] = None  # Optional scope limitation


class ConsentManager:
    """
    Manage consent relations between entities.
    
    Consent is:
    - Binary: GRANT or DENY, no probabilities
    - Explicit: Must be actively granted, never assumed
    - Revocable: Can be withdrawn at any time
    - Scoped: Applies to specific actions, not global
    
    Consent does NOT chain: A→B and B→C does not imply A→C
    """
    
    def __init__(self) -> None:
        """Initialize consent manager."""
        # Map (from, to, action) -> ConsentState
        self._consent_map: Dict[Tuple[str, str, str], ConsentState] = {}
        # History of all consent actions
        self._history: list[ConsentAction] = []
        # Track entities that have ever interacted
        self._entities: Set[str] = set()
    
    def grant_consent(
        self,
        entity_from: str,
        entity_to: str,
        action: str,
        scope: Optional[str] = None,
    ) -> None:
        """
        Grant consent for an action.
        
        Args:
            entity_from: Entity granting consent
            entity_to: Entity receiving permission
            action: Action being consented to
            scope: Optional limitation on consent
        """
        key = (entity_from, entity_to, action)
        self._consent_map[key] = ConsentState.GRANT
        
        self._entities.add(entity_from)
        self._entities.add(entity_to)
        
        self._history.append(ConsentAction(
            entity_from=entity_from,
            entity_to=entity_to,
            action=action,
            state=ConsentState.GRANT,
            timestamp=datetime.now(),
            scope=scope,
        ))
    
    def revoke_consent(
        self,
        entity_from: str,
        entity_to: str,
        action: str,
    ) -> None:
        """
        Revoke previously granted consent.
        
        Args:
            entity_from: Entity revoking consent
            entity_to: Entity losing permission
            action: Action no longer consented to
        """
        key = (entity_from, entity_to, action)
        self._consent_map[key] = ConsentState.DENY
        
        self._history.append(ConsentAction(
            entity_from=entity_from,
            entity_to=entity_to,
            action=action,
            state=ConsentState.DENY,
            timestamp=datetime.now(),
        ))
    
    def check_consent(
        self,
        entity_from: str,
        entity_to: str,
        action: str,
    ) -> bool:
        """
        Check if consent is currently granted.
        
        Args:
            entity_from: Entity that must grant consent
            entity_to: Entity requesting permission
            action: Action requiring consent
        
        Returns:
            True if consent is GRANT, False otherwise (including DENY or not set)
        
        Note:
            Absence of consent is treated as DENY (explicit consent required)
        """
        key = (entity_from, entity_to, action)
        state = self._consent_map.get(key, ConsentState.DENY)
        return state == ConsentState.GRANT
    
    def get_consent_state(
        self,
        entity_from: str,
        entity_to: str,
        action: str,
    ) -> ConsentState:
        """
        Get current consent state.
        
        Args:
            entity_from: Entity granting consent
            entity_to: Entity receiving consent
            action: Action in question
        
        Returns:
            Current ConsentState (defaults to DENY if not set)
        """
        key = (entity_from, entity_to, action)
        return self._consent_map.get(key, ConsentState.DENY)
    
    def check_mutual_consent(
        self,
        entity_a: str,
        entity_b: str,
        action: str,
    ) -> bool:
        """
        Check if both entities consent to action with each other.
        
        Args:
            entity_a: First entity
            entity_b: Second entity
            action: Mutual action requiring consent
        
        Returns:
            True only if both directions are granted
        """
        return (
            self.check_consent(entity_a, entity_b, action)
            and self.check_consent(entity_b, entity_a, action)
        )
    
    def check_chain_consent(
        self,
        entity_from: str,
        entity_via: str,
        entity_to: str,
        action: str,
    ) -> bool:
        """
        Check consent chain with explicit indirect permission.
        
        Prevents transitive extraction: requires explicit consent
        at each step AND consent for indirect sharing.
        
        Args:
            entity_from: Original entity
            entity_via: Intermediate entity
            entity_to: Final entity
            action: Action being chained
        
        Returns:
            True only if all three consent relations are granted:
            - entity_from → entity_via (action)
            - entity_via → entity_to (action)
            - entity_from → entity_to (indirect-{action})
        """
        return (
            self.check_consent(entity_from, entity_via, action)
            and self.check_consent(entity_via, entity_to, action)
            and self.check_consent(entity_from, entity_to, f"indirect-{action}")
        )
    
    def get_history(self) -> list[ConsentAction]:
        """
        Get complete consent history.
        
        Returns:
            List of all consent actions (grants and revocations)
        """
        return self._history.copy()
    
    def get_entities(self) -> Set[str]:
        """
        Get all entities that have participated in consent relations.
        
        Returns:
            Set of entity identifiers
        """
        return self._entities.copy()
    
    def audit_consent_changes(self, entity: str) -> list[ConsentAction]:
        """
        Audit all consent changes involving an entity.
        
        Args:
            entity: Entity to audit
        
        Returns:
            List of consent actions where entity is sender or receiver
        """
        return [
            action for action in self._history
            if action.entity_from == entity or action.entity_to == entity
        ]
