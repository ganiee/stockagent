# Feature 009: Verification

## Prerequisites
- Features 001-008 completed
- pytest installed (`pip install pytest pytest-cov pytest-mock`)

## Local Commands to Run

### 1. Verify Test Directory Structure
```bash
ls -la tests/
ls -la tests/unit/
ls -la tests/integration/
```

Expected: All directories exist with test files.

### 2. Verify pytest Configuration
```bash
# Check config file exists
ls pytest.ini || ls pyproject.toml | xargs grep -l "pytest"

# Verify pytest can find tests
pytest --collect-only
```

Expected: pytest finds and lists all tests.

### 3. Run All Tests
```bash
pytest -v
```

Expected: All tests pass (exit code 0).

### 4. Run Unit Tests Only
```bash
pytest tests/unit/ -v
```

Expected: All unit tests pass.

### 5. Run Integration Tests Only
```bash
pytest tests/integration/ -v
```

Expected: All integration tests pass.

### 6. Run with Coverage
```bash
pytest --cov=stockagent --cov-report=term-missing
```

Expected:
- Coverage report generated
- `analysis/indicators.py` > 80%
- `analysis/scoring.py` > 80%

### 7. Verify Indicator Tests
```bash
pytest tests/unit/test_indicators.py -v
```

Expected: All indicator tests pass.

### 8. Verify Scoring Tests
```bash
pytest tests/unit/test_scoring.py -v
```

Expected: All scoring tests pass.

### 9. Verify Sentiment Tests
```bash
pytest tests/unit/test_sentiment.py -v
```

Expected: All sentiment tests pass.

### 10. Verify Client Tests (Mocked)
```bash
pytest tests/integration/test_polygon_client.py -v
```

Expected: All client tests pass without network calls.

### 11. Verify Workflow Tests
```bash
pytest tests/integration/test_workflow.py -v
```

Expected: Workflow integration tests pass.

### 12. Verify Golden Run Test
```bash
pytest -k "golden" -v
```

Expected: Golden run test passes.

## Quick Verification (All-in-One)
```bash
pytest -v --tb=short && echo "Feature 009 verification: PASSED"
```

## Coverage Report Command
```bash
pytest --cov=stockagent --cov-report=html
# Then open htmlcov/index.html in browser
```

## Minimum Test Count Verification
```bash
pytest --collect-only -q | tail -1
# Should show "X tests collected"
# Expect at least 20 tests
```
