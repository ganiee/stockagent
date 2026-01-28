# Feature 006: Recommendation Engine

## Purpose

Implement the scoring system that combines technical signals and news sentiment to produce a final Buy/Sell/Hold recommendation with confidence level and explanation factors.

## Inputs / Outputs

### Inputs
- TechnicalSignals dict (from feature 003)
- SentimentResult dict (from feature 004)

### Outputs
- `calculate_composite_score(technical_signals, sentiment) -> float` — Combined score (-100 to +100)
- `generate_recommendation(score) -> tuple[str, float]` — (recommendation, confidence)
- `get_explanation_factors(technical_signals, sentiment) -> list[str]` — List of contributing factors

## Boundaries & Non-Goals

### In Scope
- Weighted scoring system combining:
  - RSI signal (overbought/oversold)
  - MACD signal (bullish/bearish)
  - Moving average crossovers
  - Bollinger Band position
  - News sentiment score
- Recommendation thresholds:
  - STRONG BUY: score > 60
  - BUY: score > 20
  - HOLD: score between -20 and 20
  - SELL: score < -20
  - STRONG SELL: score < -60
- Confidence calculation based on signal agreement
- Explanation factors (human-readable reasons)

### Non-Goals
- No machine learning or trained models
- No historical accuracy tracking
- No user-configurable weights
- No multiple recommendation timeframes

## Dependencies

- **Feature 003**: Uses TechnicalSignals output format
- **Feature 004**: Uses SentimentResult output format
- **Feature 005**: Will be integrated into workflow's recommend node

## PRD References

- Section 4: FR-5 Recommendation Engine
- Section 5: NFR-6 Testability (deterministic scoring)
