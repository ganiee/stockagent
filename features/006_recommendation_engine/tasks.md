# Feature 006: Tasks

## Implementation Checklist

### 1. Create Scoring Module
- [ ] Create `src/stockagent/analysis/scoring.py`
- [ ] Define scoring weights as constants

### 2. Define Scoring Weights
- [ ] RSI weight: 20 points max
- [ ] MACD weight: 25 points max
- [ ] Moving average alignment: 20 points max
- [ ] Bollinger position: 15 points max
- [ ] News sentiment: 20 points max
- [ ] Total possible: ±100 points

### 3. Implement RSI Scoring
- [ ] Create `score_rsi(rsi: float | None) -> float`
- [ ] RSI < 30 (oversold) → +20 (bullish)
- [ ] RSI 30-40 → +10
- [ ] RSI 40-60 → 0 (neutral)
- [ ] RSI 60-70 → -10
- [ ] RSI > 70 (overbought) → -20 (bearish)
- [ ] None → 0

### 4. Implement MACD Scoring
- [ ] Create `score_macd(macd: dict | None) -> float`
- [ ] Positive histogram + positive MACD line → +25
- [ ] Positive histogram → +15
- [ ] Negative histogram → -15
- [ ] Negative histogram + negative MACD line → -25
- [ ] None → 0

### 5. Implement Moving Average Scoring
- [ ] Create `score_moving_averages(signals: dict) -> float`
- [ ] Price > SMA-20 > SMA-50 > SMA-200 → +20 (strong uptrend)
- [ ] Price > SMA-20, SMA-50 → +10
- [ ] Price < SMA-20 < SMA-50 < SMA-200 → -20 (strong downtrend)
- [ ] Price < SMA-20, SMA-50 → -10
- [ ] Mixed signals → 0

### 6. Implement Bollinger Scoring
- [ ] Create `score_bollinger(bollinger: dict | None, current_price: float) -> float`
- [ ] Price near lower band → +15 (potential bounce)
- [ ] Price near upper band → -15 (potential pullback)
- [ ] Price in middle → 0
- [ ] None → 0

### 7. Implement Sentiment Scoring
- [ ] Create `score_sentiment(sentiment: dict | None) -> float`
- [ ] Map sentiment score (-1 to +1) to (-20 to +20)
- [ ] Simple linear scaling: score * 20
- [ ] None → 0

### 8. Implement Composite Score
- [ ] Create `calculate_composite_score(technical_signals: dict, sentiment: dict) -> float`
- [ ] Sum all individual scores
- [ ] Clamp to range -100 to +100
- [ ] Return final score

### 9. Implement Recommendation Mapping
- [ ] Create `generate_recommendation(score: float) -> tuple[str, float]`
- [ ] Map score to recommendation string
- [ ] Calculate confidence: abs(score) / 100 * 100%
- [ ] Return (recommendation, confidence)

### 10. Implement Explanation Factors
- [ ] Create `get_explanation_factors(technical_signals: dict, sentiment: dict) -> list[str]`
- [ ] Generate human-readable strings for each contributing signal
- [ ] Include direction (bullish/bearish) for each factor
- [ ] Sort by absolute contribution

### 11. Update Workflow
- [ ] Update `src/stockagent/graph/workflow.py` recommend node
- [ ] Replace placeholder with actual scoring logic
- [ ] Populate recommendation, confidence, and factors in state

### 12. Export from Package
- [ ] Update `src/stockagent/analysis/__init__.py` to export scoring functions

## Order of Steps

1. Create module file (task 1)
2. Define weights (task 2)
3. Implement individual scoring functions (tasks 3-7)
4. Implement composite score (task 8)
5. Implement recommendation mapping (task 9)
6. Implement explanation factors (task 10)
7. Update workflow (task 11)
8. Export from package (task 12)
