# Feature 004: Verification

## Prerequisites
- Feature 001 completed
- Internet connection (for DuckDuckGo search)

## Local Commands to Run

### 1. Verify Module Imports
```bash
python -c "
from stockagent.analysis import analyze_news_sentiment
from stockagent.analysis.news_sentiment import fetch_news, analyze_sentiment
print('Imports successful')
"
```

### 2. Verify Headline Sentiment (No Network)
```bash
python -c "
from stockagent.analysis.news_sentiment import analyze_sentiment

# Test positive headline
pos = analyze_sentiment('Stock surges to record high after strong earnings')
print(f'Positive headline score: {pos[\"score\"]}, label: {pos[\"label\"]}')
assert pos['score'] > 0, 'Expected positive score'
assert pos['label'] == 'positive', 'Expected positive label'

# Test negative headline
neg = analyze_sentiment('Company reports massive losses and layoffs')
print(f'Negative headline score: {neg[\"score\"]}, label: {neg[\"label\"]}')
assert neg['score'] < 0, 'Expected negative score'
assert neg['label'] == 'negative', 'Expected negative label'

# Test neutral headline
neu = analyze_sentiment('Company announces quarterly results')
print(f'Neutral headline score: {neu[\"score\"]}, label: {neu[\"label\"]}')
assert -0.3 <= neu['score'] <= 0.3, 'Expected near-neutral score'

# Test score bounds
assert -1.0 <= pos['score'] <= 1.0
assert -1.0 <= neg['score'] <= 1.0
print('Headline sentiment: PASSED')
"
```

### 3. Verify News Fetching (Requires Network)
```bash
python -c "
from stockagent.analysis.news_sentiment import fetch_news

headlines = fetch_news('AAPL', 'Apple Inc.', max_results=5)
print(f'Fetched {len(headlines)} headlines')
if headlines:
    print(f'First headline: {headlines[0][\"title\"][:50]}...')
    assert 'title' in headlines[0]
    assert 'url' in headlines[0]
print('News fetching: PASSED')
"
```

### 4. Verify Aggregate Sentiment
```bash
python -c "
from stockagent.analysis import analyze_news_sentiment

result = analyze_news_sentiment('MSFT', 'Microsoft Corporation')
print(f'Overall score: {result[\"overall_score\"]}')
print(f'Overall label: {result[\"overall_label\"]}')
print(f'Headlines analyzed: {len(result[\"headlines\"])}')

assert 'overall_score' in result
assert 'overall_label' in result
assert 'headlines' in result
assert -1.0 <= result['overall_score'] <= 1.0
assert len(result['headlines']) <= 5
print('Aggregate sentiment: PASSED')
"
```

### 5. Verify Edge Case - No News
```bash
python -c "
from stockagent.analysis import analyze_news_sentiment

# Use obscure ticker that likely has no news
result = analyze_news_sentiment('XYZABC123', 'Nonexistent Company Inc')
print(f'No news result: score={result[\"overall_score\"]}, label={result[\"overall_label\"]}')
# Should return neutral, not crash
assert result['overall_label'] == 'neutral'
print('No news handling: PASSED')
"
```

## Quick Verification (All-in-One)
```bash
python -c "
from stockagent.analysis import analyze_news_sentiment
from stockagent.analysis.news_sentiment import analyze_sentiment

# Test sentiment analysis
assert analyze_sentiment('great profit growth')['score'] > 0
assert analyze_sentiment('massive decline')['score'] < 0

# Test aggregate (with network)
result = analyze_news_sentiment('GOOGL', 'Alphabet Inc.')
assert 'overall_score' in result
print('Feature 004 verification: PASSED')
"
```

## Run Automated Tests (Recommended)
```bash
# Run all feature 004 tests (mocked, no network required)
pytest -m feature004 -v

# Or use the feature test script
python scripts/run_feature_tests.py 004

# Run with coverage
pytest -m feature004 --cov=src/stockagent --cov-report=term-missing
```

Expected: All 31 tests pass.
