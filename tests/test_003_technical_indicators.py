"""Tests for Feature 003: Technical Indicators."""

import pytest


class TestIndicatorImports:
    """Test that indicator functions can be imported."""

    @pytest.mark.feature003
    def test_calculate_all_indicators_import(self):
        """Test that calculate_all_indicators can be imported."""
        from stockagent.analysis import calculate_all_indicators

        assert calculate_all_indicators is not None

    @pytest.mark.feature003
    def test_individual_indicators_import(self):
        """Test that individual indicator functions can be imported."""
        from stockagent.analysis import (
            calculate_bollinger_bands,
            calculate_macd,
            calculate_rsi,
            calculate_sma,
        )

        assert calculate_sma is not None
        assert calculate_rsi is not None
        assert calculate_macd is not None
        assert calculate_bollinger_bands is not None

    @pytest.mark.feature003
    def test_interpretation_functions_import(self):
        """Test that interpretation functions can be imported."""
        from stockagent.analysis import interpret_macd, interpret_rsi

        assert interpret_rsi is not None
        assert interpret_macd is not None


class TestSMA:
    """Test Simple Moving Average calculation."""

    @pytest.mark.feature003
    def test_sma_basic_calculation(self):
        """Test SMA with known values."""
        from stockagent.analysis import calculate_sma

        # SMA of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] with period 10
        prices = list(range(1, 11))
        result = calculate_sma(prices, 10)

        assert result == 5.5  # (1+2+3+4+5+6+7+8+9+10) / 10

    @pytest.mark.feature003
    def test_sma_uses_last_n_prices(self):
        """Test that SMA uses only the last n prices."""
        from stockagent.analysis import calculate_sma

        prices = [100, 200, 300, 10, 20, 30, 40, 50]
        result = calculate_sma(prices, 5)

        # Should use last 5: [30, 40, 50, 10, 20] - wait, order matters
        # Last 5 are: 10, 20, 30, 40, 50
        assert result == 30.0  # (10+20+30+40+50) / 5

    @pytest.mark.feature003
    def test_sma_insufficient_data(self):
        """Test SMA returns None with insufficient data."""
        from stockagent.analysis import calculate_sma

        prices = [1, 2, 3]
        result = calculate_sma(prices, 5)

        assert result is None

    @pytest.mark.feature003
    def test_sma_exact_period(self):
        """Test SMA with exactly period number of prices."""
        from stockagent.analysis import calculate_sma

        prices = [10, 20, 30, 40, 50]
        result = calculate_sma(prices, 5)

        assert result == 30.0

    @pytest.mark.feature003
    def test_sma_20(self):
        """Test SMA-20 with 20 prices."""
        from stockagent.analysis import calculate_sma

        prices = list(range(1, 21))  # 1 to 20
        result = calculate_sma(prices, 20)

        assert result == 10.5  # (1+2+...+20) / 20


class TestRSI:
    """Test Relative Strength Index calculation."""

    @pytest.mark.feature003
    def test_rsi_range(self):
        """Test that RSI is always between 0 and 100."""
        from stockagent.analysis import calculate_rsi

        # Uptrending prices
        prices = [100 + i for i in range(20)]
        result = calculate_rsi(prices, 14)

        assert result is not None
        assert 0 <= result <= 100

    @pytest.mark.feature003
    def test_rsi_uptrend_high(self):
        """Test that RSI is high in strong uptrend."""
        from stockagent.analysis import calculate_rsi

        # Strong uptrend - each price higher
        prices = [100 + i * 2 for i in range(20)]
        result = calculate_rsi(prices, 14)

        assert result is not None
        assert result > 70  # Should be overbought

    @pytest.mark.feature003
    def test_rsi_downtrend_low(self):
        """Test that RSI is low in strong downtrend."""
        from stockagent.analysis import calculate_rsi

        # Strong downtrend - each price lower
        prices = [200 - i * 2 for i in range(20)]
        result = calculate_rsi(prices, 14)

        assert result is not None
        assert result < 30  # Should be oversold

    @pytest.mark.feature003
    def test_rsi_insufficient_data(self):
        """Test RSI returns None with insufficient data."""
        from stockagent.analysis import calculate_rsi

        prices = [100, 101, 102]  # Only 3 prices, need 15 for period=14
        result = calculate_rsi(prices, 14)

        assert result is None

    @pytest.mark.feature003
    def test_rsi_neutral_range(self):
        """Test RSI in neutral range for mixed prices."""
        from stockagent.analysis import calculate_rsi

        # Alternating up and down
        prices = [100, 102, 101, 103, 102, 104, 103, 105, 104, 106, 105, 107, 106, 108, 107]
        result = calculate_rsi(prices, 14)

        assert result is not None
        assert 30 <= result <= 70  # Should be neutral range

    @pytest.mark.feature003
    def test_rsi_deterministic(self):
        """Test that RSI is deterministic."""
        from stockagent.analysis import calculate_rsi

        prices = [100, 102, 101, 103, 105, 104, 106, 108, 107, 109, 111, 110, 112, 114, 113]

        result1 = calculate_rsi(prices, 14)
        result2 = calculate_rsi(prices, 14)

        assert result1 == result2


class TestMACD:
    """Test MACD calculation."""

    @pytest.mark.feature003
    def test_macd_returns_dict(self):
        """Test that MACD returns correct dict structure."""
        from stockagent.analysis import calculate_macd

        prices = [100 + i * 0.5 for i in range(50)]
        result = calculate_macd(prices)

        assert result is not None
        assert "macd_line" in result
        assert "signal_line" in result
        assert "histogram" in result

    @pytest.mark.feature003
    def test_macd_histogram_calculation(self):
        """Test that histogram = macd_line - signal_line."""
        from stockagent.analysis import calculate_macd

        prices = [100 + i * 0.5 for i in range(50)]
        result = calculate_macd(prices)

        assert result is not None
        expected_histogram = result["macd_line"] - result["signal_line"]
        assert abs(result["histogram"] - expected_histogram) < 0.0001

    @pytest.mark.feature003
    def test_macd_insufficient_data(self):
        """Test MACD returns None with insufficient data."""
        from stockagent.analysis import calculate_macd

        prices = [100, 101, 102]  # Only 3 prices, need 26
        result = calculate_macd(prices)

        assert result is None

    @pytest.mark.feature003
    def test_macd_uptrend_positive(self):
        """Test that MACD is positive in uptrend."""
        from stockagent.analysis import calculate_macd

        # Strong uptrend
        prices = [100 + i * 2 for i in range(50)]
        result = calculate_macd(prices)

        assert result is not None
        assert result["macd_line"] > 0

    @pytest.mark.feature003
    def test_macd_downtrend_negative(self):
        """Test that MACD is negative in downtrend."""
        from stockagent.analysis import calculate_macd

        # Strong downtrend
        prices = [200 - i * 2 for i in range(50)]
        result = calculate_macd(prices)

        assert result is not None
        assert result["macd_line"] < 0

    @pytest.mark.feature003
    def test_macd_deterministic(self):
        """Test that MACD is deterministic."""
        from stockagent.analysis import calculate_macd

        prices = [100 + i * 0.5 for i in range(50)]

        result1 = calculate_macd(prices)
        result2 = calculate_macd(prices)

        assert result1["macd_line"] == result2["macd_line"]
        assert result1["signal_line"] == result2["signal_line"]


class TestBollingerBands:
    """Test Bollinger Bands calculation."""

    @pytest.mark.feature003
    def test_bollinger_returns_dict(self):
        """Test that Bollinger Bands returns correct dict structure."""
        from stockagent.analysis import calculate_bollinger_bands

        prices = [100 + i * 0.5 for i in range(30)]
        result = calculate_bollinger_bands(prices, 20, 2)

        assert result is not None
        assert "upper" in result
        assert "middle" in result
        assert "lower" in result

    @pytest.mark.feature003
    def test_bollinger_band_order(self):
        """Test that upper > middle > lower."""
        from stockagent.analysis import calculate_bollinger_bands

        prices = [100 + i * 0.5 for i in range(30)]
        result = calculate_bollinger_bands(prices, 20, 2)

        assert result is not None
        assert result["upper"] > result["middle"]
        assert result["middle"] > result["lower"]

    @pytest.mark.feature003
    def test_bollinger_middle_is_sma(self):
        """Test that middle band equals SMA."""
        from stockagent.analysis import calculate_bollinger_bands, calculate_sma

        prices = [100 + i * 0.5 for i in range(30)]
        result = calculate_bollinger_bands(prices, 20, 2)
        sma = calculate_sma(prices, 20)

        assert result is not None
        assert abs(result["middle"] - sma) < 0.0001

    @pytest.mark.feature003
    def test_bollinger_insufficient_data(self):
        """Test Bollinger returns None with insufficient data."""
        from stockagent.analysis import calculate_bollinger_bands

        prices = [100, 101, 102]  # Only 3 prices, need 20
        result = calculate_bollinger_bands(prices, 20, 2)

        assert result is None

    @pytest.mark.feature003
    def test_bollinger_symmetric_bands(self):
        """Test that bands are symmetric around middle."""
        from stockagent.analysis import calculate_bollinger_bands

        prices = [100 + i * 0.5 for i in range(30)]
        result = calculate_bollinger_bands(prices, 20, 2)

        assert result is not None
        upper_distance = result["upper"] - result["middle"]
        lower_distance = result["middle"] - result["lower"]
        assert abs(upper_distance - lower_distance) < 0.0001

    @pytest.mark.feature003
    def test_bollinger_deterministic(self):
        """Test that Bollinger Bands are deterministic."""
        from stockagent.analysis import calculate_bollinger_bands

        prices = [100 + i * 0.5 for i in range(30)]

        result1 = calculate_bollinger_bands(prices, 20, 2)
        result2 = calculate_bollinger_bands(prices, 20, 2)

        assert result1["upper"] == result2["upper"]
        assert result1["middle"] == result2["middle"]


class TestInterpretations:
    """Test interpretation functions."""

    @pytest.mark.feature003
    def test_interpret_rsi_overbought(self):
        """Test RSI overbought interpretation."""
        from stockagent.analysis import interpret_rsi

        assert interpret_rsi(75) == "overbought"
        assert interpret_rsi(80) == "overbought"
        assert interpret_rsi(100) == "overbought"

    @pytest.mark.feature003
    def test_interpret_rsi_oversold(self):
        """Test RSI oversold interpretation."""
        from stockagent.analysis import interpret_rsi

        assert interpret_rsi(25) == "oversold"
        assert interpret_rsi(20) == "oversold"
        assert interpret_rsi(0) == "oversold"

    @pytest.mark.feature003
    def test_interpret_rsi_neutral(self):
        """Test RSI neutral interpretation."""
        from stockagent.analysis import interpret_rsi

        assert interpret_rsi(50) == "neutral"
        assert interpret_rsi(30) == "neutral"
        assert interpret_rsi(70) == "neutral"

    @pytest.mark.feature003
    def test_interpret_rsi_none(self):
        """Test RSI interpretation with None."""
        from stockagent.analysis import interpret_rsi

        assert interpret_rsi(None) == "neutral"

    @pytest.mark.feature003
    def test_interpret_macd_bullish(self):
        """Test MACD bullish interpretation."""
        from stockagent.analysis import interpret_macd

        assert interpret_macd({"histogram": 0.5}) == "bullish"
        assert interpret_macd({"histogram": 1.0}) == "bullish"

    @pytest.mark.feature003
    def test_interpret_macd_bearish(self):
        """Test MACD bearish interpretation."""
        from stockagent.analysis import interpret_macd

        assert interpret_macd({"histogram": -0.5}) == "bearish"
        assert interpret_macd({"histogram": -1.0}) == "bearish"

    @pytest.mark.feature003
    def test_interpret_macd_neutral(self):
        """Test MACD neutral interpretation."""
        from stockagent.analysis import interpret_macd

        assert interpret_macd({"histogram": 0}) == "neutral"
        assert interpret_macd(None) == "neutral"


class TestCalculateAllIndicators:
    """Test the aggregate indicator function."""

    @pytest.mark.feature003
    def test_calculate_all_returns_dict(self):
        """Test that calculate_all_indicators returns correct structure."""
        from stockagent.analysis import calculate_all_indicators

        bars = [{"close": 100 + i * 0.5} for i in range(50)]
        result = calculate_all_indicators(bars)

        assert "rsi" in result
        assert "rsi_interpretation" in result
        assert "macd" in result
        assert "macd_interpretation" in result
        assert "bollinger" in result
        assert "sma_20" in result
        assert "sma_50" in result
        assert "sma_200" in result
        assert "current_price" in result

    @pytest.mark.feature003
    def test_calculate_all_with_sufficient_data(self):
        """Test all indicators calculated with sufficient data."""
        from stockagent.analysis import calculate_all_indicators

        bars = [{"close": 100 + i * 0.5} for i in range(250)]
        result = calculate_all_indicators(bars)

        assert result["rsi"] is not None
        assert result["macd"] is not None
        assert result["bollinger"] is not None
        assert result["sma_20"] is not None
        assert result["sma_50"] is not None
        assert result["sma_200"] is not None

    @pytest.mark.feature003
    def test_calculate_all_with_insufficient_data(self):
        """Test graceful handling of insufficient data."""
        from stockagent.analysis import calculate_all_indicators

        bars = [{"close": 100 + i} for i in range(10)]
        result = calculate_all_indicators(bars)

        # Should still return dict, just with None values
        assert "rsi" in result
        assert "sma_200" in result
        assert result["sma_200"] is None  # Need 200 prices

    @pytest.mark.feature003
    def test_calculate_all_empty_bars(self):
        """Test with empty bars list."""
        from stockagent.analysis import calculate_all_indicators

        result = calculate_all_indicators([])

        assert result["rsi"] is None
        assert result["current_price"] == 0.0

    @pytest.mark.feature003
    def test_calculate_all_current_price(self):
        """Test that current_price is the last close."""
        from stockagent.analysis import calculate_all_indicators

        bars = [{"close": 100}, {"close": 110}, {"close": 120}]
        result = calculate_all_indicators(bars)

        assert result["current_price"] == 120

    @pytest.mark.feature003
    def test_calculate_all_includes_interpretations(self):
        """Test that interpretations are included."""
        from stockagent.analysis import calculate_all_indicators

        bars = [{"close": 100 + i * 0.5} for i in range(50)]
        result = calculate_all_indicators(bars)

        assert result["rsi_interpretation"] in ["overbought", "oversold", "neutral"]
        assert result["macd_interpretation"] in ["bullish", "bearish", "neutral"]
