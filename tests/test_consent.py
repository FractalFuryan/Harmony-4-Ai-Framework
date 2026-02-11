"""Tests for consent module."""

from harmony.core.consent import ConsentManager, ConsentState


def test_consent_manager_initialization():
    """Test ConsentManager initialization."""
    cm = ConsentManager()
    assert len(cm.get_entities()) == 0
    assert len(cm.get_history()) == 0


def test_grant_consent():
    """Test granting consent."""
    cm = ConsentManager()
    cm.grant_consent("alice", "bob", "share_data")

    assert cm.check_consent("alice", "bob", "share_data")
    assert not cm.check_consent("bob", "alice", "share_data")  # Not symmetric


def test_revoke_consent():
    """Test revoking consent."""
    cm = ConsentManager()
    cm.grant_consent("alice", "bob", "share_data")
    assert cm.check_consent("alice", "bob", "share_data")

    cm.revoke_consent("alice", "bob", "share_data")
    assert not cm.check_consent("alice", "bob", "share_data")


def test_default_deny():
    """Test that absence of consent is treated as DENY."""
    cm = ConsentManager()
    # Never granted
    assert not cm.check_consent("alice", "bob", "share_data")

    state = cm.get_consent_state("alice", "bob", "share_data")
    assert state == ConsentState.DENY


def test_mutual_consent():
    """Test mutual consent checking."""
    cm = ConsentManager()

    # Only one direction
    cm.grant_consent("alice", "bob", "share_data")
    assert not cm.check_mutual_consent("alice", "bob", "share_data")

    # Both directions
    cm.grant_consent("bob", "alice", "share_data")
    assert cm.check_mutual_consent("alice", "bob", "share_data")


def test_consent_chain_with_indirect():
    """Test consent chaining requires indirect consent."""
    cm = ConsentManager()

    # alice -> bob, bob -> charlie
    cm.grant_consent("alice", "bob", "share_data")
    cm.grant_consent("bob", "charlie", "share_data")

    # Not sufficient without indirect consent
    assert not cm.check_chain_consent("alice", "bob", "charlie", "share_data")

    # Grant indirect consent
    cm.grant_consent("alice", "charlie", "indirect-share_data")
    assert cm.check_chain_consent("alice", "bob", "charlie", "share_data")


def test_consent_history_tracking():
    """Test that consent changes are recorded."""
    cm = ConsentManager()

    cm.grant_consent("alice", "bob", "action1")
    cm.revoke_consent("alice", "bob", "action1")
    cm.grant_consent("bob", "charlie", "action2")

    history = cm.get_history()
    assert len(history) == 3
    assert history[0].state == ConsentState.GRANT
    assert history[1].state == ConsentState.DENY
    assert history[2].entity_from == "bob"


def test_consent_audit():
    """Test consent auditing for specific entity."""
    cm = ConsentManager()

    cm.grant_consent("alice", "bob", "action1")
    cm.grant_consent("bob", "charlie", "action2")
    cm.grant_consent("charlie", "alice", "action3")

    alice_actions = cm.audit_consent_changes("alice")
    assert len(alice_actions) == 2  # alice as sender and receiver

    bob_actions = cm.audit_consent_changes("bob")
    assert len(bob_actions) == 2
