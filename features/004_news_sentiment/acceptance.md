# Feature 004: Acceptance Criteria

## Required Outcomes

### AC-1: Module Imports Successfully
- [ ] `from stockagent.analysis import analyze_news_sentiment` works
- [ ] `from stockagent.analysis.news_sentiment import fetch_news, analyze_sentiment` works

### AC-2: Headline Sentiment Analysis Works
- [ ] "Stock surges to record high" → positive score (> 0)
- [ ] "Company reports massive losses" → negative score (< 0)
- [ ] "Company announces quarterly results" → neutral score (≈ 0)
- [ ] Score always in range [-1.0, +1.0]
- [ ] Returns dict with `score`, `label`

### AC-3: News Fetching Works
- [ ] Returns list of headline dicts for valid ticker/company
- [ ] Each dict contains: `title`, `url`, `date`
- [ ] Returns empty list for obscure/invalid ticker (not crash)
- [ ] Respects max_results parameter

### AC-4: Aggregate Sentiment Works
- [ ] `analyze_news_sentiment("AAPL", "Apple Inc.")` returns SentimentResult
- [ ] Result contains `overall_score`, `overall_label`, `headlines`
- [ ] `headlines` is list of dicts with individual scores
- [ ] At most 5 headlines in result

### AC-5: Edge Cases Handled
- [ ] No news found → returns neutral (score ≈ 0.0)
- [ ] Empty company name → uses ticker only, no crash
- [ ] Network error → returns neutral, no crash

### AC-6: Sentiment Labels Correct
- [ ] Score > 0.2 → label "positive"
- [ ] Score < -0.2 → label "negative"
- [ ] Score between -0.2 and 0.2 → label "neutral"

## Observable Outcomes

1. Sentiment analysis is deterministic for same headline
2. Real news headlines produce reasonable sentiment scores
3. No crashes on edge cases or API issues
