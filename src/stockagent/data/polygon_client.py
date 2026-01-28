"""Polygon.io API client for fetching stock market data."""

from datetime import datetime, timedelta

from polygon import RESTClient
from polygon.exceptions import BadResponse

from stockagent.config import get_polygon_api_key


class PolygonAPIError(Exception):
    """Base exception for Polygon API errors."""

    def __init__(self, message: str = "An error occurred with the Polygon API"):
        self.message = message
        super().__init__(self.message)


class TickerNotFoundError(PolygonAPIError):
    """Raised when a ticker symbol is not found."""

    def __init__(self, ticker: str):
        self.ticker = ticker
        message = f"Ticker '{ticker}' not found. Please check the symbol and try again."
        super().__init__(message)


class RateLimitError(PolygonAPIError):
    """Raised when API rate limit is exceeded."""

    def __init__(self):
        message = (
            "API rate limit exceeded. Please wait a moment and try again. "
            "Free tier allows 5 calls per minute."
        )
        super().__init__(message)


class PolygonClient:
    """Client for interacting with Polygon.io API.

    Provides methods to fetch stock market data including:
    - Historical OHLCV bars (aggregates)
    - Ticker/company details
    - Previous close prices

    Rate Limits (Free Tier):
    - 5 API calls per minute
    - Historical data limited to 2 years
    - Data is delayed (not real-time)
    """

    def __init__(self, api_key: str | None = None):
        """Initialize the Polygon client.

        Args:
            api_key: Polygon API key. If not provided, will be loaded from config.
        """
        self._api_key = api_key or get_polygon_api_key()
        self._client = RESTClient(api_key=self._api_key)

    def get_previous_close(self, ticker: str) -> dict:
        """Get the previous close price for a ticker.

        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')

        Returns:
            dict with keys:
                - previous_close: float - Previous trading day's close price
                - current_price: float - Most recent price (same as previous_close for daily)

        Raises:
            TickerNotFoundError: If the ticker is not found
            RateLimitError: If API rate limit is exceeded
            PolygonAPIError: For other API errors
        """
        ticker = ticker.upper().strip()

        try:
            # get_previous_close_agg returns a list directly
            results = self._client.get_previous_close_agg(ticker)

            if not results or len(results) == 0:
                raise TickerNotFoundError(ticker)

            result = results[0]
            close_price = float(result.close)

            return {
                "previous_close": close_price,
                "current_price": close_price,  # For daily data, current = previous close
            }

        except BadResponse as e:
            self._handle_api_error(e, ticker)

    def get_ticker_details(self, ticker: str) -> dict:
        """Get company details for a ticker.

        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')

        Returns:
            dict with keys:
                - company_name: str - Full company name
                - sector: str - Industry sector (if available)

        Raises:
            TickerNotFoundError: If the ticker is not found
            RateLimitError: If API rate limit is exceeded
            PolygonAPIError: For other API errors
        """
        ticker = ticker.upper().strip()

        try:
            response = self._client.get_ticker_details(ticker)

            if not response:
                raise TickerNotFoundError(ticker)

            # The response is the TickerDetails object directly
            company_name = getattr(response, "name", ticker)
            sector = getattr(response, "sic_description", "Unknown")

            return {
                "company_name": company_name,
                "sector": sector,
            }

        except BadResponse as e:
            self._handle_api_error(e, ticker)

    def get_stock_aggregates(self, ticker: str, days: int = 90) -> list[dict]:
        """Get historical OHLCV bars for a ticker.

        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
            days: Number of days of historical data (default 90)

        Returns:
            List of OHLCV dicts, each containing:
                - open: float
                - high: float
                - low: float
                - close: float
                - volume: int
                - timestamp: str (ISO format date)

        Raises:
            TickerNotFoundError: If the ticker is not found or has no data
            RateLimitError: If API rate limit is exceeded
            PolygonAPIError: For other API errors
        """
        ticker = ticker.upper().strip()

        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        try:
            # Fetch daily aggregates
            aggs = self._client.get_aggs(
                ticker=ticker,
                multiplier=1,
                timespan="day",
                from_=start_date.strftime("%Y-%m-%d"),
                to=end_date.strftime("%Y-%m-%d"),
                limit=days + 10,  # Buffer for weekends/holidays
            )

            if not aggs or len(aggs) == 0:
                raise TickerNotFoundError(ticker)

            # Transform to OHLCV format
            bars = []
            for agg in aggs:
                bar = {
                    "open": float(agg.open),
                    "high": float(agg.high),
                    "low": float(agg.low),
                    "close": float(agg.close),
                    "volume": int(agg.volume),
                    "timestamp": datetime.fromtimestamp(agg.timestamp / 1000).strftime(
                        "%Y-%m-%d"
                    ),
                }
                bars.append(bar)

            return bars

        except BadResponse as e:
            self._handle_api_error(e, ticker)

    def _handle_api_error(self, error: BadResponse, ticker: str) -> None:
        """Handle API errors and raise appropriate exceptions.

        Args:
            error: The BadResponse exception from Polygon
            ticker: The ticker that was being queried

        Raises:
            TickerNotFoundError: For 404 errors
            RateLimitError: For 429 errors
            PolygonAPIError: For other errors
        """
        error_str = str(error).lower()

        # Check for rate limit (429)
        if "429" in str(error) or "rate limit" in error_str:
            raise RateLimitError()

        # Check for not found (404)
        if "404" in str(error) or "not found" in error_str:
            raise TickerNotFoundError(ticker)

        # Generic API error
        raise PolygonAPIError(f"API error for ticker '{ticker}': {error}")
