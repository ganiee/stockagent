# Feature 009: Acceptance Criteria

## Required Outcomes

### AC-1: Test Directory Structure Exists
- [ ] `tests/` directory exists
- [ ] `tests/conftest.py` exists with fixtures
- [ ] `tests/unit/` directory exists
- [ ] `tests/integration/` directory exists

### AC-2: pytest Runs Successfully
- [ ] `pytest` command runs without configuration errors
- [ ] `python -m pytest` also works
- [ ] Test discovery finds all tests

### AC-3: Indicator Tests Pass
- [ ] `tests/unit/test_indicators.py` exists
- [ ] All indicator calculation tests pass
- [ ] Edge cases (None, insufficient data) tested
- [ ] At least 5 test functions for indicators

### AC-4: Scoring Tests Pass
- [ ] `tests/unit/test_scoring.py` exists
- [ ] All scoring function tests pass
- [ ] Recommendation thresholds verified
- [ ] At least 5 test functions for scoring

### AC-5: Sentiment Tests Pass
- [ ] `tests/unit/test_sentiment.py` exists
- [ ] Keyword sentiment tests pass
- [ ] Score bounds verified
- [ ] At least 3 test functions for sentiment

### AC-6: Client Tests Pass (Mocked)
- [ ] `tests/integration/test_polygon_client.py` exists
- [ ] API calls mocked (no real network)
- [ ] Success and error cases tested
- [ ] At least 4 test functions for client

### AC-7: Workflow Tests Pass
- [ ] `tests/integration/test_workflow.py` exists
- [ ] Full workflow execution tested
- [ ] State structure validated
- [ ] At least 2 test functions for workflow

### AC-8: Coverage Meets Target
- [ ] Coverage for `analysis/indicators.py` > 80%
- [ ] Coverage for `analysis/scoring.py` > 80%
- [ ] Coverage for `analysis/news_sentiment.py` > 80%
- [ ] Overall coverage report generated

### AC-9: Golden Run Test Passes
- [ ] Test verifies output structure matches expected
- [ ] All required keys present in result
- [ ] Types match expected types

### AC-10: No Test Failures
- [ ] `pytest` exits with code 0
- [ ] All tests pass (no failures, no errors)
- [ ] No warnings that indicate problems

## Observable Outcomes

1. `pytest` runs and shows all tests passing
2. `pytest --cov=stockagent` shows coverage > 80% for core modules
3. Adding new code that breaks tests causes test failures
4. Test output is readable and helpful
