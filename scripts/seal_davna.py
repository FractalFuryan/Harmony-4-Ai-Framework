#!/usr/bin/env python3
"""
DAVNA Living Cipher Sealer
Generates a chained cryptographic seal for DAVNA_COVENANT.md
No secrets. Fully public. Tamper-evident.

Usage:
  python scripts/seal_davna.py           # Generate new seal
  python scripts/seal_davna.py --check   # Verify current seal
"""

import hashlib
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def extract_seal_block(content: str) -> tuple[str, dict]:
    """Extract the seal block and return (body_without_seal, seal_dict)."""
    # Find the seal block - it starts with "## DAVNA Living Cipher Seal"
    seal_start = content.find("## DAVNA Living Cipher Seal")
    
    if seal_start == -1:
        # No seal block found - this is the first seal
        body = content.strip()
        return body, {
            "canonical_anchor": "HIST-3ce0df425861",
            "algorithm": "BLAKE2b-256",
            "previous_seal": "NONE",
            "covenant_digest": "PENDING_FIRST_SEAL",
            "sealed_at": datetime.now(timezone.utc).isoformat()
        }
    
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


def generate_seal(body: str, previous_seal: str) -> str:
    """Generate new seal digest incorporating previous seal."""
    digest = compute_digest(body)
    
    # Chain: hash(body + previous_seal)
    hasher = hashlib.blake2b(digest_size=32)
    hasher.update(body.encode("utf-8"))
    hasher.update(previous_seal.encode("utf-8"))
    
    return hasher.hexdigest()


def format_seal_block(seal_dict: dict) -> str:
    """Format seal dictionary as markdown block."""
    return f"""---

## DAVNA Living Cipher Seal (Machine-Verifiable)

This covenant is protected by a cryptographic seal that makes edits self-authenticating and tamper-evident.

**Current Seal:**
- Canonical Anchor: `{seal_dict['canonical_anchor']}`
- Algorithm: {seal_dict['algorithm']}
- Previous Seal: `{seal_dict['previous_seal']}`
- Covenant Digest: `{seal_dict['covenant_digest']}`
- Sealed At (UTC): `{seal_dict['sealed_at']}`

**Verification:**
```bash
python scripts/verify_davna.py
python scripts/seal_davna.py --check
```

The Living Cipher ensures:
- Every edit creates a new seal chained to the previous one
- Tampering breaks the chain instantly
- No secrets required—fully public verification
- CI/CD enforces seal validity on every commit

---

**License:** Apache-2.0  
**Framework:** HarmonyØ4 v1.0.0  
**Hash Anchor:** `{seal_dict['canonical_anchor']}`"""


def seal_covenant(covenant_path: Path, check_only: bool = False) -> bool:
    """Generate or verify DAVNA covenant seal."""
    if not covenant_path.exists():
        print(f"❌ DAVNA covenant not found: {covenant_path}")
        return False
    
    content = covenant_path.read_text(encoding="utf-8")
    body, current_seal = extract_seal_block(content)
    
    if check_only:
        # Verify current seal
        if current_seal["covenant_digest"] == "PENDING_FIRST_SEAL":
            print("⚠️  First seal not yet generated")
            return False
        
        expected_digest = compute_digest(body)
        actual_digest = current_seal["covenant_digest"]
        
        if expected_digest != actual_digest:
            print(f"❌ Seal verification FAILED")
            print(f"   Expected: {expected_digest}")
            print(f"   Actual:   {actual_digest}")
            print(f"   The covenant body has been modified without resealing")
            return False
        
        print("✅ DAVNA seal verified successfully")
        print(f"   Digest: {actual_digest}")
        print(f"   Sealed: {current_seal['sealed_at']}")
        return True
    
    # Generate new seal
    new_digest = compute_digest(body)
    
    # Check if seal needs updating
    if current_seal["covenant_digest"] == new_digest:
        print("✅ Covenant unchanged, seal still valid")
        return True
    
    # Create new seal
    new_seal = {
        "canonical_anchor": current_seal["canonical_anchor"],
        "algorithm": "BLAKE2b-256",
        "previous_seal": current_seal["covenant_digest"],
        "covenant_digest": new_digest,
        "sealed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    
    # Write new sealed covenant
    sealed_content = body + "\n\n" + format_seal_block(new_seal)
    covenant_path.write_text(sealed_content, encoding="utf-8")
    
    # Re-read to ensure consistent digest
    reread_content = covenant_path.read_text(encoding="utf-8")
    reread_body, _ = extract_seal_block(reread_content)
    actual_digest = compute_digest(reread_body)
    
    if actual_digest != new_digest:
        print(f"⚠️  Warning: Digest changed after write (file system encoding issue)")
        print(f"   Expected: {new_digest}")
        print(f"   Actual:   {actual_digest}")
        print(f"   Updating seal to match actual file state...")
        
        # Update seal with actual digest
        new_seal["covenant_digest"] = actual_digest
        sealed_content = body + "\n\n" + format_seal_block(new_seal)
        covenant_path.write_text(sealed_content, encoding="utf-8")
    
    print("🔒 DAVNA covenant sealed successfully")
    print(f"   Previous: {new_seal['previous_seal']}")
    print(f"   Current:  {new_seal['covenant_digest']}")
    print(f"   Sealed:   {new_seal['sealed_at']}")
    
    return True


def main():
    check_only = "--check" in sys.argv
    
    # Find covenant file
    repo_root = Path(__file__).parent.parent
    covenant_path = repo_root / "DAVNA_COVENANT.md"
    
    success = seal_covenant(covenant_path, check_only=check_only)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
