#!/usr/bin/env python3
"""
HarmonyØ4 Ethics Verification Script

Scans code for prohibited patterns that violate ethical invariants.
This is the CRITICAL checkpoint—all PRs must pass this check.
"""

import ast
import re
import sys
from pathlib import Path
from typing import List, Tuple


class EthicsViolation:
    """Record of an ethics violation."""

    def __init__(
        self,
        file_path: str,
        line_number: int,
        violation_type: str,
        message: str,
        severity: str = "ERROR",
    ):
        self.file_path = file_path
        self.line_number = line_number
        self.violation_type = violation_type
        self.message = message
        self.severity = severity

    def __str__(self) -> str:
        return (
            f"{self.severity}: {self.file_path}:{self.line_number} - "
            f"[{self.violation_type}] {self.message}"
        )


class EthicsVerifier:
    """Main ethics verification engine."""

    # Prohibited patterns
    COERCION_KEYWORDS = [
        r"\bforce[_\w]*\(",
        r"\bmanipulate[_\w]*\(",
        r"\bextract[_\w]*\(",
        r"\boverride[_\w]*consent",
        r"\bbypass[_\w]*boundary",
        r"\.backward\(",  # Unconstrained gradient descent
    ]

    HIDDEN_OPTIMIZATION_PATTERNS = [
        r"# TODO.*bypass",
        r"# HACK.*consent",
        r"# TEMP.*disable.*ethics",
        r"if\s+False\s*:.*consent",  # Dead code bypassing consent
    ]

    CONSENT_BYPASS_PATTERNS = [
        r"consent\s*=\s*True\s*#.*always",
        r"if\s+not\s+consent\s*:.*pass\s*#.*ignore",
        r"consent_required\s*=\s*False",
    ]

    def __init__(self):
        self.violations: List[EthicsViolation] = []

    def verify_file(self, file_path: Path) -> None:
        """Verify a single Python file."""
        if not file_path.suffix == ".py":
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")

            # Pattern-based checks
            self._check_coercion_keywords(file_path, lines)
            self._check_hidden_optimization(file_path, lines)
            self._check_consent_bypass(file_path, lines)

            # AST-based checks
            try:
                tree = ast.parse(content, filename=str(file_path))
                self._check_ast(file_path, tree)
            except SyntaxError:
                # Syntax errors will be caught by linter
                pass

        except Exception as e:
            print(f"Warning: Could not verify {file_path}: {e}")

    def _check_coercion_keywords(self, file_path: Path, lines: List[str]) -> None:
        """Check for coercive function patterns."""
        for pattern in self.COERCION_KEYWORDS:
            for line_num, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    # Allow in comments explaining what NOT to do
                    if "# PROHIBITED" in line or "# Example of violation" in line:
                        continue

                    self.violations.append(
                        EthicsViolation(
                            file_path=str(file_path),
                            line_number=line_num,
                            violation_type="COERCION",
                            message=f"Potential coercive pattern: {pattern}",
                            severity="WARNING",
                        )
                    )

    def _check_hidden_optimization(self, file_path: Path, lines: List[str]) -> None:
        """Check for hidden or commented-out optimization."""
        for pattern in self.HIDDEN_OPTIMIZATION_PATTERNS:
            for line_num, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    self.violations.append(
                        EthicsViolation(
                            file_path=str(file_path),
                            line_number=line_num,
                            violation_type="HIDDEN_OPTIMIZATION",
                            message="Potential attempt to bypass ethics checks",
                            severity="ERROR",
                        )
                    )

    def _check_consent_bypass(self, file_path: Path, lines: List[str]) -> None:
        """Check for consent mechanism bypasses."""
        for pattern in self.CONSENT_BYPASS_PATTERNS:
            for line_num, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    self.violations.append(
                        EthicsViolation(
                            file_path=str(file_path),
                            line_number=line_num,
                            violation_type="CONSENT_BYPASS",
                            message="Potential consent bypass detected",
                            severity="ERROR",
                        )
                    )

    def _check_ast(self, file_path: Path, tree: ast.AST) -> None:
        """AST-based checks for structural violations."""
        for node in ast.walk(tree):
            # Check for forced state transitions
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Attribute):
                        if target.attr == "_internal_state":
                            # Direct internal state manipulation
                            self.violations.append(
                                EthicsViolation(
                                    file_path=str(file_path),
                                    line_number=node.lineno,
                                    violation_type="BOUNDARY_VIOLATION",
                                    message="Direct internal state manipulation bypasses consent",
                                    severity="WARNING",
                                )
                            )

    def verify_directory(self, directory: Path) -> None:
        """Recursively verify all Python files in directory."""
        for py_file in directory.rglob("*.py"):
            # Skip test files and verification script itself
            if "test_" in py_file.name or "verify_ethics" in py_file.name:
                continue

            self.verify_file(py_file)

    def report(self) -> Tuple[int, int]:
        """
        Print verification report.

        Returns:
            Tuple of (num_errors, num_warnings)
        """
        errors = [v for v in self.violations if v.severity == "ERROR"]
        warnings = [v for v in self.violations if v.severity == "WARNING"]

        if not self.violations:
            print("✅ Ethics verification passed—no violations detected.")
            return 0, 0

        print(f"\n{'='*80}")
        print("ETHICS VERIFICATION REPORT")
        print(f"{'='*80}\n")

        if errors:
            print(f"❌ ERRORS ({len(errors)}):\n")
            for error in errors:
                print(f"  {error}")
            print()

        if warnings:
            print(f"⚠️  WARNINGS ({len(warnings)}):\n")
            for warning in warnings:
                print(f"  {warning}")
            print()

        print(f"{'='*80}")
        print(f"Total: {len(errors)} errors, {len(warnings)} warnings")
        print(f"{'='*80}\n")

        if errors:
            print("❌ Ethics verification FAILED")
            print("\nEthical violations detected. Review the errors above.")
            print("Resolve all ERRORs before submitting PR.")
        else:
            print("⚠️  Ethics verification passed with warnings")
            print("Review warnings—they may indicate design issues.")

        return len(errors), len(warnings)


def main():
    """Main entry point."""
    print("HarmonyØ4 Ethics Verification")
    print("=" * 80)

    # Get project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    harmony_dir = project_root / "harmony"

    if not harmony_dir.exists():
        print(f"❌ Error: harmony/ directory not found at {harmony_dir}")
        sys.exit(1)

    print(f"Verifying: {harmony_dir}\n")

    verifier = EthicsVerifier()
    verifier.verify_directory(harmony_dir)

    num_errors, num_warnings = verifier.report()

    # Exit code: 0 = success, 1 = errors found
    if num_errors > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
