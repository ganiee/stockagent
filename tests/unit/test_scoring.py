"""Unit tests for scoring functions."""

import pytest


class TestScoreRSI:
    """Test RSI scoring function."""

    @pytest.mark.feature009
    def test_score_rsi_oversold(self):
        """Test RSI oversold gives positive score."""
        from stockagent.analysis import score_rsi

        assert score_rsi(20.0) == 20.0
        assert score_rsi(29.0) == 20.0

    @pytest.mark.feature009
    def test_score_rsi_slightly_oversold(self):
        """Test RSI slightly oversold gives moderate positive score."""
        from stockagent.analysis import score_rsi

        assert score_rsi(35.0) == 10.0

    @pytest.mark.feature009
    def test_score_rsi_neutral(self):
        """Test RSI neutral gives zero score."""
        from stockagent.analysis import score_rsi

        assert score_rsi(50.0) == 0.0
        assert score_rsi(45.0) == 0.0

    @pytest.mark.feature009
    def test_score_rsi_overbought(self):
        """Test RSI overbought gives negative score."""
        from stockagent.analysis import score_rsi

        assert score_rsi(75.0) == -20.0
        assert score_rsi(85.0) == -20.0

    @pytest.mark.feature009
    def test_score_rsi_none(self):
        """Test RSI None gives zero score."""
        from stockagent.analysis import score_rsi

        assert score_rsi(None) == 0.0


class TestScoreMACD:
    """Test MACD scoring function."""

    @pytest.mark.feature009
    def test_score_macd_strong_bullish(self):
        """Test MACD strong bullish gives max positive score."""
        from stockagent.analysis import score_macd

        macd = {"histogram": 1.0, "macd_line": 1.0}
        assert score_macd(macd) == 25.0

    @pytest.mark.feature009
    def test_score_macd_bullish(self):
        """Test MACD bullish gives positive score."""
        from stockagent.analysis import score_macd

        macd = {"histogram": 1.0, "macd_line": -0.5}
        assert score_macd(macd) == 15.0

    @pytest.mark.feature009
    def test_score_macd_strong_bearish(self):
        """Test MACD strong bearish gives max negative score."""
        from stockagent.analysis import score_macd

        macd = {"histogram": -1.0, "macd_line": -1.0}
        assert score_macd(macd) == -25.0

    @pytest.mark.feature009
    def test_score_macd_bearish(self):
        """Test MACD bearish gives negative score."""
        from stockagent.analysis import score_macd

        macd = {"histogram": -1.0, "macd_line": 0.5}
        assert score_macd(macd) == -15.0

    @pytest.mark.feature009
    def test_score_macd_none(self):
        """Test MACD None gives zero score."""
        from stockagent.analysis import score_macd

        assert score_macd(None) == 0.0


class TestScoreMovingAverages:
    """Test moving average scoring function."""

    @pytest.mark.feature009
    def test_score_ma_strong_uptrend(self):
        """Test strong uptrend gives max positive score."""
        from stockagent.analysis import score_moving_averages

        signals = {
            "current_price": 150.0,
            "sma_20": 145.0,
            "sma_50": 140.0,
            "sma_200": 130.0,
        }
        assert score_moving_averages(signals) == 20.0

    @pytest.mark.feature009
    def test_score_ma_strong_downtrend(self):
        """Test strong downtrend gives max negative score."""
        from stockagent.analysis import score_moving_averages

        signals = {
            "current_price": 100.0,
            "sma_20": 110.0,
            "sma_50": 120.0,
            "sma_200": 130.0,
        }
        assert score_moving_averages(signals) == -20.0

    @pytest.mark.feature009
    def test_score_ma_missing_data(self):
        """Test missing data gives zero score."""
        from stockagent.analysis import score_moving_averages

        assert score_moving_averages({}) == 0.0


class TestScoreBollinger:
    """Test Bollinger scoring function."""

    @pytest.mark.feature009
    def test_score_bollinger_near_lower(self):
        """Test price near lower band gives positive score."""
        from stockagent.analysis import score_bollinger

        bollinger = {"upper": 110.0, "middle": 100.0, "lower": 90.0}
        assert score_bollinger(bollinger, 91.0) == 15.0

    @pytest.mark.feature009
    def test_score_bollinger_near_upper(self):
        """Test price near upper band gives negative score."""
        from stockagent.analysis import score_bollinger

        bollinger = {"upper": 110.0, "middle": 100.0, "lower": 90.0}
        assert score_bollinger(bollinger, 109.0) == -15.0

    @pytest.mark.feature009
    def test_score_bollinger_middle(self):
        """Test price at middle gives zero score."""
        from stockagent.analysis import score_bollinger

        bollinger = {"upper": 110.0, "middle": 100.0, "lower": 90.0}
        assert score_bollinger(bollinger, 100.0) == 0.0

    @pytest.mark.feature009
    def test_score_bollinger_none(self):
        """Test None Bollinger gives zero score."""
        from stockagent.analysis import score_bollinger

        assert score_bollinger(None, 100.0) == 0.0


class TestScoreSentiment:
    """Test sentiment scoring function."""

    @pytest.mark.feature009
    def test_score_sentiment_positive(self):
        """Test positive sentiment gives positive score."""
        from stockagent.analysis import score_sentiment

        sentiment = {"overall_score": 0.5}
        assert score_sentiment(sentiment) == 10.0

    @pytest.mark.feature009
    def test_score_sentiment_negative(self):
        """Test negative sentiment gives negative score."""
        from stockagent.analysis import score_sentiment

        sentiment = {"overall_score": -0.5}
        assert score_sentiment(sentiment) == -10.0

    @pytest.mark.feature009
    def test_score_sentiment_max(self):
        """Test max sentiment gives max score."""
        from stockagent.analysis import score_sentiment

        sentiment = {"overall_score": 1.0}
        assert score_sentiment(sentiment) == 20.0

    @pytest.mark.feature009
    def test_score_sentiment_none(self):
        """Test None sentiment gives zero score."""
        from stockagent.analysis import score_sentiment

        assert score_sentiment(None) == 0.0


class TestCompositeScore:
    """Test composite score calculation."""

    @pytest.mark.feature009
    def test_composite_score_bounds(self):
        """Test composite score is within bounds."""
        from stockagent.analysis import calculate_composite_score

        score = calculate_composite_score({}, {})
        assert -100 <= score <= 100

    @pytest.mark.feature009
    def test_composite_score_deterministic(self):
        """Test same inputs give same output."""
        from stockagent.analysis import calculate_composite_score

        technical = {"rsi": 50.0}
        sentiment = {"overall_score": 0.0}

        score1 = calculate_composite_score(technical, sentiment)
        score2 = calculate_composite_score(technical, sentiment)
        score3 = calculate_composite_score(technical, sentiment)

        assert score1 == score2 == score3

    @pytest.mark.feature009
    def test_composite_score_clamped(self):
        """Test composite score is clamped to bounds."""
        from stockagent.analysis import calculate_composite_score

        # Even with extreme values
        technical = {"rsi": 0.0}
        sentiment = {"overall_score": 10.0}  # Invalid but tests clamping

        score = calculate_composite_score(technical, sentiment)
        assert score <= 100.0


class TestGenerateRecommendation:
    """Test recommendation generation."""

    @pytest.mark.feature009
    def test_strong_buy_threshold(self):
        """Test score > 60 gives STRONG BUY."""
        from stockagent.analysis import generate_recommendation

        rec, conf = generate_recommendation(70.0)
        assert rec == "STRONG BUY"
        assert conf == 70.0

    @pytest.mark.feature009
    def test_buy_threshold(self):
        """Test score 20-60 gives BUY."""
        from stockagent.analysis import generate_recommendation

        rec, _ = generate_recommendation(40.0)
        assert rec == "BUY"

    @pytest.mark.feature009
    def test_hold_threshold(self):
        """Test score -20 to 20 gives HOLD."""
        from stockagent.analysis import generate_recommendation

        rec, _ = generate_recommendation(0.0)
        assert rec == "HOLD"

    @pytest.mark.feature009
    def test_sell_threshold(self):
        """Test score -60 to -20 gives SELL."""
        from stockagent.analysis import generate_recommendation

        rec, _ = generate_recommendation(-40.0)
        assert rec == "SELL"

    @pytest.mark.feature009
    def test_strong_sell_threshold(self):
        """Test score < -60 gives STRONG SELL."""
        from stockagent.analysis import generate_recommendation

        rec, _ = generate_recommendation(-70.0)
        assert rec == "STRONG SELL"

    @pytest.mark.feature009
    def test_confidence_equals_abs_score(self):
        """Test confidence equals abs(score)."""
        from stockagent.analysis import generate_recommendation

        _, conf = generate_recommendation(65.0)
        assert conf == 65.0

        _, conf = generate_recommendation(-45.0)
        assert conf == 45.0


class TestExplanationFactors:
    """Test explanation factors generation."""

    @pytest.mark.feature009
    def test_returns_list(self):
        """Test returns list of strings."""
        from stockagent.analysis import get_explanation_factors

        factors = get_explanation_factors({"rsi": 25.0}, {})
        assert isinstance(factors, list)
        assert all(isinstance(f, str) for f in factors)

    @pytest.mark.feature009
    def test_empty_for_neutral(self):
        """Test empty list for neutral signals."""
        from stockagent.analysis import get_explanation_factors

        factors = get_explanation_factors({"rsi": 50.0}, {"overall_score": 0.0})
        assert factors == []

    @pytest.mark.feature009
    def test_includes_contributing_factors(self):
        """Test includes factors that contribute to score."""
        from stockagent.analysis import get_explanation_factors

        factors = get_explanation_factors({"rsi": 25.0}, {})
        assert len(factors) > 0
        assert any("RSI" in f for f in factors)
