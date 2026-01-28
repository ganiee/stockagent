# Feature 002: Tasks

## Implementation Checklist

### 1. Create Polygon Client Module
- [ ] Create `src/stockagent/data/polygon_client.py`
- [ ] Import polygon-api-client library
- [ ] Import config for API key

### 2. Implement Client Class
- [ ] Create `PolygonClient` class
- [ ] Initialize with API key from config
- [ ] Create internal polygon RESTClient instance

### 3. Implement get_stock_aggregates()
- [ ] Accept ticker (str) and days (int, default=90) parameters
- [ ] Calculate date range (today - days to today)
- [ ] Call Polygon aggregates endpoint (daily bars)
- [ ] Transform response to list of OHLCV dicts
- [ ] Handle empty response (no data for ticker)
- [ ] Handle API errors

### 4. Implement get_ticker_details()
- [ ] Accept ticker (str) parameter
- [ ] Call Polygon ticker details endpoint
- [ ] Extract company name and sector
- [ ] Return dict with company_name, sector fields
- [ ] Handle ticker not found

### 5. Implement get_previous_close()
- [ ] Accept ticker (str) parameter
- [ ] Call Polygon previous close endpoint
- [ ] Extract previous close price and current price
- [ ] Return dict with previous_close, current_price fields
- [ ] Handle ticker not found

### 6. Implement Error Handling
- [ ] Create custom exceptions: `PolygonAPIError`, `TickerNotFoundError`, `RateLimitError`
- [ ] Catch HTTP 404 → raise `TickerNotFoundError`
- [ ] Catch HTTP 429 → raise `RateLimitError`
- [ ] Catch other HTTP errors → raise `PolygonAPIError`
- [ ] All exceptions include user-friendly messages

### 7. Add Rate Limit Awareness
- [ ] Add delay between consecutive calls if needed
- [ ] Document rate limit constraints in docstrings

### 8. Export from Package
- [ ] Update `src/stockagent/data/__init__.py` to export `PolygonClient`

## Order of Steps

1. Create module file (task 1)
2. Create client class skeleton (task 2)
3. Implement error handling first (task 6)
4. Implement get_previous_close (task 5) — simplest endpoint
5. Implement get_ticker_details (task 4)
6. Implement get_stock_aggregates (task 3) — most complex
7. Add rate limit handling (task 7)
8. Export from package (task 8)
