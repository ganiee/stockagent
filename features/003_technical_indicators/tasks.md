# Feature 003: Tasks

## Implementation Checklist

### 1. Create Indicators Module
- [ ] Create `src/stockagent/analysis/indicators.py`
- [ ] Import numpy and pandas for calculations

### 2. Implement RSI Calculation
- [ ] Create `calculate_rsi(prices: list[float], period: int = 14) -> float | None`
- [ ] Calculate price changes (deltas)
- [ ] Separate gains and losses
- [ ] Calculate average gain and average loss
- [ ] Apply RSI formula: `100 - (100 / (1 + RS))` where RS = avg_gain / avg_loss
- [ ] Return None if insufficient data (< period + 1 prices)

### 3. Implement MACD Calculation
- [ ] Create `calculate_macd(prices: list[float]) -> dict | None`
- [ ] Calculate 12-period EMA
- [ ] Calculate 26-period EMA
- [ ] MACD line = 12-EMA - 26-EMA
- [ ] Signal line = 9-period EMA of MACD line
- [ ] Histogram = MACD line - Signal line
- [ ] Return dict with `macd_line`, `signal_line`, `histogram`
- [ ] Return None if insufficient data (< 26 prices)

### 4. Implement Bollinger Bands
- [ ] Create `calculate_bollinger_bands(prices: list[float], period: int = 20, std_dev: int = 2) -> dict | None`
- [ ] Calculate SMA for middle band
- [ ] Calculate standard deviation
- [ ] Upper band = SMA + (std_dev * standard deviation)
- [ ] Lower band = SMA - (std_dev * standard deviation)
- [ ] Return dict with `upper`, `middle`, `lower`
- [ ] Return None if insufficient data (< period prices)

### 5. Implement Simple Moving Average
- [ ] Create `calculate_sma(prices: list[float], period: int) -> float | None`
- [ ] Calculate arithmetic mean of last `period` prices
- [ ] Return None if insufficient data

### 6. Implement Signal Interpretation
- [ ] Create `interpret_rsi(rsi: float) -> str`
  - RSI > 70 → "overbought"
  - RSI < 30 → "oversold"
  - else → "neutral"
- [ ] Create `interpret_macd(macd: dict) -> str`
  - histogram > 0 → "bullish"
  - histogram < 0 → "bearish"
  - else → "neutral"

### 7. Implement Aggregate Function
- [ ] Create `calculate_all_indicators(bars: list[dict]) -> TechnicalSignals`
- [ ] Extract close prices from bars
- [ ] Call all individual indicator functions
- [ ] Package results into TechnicalSignals dict
- [ ] Include interpretations for each indicator

### 8. Export from Package
- [ ] Update `src/stockagent/analysis/__init__.py` to export functions

## Order of Steps

1. Create module file (task 1)
2. Implement SMA first (task 5) — simplest, used by others
3. Implement RSI (task 2)
4. Implement Bollinger Bands (task 4) — uses SMA
5. Implement MACD (task 3) — most complex
6. Implement signal interpretation (task 6)
7. Implement aggregate function (task 7)
8. Export from package (task 8)
