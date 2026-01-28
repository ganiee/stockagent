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

## Automated Tests

All acceptance criteria are validated by automated tests in `tests/test_006_recommendation_engine.py`.

Run tests with:
```bash
pytest -m feature006 -v
```

Expected: 63 tests pass.

### Test Coverage

| AC | Test Class | Tests |
|----|-----------|-------|
| AC-1 | TestScoringImports | test_calculate_composite_score_import, test_generate_recommendation_import, test_get_explanation_factors_import, test_imports_from_analysis_package |
| AC-2 | TestRSIScoring | test_rsi_oversold_bullish, test_rsi_overbought_bearish, test_rsi_neutral, test_rsi_none_returns_zero |
| AC-3 | TestMACDScoring | test_macd_strong_bullish, test_macd_bearish, test_macd_none_returns_zero |
| AC-4 | TestCompositeScore | test_all_bullish_signals, test_all_bearish_signals, test_mixed_signals_near_zero, test_deterministic, test_score_clamped_* |
| AC-5 | TestGenerateRecommendation | test_strong_buy_threshold, test_buy_threshold, test_hold_threshold, test_sell_threshold, test_strong_sell_threshold, test_boundary_values |
| AC-6 | TestGenerateRecommendation | test_confidence_is_abs_score, test_confidence_capped_at_100 |
| AC-7 | TestExplanationFactors | test_returns_list_of_strings, test_includes_rsi_factor, test_includes_macd_factor, test_includes_sentiment_factor, test_sorted_by_contribution |
| AC-8 | TestWorkflowIntegration | test_recommend_returns_real_recommendation, test_recommend_not_placeholder, test_run_analysis_returns_real_recommendation |
