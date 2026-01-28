# Feature 006: Verification

## Prerequisites
- Features 001-005 completed
- Valid `.env` file with `POLYGON_API_KEY`

## Local Commands to Run

### 1. Verify Module Imports
```bash
python -c "
from stockagent.analysis.scoring import calculate_composite_score, generate_recommendation, get_explanation_factors
print('Imports successful')
"
```

### 2. Verify RSI Scoring
```bash
python -c "
from stockagent.analysis.scoring import score_rsi

# Oversold (bullish)
assert score_rsi(25) > 0, 'RSI 25 should be positive'
# Overbought (bearish)
assert score_rsi(75) < 0, 'RSI 75 should be negative'
# Neutral
assert score_rsi(50) == 0, 'RSI 50 should be zero'
# None
assert score_rsi(None) == 0, 'RSI None should be zero'
print('RSI scoring: PASSED')
"
```

### 3. Verify MACD Scoring
```bash
python -c "
from stockagent.analysis.scoring import score_macd

bullish = {'macd_line': 1.0, 'signal_line': 0.5, 'histogram': 0.5}
bearish = {'macd_line': -1.0, 'signal_line': -0.5, 'histogram': -0.5}

assert score_macd(bullish) > 0, 'Bullish MACD should be positive'
assert score_macd(bearish) < 0, 'Bearish MACD should be negative'
assert score_macd(None) == 0, 'None MACD should be zero'
print('MACD scoring: PASSED')
"
```

### 4. Verify Composite Score
```bash
python -c "
from stockagent.analysis.scoring import calculate_composite_score

# Create bullish signals
bullish_tech = {
    'rsi': 25,  # oversold
    'macd': {'histogram': 1.0, 'macd_line': 1.0},
    'sma_20': 100, 'sma_50': 95, 'sma_200': 90,
    'bollinger': {'lower': 95, 'middle': 100, 'upper': 105},
    'current_price': 102
}
bullish_sentiment = {'overall_score': 0.8}

score = calculate_composite_score(bullish_tech, bullish_sentiment)
print(f'Bullish composite score: {score}')
assert score > 30, f'Bullish signals should produce positive score, got {score}'
assert -100 <= score <= 100, 'Score should be in range'
print('Composite score: PASSED')
"
```

### 5. Verify Recommendation Thresholds
```bash
python -c "
from stockagent.analysis.scoring import generate_recommendation

tests = [
    (80, 'STRONG BUY'),
    (40, 'BUY'),
    (0, 'HOLD'),
    (-40, 'SELL'),
    (-80, 'STRONG SELL'),
]

for score, expected in tests:
    rec, conf = generate_recommendation(score)
    assert rec == expected, f'Score {score} should be {expected}, got {rec}'
    print(f'Score {score}: {rec} ({conf:.0f}%)')

print('Recommendation thresholds: PASSED')
"
```

### 6. Verify Explanation Factors
```bash
python -c "
from stockagent.analysis.scoring import get_explanation_factors

tech = {'rsi': 25, 'macd': {'histogram': 1.0}}
sentiment = {'overall_score': 0.5}

factors = get_explanation_factors(tech, sentiment)
print(f'Explanation factors: {factors}')
assert len(factors) > 0, 'Should have explanation factors'
assert all(isinstance(f, str) for f in factors), 'Factors should be strings'
print('Explanation factors: PASSED')
"
```

### 7. Verify Workflow Integration
```bash
python -c "
from stockagent.graph import run_analysis

result = run_analysis('AAPL')
rec = result.get('recommendation')
conf = result.get('confidence')

print(f'Recommendation: {rec}')
print(f'Confidence: {conf}')

assert rec in ['STRONG BUY', 'BUY', 'HOLD', 'SELL', 'STRONG SELL'], f'Invalid recommendation: {rec}'
assert 0 <= conf <= 100, f'Invalid confidence: {conf}'
print('Workflow integration: PASSED')
"
```

## Quick Verification (All-in-One)
```bash
python -c "
from stockagent.analysis.scoring import calculate_composite_score, generate_recommendation
from stockagent.graph import run_analysis

# Test scoring
score = calculate_composite_score({'rsi': 50}, {'overall_score': 0})
assert -100 <= score <= 100

# Test recommendation
rec, conf = generate_recommendation(0)
assert rec == 'HOLD'

# Test workflow
result = run_analysis('MSFT')
assert result.get('recommendation') is not None
print('Feature 006 verification: PASSED')
"
```
