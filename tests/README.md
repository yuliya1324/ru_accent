# ru_accent_poet Test Suite

This directory contains automated tests for the ru_accent_poet package. The tests ensure that the package functions correctly and maintains compatibility with the latest versions of TensorFlow and Keras.

## Test Structure

The test suite is organized into separate modules:

1. `test_accent.py` - Tests for the core accent functionality
   - Tests for the combined approach (neural + rules)
   - Tests for rules-based accentuation
   - Tests for neural-based accentuation
   - Tests for file processing functions

2. `test_compatibility.py` - Tests specifically for TensorFlow/Keras compatibility
   - Tests for TensorFlow and Keras version requirements
   - Tests for the PatchedAccent class
   - Tests for model prediction behavior

## Running Tests

You can run the tests using either pytest or unittest:

### Using pytest (recommended)

```bash
# From the project root directory
python run_tests.py

# Or directly with pytest
pytest -v
```

### Using unittest

```bash
# From the project root directory
python run_tests.py --unittest

# Or directly with unittest
python -m unittest discover -v
```

## Adding New Tests

When adding new tests:

1. Follow the existing naming convention: `test_*.py` for test modules and `test_*` for test methods
2. Organize tests by functionality in appropriate test classes
3. Use descriptive method names that clearly state what is being tested
4. Use appropriate assertions to verify expected behavior
5. For Russian text tests, use `re.compile()` with regex patterns to allow for reasonable variations in accent placement

## Test Coverage

The current test suite covers:

- Basic accentuation functionality
- Special cases (short words, 'ё', etc.)
- Proper handling of punctuation and capitalization
- TensorFlow/Keras compatibility
- File processing functions
- Dictionary and neural network approaches

## Requirements

To run the tests, you need:

- pytest (for running the tests with pytest)
- tensorflow (≥ 2.15.0)
- All other dependencies required by ru_accent_poet