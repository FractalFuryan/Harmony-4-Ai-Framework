# Contributing to HarmonyØ4

Thank you for your interest in contributing to HarmonyØ4. This project operates under strict ethical constraints—contributions must align with the core principles of coherence, consent, and non-coercion.

## Core Principles

Before contributing, understand that HarmonyØ4 is **not a typical ML/AI project**:

1. **Stability emerges—it is never forced**
2. **Consent is binary, explicit, and revocable**
3. **No optimization that violates observer boundaries**
4. **All changes must preserve ethical invariants**

## What We Accept

### ✅ Welcome Contributions

* Bug fixes that preserve invariants
* Documentation improvements
* Test coverage expansion
* Performance optimizations that **do not** compromise ethics
* Accessibility improvements
* Translation and localization
* Examples demonstrating ethical use

### ❌ What Will Be Rejected

* Code that introduces coercive logic
* Optimizations that erode consent mechanisms
* Features that enable extraction or manipulation
* Bypasses of boundary safeguards
* Proprietary or closed-source integrations without consent
* Code that exposes private field equations or optimization kernels

## Getting Started

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/harmony04.git
cd harmony04
```

### 2. Set Up Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### 3. Run Tests

```bash
pytest
```

### 4. Run Ethics Verification

```bash
python scripts/verify_ethics.py
```

**All PRs must pass ethics verification.** This is non-negotiable.

## Development Workflow

### Branch Naming

* `feature/your-feature-name`
* `fix/issue-description`
* `docs/documentation-update`

### Commit Messages

Use clear, imperative mood:

```
Add boundary drift detection to observer module

- Implement threshold-based detection
- Add tests for edge cases
- Preserve consent revocation logic
```

### Before Submitting a PR

1. Run `black .` to format code
2. Run `ruff check .` to lint
3. Run `pytest` to verify tests pass
4. Run `python scripts/verify_ethics.py` to ensure ethics compliance
5. Update documentation if adding features

## Pull Request Process

1. **Fill out the PR template completely**
2. **Link to related issues**
3. **Describe ethical implications** if applicable
4. **Ensure CI passes** (tests + ethics verification)
5. **Be responsive** to review feedback

### PR Review Criteria

* Code quality and clarity
* Test coverage (aim for >90%)
* Documentation completeness
* **Ethics compliance** (automated + manual review)
* Performance impact
* Backward compatibility

## Ethics Review

All PRs undergo **dual review**:

1. **Automated**: `verify_ethics.py` scans for prohibited patterns
2. **Human**: Maintainers assess conceptual alignment

**Red flags include:**

* Forced state transitions
* Hidden consent mechanisms
* Boundary violations
* Drift without detection
* Optimization over observer integrity

## Testing Requirements

* All new features require tests
* Bug fixes require regression tests
* Aim for >90% code coverage
* Include edge cases and failure modes

## Documentation Standards

* Public API must have docstrings (Google style)
* Complex algorithms need inline comments
* Update `docs/` for conceptual changes
* Include usage examples

## Community

* Be respectful and constructive
* Assume good intent
* Focus on ideas, not individuals
* Follow the [Code of Conduct](CODE_OF_CONDUCT.md)

## Questions?

* Open a [Discussion](https://github.com/harmony04/harmony04/discussions) for general questions
* Open an [Issue](https://github.com/harmony04/harmony04/issues) for bugs or feature requests
* See [docs/philosophy.md](docs/philosophy.md) for deeper context

## License

By contributing, you agree that your contributions will be licensed under the Apache-2.0 License.

---

**Remember**: HarmonyØ4 prioritizes **ethics over efficiency**. If you're unsure whether a change aligns with project values, ask before implementing.
