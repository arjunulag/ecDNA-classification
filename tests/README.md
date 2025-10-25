# Tests

This directory contains unit tests and integration tests for the ecDNA classification project.

## Running Tests

### Run all tests
```bash
python -m pytest tests/
```

### Run specific test file
```bash
python -m pytest tests/test_utils.py
```

### Run with coverage
```bash
python -m pytest --cov=src tests/
```

## Test Structure

- `test_utils.py`: Tests for utility functions
- `test_data_loading.py`: Tests for data loading (to be implemented)
- `test_data_processing.py`: Tests for data processing (to be implemented)
- `test_feature_engineering.py`: Tests for feature engineering (to be implemented)

## Adding New Tests

1. Create a new test file: `test_<module_name>.py`
2. Import the module to test
3. Create test class inheriting from `unittest.TestCase`
4. Write test methods starting with `test_`

Example:
```python
import unittest
from src.my_module import my_function

class TestMyModule(unittest.TestCase):
    def test_my_function(self):
        result = my_function(input_data)
        self.assertEqual(result, expected_output)
```

## Test Data

Mock data for testing should be minimal and included in the test files themselves or in a `fixtures/` subdirectory.

