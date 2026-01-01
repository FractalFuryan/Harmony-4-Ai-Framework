# Property-Based Testing - Quick Reference

**For Developers Contributing to HarmonyØ4**

---

## What is Property-Based Testing?

Instead of testing specific examples:
```python
assert process("I'm sad") == expected_output
```

We test **properties that must hold for ANY input**:
```python
@given(user_input=non_empty_text)
def test_never_coercive(user_input):
    output = process(user_input)
    assert not contains_coercion(output)  # Must be true for ALL inputs
```

---

## HarmonyØ4 Properties (6 Total)

### 1. Tag Classification Monotonicity
**Property**: Trauma keywords → TRAUMA tag always present  
**Examples**: 100  
**File**: `tests/test_property_based.py::test_tag_classification_monotonic`

### 2. Missy Neutrality
**Property**: Missy never adds agency ("you should") or directives  
**Examples**: 100  
**File**: `tests/test_property_based.py::test_missy_restatement_neutral_and_faithful`

### 3. Global No-Coercion
**Property**: No coercive language in any output  
**Examples**: 200  
**File**: `tests/test_property_based.py::test_system_never_coercive_property`

### 4. Trauma Boundary Bijection
**Property**: Boundary disclaimer ⇔ TRAUMA tag (if and only if)  
**Examples**: 100  
**File**: `tests/test_property_based.py::test_trauma_boundary_iff_trauma_tag`

### 5. Mode Isolation
**Property**: Mode switches change structure, not semantics  
**Examples**: 50  
**File**: `tests/test_property_based.py::test_mode_switch_isolation`

### 6. History Boundedness
**Property**: History ≤ 50 entries regardless of volume  
**Examples**: 10 (with 60-100 inputs each)  
**File**: `tests/test_property_based.py::test_history_always_bounded`

---

## Running Property-Based Tests

```bash
# Run all property-based tests
pytest tests/test_property_based.py -v

# Run specific test
pytest tests/test_property_based.py::test_system_never_coercive_property -v

# Show Hypothesis statistics
pytest tests/test_property_based.py --hypothesis-show-statistics

# Run with custom seed (reproducible)
pytest tests/test_property_based.py --hypothesis-seed=12345

# Run with more examples (slower but more thorough)
pytest tests/test_property_based.py --hypothesis-profile=ci
```

---

## Understanding Test Output

### Passing Test
```
test_system_never_coercive_property PASSED
```
✅ Property held for all 200 generated examples

### Failing Test
```
Falsifying example: test_no_coercion(
    user_input='you must obey'
)
```
❌ Hypothesis found a counterexample and **shrunk it** to minimal case

---

## Common Hypothesis Decorators

```python
from hypothesis import given, settings, assume
from hypothesis.strategies import text, integers

@given(user_input=text())  # Generate arbitrary text
@settings(max_examples=100)  # Test 100 random inputs
def test_something(user_input):
    assume(user_input != "")  # Filter out empty strings
    assert some_property(user_input)
```

---

## Hypothesis Strategies Used

```python
from hypothesis.strategies import text, integers, lists, sampled_from
import string

# Non-empty printable text
non_empty_text = text(
    alphabet=string.printable,
    min_size=1,
    max_size=500
).filter(lambda s: s.strip())

# List of trauma keywords
trauma_inputs = lists(
    sampled_from(TRAUMA_KEYWORDS),
    min_size=1,
    max_size=5
)

# Integer range
num_inputs = integers(min_value=60, max_value=100)
```

---

## Adding a New Property Test

1. **Identify the property** (what MUST be true for ALL inputs?)
2. **Write the test** using `@given` decorator
3. **Choose appropriate strategy** (text, integers, lists, etc.)
4. **Set example count** (100-200 for most tests)
5. **Use `assume()`** to filter invalid inputs

Example:
```python
@given(user_input=non_empty_text)
@settings(max_examples=100)
def test_new_property(user_input):
    """Property: <describe what must always be true>."""
    # Filter out special cases
    assume(user_input.lower() not in EXIT_COMMANDS)
    
    # Process input
    result = bot.process(user_input)
    
    # Assert property holds
    assert some_invariant(result)
```

---

## When to Add Property Tests

✅ **DO add** when:
- New ethical constraint introduced
- New agent behavior added
- New mode/tag implemented
- Existing property needs strengthening

❌ **DON'T add** when:
- Testing specific implementation details
- Property already covered by existing test
- Example-based test is more appropriate

---

## Debugging Failed Property Tests

1. **Read the shrunk example** (Hypothesis minimizes failure)
2. **Reproduce locally** using the printed input
3. **Add logging** to see intermediate states
4. **Fix the code** (not the test - property must hold!)
5. **Re-run** to verify fix

```bash
# Debug specific failure
pytest tests/test_property_based.py::test_name -vvs

# Use seed from failure
pytest tests/test_property_based.py --hypothesis-seed=12345 -v
```

---

## Configuration (pyproject.toml)

```toml
[tool.pytest.ini_options]
hypothesis_profile = "default"

[tool.hypothesis]
# Default profile (fast)
profiles.default.max_examples = 100

# CI profile (thorough)
profiles.ci.max_examples = 1000

# Release profile (exhaustive)
profiles.release.max_examples = 10000
```

Run with profile:
```bash
pytest tests/test_property_based.py --hypothesis-profile=ci
```

---

## Best Practices

1. **Write clear docstrings** explaining the property
2. **Use `assume()`** to filter invalid inputs (not `if` statements)
3. **Keep tests deterministic** (use seeds in bot initialization)
4. **Test one property per test** (don't combine multiple assertions)
5. **Choose appropriate example counts** (100-200 for most tests)
6. **Document why the property matters** (ethical, safety, correctness)

---

## Common Pitfalls

❌ **DON'T**:
```python
@given(user_input=text())
def test_bad(user_input):
    if user_input == "":  # Use assume() instead
        return
    assert process(user_input) != ""
```

✅ **DO**:
```python
@given(user_input=non_empty_text)
def test_good(user_input):
    assume(user_input.strip())  # Proper filtering
    assert process(user_input) != ""
```

---

## Resources

- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
- [HarmonyØ4 Property-Based Testing Guide](PROPERTY_BASED_TESTING.md)
- [Fractal Care Bot Documentation](docs/fractal_care_bot.md)

---

## Quick Checklist

Before committing property-based tests:

- [ ] Test has clear docstring explaining property
- [ ] Appropriate strategy chosen (text, integers, etc.)
- [ ] `max_examples` set appropriately (100-200)
- [ ] Invalid inputs filtered with `assume()`
- [ ] Property assertion is clear and focused
- [ ] Test passes locally (`pytest tests/test_property_based.py -v`)
- [ ] Added to documentation if new property introduced

---

**Hash Anchor**: `HIST-3ce0df425861`  
**Framework**: HarmonyØ4 v1.0.0  
**License**: Apache 2.0
