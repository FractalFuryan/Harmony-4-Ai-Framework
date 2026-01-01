# HarmonyØ4 Deployment Checklist

Use this checklist before pushing to GitHub or releasing a version.

## Pre-Push Checklist

### Provenance Verification
- [ ] Hash anchor verified (`python scripts/verify_hash.py`)
- [ ] Canonical hash matches: `HIST-3ce0df425861`
- [ ] PROVENANCE.md and HASH_ANCHOR.md present
- [ ] If forking/extending, descendant hash computed

### Code Quality
- [ ] All Python files pass `black` formatting
- [ ] All Python files pass `ruff` linting
- [ ] All type hints pass `mypy` checking
- [ ] No TODO comments in production code
- [ ] No debug print statements

### Testing
- [ ] All tests pass locally (`pytest`)
- [ ] Test coverage ≥ 80% (`pytest --cov`)
- [ ] No skipped tests without justification
- [ ] Edge cases documented and tested
- [ ] Error handling tested

### Ethics Verification
- [ ] `python scripts/verify_ethics.py` passes
- [ ] No ERROR-level violations
- [ ] All WARNING-level violations reviewed and justified
- [ ] No coercion keywords in new code
- [ ] No consent bypass patterns
- [ ] No hidden optimization

### Documentation
- [ ] README.md is current
- [ ] Hash anchor badge present in README
- [ ] All docstrings complete (Google style)
- [ ] Examples run without errors
- [ ] CHANGELOG.md updated (if versioning)
- [ ] API changes documented

### Security
- [ ] No credentials in code
- [ ] No API keys committed
- [ ] .gitignore includes private/ and field_equations/
- [ ] No personal data in examples
- [ ] Dependencies audited (`pip-audit`)

### Configuration
- [ ] pyproject.toml version updated
- [ ] LICENSE file present
- [ ] CONTRIBUTING.md current
- [ ] CODE_OF_CONDUCT.md enforced

### CI/CD
- [ ] GitHub Actions workflow configured
- [ ] Hash verification job runs first
- [ ] Ethics verification job blocks on error
- [ ] All CI jobs pass on test branch
- [ ] Ethics verification job enabled
- [ ] Coverage reporting configured

## First GitHub Push

### Repository Setup
- [ ] Create GitHub repository (public or private)
- [ ] Add repository description
- [ ] Add topics/tags: `ai-ethics`, `consent`, `coherence`, `python`
- [ ] Enable Issues
- [ ] Enable Discussions
- [ ] Configure branch protection (require CI pass)

### Initial Commit
```bash
# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit: HarmonyØ4 v0.1.0"

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/harmony04.git

# Push
git branch -M main
git push -u origin main
```

### Post-Push Configuration
- [ ] Add CI badge to README.md
- [ ] Set up Codecov (optional)
- [ ] Create initial release/tag (v0.1.0)
- [ ] Pin exact dependency versions for reproducibility
- [ ] Archive source code for citation

## Release Checklist (v0.1.0 → v0.2.0)

### Pre-Release
- [ ] All features complete
- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md drafted
- [ ] Version bumped in pyproject.toml
- [ ] Ethics verification passes

### Release Process
- [ ] Create release branch
- [ ] Final testing on release branch
- [ ] Merge to main
- [ ] Tag release: `git tag v0.2.0`
- [ ] Push tag: `git push origin v0.2.0`
- [ ] Create GitHub Release with notes
- [ ] Build package: `python -m build`
- [ ] Upload to PyPI (if public): `twine upload dist/*`

### Post-Release
- [ ] Announce release (discussions, social media)
- [ ] Update documentation site (if exists)
- [ ] Archive release for reproducibility
- [ ] Start next milestone planning

## Common Issues to Check

### Import Errors
```bash
# Test clean install
python -m venv test_env
source test_env/bin/activate
pip install -e .
python -c "import harmony; print(harmony.__version__)"
```

### Missing Dependencies
```bash
# Verify all imports work
python -c "from harmony.api.public import *"
```

### Ethics Violations
```bash
# Scan for common issues
grep -r "force" harmony/ --include="*.py"
grep -r "override.*consent" harmony/ --include="*.py"
grep -r "bypass.*boundary" harmony/ --include="*.py"
```

### Documentation Drift
- [ ] All function signatures in docs match code
- [ ] All examples in README.md run
- [ ] All links in docs resolve

## Optional Enhancements

### Before v1.0
- [ ] Performance benchmarks established
- [ ] Additional examples (multi-agent systems)
- [ ] Tutorial notebooks (Jupyter)
- [ ] API reference documentation (Sphinx/MkDocs)
- [ ] Contribution from external contributors
- [ ] Community feedback incorporated

### Infrastructure
- [ ] Set up Read the Docs
- [ ] Configure pre-commit hooks
- [ ] Add issue templates
- [ ] Add PR checklist automation
- [ ] Set up dependabot
- [ ] Configure CODEOWNERS

### Community
- [ ] Create Discord/Slack channel (optional)
- [ ] Write blog post about philosophy
- [ ] Submit to relevant conferences
- [ ] Engage with AI ethics community

## Emergency Rollback Procedure

If critical ethics violation discovered:

1. **Immediate**: Mark all affected releases as vulnerable
2. **Within 1 hour**: Push fix to new branch
3. **Within 24 hours**: Release patched version
4. **Within 72 hours**: Post-mortem and process update

**Contact**: [SECURITY EMAIL]

---

## Final Pre-Push Command

```bash
# Run all checks in sequence
pytest && \
python scripts/verify_ethics.py && \
black harmony/ tests/ --check && \
ruff check harmony/ tests/ && \
echo "✅ All checks passed - ready to push!"
```

---

**Remember**: HarmonyØ4 prioritizes **ethics over speed**. Take time to verify.

*Last updated: January 1, 2026*
