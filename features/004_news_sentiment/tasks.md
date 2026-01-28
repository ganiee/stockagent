# Feature 004: Tasks

## Implementation Checklist

### 1. Create News Sentiment Module
- [ ] Create `src/stockagent/analysis/news_sentiment.py`
- [ ] Import duckduckgo_search library

### 2. Define Sentiment Keywords
- [ ] Create POSITIVE_KEYWORDS list (e.g., "surge", "growth", "profit", "bullish", "upgrade", "beat", "record", "strong")
- [ ] Create NEGATIVE_KEYWORDS list (e.g., "crash", "loss", "decline", "bearish", "downgrade", "miss", "weak", "layoff")
- [ ] Ensure keywords are lowercase for matching

### 3. Implement News Fetching
- [ ] Create `fetch_news(ticker: str, company_name: str, max_results: int = 8) -> list[dict]`
- [ ] Use DDGS.news() to search for "{company_name} stock" or "{ticker} stock"
- [ ] Extract: title, url, date, source
- [ ] Return top N results sorted by date
- [ ] Handle no results (return empty list)
- [ ] Handle rate limiting / errors gracefully

### 4. Implement Headline Sentiment Analysis
- [ ] Create `analyze_sentiment(headline: str) -> dict`
- [ ] Convert headline to lowercase
- [ ] Count positive keyword matches
- [ ] Count negative keyword matches
- [ ] Calculate score: (positive - negative) / (positive + negative + 1)
- [ ] Clamp to range -1.0 to +1.0
- [ ] Assign label: "positive" (>0.2), "negative" (<-0.2), "neutral" (else)
- [ ] Return dict with `score`, `label`, `positive_count`, `negative_count`

### 5. Implement Aggregate Sentiment
- [ ] Create `analyze_news_sentiment(ticker: str, company_name: str) -> SentimentResult`
- [ ] Fetch news headlines
- [ ] Analyze each headline
- [ ] Calculate aggregate score (average of headline scores)
- [ ] Keep top 5 headlines with highest absolute sentiment
- [ ] Return SentimentResult dict with:
  - `overall_score`: aggregate (-1.0 to +1.0)
  - `overall_label`: positive/negative/neutral
  - `headlines`: list of headlines with individual scores
  - `headline_count`: number analyzed

### 6. Handle Edge Cases
- [ ] No news found → return neutral sentiment (0.0)
- [ ] API error → log warning, return neutral sentiment
- [ ] Empty company_name → use ticker only

### 7. Export from Package
- [ ] Update `src/stockagent/analysis/__init__.py` to export `analyze_news_sentiment`

## Order of Steps

1. Create module file (task 1)
2. Define keyword lists (task 2)
3. Implement headline sentiment (task 4) — no external calls
4. Implement news fetching (task 3)
5. Implement aggregate function (task 5)
6. Handle edge cases (task 6)
7. Export from package (task 7)
