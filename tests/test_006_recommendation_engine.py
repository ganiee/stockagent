"""Tests for Feature 006: Recommendation Engine."""

from unittest.mock import MagicMock, patch

import pytest


class TestScoringImports:
    """Test that scoring functions can be imported."""

    @pytest.mark.feature006
    def test_calculate_composite_score_import(self):
        """Test that calculate_composite_score can be imported."""
        from stockagent.analysis.scoring import calculate_composite_score

        assert calculate_composite_score is not None

    @pytest.mark.feature006
    def test_generate_recommendation_import(self):
        """Test that generate_recommendation can be imported."""
        from stockagent.analysis.scoring import generate_recommendation

        assert generate_recommendation is not None

    @pytest.mark.feature006
    def test_get_explanation_factors_import(self):
        """Test that get_explanation_factors can be imported."""
        from stockagent.analysis.scoring import get_explanation_factors

        assert get_explanation_factors is not None

    @pytest.mark.feature006
    def test_individual_scoring_functions_import(self):
        """Test that individual scoring functions can be imported."""
        from stockagent.analysis.scoring import (
            score_bollinger,
            score_macd,
            score_moving_averages,
            score_rsi,
            score_sentiment,
        )

        assert score_rsi is not None
        assert score_macd is not None
        assert score_moving_averages is not None
        assert score_bollinger is not None
        assert score_sentiment is not None

    @pytest.mark.feature006
    def test_imports_from_analysis_package(self):
        """Test that scoring functions can be imported from analysis package."""
        from stockagent.analysis import (
            calculate_composite_score,
            generate_recommendation,
            get_explanation_factors,
        )

        assert calculate_composite_score is not None
        assert generate_recommendation is not None
        assert get_explanation_factors is not None


class TestRSIScoring:
    """Test RSI scoring function."""

    @pytest.mark.feature006
    def test_rsi_oversold_bullish(self):
        """Test RSI < 30 returns positive score (bullish)."""
        from stockagent.analysis.scoring import score_rsi

        score = score_rsi(25.0)
        assert score > 0
        assert score == 20.0  # Max bullish RSI score

    @pytest.mark.feature006
    def test_rsi_slightly_oversold(self):
        """Test RSI 30-40 returns slightly positive score."""
        from stockagent.analysis.scoring import score_rsi

        score = score_rsi(35.0)
        assert score > 0
        assert score == 10.0

    @pytest.mark.feature006
    def test_rsi_neutral(self):
        """Test RSI 40-60 returns zero score (neutral)."""
        from stockagent.analysis.scoring import score_rsi

        assert score_rsi(50.0) == 0.0
        assert score_rsi(40.0) == 0.0
        assert score_rsi(60.0) == 0.0

    @pytest.mark.feature006
    def test_rsi_slightly_overbought(self):
        """Test RSI 60-70 returns slightly negative score."""
        from stockagent.analysis.scoring import score_rsi

        score = score_rsi(65.0)
        assert score < 0
        assert score == -10.0

    @pytest.mark.feature006
    def test_rsi_overbought_bearish(self):
        """Test RSI > 70 returns negative score (bearish)."""
        from stockagent.analysis.scoring import score_rsi

        score = score_rsi(75.0)
        assert score < 0
        assert score == -20.0  # Max bearish RSI score

    @pytest.mark.feature006
    def test_rsi_none_returns_zero(self):
        """Test RSI None returns zero score."""
        from stockagent.analysis.scoring import score_rsi

        assert score_rsi(None) == 0.0


class TestMACDScoring:
    """Test MACD scoring function."""

    @pytest.mark.feature006
    def test_macd_strong_bullish(self):
        """Test positive histogram + positive MACD line → strong bullish."""
        from stockagent.analysis.scoring import score_macd

        macd = {"histogram": 1.5, "macd_line": 2.0, "signal_line": 0.5}
        score = score_macd(macd)
        assert score > 0
        assert score == 25.0  # Max bullish MACD score

    @pytest.mark.feature006
    def test_macd_bullish(self):
        """Test positive histogram → bullish."""
        from stockagent.analysis.scoring import score_macd

        macd = {"histogram": 1.5, "macd_line": -0.5, "signal_line": -2.0}
        score = score_macd(macd)
        assert score > 0
        assert score == 15.0

    @pytest.mark.feature006
    def test_macd_bearish(self):
        """Test negative histogram → bearish."""
        from stockagent.analysis.scoring import score_macd

        macd = {"histogram": -1.5, "macd_line": 0.5, "signal_line": 2.0}
        score = score_macd(macd)
        assert score < 0
        assert score == -15.0

    @pytest.mark.feature006
    def test_macd_strong_bearish(self):
        """Test negative histogram + negative MACD line → strong bearish."""
        from stockagent.analysis.scoring import score_macd

        macd = {"histogram": -1.5, "macd_line": -2.0, "signal_line": -0.5}
        score = score_macd(macd)
        assert score < 0
        assert score == -25.0  # Max bearish MACD score

    @pytest.mark.feature006
    def test_macd_zero_histogram(self):
        """Test zero histogram returns zero score."""
        from stockagent.analysis.scoring import score_macd

        macd = {"histogram": 0.0, "macd_line": 1.0, "signal_line": 1.0}
        assert score_macd(macd) == 0.0

    @pytest.mark.feature006
    def test_macd_none_returns_zero(self):
        """Test MACD None returns zero score."""
        from stockagent.analysis.scoring import score_macd

        assert score_macd(None) == 0.0


class TestMovingAverageScoring:
    """Test moving average scoring function."""

    @pytest.mark.feature006
    def test_strong_uptrend(self):
        """Test price > SMA-20 > SMA-50 > SMA-200 → strong uptrend."""
        from stockagent.analysis.scoring import score_moving_averages

        signals = {
            "current_price": 150.0,
            "sma_20": 145.0,
            "sma_50": 140.0,
            "sma_200": 130.0,
        }
        score = score_moving_averages(signals)
        assert score == 20.0  # Max bullish MA score

    @pytest.mark.feature006
    def test_moderate_uptrend(self):
        """Test price above SMA-20 and SMA-50 → moderate uptrend."""
        from stockagent.analysis.scoring import score_moving_averages

        signals = {
            "current_price": 150.0,
            "sma_20": 145.0,
            "sma_50": 140.0,
            "sma_200": 160.0,  # Not in alignment
        }
        score = score_moving_averages(signals)
        assert score == 10.0

    @pytest.mark.feature006
    def test_strong_downtrend(self):
        """Test price < SMA-20 < SMA-50 < SMA-200 → strong downtrend."""
        from stockagent.analysis.scoring import score_moving_averages

        signals = {
            "current_price": 100.0,
            "sma_20": 110.0,
            "sma_50": 120.0,
            "sma_200": 130.0,
        }
        score = score_moving_averages(signals)
        assert score == -20.0  # Max bearish MA score

    @pytest.mark.feature006
    def test_moderate_downtrend(self):
        """Test price below SMA-20 and SMA-50 → moderate downtrend."""
        from stockagent.analysis.scoring import score_moving_averages

        signals = {
            "current_price": 100.0,
            "sma_20": 110.0,
            "sma_50": 120.0,
            "sma_200": 90.0,  # Not in alignment
        }
        score = score_moving_averages(signals)
        assert score == -10.0

    @pytest.mark.feature006
    def test_no_sma_data(self):
        """Test missing SMA data returns zero."""
        from stockagent.analysis.scoring import score_moving_averages

        signals = {"current_price": 100.0}
        assert score_moving_averages(signals) == 0.0

    @pytest.mark.feature006
    def test_no_price(self):
        """Test missing price returns zero."""
        from stockagent.analysis.scoring import score_moving_averages

        signals = {"sma_20": 100.0, "sma_50": 95.0}
        assert score_moving_averages(signals) == 0.0


class TestBollingerScoring:
    """Test Bollinger Bands scoring function."""

    @pytest.mark.feature006
    def test_price_near_lower_band(self):
        """Test price near lower band → bullish (potential bounce)."""
        from stockagent.analysis.scoring import score_bollinger

        bollinger = {"upper": 110.0, "middle": 100.0, "lower": 90.0}
        score = score_bollinger(bollinger, 91.0)  # Near lower band
        assert score > 0
        assert score == 15.0  # Max bullish Bollinger score

    @pytest.mark.feature006
    def test_price_near_upper_band(self):
        """Test price near upper band → bearish (potential pullback)."""
        from stockagent.analysis.scoring import score_bollinger

        bollinger = {"upper": 110.0, "middle": 100.0, "lower": 90.0}
        score = score_bollinger(bollinger, 109.0)  # Near upper band
        assert score < 0
        assert score == -15.0  # Max bearish Bollinger score

    @pytest.mark.feature006
    def test_price_in_middle(self):
        """Test price in middle of bands → neutral."""
        from stockagent.analysis.scoring import score_bollinger

        bollinger = {"upper": 110.0, "middle": 100.0, "lower": 90.0}
        score = score_bollinger(bollinger, 100.0)  # At middle
        assert score == 0.0

    @pytest.mark.feature006
    def test_bollinger_none_returns_zero(self):
        """Test Bollinger None returns zero score."""
        from stockagent.analysis.scoring import score_bollinger

        assert score_bollinger(None, 100.0) == 0.0

    @pytest.mark.feature006
    def test_price_zero_returns_zero(self):
        """Test price zero returns zero score."""
        from stockagent.analysis.scoring import score_bollinger

        bollinger = {"upper": 110.0, "middle": 100.0, "lower": 90.0}
        assert score_bollinger(bollinger, 0.0) == 0.0


class TestSentimentScoring:
    """Test sentiment scoring function."""

    @pytest.mark.feature006
    def test_positive_sentiment(self):
        """Test positive sentiment → positive score."""
        from stockagent.analysis.scoring import score_sentiment

        sentiment = {"overall_score": 0.8, "overall_label": "positive"}
        score = score_sentiment(sentiment)
        assert score > 0
        assert score == 16.0  # 0.8 * 20

    @pytest.mark.feature006
    def test_negative_sentiment(self):
        """Test negative sentiment → negative score."""
        from stockagent.analysis.scoring import score_sentiment

        sentiment = {"overall_score": -0.5, "overall_label": "negative"}
        score = score_sentiment(sentiment)
        assert score < 0
        assert score == -10.0  # -0.5 * 20

    @pytest.mark.feature006
    def test_neutral_sentiment(self):
        """Test neutral sentiment → zero score."""
        from stockagent.analysis.scoring import score_sentiment

        sentiment = {"overall_score": 0.0, "overall_label": "neutral"}
        assert score_sentiment(sentiment) == 0.0

    @pytest.mark.feature006
    def test_max_positive_sentiment(self):
        """Test max positive sentiment → max score."""
        from stockagent.analysis.scoring import score_sentiment

        sentiment = {"overall_score": 1.0, "overall_label": "positive"}
        assert score_sentiment(sentiment) == 20.0

    @pytest.mark.feature006
    def test_max_negative_sentiment(self):
        """Test max negative sentiment → min score."""
        from stockagent.analysis.scoring import score_sentiment

        sentiment = {"overall_score": -1.0, "overall_label": "negative"}
        assert score_sentiment(sentiment) == -20.0

    @pytest.mark.feature006
    def test_sentiment_none_returns_zero(self):
        """Test sentiment None returns zero score."""
        from stockagent.analysis.scoring import score_sentiment

        assert score_sentiment(None) == 0.0


class TestCompositeScore:
    """Test composite score calculation."""

    @pytest.mark.feature006
    def test_all_bullish_signals(self):
        """Test all bullish signals → high positive score."""
        from stockagent.analysis.scoring import calculate_composite_score

        technical = {
            "rsi": 25.0,  # Oversold → +20
            "macd": {"histogram": 1.0, "macd_line": 1.0},  # Strong bullish → +25
            "current_price": 150.0,
            "sma_20": 145.0,
            "sma_50": 140.0,
            "sma_200": 130.0,  # Strong uptrend → +20
            "bollinger": {"upper": 160.0, "middle": 150.0, "lower": 140.0},  # Price in middle → 0
        }
        sentiment = {"overall_score": 1.0}  # Max positive → +20

        score = calculate_composite_score(technical, sentiment)
        # RSI: +20, MACD: +25, MA: +20, Bollinger: 0, Sentiment: +20 = 85
        assert score > 50
        assert score <= 100.0

    @pytest.mark.feature006
    def test_all_bearish_signals(self):
        """Test all bearish signals → high negative score."""
        from stockagent.analysis.scoring import calculate_composite_score

        technical = {
            "rsi": 80.0,  # Overbought → -20
            "macd": {"histogram": -1.0, "macd_line": -1.0},  # Strong bearish → -25
            "current_price": 100.0,
            "sma_20": 110.0,
            "sma_50": 120.0,
            "sma_200": 130.0,  # Strong downtrend → -20
            "bollinger": {"upper": 105.0, "middle": 100.0, "lower": 95.0},  # Price in middle → 0
        }
        sentiment = {"overall_score": -1.0}  # Max negative → -20

        score = calculate_composite_score(technical, sentiment)
        # RSI: -20, MACD: -25, MA: -20, Bollinger: 0, Sentiment: -20 = -85
        assert score < -50
        assert score >= -100.0

    @pytest.mark.feature006
    def test_mixed_signals_near_zero(self):
        """Test mixed signals → score near zero."""
        from stockagent.analysis.scoring import calculate_composite_score

        technical = {
            "rsi": 50.0,  # Neutral → 0
            "macd": {"histogram": 0.0, "macd_line": 0.0},  # Neutral → 0
            "current_price": 100.0,
            "sma_20": 100.0,
            "sma_50": 100.0,
            "sma_200": 100.0,
        }
        sentiment = {"overall_score": 0.0}  # Neutral → 0

        score = calculate_composite_score(technical, sentiment)
        assert -20 <= score <= 20

    @pytest.mark.feature006
    def test_score_clamped_to_100(self):
        """Test score is clamped to max 100."""
        from stockagent.analysis.scoring import calculate_composite_score

        # Even with extreme values, score should not exceed 100
        technical = {"rsi": 0.0}  # Would give more than max
        sentiment = {"overall_score": 5.0}  # Invalid but tests clamping

        score = calculate_composite_score(technical, sentiment)
        assert score <= 100.0

    @pytest.mark.feature006
    def test_score_clamped_to_minus_100(self):
        """Test score is clamped to min -100."""
        from stockagent.analysis.scoring import calculate_composite_score

        technical = {"rsi": 100.0}
        sentiment = {"overall_score": -5.0}  # Invalid but tests clamping

        score = calculate_composite_score(technical, sentiment)
        assert score >= -100.0

    @pytest.mark.feature006
    def test_deterministic(self):
        """Test same inputs always produce same output."""
        from stockagent.analysis.scoring import calculate_composite_score

        technical = {"rsi": 45.0, "macd": {"histogram": 0.5, "macd_line": 0.3}}
        sentiment = {"overall_score": 0.2}

        score1 = calculate_composite_score(technical, sentiment)
        score2 = calculate_composite_score(technical, sentiment)
        score3 = calculate_composite_score(technical, sentiment)

        assert score1 == score2 == score3

    @pytest.mark.feature006
    def test_empty_inputs(self):
        """Test empty inputs don't crash."""
        from stockagent.analysis.scoring import calculate_composite_score

        score = calculate_composite_score({}, {})
        assert score == 0.0


class TestGenerateRecommendation:
    """Test recommendation generation from score."""

    @pytest.mark.feature006
    def test_strong_buy_threshold(self):
        """Test score > 60 → STRONG BUY."""
        from stockagent.analysis.scoring import generate_recommendation

        rec, conf = generate_recommendation(80.0)
        assert rec == "STRONG BUY"
        assert conf == 80.0

    @pytest.mark.feature006
    def test_buy_threshold(self):
        """Test score 20-60 → BUY."""
        from stockagent.analysis.scoring import generate_recommendation

        rec, conf = generate_recommendation(40.0)
        assert rec == "BUY"
        assert conf == 40.0

    @pytest.mark.feature006
    def test_hold_threshold(self):
        """Test score -20 to 20 → HOLD."""
        from stockagent.analysis.scoring import generate_recommendation

        rec, conf = generate_recommendation(0.0)
        assert rec == "HOLD"
        assert conf == 0.0

        rec, conf = generate_recommendation(15.0)
        assert rec == "HOLD"
        assert conf == 15.0

        rec, conf = generate_recommendation(-15.0)
        assert rec == "HOLD"
        assert conf == 15.0

    @pytest.mark.feature006
    def test_sell_threshold(self):
        """Test score -60 to -20 → SELL."""
        from stockagent.analysis.scoring import generate_recommendation

        rec, conf = generate_recommendation(-40.0)
        assert rec == "SELL"
        assert conf == 40.0

    @pytest.mark.feature006
    def test_strong_sell_threshold(self):
        """Test score < -60 → STRONG SELL."""
        from stockagent.analysis.scoring import generate_recommendation

        rec, conf = generate_recommendation(-80.0)
        assert rec == "STRONG SELL"
        assert conf == 80.0

    @pytest.mark.feature006
    def test_confidence_is_abs_score(self):
        """Test confidence equals absolute value of score."""
        from stockagent.analysis.scoring import generate_recommendation

        _, conf = generate_recommendation(75.0)
        assert conf == 75.0

        _, conf = generate_recommendation(-60.0)
        assert conf == 60.0

    @pytest.mark.feature006
    def test_confidence_capped_at_100(self):
        """Test confidence is capped at 100."""
        from stockagent.analysis.scoring import generate_recommendation

        _, conf = generate_recommendation(100.0)
        assert conf == 100.0

    @pytest.mark.feature006
    def test_boundary_values(self):
        """Test exact boundary values."""
        from stockagent.analysis.scoring import generate_recommendation

        # Exactly at boundaries
        rec, _ = generate_recommendation(60.0)
        assert rec == "BUY"  # 60 is not > 60

        rec, _ = generate_recommendation(60.1)
        assert rec == "STRONG BUY"

        rec, _ = generate_recommendation(20.0)
        assert rec == "HOLD"  # 20 is not > 20

        rec, _ = generate_recommendation(20.1)
        assert rec == "BUY"

        rec, _ = generate_recommendation(-20.0)
        assert rec == "HOLD"  # -20 is >= -20

        rec, _ = generate_recommendation(-20.1)
        assert rec == "SELL"

        rec, _ = generate_recommendation(-60.0)
        assert rec == "SELL"  # -60 is >= -60

        rec, _ = generate_recommendation(-60.1)
        assert rec == "STRONG SELL"


class TestExplanationFactors:
    """Test explanation factor generation."""

    @pytest.mark.feature006
    def test_returns_list_of_strings(self):
        """Test returns list of strings."""
        from stockagent.analysis.scoring import get_explanation_factors

        technical = {"rsi": 25.0}
        sentiment = {"overall_score": 0.5}

        factors = get_explanation_factors(technical, sentiment)
        assert isinstance(factors, list)
        assert all(isinstance(f, str) for f in factors)

    @pytest.mark.feature006
    def test_includes_rsi_factor(self):
        """Test includes RSI explanation when present."""
        from stockagent.analysis.scoring import get_explanation_factors

        technical = {"rsi": 25.0}
        factors = get_explanation_factors(technical, {})

        assert len(factors) > 0
        assert any("RSI" in f for f in factors)
        assert any("oversold" in f.lower() or "bullish" in f.lower() for f in factors)

    @pytest.mark.feature006
    def test_includes_macd_factor(self):
        """Test includes MACD explanation when present."""
        from stockagent.analysis.scoring import get_explanation_factors

        technical = {"macd": {"histogram": 1.5, "macd_line": 2.0}}
        factors = get_explanation_factors(technical, {})

        assert len(factors) > 0
        assert any("MACD" in f for f in factors)

    @pytest.mark.feature006
    def test_includes_sentiment_factor(self):
        """Test includes sentiment explanation when present."""
        from stockagent.analysis.scoring import get_explanation_factors

        sentiment = {
            "overall_score": 0.7,
            "overall_label": "positive",
            "headline_count": 5,
        }
        factors = get_explanation_factors({}, sentiment)

        assert len(factors) > 0
        assert any("sentiment" in f.lower() for f in factors)

    @pytest.mark.feature006
    def test_sorted_by_contribution(self):
        """Test factors are sorted by absolute contribution."""
        from stockagent.analysis.scoring import get_explanation_factors

        # MACD has highest weight (25), then RSI (20)
        technical = {
            "rsi": 25.0,  # +20 contribution
            "macd": {"histogram": 1.5, "macd_line": 2.0},  # +25 contribution
        }
        factors = get_explanation_factors(technical, {})

        assert len(factors) >= 2
        # MACD should come first (higher contribution)
        assert "MACD" in factors[0]
        assert "RSI" in factors[1]

    @pytest.mark.feature006
    def test_empty_inputs_return_empty_list(self):
        """Test empty inputs return empty list."""
        from stockagent.analysis.scoring import get_explanation_factors

        factors = get_explanation_factors({}, {})
        assert factors == []

    @pytest.mark.feature006
    def test_neutral_signals_not_included(self):
        """Test neutral signals are not included in factors."""
        from stockagent.analysis.scoring import get_explanation_factors

        technical = {"rsi": 50.0}  # Neutral RSI
        sentiment = {"overall_score": 0.0}  # Neutral sentiment

        factors = get_explanation_factors(technical, sentiment)
        assert factors == []


class TestWorkflowIntegration:
    """Test integration with workflow recommend node."""

    @pytest.mark.feature006
    def test_recommend_returns_real_recommendation(self):
        """Test workflow recommend returns real recommendation."""
        from stockagent.graph.workflow import recommend

        state = {
            "ticker": "AAPL",
            "technical_signals": {
                "rsi": 25.0,
                "macd": {"histogram": 1.5, "macd_line": 2.0, "signal_line": 0.5},
                "current_price": 150.0,
                "sma_20": 145.0,
            },
            "news_sentiment": {
                "overall_score": 0.5,
                "overall_label": "positive",
                "headline_count": 3,
            },
            "errors": [],
        }

        result = recommend(state)

        assert "recommendation" in result
        assert result["recommendation"] in ["STRONG BUY", "BUY", "HOLD", "SELL", "STRONG SELL"]
        assert "confidence" in result
        assert 0 <= result["confidence"] <= 100
        assert "explanation_factors" in result
        assert isinstance(result["explanation_factors"], list)

    @pytest.mark.feature006
    def test_recommend_not_placeholder(self):
        """Test workflow recommend is not returning placeholder."""
        from stockagent.graph.workflow import recommend

        # With bullish signals, should not return HOLD with 50% confidence
        state = {
            "technical_signals": {
                "rsi": 20.0,
                "macd": {"histogram": 2.0, "macd_line": 3.0},
                "current_price": 150.0,
                "sma_20": 140.0,
                "sma_50": 130.0,
                "sma_200": 120.0,
            },
            "news_sentiment": {"overall_score": 0.8},
            "errors": [],
        }

        result = recommend(state)

        # Should be BUY or STRONG BUY, not HOLD
        assert result["recommendation"] in ["BUY", "STRONG BUY"]
        # Confidence should not be exactly 50.0 (placeholder value)
        assert result["confidence"] != 50.0

    @pytest.mark.feature006
    def test_run_analysis_returns_real_recommendation(self):
        """Test run_analysis returns real recommendation."""
        from stockagent.graph import run_analysis

        mock_client = MagicMock()
        mock_client.get_stock_aggregates.return_value = [
            {"close": 100 + i * 0.5} for i in range(100)
        ]
        mock_client.get_ticker_details.return_value = {"company_name": "Test Corp", "sector": "Tech"}
        mock_client.get_previous_close.return_value = {"previous_close": 149.0, "current_price": 150.0}

        mock_sentiment = {
            "overall_score": 0.3,
            "overall_label": "positive",
            "headlines": [],
            "headline_count": 0,
        }

        with patch("stockagent.graph.workflow.PolygonClient", return_value=mock_client):
            with patch("stockagent.graph.workflow.analyze_news_sentiment", return_value=mock_sentiment):
                result = run_analysis("TEST")

                assert result["recommendation"] in ["STRONG BUY", "BUY", "HOLD", "SELL", "STRONG SELL"]
                assert "confidence" in result
                assert "explanation_factors" in result

    @pytest.mark.feature006
    def test_recommend_handles_missing_data(self):
        """Test recommend handles missing technical/sentiment data."""
        from stockagent.graph.workflow import recommend

        state = {
            "technical_signals": {},
            "news_sentiment": {},
            "errors": [],
        }

        result = recommend(state)

        # Should return HOLD for neutral/missing data
        assert result["recommendation"] == "HOLD"
        assert result["confidence"] == 0.0

    @pytest.mark.feature006
    def test_recommend_handles_error(self):
        """Test recommend handles errors gracefully."""
        from stockagent.graph.workflow import recommend

        # Pass invalid data that might cause errors
        state = {
            "technical_signals": None,
            "news_sentiment": None,
            "errors": [],
        }

        # Should not crash
        result = recommend(state)
        assert "recommendation" in result


class TestEndToEnd:
    """End-to-end tests for the recommendation engine."""

    @pytest.mark.feature006
    def test_bullish_scenario(self):
        """Test complete bullish scenario."""
        from stockagent.analysis.scoring import (
            calculate_composite_score,
            generate_recommendation,
            get_explanation_factors,
        )

        technical = {
            "rsi": 28.0,
            "macd": {"histogram": 0.8, "macd_line": 1.2, "signal_line": 0.4},
            "current_price": 155.0,
            "sma_20": 150.0,
            "sma_50": 145.0,
            "sma_200": 135.0,
            "bollinger": {"upper": 165.0, "middle": 150.0, "lower": 135.0},
        }
        sentiment = {
            "overall_score": 0.6,
            "overall_label": "positive",
            "headline_count": 5,
        }

        score = calculate_composite_score(technical, sentiment)
        recommendation, confidence = generate_recommendation(score)
        factors = get_explanation_factors(technical, sentiment)

        assert score > 50
        assert recommendation in ["BUY", "STRONG BUY"]
        assert confidence > 50
        assert len(factors) > 0

    @pytest.mark.feature006
    def test_bearish_scenario(self):
        """Test complete bearish scenario."""
        from stockagent.analysis.scoring import (
            calculate_composite_score,
            generate_recommendation,
            get_explanation_factors,
        )

        technical = {
            "rsi": 78.0,
            "macd": {"histogram": -1.2, "macd_line": -0.8, "signal_line": 0.4},
            "current_price": 95.0,
            "sma_20": 100.0,
            "sma_50": 105.0,
            "sma_200": 115.0,
            "bollinger": {"upper": 105.0, "middle": 100.0, "lower": 95.0},
        }
        sentiment = {
            "overall_score": -0.5,
            "overall_label": "negative",
            "headline_count": 4,
        }

        score = calculate_composite_score(technical, sentiment)
        recommendation, confidence = generate_recommendation(score)
        factors = get_explanation_factors(technical, sentiment)

        assert score < -50
        assert recommendation in ["SELL", "STRONG SELL"]
        assert confidence > 50
        assert len(factors) > 0
