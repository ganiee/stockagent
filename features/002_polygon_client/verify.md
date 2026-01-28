# Feature 002: Verification

## Prerequisites
- Valid `.env` file with `POLYGON_API_KEY` set
- Feature 001 completed

## Local Commands to Run

### 1. Verify Module Imports
```bash
python -c "
from stockagent.data import PolygonClient
from stockagent.data.polygon_client import PolygonAPIError, TickerNotFoundError, RateLimitError
print('Imports successful')
"
```

### 2. Verify get_previous_close (Quick Test)
```bash
python -c "
from stockagent.data import PolygonClient
client = PolygonClient()
result = client.get_previous_close('AAPL')
print(f'Previous close: {result}')
assert 'previous_close' in result
assert 'current_price' in result
assert isinstance(result['previous_close'], (int, float))
print('get_previous_close: PASSED')
"
```

### 3. Verify get_ticker_details
```bash
python -c "
from stockagent.data import PolygonClient
client = PolygonClient()
result = client.get_ticker_details('AAPL')
print(f'Ticker details: {result}')
assert 'company_name' in result
assert 'Apple' in result['company_name']
print('get_ticker_details: PASSED')
"
```

### 4. Verify get_stock_aggregates
```bash
python -c "
from stockagent.data import PolygonClient
client = PolygonClient()
result = client.get_stock_aggregates('AAPL', days=30)
print(f'Got {len(result)} bars')
assert len(result) > 0
bar = result[0]
assert all(k in bar for k in ['open', 'high', 'low', 'close', 'volume'])
print('get_stock_aggregates: PASSED')
"
```

### 5. Verify Invalid Ticker Handling
```bash
python -c "
from stockagent.data import PolygonClient
from stockagent.data.polygon_client import TickerNotFoundError
client = PolygonClient()
try:
    client.get_previous_close('INVALIDXYZ123')
    print('ERROR: Should have raised TickerNotFoundError')
except TickerNotFoundError as e:
    print(f'Correct error raised: {e}')
    print('Invalid ticker handling: PASSED')
"
```

### 6. Verify Error Message Quality
```bash
python -c "
from stockagent.data.polygon_client import TickerNotFoundError, RateLimitError, PolygonAPIError

# Check error messages are user-friendly
e1 = TickerNotFoundError('XYZ')
assert 'XYZ' in str(e1)
print(f'TickerNotFoundError message: {e1}')

e2 = RateLimitError()
assert 'wait' in str(e2).lower() or 'limit' in str(e2).lower()
print(f'RateLimitError message: {e2}')

print('Error messages: PASSED')
"
```

## Quick Verification (All-in-One)
```bash
python -c "
from stockagent.data import PolygonClient
client = PolygonClient()

# Test all three methods
close = client.get_previous_close('MSFT')
details = client.get_ticker_details('MSFT')
bars = client.get_stock_aggregates('MSFT', days=10)

print(f'Close: {close[\"previous_close\"]}')
print(f'Company: {details[\"company_name\"]}')
print(f'Bars: {len(bars)} days')
print('Feature 002 verification: PASSED')
"
```
