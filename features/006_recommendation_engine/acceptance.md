# Feature 006: Acceptance Criteria

## Required Outcomes

### AC-1: Module Imports Successfully
- [ ] `from stockagent.analysis.scoring import calculate_composite_score, generate_recommendation` works
- [ ] `from stockagent.analysis.scoring import get_explanation_factors` works

### AC-2: RSI Scoring Works
- [ ] RSI 25 → positive score (oversold = bullish)
- [ ] RSI 75 → negative score (overbought = bearish)
- [ ] RSI 50 → zero score (neutral)
- [ ] RSI None → zero score

### AC-3: MACD Scoring Works
- [ ] Positive histogram → positive score
- [ ] Negative histogram → negative score
- [ ] None → zero score

### AC-4: Composite Score Works
- [ ] Score is in range [-100, +100]
- [ ] All bullish signals → score > 50
- [ ] All bearish signals → score < -50
- [ ] Mixed signals → score near 0
- [ ] Deterministic (same inputs → same output)

### AC-5: Recommendation Thresholds Correct
- [ ] Score > 60 → "STRONG BUY"
- [ ] Score 20-60 → "BUY"
- [ ] Score -20 to 20 → "HOLD"
- [ ] Score -60 to -20 → "SELL"
- [ ] Score < -60 → "STRONG SELL"

### AC-6: Confidence Calculation Works
- [ ] Confidence = abs(score) (as percentage)
- [ ] Score 80 → confidence 80%
- [ ] Score -60 → confidence 60%
- [ ] Confidence always 0-100%

### AC-7: Explanation Factors Generated
- [ ] Returns list of strings
- [ ] Each string describes a contributing factor
- [ ] Factors include direction (bullish/bearish)
- [ ] Non-empty for non-neutral inputs

### AC-8: Workflow Integration Works
- [ ] `run_analysis()` returns real recommendation (not placeholder)
- [ ] Recommendation matches score thresholds
- [ ] Confidence is populated

## Observable Outcomes

1. Same technical + sentiment inputs always produce same recommendation
2. Extreme bullish signals → STRONG BUY
3. Extreme bearish signals → STRONG SELL
4. Explanations help user understand the recommendation
