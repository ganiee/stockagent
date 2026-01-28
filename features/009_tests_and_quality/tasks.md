# Feature 009: Tasks

## Implementation Checklist

### 1. Create Test Directory Structure
- [ ] Create `tests/` directory
- [ ] Create `tests/__init__.py`
- [ ] Create `tests/conftest.py` for shared fixtures
- [ ] Create subdirectories: `tests/unit/`, `tests/integration/`

### 2. Add pytest to Requirements
- [ ] Add `pytest` to requirements.txt
- [ ] Add `pytest-cov` for coverage
- [ ] Add `pytest-mock` for mocking
- [ ] Run `pip install -r requirements.txt`

### 3. Create pytest Configuration
- [ ] Create `pytest.ini` or add [tool.pytest] to pyproject.toml
- [ ] Configure test discovery paths
- [ ] Configure coverage settings
- [ ] Set default options (verbose, coverage)

### 4. Create Test Fixtures
- [ ] Create mock OHLCV data fixture
- [ ] Create mock technical signals fixture
- [ ] Create mock sentiment result fixture
- [ ] Create mock StockAnalysisState fixture

### 5. Write Indicator Unit Tests
- [ ] Test `calculate_sma()` with known values
- [ ] Test `calculate_rsi()` with known values
- [ ] Test `calculate_macd()` with known values
- [ ] Test `calculate_bollinger_bands()` with known values
- [ ] Test insufficient data handling (returns None)
- [ ] Test edge cases (empty list, single value)

### 6. Write Scoring Unit Tests
- [ ] Test `score_rsi()` for all ranges
- [ ] Test `score_macd()` for bullish/bearish
- [ ] Test `calculate_composite_score()` bounds
- [ ] Test `generate_recommendation()` thresholds
- [ ] Test determinism (same input → same output)

### 7. Write Sentiment Unit Tests
- [ ] Test `analyze_sentiment()` with positive headlines
- [ ] Test `analyze_sentiment()` with negative headlines
- [ ] Test `analyze_sentiment()` with neutral headlines
- [ ] Test score bounds (-1.0 to +1.0)

### 8. Write Polygon Client Tests (Mocked)
- [ ] Mock API responses
- [ ] Test `get_previous_close()` success
- [ ] Test `get_ticker_details()` success
- [ ] Test `get_stock_aggregates()` success
- [ ] Test error handling (404, 429, network error)

### 9. Write Workflow Integration Tests
- [ ] Test `run_analysis()` with mocked API
- [ ] Verify state transitions
- [ ] Verify all fields populated
- [ ] Test error propagation

### 10. Write Golden Run Test
- [ ] Create expected output structure snapshot
- [ ] Test that `run_analysis()` returns correct structure
- [ ] Verify all expected keys present
- [ ] Verify types of values

### 11. Write Report Generation Tests
- [ ] Test `generate_report()` returns valid markdown
- [ ] Test all sections present
- [ ] Test with minimal state
- [ ] Test with complete state

### 12. Document Test Commands
- [ ] Document: `pytest` (run all tests)
- [ ] Document: `pytest tests/unit/` (unit only)
- [ ] Document: `pytest --cov=stockagent` (with coverage)
- [ ] Add test commands to CLAUDE.md

## Order of Steps

1. Create directory structure (task 1)
2. Add pytest dependencies (task 2)
3. Create configuration (task 3)
4. Create fixtures (task 4)
5. Write indicator tests (task 5)
6. Write scoring tests (task 6)
7. Write sentiment tests (task 7)
8. Write client tests (task 8)
9. Write workflow tests (task 9)
10. Write golden run test (task 10)
11. Write report tests (task 11)
12. Document commands (task 12)
