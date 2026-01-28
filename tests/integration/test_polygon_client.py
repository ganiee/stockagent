"""Integration tests for Polygon client with mocked API."""

from unittest.mock import MagicMock, patch

import pytest


class TestPolygonClientSuccess:
    """Test Polygon client successful API calls."""

    @pytest.mark.feature009
    def test_get_previous_close_success(self, mock_env_with_api_key):
        """Test get_previous_close returns correct data."""
        from stockagent.data import PolygonClient

        mock_result = MagicMock()
        mock_result.close = 150.0
        mock_result.open = 148.0

        mock_response = MagicMock()
        mock_response.results = [mock_result]

        mock_client = MagicMock()
        mock_client.get_previous_close.return_value = mock_response

        with patch("stockagent.data.polygon_client.RESTClient", return_value=mock_client):
            client = PolygonClient()
            result = client.get_previous_close("AAPL")

            assert "previous_close" in result
            assert "current_price" in result
            assert result["current_price"] == 150.0

    @pytest.mark.feature009
    def test_get_ticker_details_success(self, mock_env_with_api_key):
        """Test get_ticker_details returns correct data."""
        from stockagent.data import PolygonClient

        mock_result = MagicMock()
        mock_result.name = "Apple Inc."
        mock_result.sic_description = "Technology"

        mock_response = MagicMock()
        mock_response.results = mock_result

        mock_client = MagicMock()
        mock_client.get_ticker_details.return_value = mock_response

        with patch("stockagent.data.polygon_client.RESTClient", return_value=mock_client):
            client = PolygonClient()
            result = client.get_ticker_details("AAPL")

            assert "company_name" in result
            assert "Apple" in result["company_name"]

    @pytest.mark.feature009
    def test_get_stock_aggregates_success(self, mock_env_with_api_key):
        """Test get_stock_aggregates returns correct data."""
        from stockagent.data import PolygonClient

        mock_agg1 = MagicMock()
        mock_agg1.open = 100.0
        mock_agg1.high = 105.0
        mock_agg1.low = 99.0
        mock_agg1.close = 103.0
        mock_agg1.volume = 1000000
        mock_agg1.timestamp = 1704067200000  # 2024-01-01

        mock_agg2 = MagicMock()
        mock_agg2.open = 103.0
        mock_agg2.high = 107.0
        mock_agg2.low = 102.0
        mock_agg2.close = 106.0
        mock_agg2.volume = 1100000
        mock_agg2.timestamp = 1704153600000  # 2024-01-02

        mock_client = MagicMock()
        mock_client.get_aggs.return_value = [mock_agg1, mock_agg2]

        with patch("stockagent.data.polygon_client.RESTClient", return_value=mock_client):
            client = PolygonClient()
            result = client.get_stock_aggregates("AAPL", days=5)

            assert isinstance(result, list)
            assert len(result) == 2
            assert "close" in result[0]
            assert "open" in result[0]
            assert result[0]["close"] == 103.0

    @pytest.mark.feature009
    def test_get_stock_aggregates_empty_results(self, mock_env_with_api_key):
        """Test get_stock_aggregates handles empty results."""
        from stockagent.data import PolygonClient, TickerNotFoundError

        mock_client = MagicMock()
        mock_client.get_aggs.return_value = []

        with patch("stockagent.data.polygon_client.RESTClient", return_value=mock_client):
            client = PolygonClient()
            # Empty results should raise TickerNotFoundError
            with pytest.raises(TickerNotFoundError):
                client.get_stock_aggregates("INVALID", days=5)


class TestPolygonClientErrors:
    """Test Polygon client error handling."""

    @pytest.mark.feature009
    def test_ticker_not_found(self, mock_env_with_api_key):
        """Test 404 raises TickerNotFoundError."""
        from polygon.exceptions import BadResponse

        from stockagent.data import PolygonClient, TickerNotFoundError

        mock_client = MagicMock()
        mock_client.get_previous_close.side_effect = BadResponse("404 Not Found")

        with patch("stockagent.data.polygon_client.RESTClient", return_value=mock_client):
            client = PolygonClient()
            with pytest.raises(TickerNotFoundError):
                client.get_previous_close("INVALIDTICKER")

    @pytest.mark.feature009
    def test_rate_limit_error(self, mock_env_with_api_key):
        """Test 429 raises RateLimitError."""
        from polygon.exceptions import BadResponse

        from stockagent.data import PolygonClient, RateLimitError

        mock_client = MagicMock()
        mock_client.get_previous_close.side_effect = BadResponse("429 Rate Limit Exceeded")

        with patch("stockagent.data.polygon_client.RESTClient", return_value=mock_client):
            client = PolygonClient()
            with pytest.raises(RateLimitError):
                client.get_previous_close("AAPL")

    @pytest.mark.feature009
    def test_api_error(self, mock_env_with_api_key):
        """Test other errors raise PolygonAPIError."""
        from polygon.exceptions import BadResponse

        from stockagent.data import PolygonAPIError, PolygonClient

        mock_client = MagicMock()
        mock_client.get_previous_close.side_effect = BadResponse("500 Internal Server Error")

        with patch("stockagent.data.polygon_client.RESTClient", return_value=mock_client):
            client = PolygonClient()
            with pytest.raises(PolygonAPIError):
                client.get_previous_close("AAPL")

    @pytest.mark.feature009
    def test_empty_results_raises_ticker_not_found(self, mock_env_with_api_key):
        """Test empty results raise TickerNotFoundError."""
        from stockagent.data import PolygonClient, TickerNotFoundError

        mock_response = MagicMock()
        mock_response.results = None

        mock_client = MagicMock()
        mock_client.get_previous_close.return_value = mock_response

        with patch("stockagent.data.polygon_client.RESTClient", return_value=mock_client):
            client = PolygonClient()
            with pytest.raises(TickerNotFoundError):
                client.get_previous_close("INVALIDTICKER")


class TestPolygonClientConfig:
    """Test Polygon client configuration."""

    @pytest.mark.feature009
    def test_client_uses_api_key(self, mock_env_with_api_key):
        """Test client uses API key from environment."""
        from stockagent.data import PolygonClient

        with patch("stockagent.data.polygon_client.RESTClient") as mock_rest:
            client = PolygonClient()
            # Verify RESTClient was called with the API key
            mock_rest.assert_called_once_with(api_key="test_api_key_12345")

    @pytest.mark.feature009
    def test_client_raises_without_api_key(self, mock_env_without_api_key):
        """Test client raises error without API key."""
        from stockagent.data import PolygonClient

        with pytest.raises(ValueError):
            PolygonClient()

    @pytest.mark.feature009
    def test_client_accepts_explicit_api_key(self, mock_env_without_api_key):
        """Test client accepts explicit API key parameter."""
        from stockagent.data import PolygonClient

        with patch("stockagent.data.polygon_client.RESTClient") as mock_rest:
            client = PolygonClient(api_key="explicit_key_123")
            mock_rest.assert_called_once_with(api_key="explicit_key_123")
