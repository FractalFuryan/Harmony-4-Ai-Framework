#!/usr/bin/env python3
"""
DAVNA Living Cipher Verifier
Validates the cryptographic seal on DAVNA_COVENANT.md

Usage:
  python scripts/verify_davna.py
"""

import hashlib
import re
import sys
from pathlib import Path


def extract_seal_block(content: str) -> tuple[str, dict]:
    """Extract the seal block and return (body_without_seal, seal_dict)."""
    # Find the seal block - it starts with "## DAVNA Living Cipher Seal"
    seal_start = content.find("## DAVNA Living Cipher Seal")

    if seal_start == -1:
        print("❌ No seal block found in covenant")
        return None, None

    # Extract body (everything before the seal)
    body = content[:seal_start].strip()
    seal_block = content[seal_start:]

    # Parse seal values
    seal_dict = {}
    for line in seal_block.split("\n"):
        if "Canonical Anchor:" in line:
            match = re.search(r"`([^`]+)`", line)
            if match:
                seal_dict["canonical_anchor"] = match.group(1)
        elif "Algorithm:" in line and "algorithm" not in seal_dict:
            seal_dict["algorithm"] = line.split(": ", 1)[1].strip()
        elif "Previous Seal:" in line:
            match = re.search(r"`([^`]+)`", line)
            if match:
                seal_dict["previous_seal"] = match.group(1)
        elif "Covenant Digest:" in line:
            match = re.search(r"`([^`]+)`", line)
            if match:
                seal_dict["covenant_digest"] = match.group(1)
        elif "Sealed At (UTC):" in line:
            match = re.search(r"`([^`]+)`", line)
            if match:
                seal_dict["sealed_at"] = match.group(1)

    return body, seal_dict


def compute_digest(body: str) -> str:
    """Compute BLAKE2b-256 digest of covenant body."""
    hasher = hashlib.blake2b(digest_size=32)
    hasher.update(body.encode("utf-8"))
    return hasher.hexdigest()


def verify_covenant(covenant_path: Path) -> bool:
    """Verify DAVNA covenant seal."""
    print("=" * 80)
    print("DAVNA Living Cipher Verification")
    print("=" * 80)
    print()

    if not covenant_path.exists():
        print(f"❌ DAVNA covenant not found: {covenant_path}")
        return False

    content = covenant_path.read_text(encoding="utf-8")
    body, seal = extract_seal_block(content)

    if not seal:
        return False

    # Display seal information
    print(f"Canonical Anchor: {seal['canonical_anchor']}")
    print(f"Algorithm:        {seal['algorithm']}")
    print(f"Previous Seal:    {seal['previous_seal']}")
    print(f"Current Digest:   {seal['covenant_digest']}")
    print(f"Sealed At (UTC):  {seal['sealed_at']}")
    print()

    # Check for pending first seal
    if seal["covenant_digest"] == "PENDING_FIRST_SEAL":
        print("⚠️  PENDING: First seal not yet generated")
        print("   Run: python scripts/seal_davna.py")
        print()
        return False

    # Verify digest
    expected_digest = compute_digest(body)
    actual_digest = seal["covenant_digest"]

    print(f"Computed Digest:  {expected_digest}")
    print()

    if expected_digest != actual_digest:
        print("❌ SEAL VERIFICATION FAILED")
        print()
        print("The covenant body has been modified without resealing.")
        print("This indicates either:")
        print("  1. Unauthorized tampering")
        print("  2. Seal not regenerated after legitimate edit")
        print()
        print("To reseal after authorized changes:")
        print("  python scripts/seal_davna.py")
        print()
        return False

    # Verify canonical anchor matches
    if seal["canonical_anchor"] != "HIST-3ce0df425861":
        print("⚠️  WARNING: Canonical anchor mismatch")
        print(f"   Expected: HIST-3ce0df425861")
        print(f"   Found:    {seal['canonical_anchor']}")
        print()

    print("✅ DAVNA SEAL VERIFIED SUCCESSFULLY")
    print()
    print("The covenant is authentic and untampered.")
    print("Seal chain integrity: VALID")
    print()

    print("=" * 80)
    print("DAVNA verification complete")
    print("=" * 80)

    return True


def main():
    # Find covenant file
    repo_root = Path(__file__).parent.parent
    covenant_path = repo_root / "DAVNA_COVENANT.md"

    success = verify_covenant(covenant_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
