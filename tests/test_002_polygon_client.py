"""Tests for Feature 002: Polygon Client."""

from unittest.mock import MagicMock, patch

import pytest


class TestPolygonClientImports:
    """Test that Polygon client can be imported."""

    @pytest.mark.feature002
    def test_polygon_client_import(self):
        """Test that PolygonClient can be imported."""
        from stockagent.data import PolygonClient

        assert PolygonClient is not None

    @pytest.mark.feature002
    def test_exceptions_import(self):
        """Test that custom exceptions can be imported."""
        from stockagent.data import PolygonAPIError, RateLimitError, TickerNotFoundError

        assert PolygonAPIError is not None
        assert TickerNotFoundError is not None
        assert RateLimitError is not None

    @pytest.mark.feature002
    def test_exception_inheritance(self):
        """Test that custom exceptions inherit properly."""
        from stockagent.data import PolygonAPIError, RateLimitError, TickerNotFoundError

        assert issubclass(TickerNotFoundError, PolygonAPIError)
        assert issubclass(RateLimitError, PolygonAPIError)
        assert issubclass(PolygonAPIError, Exception)


class TestTickerNotFoundError:
    """Test TickerNotFoundError exception."""

    @pytest.mark.feature002
    def test_ticker_not_found_message(self):
        """Test that TickerNotFoundError includes ticker in message."""
        from stockagent.data import TickerNotFoundError

        error = TickerNotFoundError("XYZ")
        assert "XYZ" in str(error)
        assert "not found" in str(error).lower()

    @pytest.mark.feature002
    def test_ticker_not_found_stores_ticker(self):
        """Test that TickerNotFoundError stores the ticker."""
        from stockagent.data import TickerNotFoundError

        error = TickerNotFoundError("ABC")
        assert error.ticker == "ABC"


class TestRateLimitError:
    """Test RateLimitError exception."""

    @pytest.mark.feature002
    def test_rate_limit_message(self):
        """Test that RateLimitError has helpful message."""
        from stockagent.data import RateLimitError

        error = RateLimitError()
        error_str = str(error).lower()
        assert "rate limit" in error_str or "wait" in error_str


class TestPolygonClientInitialization:
    """Test PolygonClient initialization."""

    @pytest.mark.feature002
    def test_client_with_provided_api_key(self, mock_env_without_api_key):
        """Test that client can be initialized with provided API key."""
        from stockagent.data import PolygonClient

        # Should not raise even without env var when key is provided
        client = PolygonClient(api_key="test_key_123")
        assert client._api_key == "test_key_123"

    @pytest.mark.feature002
    def test_client_loads_api_key_from_config(self, mock_env_with_api_key):
        """Test that client loads API key from config when not provided."""
        from stockagent.data import PolygonClient

        client = PolygonClient()
        assert client._api_key == "test_api_key_12345"

    @pytest.mark.feature002
    def test_client_raises_without_api_key(self, mock_env_without_api_key):
        """Test that client raises ValueError when no API key available."""
        from stockagent.data import PolygonClient

        with pytest.raises(ValueError) as exc_info:
            PolygonClient()

        assert "POLYGON_API_KEY" in str(exc_info.value)


class TestGetPreviousClose:
    """Test get_previous_close method."""

    @pytest.mark.feature002
    def test_get_previous_close_success(self, mock_env_with_api_key):
        """Test successful previous close fetch."""
        from stockagent.data import PolygonClient

        # Create mock response
        mock_result = MagicMock()
        mock_result.close = 150.25

        mock_response = MagicMock()
        mock_response.results = [mock_result]

        with patch.object(
            PolygonClient, "__init__", lambda self, api_key=None: None
        ):
            client = PolygonClient()
            client._api_key = "test_key"
            client._client = MagicMock()
            client._client.get_previous_close.return_value = mock_response

            result = client.get_previous_close("AAPL")

            assert result["previous_close"] == 150.25
            assert result["current_price"] == 150.25
            client._client.get_previous_close.assert_called_once_with("AAPL")

    @pytest.mark.feature002
    def test_get_previous_close_normalizes_ticker(self, mock_env_with_api_key):
        """Test that ticker is normalized to uppercase."""
        from stockagent.data import PolygonClient

        mock_result = MagicMock()
        mock_result.close = 100.0

        mock_response = MagicMock()
        mock_response.results = [mock_result]

        with patch.object(
            PolygonClient, "__init__", lambda self, api_key=None: None
        ):
            client = PolygonClient()
            client._api_key = "test_key"
            client._client = MagicMock()
            client._client.get_previous_close.return_value = mock_response

            client.get_previous_close("aapl")  # lowercase

            client._client.get_previous_close.assert_called_once_with("AAPL")

    @pytest.mark.feature002
    def test_get_previous_close_empty_response(self, mock_env_with_api_key):
        """Test that empty response raises TickerNotFoundError."""
        from stockagent.data import PolygonClient, TickerNotFoundError

        mock_response = MagicMock()
        mock_response.results = []

        with patch.object(
            PolygonClient, "__init__", lambda self, api_key=None: None
        ):
            client = PolygonClient()
            client._api_key = "test_key"
            client._client = MagicMock()
            client._client.get_previous_close.return_value = mock_response

            with pytest.raises(TickerNotFoundError) as exc_info:
                client.get_previous_close("INVALID")

            assert "INVALID" in str(exc_info.value)


class TestGetTickerDetails:
    """Test get_ticker_details method."""

    @pytest.mark.feature002
    def test_get_ticker_details_success(self, mock_env_with_api_key):
        """Test successful ticker details fetch."""
        from stockagent.data import PolygonClient

        mock_result = MagicMock()
        mock_result.name = "Apple Inc."
        mock_result.sic_description = "Technology"

        mock_response = MagicMock()
        mock_response.results = mock_result

        with patch.object(
            PolygonClient, "__init__", lambda self, api_key=None: None
        ):
            client = PolygonClient()
            client._api_key = "test_key"
            client._client = MagicMock()
            client._client.get_ticker_details.return_value = mock_response

            result = client.get_ticker_details("AAPL")

            assert result["company_name"] == "Apple Inc."
            assert result["sector"] == "Technology"

    @pytest.mark.feature002
    def test_get_ticker_details_missing_fields(self, mock_env_with_api_key):
        """Test that missing fields have defaults."""
        from stockagent.data import PolygonClient

        mock_result = MagicMock(spec=[])  # Empty spec means no attributes

        mock_response = MagicMock()
        mock_response.results = mock_result

        with patch.object(
            PolygonClient, "__init__", lambda self, api_key=None: None
        ):
            client = PolygonClient()
            client._api_key = "test_key"
            client._client = MagicMock()
            client._client.get_ticker_details.return_value = mock_response

            result = client.get_ticker_details("XYZ")

            # Should have defaults
            assert "company_name" in result
            assert "sector" in result


class TestGetStockAggregates:
    """Test get_stock_aggregates method."""

    @pytest.mark.feature002
    def test_get_stock_aggregates_success(self, mock_env_with_api_key):
        """Test successful aggregates fetch."""
        from stockagent.data import PolygonClient

        # Create mock aggregates
        mock_agg1 = MagicMock()
        mock_agg1.open = 100.0
        mock_agg1.high = 105.0
        mock_agg1.low = 99.0
        mock_agg1.close = 103.0
        mock_agg1.volume = 1000000
        mock_agg1.timestamp = 1704067200000  # 2024-01-01 in milliseconds

        mock_agg2 = MagicMock()
        mock_agg2.open = 103.0
        mock_agg2.high = 108.0
        mock_agg2.low = 102.0
        mock_agg2.close = 107.0
        mock_agg2.volume = 1100000
        mock_agg2.timestamp = 1704153600000  # 2024-01-02 in milliseconds

        with patch.object(
            PolygonClient, "__init__", lambda self, api_key=None: None
        ):
            client = PolygonClient()
            client._api_key = "test_key"
            client._client = MagicMock()
            client._client.get_aggs.return_value = [mock_agg1, mock_agg2]

            result = client.get_stock_aggregates("AAPL", days=30)

            assert len(result) == 2
            assert result[0]["open"] == 100.0
            assert result[0]["high"] == 105.0
            assert result[0]["low"] == 99.0
            assert result[0]["close"] == 103.0
            assert result[0]["volume"] == 1000000
            assert "timestamp" in result[0]

    @pytest.mark.feature002
    def test_get_stock_aggregates_empty_response(self, mock_env_with_api_key):
        """Test that empty response raises TickerNotFoundError."""
        from stockagent.data import PolygonClient, TickerNotFoundError

        with patch.object(
            PolygonClient, "__init__", lambda self, api_key=None: None
        ):
            client = PolygonClient()
            client._api_key = "test_key"
            client._client = MagicMock()
            client._client.get_aggs.return_value = []

            with pytest.raises(TickerNotFoundError):
                client.get_stock_aggregates("INVALID")

    @pytest.mark.feature002
    def test_get_stock_aggregates_ohlcv_format(self, mock_env_with_api_key):
        """Test that returned data matches OHLCV format."""
        from stockagent.data import PolygonClient

        mock_agg = MagicMock()
        mock_agg.open = 100.0
        mock_agg.high = 105.0
        mock_agg.low = 99.0
        mock_agg.close = 103.0
        mock_agg.volume = 1000000
        mock_agg.timestamp = 1704067200000

        with patch.object(
            PolygonClient, "__init__", lambda self, api_key=None: None
        ):
            client = PolygonClient()
            client._api_key = "test_key"
            client._client = MagicMock()
            client._client.get_aggs.return_value = [mock_agg]

            result = client.get_stock_aggregates("AAPL", days=10)

            bar = result[0]
            assert "open" in bar
            assert "high" in bar
            assert "low" in bar
            assert "close" in bar
            assert "volume" in bar
            assert "timestamp" in bar
            assert isinstance(bar["open"], float)
            assert isinstance(bar["volume"], int)


class TestErrorHandling:
    """Test API error handling."""

    @pytest.mark.feature002
    def test_handle_404_error(self, mock_env_with_api_key):
        """Test that 404 errors raise TickerNotFoundError."""
        from polygon.exceptions import BadResponse

        from stockagent.data import PolygonClient, TickerNotFoundError

        with patch.object(
            PolygonClient, "__init__", lambda self, api_key=None: None
        ):
            client = PolygonClient()
            client._api_key = "test_key"
            client._client = MagicMock()
            client._client.get_previous_close.side_effect = BadResponse("404 Not Found")

            with pytest.raises(TickerNotFoundError):
                client.get_previous_close("INVALID")

    @pytest.mark.feature002
    def test_handle_429_error(self, mock_env_with_api_key):
        """Test that 429 errors raise RateLimitError."""
        from polygon.exceptions import BadResponse

        from stockagent.data import PolygonClient, RateLimitError

        with patch.object(
            PolygonClient, "__init__", lambda self, api_key=None: None
        ):
            client = PolygonClient()
            client._api_key = "test_key"
            client._client = MagicMock()
            client._client.get_previous_close.side_effect = BadResponse("429 Rate Limit")

            with pytest.raises(RateLimitError):
                client.get_previous_close("AAPL")

    @pytest.mark.feature002
    def test_handle_generic_error(self, mock_env_with_api_key):
        """Test that generic errors raise PolygonAPIError."""
        from polygon.exceptions import BadResponse

        from stockagent.data import PolygonAPIError, PolygonClient

        with patch.object(
            PolygonClient, "__init__", lambda self, api_key=None: None
        ):
            client = PolygonClient()
            client._api_key = "test_key"
            client._client = MagicMock()
            client._client.get_previous_close.side_effect = BadResponse("500 Internal Error")

            with pytest.raises(PolygonAPIError):
                client.get_previous_close("AAPL")
