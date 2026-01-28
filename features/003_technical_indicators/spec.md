# Feature 003: Technical Indicators

## Purpose

Implement deterministic technical indicator calculations using standard financial formulas. These indicators analyze price data to generate trading signals.

## Inputs / Outputs

### Inputs
- List of OHLCV bars (from Polygon client)
- Each bar contains: open, high, low, close, volume, timestamp

### Outputs
- `calculate_rsi(prices, period=14)` → RSI value (0-100)
- `calculate_macd(prices)` → MACD line, signal line, histogram
- `calculate_bollinger_bands(prices, period=20, std_dev=2)` → upper, middle, lower bands
- `calculate_sma(prices, period)` → Simple moving average value
- `calculate_all_indicators(bars)` → TechnicalSignals dict with all indicators

## Boundaries & Non-Goals

### In Scope
- RSI (Relative Strength Index) with 14-period default
- MACD with standard 12/26/9 parameters
- Bollinger Bands with 20-period, 2 standard deviations
- Simple Moving Averages: SMA-20, SMA-50, SMA-200
- Signal interpretation (overbought/oversold, bullish/bearish)
- Handle insufficient data gracefully (return None for indicators needing more data)

### Non-Goals
- No exponential moving averages (keep simple for v1)
- No custom indicator parameters from user
- No charting/visualization (that's UI feature)
- No recommendation logic (that's feature 006)

## Dependencies

- **Feature 002**: Uses OHLCV data from Polygon client

## PRD References

- Section 4: FR-2 Technical Indicator Calculation
- Section 5: NFR-6 Testability (pure functions)
- Section 10: Success Metrics (determinism)
