"""Unit tests for technical indicator calculations."""

import pytest


class TestSMACalculation:
    """Test Simple Moving Average calculation."""

    @pytest.mark.feature009
    def test_sma_basic(self):
        """Test SMA with known values."""
        from stockagent.analysis import calculate_sma

        prices = [10.0, 20.0, 30.0, 40.0, 50.0]
        result = calculate_sma(prices, period=5)
        assert result == 30.0  # (10+20+30+40+50)/5

    @pytest.mark.feature009
    def test_sma_period_3(self):
        """Test SMA with period 3."""
        from stockagent.analysis import calculate_sma

        prices = [10.0, 20.0, 30.0, 40.0, 50.0]
        result = calculate_sma(prices, period=3)
        assert result == 40.0  # (30+40+50)/3

    @pytest.mark.feature009
    def test_sma_insufficient_data(self):
        """Test SMA returns None with insufficient data."""
        from stockagent.analysis import calculate_sma

        prices = [10.0, 20.0]
        result = calculate_sma(prices, period=5)
        assert result is None

    @pytest.mark.feature009
    def test_sma_empty_list(self):
        """Test SMA with empty list."""
        from stockagent.analysis import calculate_sma

        result = calculate_sma([], period=5)
        assert result is None

    @pytest.mark.feature009
    def test_sma_single_value(self):
        """Test SMA with single value."""
        from stockagent.analysis import calculate_sma

        result = calculate_sma([100.0], period=1)
        assert result == 100.0


class TestRSICalculation:
    """Test RSI calculation."""

    @pytest.mark.feature009
    def test_rsi_uptrend(self):
        """Test RSI in uptrend (high value)."""
        from stockagent.analysis import calculate_rsi

        # Mostly increasing prices should give high RSI
        prices = [100 + i * 2 for i in range(20)]
        result = calculate_rsi(prices, period=14)
        assert result is not None
        assert result > 50  # Should be above neutral

    @pytest.mark.feature009
    def test_rsi_downtrend(self):
        """Test RSI in downtrend (low value)."""
        from stockagent.analysis import calculate_rsi

        # Mostly decreasing prices should give low RSI
        prices = [100 - i * 2 for i in range(20)]
        result = calculate_rsi(prices, period=14)
        assert result is not None
        assert result < 50  # Should be below neutral

    @pytest.mark.feature009
    def test_rsi_bounds(self):
        """Test RSI is always between 0 and 100."""
        from stockagent.analysis import calculate_rsi

        # Extreme uptrend
        prices_up = [100 + i * 10 for i in range(20)]
        rsi_up = calculate_rsi(prices_up, period=14)
        assert 0 <= rsi_up <= 100

        # Extreme downtrend
        prices_down = [200 - i * 5 for i in range(20)]
        rsi_down = calculate_rsi(prices_down, period=14)
        assert 0 <= rsi_down <= 100

    @pytest.mark.feature009
    def test_rsi_insufficient_data(self):
        """Test RSI returns None with insufficient data."""
        from stockagent.analysis import calculate_rsi

        prices = [100.0] * 10  # Less than period + 1
        result = calculate_rsi(prices, period=14)
        assert result is None

    @pytest.mark.feature009
    def test_rsi_empty_list(self):
        """Test RSI with empty list."""
        from stockagent.analysis import calculate_rsi

        result = calculate_rsi([], period=14)
        assert result is None


class TestMACDCalculation:
    """Test MACD calculation."""

    @pytest.mark.feature009
    def test_macd_returns_dict(self):
        """Test MACD returns dict with expected keys."""
        from stockagent.analysis import calculate_macd

        prices = [100 + i * 0.5 for i in range(50)]
        result = calculate_macd(prices)

        assert result is not None
        assert "macd_line" in result
        assert "signal_line" in result
        assert "histogram" in result

    @pytest.mark.feature009
    def test_macd_histogram_calculation(self):
        """Test MACD histogram equals MACD - signal."""
        from stockagent.analysis import calculate_macd

        prices = [100 + i * 0.5 for i in range(50)]
        result = calculate_macd(prices)

        if result:
            expected_histogram = result["macd_line"] - result["signal_line"]
            assert abs(result["histogram"] - expected_histogram) < 0.0001

    @pytest.mark.feature009
    def test_macd_insufficient_data(self):
        """Test MACD returns None with insufficient data."""
        from stockagent.analysis import calculate_macd

        prices = [100.0] * 20  # Need at least 26 for MACD
        result = calculate_macd(prices)
        assert result is None

    @pytest.mark.feature009
    def test_macd_empty_list(self):
        """Test MACD with empty list."""
        from stockagent.analysis import calculate_macd

        result = calculate_macd([])
        assert result is None


class TestBollingerBands:
    """Test Bollinger Bands calculation."""

    @pytest.mark.feature009
    def test_bollinger_returns_dict(self):
        """Test Bollinger returns dict with expected keys."""
        from stockagent.analysis import calculate_bollinger_bands

        prices = [100 + i * 0.5 for i in range(25)]
        result = calculate_bollinger_bands(prices, period=20)

        assert result is not None
        assert "upper" in result
        assert "middle" in result
        assert "lower" in result

    @pytest.mark.feature009
    def test_bollinger_band_order(self):
        """Test upper > middle > lower."""
        from stockagent.analysis import calculate_bollinger_bands

        prices = [100 + i * 0.5 for i in range(25)]
        result = calculate_bollinger_bands(prices, period=20)

        if result:
            assert result["upper"] > result["middle"]
            assert result["middle"] > result["lower"]

    @pytest.mark.feature009
    def test_bollinger_middle_is_sma(self):
        """Test middle band equals SMA."""
        from stockagent.analysis import calculate_bollinger_bands, calculate_sma

        prices = [100 + i * 0.5 for i in range(25)]
        bollinger = calculate_bollinger_bands(prices, period=20)
        sma = calculate_sma(prices, period=20)

        if bollinger and sma:
            assert abs(bollinger["middle"] - sma) < 0.0001

    @pytest.mark.feature009
    def test_bollinger_insufficient_data(self):
        """Test Bollinger returns None with insufficient data."""
        from stockagent.analysis import calculate_bollinger_bands

        prices = [100.0] * 15  # Less than period
        result = calculate_bollinger_bands(prices, period=20)
        assert result is None


class TestIndicatorInterpretations:
    """Test indicator interpretation functions."""

    @pytest.mark.feature009
    def test_rsi_interpretation_oversold(self):
        """Test RSI interpretation for oversold."""
        from stockagent.analysis import interpret_rsi

        assert interpret_rsi(25.0) == "oversold"
        assert interpret_rsi(29.0) == "oversold"

    @pytest.mark.feature009
    def test_rsi_interpretation_overbought(self):
        """Test RSI interpretation for overbought."""
        from stockagent.analysis import interpret_rsi

        assert interpret_rsi(75.0) == "overbought"
        assert interpret_rsi(80.0) == "overbought"

    @pytest.mark.feature009
    def test_rsi_interpretation_neutral(self):
        """Test RSI interpretation for neutral."""
        from stockagent.analysis import interpret_rsi

        assert interpret_rsi(50.0) == "neutral"
        assert interpret_rsi(45.0) == "neutral"

    @pytest.mark.feature009
    def test_rsi_interpretation_none(self):
        """Test RSI interpretation for None."""
        from stockagent.analysis import interpret_rsi

        assert interpret_rsi(None) == "neutral"

    @pytest.mark.feature009
    def test_macd_interpretation_bullish(self):
        """Test MACD interpretation for bullish."""
        from stockagent.analysis import interpret_macd

        macd = {"histogram": 1.0, "macd_line": 0.5, "signal_line": -0.5}
        assert interpret_macd(macd) == "bullish"

    @pytest.mark.feature009
    def test_macd_interpretation_bearish(self):
        """Test MACD interpretation for bearish."""
        from stockagent.analysis import interpret_macd

        macd = {"histogram": -1.0, "macd_line": -0.5, "signal_line": 0.5}
        assert interpret_macd(macd) == "bearish"

    @pytest.mark.feature009
    def test_macd_interpretation_none(self):
        """Test MACD interpretation for None."""
        from stockagent.analysis import interpret_macd

        assert interpret_macd(None) == "neutral"


class TestCalculateAllIndicators:
    """Test calculate_all_indicators function."""

    @pytest.mark.feature009
    def test_calculate_all_returns_dict(self):
        """Test calculate_all_indicators returns complete dict."""
        from stockagent.analysis import calculate_all_indicators

        bars = [{"close": 100 + i * 0.5} for i in range(100)]
        result = calculate_all_indicators(bars)

        assert "rsi" in result
        assert "macd" in result
        assert "bollinger" in result
        assert "sma_20" in result
        assert "sma_50" in result
        assert "rsi_interpretation" in result
        assert "macd_interpretation" in result

    @pytest.mark.feature009
    def test_calculate_all_with_empty_data(self):
        """Test calculate_all_indicators with empty data."""
        from stockagent.analysis import calculate_all_indicators

        result = calculate_all_indicators([])

        assert result["rsi"] is None
        assert result["macd"] is None
