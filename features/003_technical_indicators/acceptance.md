# Feature 003: Acceptance Criteria

## Required Outcomes

### AC-1: Module Imports Successfully
- [ ] `from stockagent.analysis import calculate_all_indicators` works
- [ ] `from stockagent.analysis.indicators import calculate_rsi, calculate_macd, calculate_bollinger_bands, calculate_sma` works

### AC-2: RSI Calculation is Correct
- [ ] Known input produces expected output (deterministic)
- [ ] Test case: 14 specific prices → expected RSI value (±0.01)
- [ ] Returns value between 0 and 100
- [ ] Returns None when given < 15 prices

### AC-3: MACD Calculation is Correct
- [ ] Returns dict with `macd_line`, `signal_line`, `histogram`
- [ ] All values are floats
- [ ] Returns None when given < 26 prices
- [ ] Histogram = macd_line - signal_line (verifiable)

### AC-4: Bollinger Bands Calculation is Correct
- [ ] Returns dict with `upper`, `middle`, `lower`
- [ ] middle = SMA(20) of prices
- [ ] upper > middle > lower (always)
- [ ] Returns None when given < 20 prices

### AC-5: SMA Calculation is Correct
- [ ] SMA-20 of [1,2,3,...,20] = 10.5
- [ ] SMA-50 returns None when given < 50 prices
- [ ] SMA-200 returns None when given < 200 prices

### AC-6: Signal Interpretation Works
- [ ] RSI 75 → "overbought"
- [ ] RSI 25 → "oversold"
- [ ] RSI 50 → "neutral"
- [ ] MACD with positive histogram → "bullish"
- [ ] MACD with negative histogram → "bearish"

### AC-7: Aggregate Function Works
- [ ] `calculate_all_indicators(bars)` returns TechnicalSignals dict
- [ ] Dict contains: `rsi`, `macd`, `bollinger`, `sma_20`, `sma_50`, `sma_200`
- [ ] Dict contains interpretations for each indicator

## Observable Outcomes

1. All indicator functions are pure (same input → same output)
2. Functions handle edge cases without crashing
3. Results match standard technical analysis formulas

## Automated Tests

Run feature 003 tests:
```bash
pytest -m feature003 -v
```

Or using the feature test script:
```bash
python scripts/run_feature_tests.py 003
```

All 39 tests in `tests/test_003_technical_indicators.py` must pass.
