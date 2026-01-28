# Feature 007: Verification

## Prerequisites
- Features 001-006 completed
- Valid `.env` file with `POLYGON_API_KEY`

## Local Commands to Run

### 1. Verify Module Imports
```bash
python -c "
from stockagent.analysis import generate_report
from stockagent.analysis.synthesis import generate_report
print('Imports successful')
"
```

### 2. Verify Report Generation with Mock Data
```bash
python -c "
from stockagent.analysis.synthesis import generate_report

# Create mock state
mock_state = {
    'ticker': 'TEST',
    'company_name': 'Test Company Inc.',
    'current_price': 150.25,
    'previous_close': 148.50,
    'technical_signals': {
        'rsi': 45.5,
        'rsi_interpretation': 'neutral',
        'macd': {'macd_line': 1.2, 'signal_line': 0.8, 'histogram': 0.4},
        'macd_interpretation': 'bullish',
        'bollinger': {'upper': 155.0, 'middle': 150.0, 'lower': 145.0},
        'sma_20': 149.0,
        'sma_50': 147.0,
        'sma_200': 140.0,
    },
    'news_sentiment': {
        'overall_score': 0.3,
        'overall_label': 'positive',
        'headlines': [
            {'title': 'Test headline 1', 'sentiment': 'positive'},
            {'title': 'Test headline 2', 'sentiment': 'neutral'},
        ]
    },
    'recommendation': 'BUY',
    'confidence': 65.0,
    'explanation_factors': ['RSI neutral', 'MACD bullish crossover', 'Positive news sentiment'],
    'errors': []
}

report = generate_report(mock_state)
print('Generated report:')
print('=' * 50)
print(report[:500])
print('...')
print('=' * 50)

# Verify sections present
assert 'TEST' in report, 'Ticker should be in report'
assert 'Technical' in report or 'technical' in report, 'Technical section should exist'
assert 'BUY' in report, 'Recommendation should be in report'
assert 'disclaimer' in report.lower() or 'educational' in report.lower(), 'Disclaimer should exist'
print('Report generation: PASSED')
"
```

### 3. Verify Report Contains Required Sections
```bash
python -c "
from stockagent.analysis.synthesis import generate_report

mock_state = {
    'ticker': 'AAPL',
    'company_name': 'Apple Inc.',
    'current_price': 175.0,
    'previous_close': 173.0,
    'technical_signals': {'rsi': 55},
    'news_sentiment': {'overall_score': 0.2, 'overall_label': 'positive', 'headlines': []},
    'recommendation': 'HOLD',
    'confidence': 45.0,
    'explanation_factors': ['Mixed signals'],
    'errors': []
}

report = generate_report(mock_state)

# Check for section headers
sections = ['Price', 'Technical', 'Sentiment', 'News', 'Recommendation', 'Disclaimer']
found = [s for s in sections if s.lower() in report.lower()]
print(f'Sections found: {found}')
assert len(found) >= 4, f'Expected at least 4 sections, found {len(found)}'
print('Section verification: PASSED')
"
```

### 4. Verify Workflow Integration
```bash
python -c "
from stockagent.graph import run_analysis

result = run_analysis('GOOGL')
synthesis = result.get('synthesis', '')

print(f'Synthesis length: {len(synthesis)} characters')
print(f'First 200 chars: {synthesis[:200]}...')

assert len(synthesis) > 100, 'Synthesis should be substantial'
assert 'GOOGL' in synthesis or 'Alphabet' in synthesis, 'Should contain ticker or company'
print('Workflow integration: PASSED')
"
```

### 5. Verify Markdown Validity
```bash
python -c "
from stockagent.analysis.synthesis import generate_report

mock_state = {
    'ticker': 'TEST',
    'company_name': 'Test Co',
    'current_price': 100.0,
    'previous_close': 99.0,
    'technical_signals': {},
    'news_sentiment': {'overall_score': 0, 'overall_label': 'neutral', 'headlines': []},
    'recommendation': 'HOLD',
    'confidence': 50.0,
    'explanation_factors': [],
    'errors': []
}

report = generate_report(mock_state)

# Basic markdown checks
assert report.count('#') >= 3, 'Should have markdown headings'
# No unclosed formatting
assert report.count('**') % 2 == 0, 'Bold markers should be paired'
assert report.count('*') % 2 == 0 or '**' in report, 'Italic markers should be paired'
print('Markdown validity: PASSED')
"
```

## Quick Verification (All-in-One)
```bash
python -c "
from stockagent.graph import run_analysis

result = run_analysis('TSLA')
synthesis = result.get('synthesis', '')
assert len(synthesis) > 100
assert result.get('recommendation') in synthesis or 'HOLD' in synthesis or 'BUY' in synthesis or 'SELL' in synthesis
print('Feature 007 verification: PASSED')
"
```
