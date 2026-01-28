# Feature 004: News Sentiment

## Purpose

Fetch recent news headlines for a stock ticker using DuckDuckGo Search and compute sentiment scores using keyword-based analysis. This provides market sentiment context alongside technical indicators.

## Inputs / Outputs

### Inputs
- Ticker symbol (string)
- Company name (string, for better search results)
- Max results (int, default 8, keep top 5)

### Outputs
- `fetch_news(ticker, company_name, max_results)` → List of news headlines with metadata
- `analyze_sentiment(headline)` → Sentiment score (-1.0 to +1.0) and label
- `analyze_news_sentiment(ticker, company_name)` → SentimentResult dict with aggregate score and headlines

## Boundaries & Non-Goals

### In Scope
- Fetch news headlines via DuckDuckGo Search (duckduckgo-search library)
- Keyword-based sentiment scoring (positive/negative word lists)
- Per-headline sentiment labels (positive/negative/neutral)
- Aggregate sentiment score (-1.0 to +1.0)
- Handle no results gracefully (return neutral sentiment)

### Non-Goals
- No LLM-based sentiment analysis (keyword-only for v1)
- No news source filtering or quality scoring
- No historical sentiment tracking
- No social media sentiment (news only)

## Dependencies

- **Feature 001**: Uses models.py for SentimentResult type
- **Feature 002**: Uses company_name from ticker details

## PRD References

- Section 4: FR-3 News Sentiment Analysis
- Section 7: Data Sources (DuckDuckGo constraints)
