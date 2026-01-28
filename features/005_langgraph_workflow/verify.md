# Feature 005: Verification

## Prerequisites
- Features 001-004 completed
- Valid `.env` file with `POLYGON_API_KEY`
- Internet connection

## Local Commands to Run

### 1. Verify Module Imports
```bash
python -c "
from stockagent.graph import create_workflow, run_analysis
print('Imports successful')
"
```

### 2. Verify Workflow Creation
```bash
python -c "
from stockagent.graph import create_workflow

graph = create_workflow()
print(f'Graph type: {type(graph)}')
print('Workflow creation: PASSED')
"
```

### 3. Verify Full Analysis Run
```bash
python -c "
from stockagent.graph import run_analysis

print('Running analysis for AAPL...')
result = run_analysis('AAPL')

print(f'Ticker: {result.get(\"ticker\")}')
print(f'Company: {result.get(\"company_name\")}')
print(f'Current Price: {result.get(\"current_price\")}')
print(f'Price Data Points: {len(result.get(\"price_data\", []))}')
print(f'Technical Signals: {list(result.get(\"technical_signals\", {}).keys())}')
print(f'News Sentiment Score: {result.get(\"news_sentiment\", {}).get(\"overall_score\")}')
print(f'Recommendation: {result.get(\"recommendation\")}')
print(f'Confidence: {result.get(\"confidence\")}')
print(f'Errors: {result.get(\"errors\", [])}')

# Verify key fields populated
assert result.get('ticker') == 'AAPL'
assert result.get('company_name') is not None
assert result.get('current_price', 0) > 0
assert len(result.get('price_data', [])) > 0
assert result.get('technical_signals') is not None
assert result.get('news_sentiment') is not None
print('Full analysis run: PASSED')
"
```

### 4. Verify Error Handling
```bash
python -c "
from stockagent.graph import run_analysis

print('Running analysis for invalid ticker...')
result = run_analysis('INVALIDXYZ123')

print(f'Errors: {result.get(\"errors\", [])}')
# Should have errors but not crash
assert len(result.get('errors', [])) > 0 or result.get('price_data') == []
print('Error handling: PASSED')
"
```

### 5. Verify Individual Nodes
```bash
python -c "
from stockagent.graph.workflow import fetch_data, technical_analysis, news_sentiment

# Test fetch_data node
state = {'ticker': 'MSFT', 'errors': []}
result = fetch_data(state)
print(f'fetch_data result keys: {list(result.keys())}')
assert 'price_data' in result or 'errors' in result

# Test technical_analysis node (needs price_data)
if 'price_data' in result and result['price_data']:
    state.update(result)
    ta_result = technical_analysis(state)
    print(f'technical_analysis result keys: {list(ta_result.keys())}')
    assert 'technical_signals' in ta_result

print('Individual nodes: PASSED')
"
```

## Quick Verification (All-in-One)
```bash
python -c "
from stockagent.graph import run_analysis

result = run_analysis('GOOGL')
assert result.get('ticker') == 'GOOGL'
assert result.get('current_price', 0) > 0
assert result.get('technical_signals') is not None
print('Feature 005 verification: PASSED')
"
```

## Run Automated Tests (Recommended)
```bash
# Run all feature 005 tests (mocked, no network required)
pytest -m feature005 -v

# Or use the feature test script
python scripts/run_feature_tests.py 005

# Run with coverage
pytest -m feature005 --cov=src/stockagent --cov-report=term-missing
```

Expected: All 20 tests pass.
