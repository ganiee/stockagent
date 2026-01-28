# Feature 002: Polygon Client

## Purpose

Implement a wrapper around the Polygon.io API to fetch real market data for stock analysis. This client abstracts API complexity and handles rate limiting, errors, and data transformation.

## Inputs / Outputs

### Inputs
- Ticker symbol (string, e.g., "AAPL")
- Days of historical data (int, default 90)
- Polygon API key (from config)

### Outputs
- `get_stock_aggregates(ticker, days)` → List of OHLCV bars
- `get_ticker_details(ticker)` → Company name, sector info
- `get_previous_close(ticker)` → Previous close price, current price

## Boundaries & Non-Goals

### In Scope
- Wrap Polygon REST API endpoints: Aggregates, Ticker Details, Previous Close
- Transform API responses to internal data structures
- Handle HTTP errors (4xx, 5xx) with clear error messages
- Handle rate limiting (5 calls/minute on free tier)
- Handle invalid tickers gracefully
- Return typed data matching `models.py` definitions

### Non-Goals
- No caching (keep it simple for v1)
- No real-time/websocket streaming
- No retry logic beyond basic error handling
- No indicator calculations (that's feature 003)

## Dependencies

- **Feature 001**: Requires `config.py` for API key, `models.py` for type definitions

## PRD References

- Section 4: FR-1 Stock Data Retrieval
- Section 5: NFR-2 Reliability (graceful error handling)
- Section 7: Data Sources & Constraints (rate limits)
