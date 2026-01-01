## Description

<!-- Provide a clear and concise description of your changes -->

## Type of Change

<!-- Mark relevant options with an 'x' -->

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Ethics/safeguard improvement
- [ ] Performance optimization
- [ ] Test coverage expansion

## Ethical Impact Assessment

<!-- REQUIRED: Answer these questions for all PRs -->

**Does this PR affect consent mechanisms?** Yes / No
<!-- If yes, explain how consent is preserved or enhanced -->

**Does this PR modify boundary logic?** Yes / No
<!-- If yes, describe safeguards against violations -->

**Could this change introduce coercive patterns?** Yes / No
<!-- If yes, explain mitigation or why it's acceptable -->

**Does this preserve all invariants?** Yes / No
<!-- If no, explain which invariants changed and why -->

## Testing

<!-- Describe the tests you ran to verify your changes -->

- [ ] All existing tests pass (`pytest`)
- [ ] Added tests for new functionality
- [ ] Tested edge cases and failure modes
- [ ] Ethics verification passes (`python scripts/verify_ethics.py`)
- [ ] Code formatting applied (`black .`)
- [ ] Linting passes (`ruff check .`)

## Checklist

- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published
- [ ] I have read and agree to the [Code of Conduct](../CODE_OF_CONDUCT.md)
- [ ] I have read the [Contributing Guidelines](../CONTRIBUTING.md)

## Related Issues

<!-- Link to related issues using #issue_number -->

Fixes #
Relates to #

## Additional Context

<!-- Add any other context, screenshots, or benchmarks about the pull request here -->

---

**By submitting this PR, I confirm that my contribution aligns with HarmonyØ4's ethical principles: coherence, consent, and non-coercion.**
