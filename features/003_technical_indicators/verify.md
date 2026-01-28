# Feature 003: Verification

## Prerequisites
- Feature 001 and 002 completed

## Local Commands to Run

### 1. Verify Module Imports
```bash
python -c "
from stockagent.analysis import calculate_all_indicators
from stockagent.analysis.indicators import calculate_rsi, calculate_macd, calculate_bollinger_bands, calculate_sma
print('Imports successful')
"
```

### 2. Verify SMA Calculation
```bash
python -c "
from stockagent.analysis.indicators import calculate_sma

# Test with known values
prices = list(range(1, 21))  # [1, 2, ..., 20]
sma = calculate_sma(prices, 20)
expected = 10.5
assert abs(sma - expected) < 0.001, f'Expected {expected}, got {sma}'
print(f'SMA-20 of 1-20: {sma} (expected {expected})')
print('SMA calculation: PASSED')
"
```

### 3. Verify RSI Calculation
```bash
python -c "
from stockagent.analysis.indicators import calculate_rsi

# Test with sufficient data
prices = [44, 44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84, 46.08, 45.89, 46.03, 45.61, 46.28]
rsi = calculate_rsi(prices, 14)
print(f'RSI: {rsi}')
assert rsi is not None
assert 0 <= rsi <= 100
print('RSI calculation: PASSED')

# Test insufficient data
rsi_none = calculate_rsi([1,2,3], 14)
assert rsi_none is None
print('RSI insufficient data handling: PASSED')
"
```

### 4. Verify MACD Calculation
```bash
python -c "
from stockagent.analysis.indicators import calculate_macd
import random

# Generate enough data for MACD
random.seed(42)
prices = [100 + random.uniform(-5, 5) for _ in range(30)]
macd = calculate_macd(prices)
print(f'MACD: {macd}')
assert macd is not None
assert 'macd_line' in macd
assert 'signal_line' in macd
assert 'histogram' in macd
# Verify histogram calculation
assert abs(macd['histogram'] - (macd['macd_line'] - macd['signal_line'])) < 0.001
print('MACD calculation: PASSED')
"
```

### 5. Verify Bollinger Bands
```bash
python -c "
from stockagent.analysis.indicators import calculate_bollinger_bands

prices = [100 + i*0.5 for i in range(25)]  # Rising prices
bb = calculate_bollinger_bands(prices, 20, 2)
print(f'Bollinger Bands: {bb}')
assert bb is not None
assert bb['upper'] > bb['middle'] > bb['lower']
print('Bollinger Bands calculation: PASSED')
"
```

### 6. Verify Signal Interpretation
```bash
python -c "
from stockagent.analysis.indicators import interpret_rsi, interpret_macd

assert interpret_rsi(75) == 'overbought'
assert interpret_rsi(25) == 'oversold'
assert interpret_rsi(50) == 'neutral'
print('RSI interpretation: PASSED')

assert interpret_macd({'histogram': 1.0}) == 'bullish'
assert interpret_macd({'histogram': -1.0}) == 'bearish'
print('MACD interpretation: PASSED')
"
```

### 7. Verify Aggregate Function
```bash
python -c "
from stockagent.analysis import calculate_all_indicators
import random

# Create mock OHLCV bars
random.seed(42)
bars = [{'close': 100 + random.uniform(-10, 10)} for _ in range(100)]
signals = calculate_all_indicators(bars)
print(f'Signals keys: {list(signals.keys())}')
assert 'rsi' in signals
assert 'macd' in signals
assert 'bollinger' in signals
print('Aggregate function: PASSED')
"
```

## Quick Verification (All-in-One)
```bash
python -c "
from stockagent.analysis import calculate_all_indicators
from stockagent.analysis.indicators import calculate_rsi, calculate_sma

# Basic sanity checks
assert calculate_sma(list(range(1, 21)), 20) == 10.5
assert calculate_rsi([1]*5, 14) is None  # insufficient data
print('Feature 003 verification: PASSED')
"
```
