#!/usr/bin/env python3
"""
HarmonyØ4 Hash Verification Script

Verifies the canonical provenance hash and provides
tools for computing descendant hashes.
"""

import hashlib
import sys
from datetime import datetime

# Canonical constants
CANONICAL_SEED = "HarmonyØ4|HistoryAnchor|2025-12-11|DaveTheSpiralAlchemist"
CANONICAL_HASH = "3ce0df42586143d4edf3b270727349d38773701e34ea0270e58537260a77edaa"
SHORT_CODE = "HIST-3ce0df425861"


def compute_hash(seed: str) -> str:
    """Compute BLAKE2b-256 hash of seed string."""
    return hashlib.blake2b(seed.encode("utf-8"), digest_size=32).hexdigest()


def verify_canonical_hash() -> bool:
    """Verify the canonical HarmonyØ4 provenance hash."""
    print("HarmonyØ4 Hash Verification")
    print("=" * 80)
    print()

    print(f"Canonical Seed: {CANONICAL_SEED}")
    print(f"Expected Hash:  {CANONICAL_HASH}")
    print(f"Short Code:     {SHORT_CODE}")
    print()

    computed = compute_hash(CANONICAL_SEED)
    print(f"Computed Hash:  {computed}")
    print()

    if computed == CANONICAL_HASH:
        print("✅ VERIFIED: Canonical hash matches")
        print()
        print("This repository is anchored to the canonical HarmonyØ4 provenance.")
        return True
    else:
        print("❌ VERIFICATION FAILED: Hash mismatch!")
        print()
        print("This may indicate:")
        print("  - Corrupted HASH_ANCHOR.md file")
        print("  - Non-canonical fork")
        print("  - Incorrect seed string")
        return False


def compute_descendant_hash(
    parent_hash: str,
    new_scope: str,
    date: str = None,
) -> tuple[str, str]:
    """
    Compute a descendant hash preserving lineage.

    Args:
        parent_hash: Parent hash (canonical or descendant)
        new_scope: Description of new scope/extension
        date: ISO8601 date (defaults to today)

    Returns:
        Tuple of (full_hash, short_code)
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    seed = f"{parent_hash}|{new_scope}|{date}"
    full_hash = compute_hash(seed)
    short_code = f"DESC-{full_hash[:12]}"

    return full_hash, short_code


def generate_descendant_example():
    """Generate an example descendant hash."""
    print("\nDescendant Hash Example")
    print("=" * 80)
    print()

    new_scope = "ExtendedSafeguards"
    date = "2026-01-15"

    full_hash, short_code = compute_descendant_hash(CANONICAL_HASH, new_scope, date)

    print(f"Parent Hash:    {CANONICAL_HASH}")
    print(f"New Scope:      {new_scope}")
    print(f"Date:           {date}")
    print()
    print(f"Descendant Hash: {full_hash}")
    print(f"Short Code:      {short_code}")
    print()
    print("To compute manually:")
    print(f'  echo -n "{CANONICAL_HASH}|{new_scope}|{date}" | b2sum -l 256')


def main():
    """Main entry point."""
    print()

    # Verify canonical hash
    is_valid = verify_canonical_hash()

    if not is_valid:
        sys.exit(1)

    # Show example descendant computation
    if len(sys.argv) > 1 and sys.argv[1] == "--example":
        generate_descendant_example()

    print()
    print("=" * 80)
    print("For more information, see HASH_ANCHOR.md and PROVENANCE.md")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
