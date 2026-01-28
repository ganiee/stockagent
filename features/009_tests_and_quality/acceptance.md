# Feature 009: Acceptance Criteria

## Required Outcomes

### AC-1: Test Directory Structure Exists
- [x] `tests/` directory exists
- [x] `tests/conftest.py` exists with fixtures
- [x] `tests/unit/` directory exists
- [x] `tests/integration/` directory exists

### AC-2: pytest Runs Successfully
- [x] `pytest` command runs without configuration errors
- [x] `python -m pytest` also works
- [x] Test discovery finds all tests

### AC-3: Indicator Tests Pass
- [x] `tests/unit/test_indicators.py` exists
- [x] All indicator calculation tests pass
- [x] Edge cases (None, insufficient data) tested
- [x] At least 5 test functions for indicators (22 tests)

### AC-4: Scoring Tests Pass
- [x] `tests/unit/test_scoring.py` exists
- [x] All scoring function tests pass
- [x] Recommendation thresholds verified
- [x] At least 5 test functions for scoring (22 tests)

### AC-5: Sentiment Tests Pass
- [x] `tests/unit/test_sentiment.py` exists
- [x] Keyword sentiment tests pass
- [x] Score bounds verified
- [x] At least 3 test functions for sentiment (12 tests)

### AC-6: Client Tests Pass (Mocked)
- [x] `tests/integration/test_polygon_client.py` exists
- [x] API calls mocked (no real network)
- [x] Success and error cases tested
- [x] At least 4 test functions for client (11 tests)

### AC-7: Workflow Tests Pass
- [x] `tests/integration/test_workflow.py` exists
- [x] Full workflow execution tested
- [x] State structure validated
- [x] At least 2 test functions for workflow (10 tests)

### AC-8: Coverage Meets Target
- [x] Coverage for `analysis/indicators.py` > 80%
- [x] Coverage for `analysis/scoring.py` > 80%
- [x] Coverage for `analysis/news_sentiment.py` > 80%
- [x] Overall coverage report generated

### AC-9: Golden Run Test Passes
- [x] Test verifies output structure matches expected
- [x] All required keys present in result
- [x] Types match expected types

### AC-10: No Test Failures
- [x] `pytest` exits with code 0
- [x] All tests pass (no failures, no errors)
- [x] No warnings that indicate problems

## Observable Outcomes

1. `pytest` runs and shows all tests passing
2. `pytest --cov=stockagent` shows coverage > 80% for core modules
3. Adding new code that breaks tests causes test failures
4. Test output is readable and helpful
