# Feature 002: Acceptance Criteria

## Required Outcomes

### AC-1: Client Imports Successfully
- [ ] `from stockagent.data import PolygonClient` works
- [ ] `from stockagent.data.polygon_client import PolygonAPIError, TickerNotFoundError, RateLimitError` works

### AC-2: get_stock_aggregates Works
- [ ] Returns list of OHLCV dicts for valid ticker (e.g., "AAPL")
- [ ] Each dict contains: `open`, `high`, `low`, `close`, `volume`, `timestamp`
- [ ] Returns data for specified number of days (default 90)
- [ ] Raises `TickerNotFoundError` for invalid ticker (e.g., "INVALIDXYZ")

### AC-3: get_ticker_details Works
- [ ] Returns dict with `company_name` for valid ticker
- [ ] Company name matches expected value (e.g., "Apple Inc." for AAPL)
- [ ] Raises `TickerNotFoundError` for invalid ticker

### AC-4: get_previous_close Works
- [ ] Returns dict with `previous_close` and `current_price` for valid ticker
- [ ] Values are floats, not strings
- [ ] Raises `TickerNotFoundError` for invalid ticker

### AC-5: Error Messages are User-Friendly
- [ ] `TickerNotFoundError` message includes the invalid ticker
- [ ] `RateLimitError` message suggests waiting
- [ ] `PolygonAPIError` message does not expose internal details

### AC-6: API Key Validation
- [ ] Client raises clear error if API key is missing/invalid
- [ ] Error message guides user to check .env file

## Observable Outcomes

1. Smoke test with real API key returns actual market data
2. Invalid ticker produces clear "not found" error
3. All returned data types match expected schemas
4. No raw stack traces exposed to callers
