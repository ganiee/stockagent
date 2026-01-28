"""Unit tests for sentiment analysis."""

import pytest


class TestAnalyzeSentiment:
    """Test headline sentiment analysis."""

    @pytest.mark.feature009
    def test_positive_headline(self):
        """Test positive headline gets positive score."""
        from stockagent.analysis import analyze_sentiment

        result = analyze_sentiment("Stock surges to record high on strong earnings")
        assert result["score"] > 0
        assert result["label"] == "positive"

    @pytest.mark.feature009
    def test_negative_headline(self):
        """Test negative headline gets negative score."""
        from stockagent.analysis import analyze_sentiment

        result = analyze_sentiment("Company reports massive losses and layoffs")
        assert result["score"] < 0
        assert result["label"] == "negative"

    @pytest.mark.feature009
    def test_neutral_headline(self):
        """Test neutral headline gets near-zero score."""
        from stockagent.analysis import analyze_sentiment

        result = analyze_sentiment("Company announces quarterly results")
        assert -0.3 <= result["score"] <= 0.3

    @pytest.mark.feature009
    def test_score_bounds(self):
        """Test score is always between -1 and 1."""
        from stockagent.analysis import analyze_sentiment

        # Very positive
        result = analyze_sentiment("surge growth profit record high beat strong")
        assert -1.0 <= result["score"] <= 1.0

        # Very negative
        result = analyze_sentiment("crash loss decline plunge drop fail")
        assert -1.0 <= result["score"] <= 1.0

    @pytest.mark.feature009
    def test_empty_headline(self):
        """Test empty headline returns neutral."""
        from stockagent.analysis import analyze_sentiment

        result = analyze_sentiment("")
        assert result["score"] == 0.0
        assert result["label"] == "neutral"

    @pytest.mark.feature009
    def test_case_insensitive(self):
        """Test analysis is case insensitive."""
        from stockagent.analysis import analyze_sentiment

        result_lower = analyze_sentiment("stock surges")
        result_upper = analyze_sentiment("STOCK SURGES")

        assert result_lower["score"] == result_upper["score"]


class TestAnalyzeNewsSentiment:
    """Test aggregate news sentiment analysis."""

    @pytest.mark.feature009
    def test_returns_correct_structure(self):
        """Test returns correct structure."""
        from unittest.mock import patch

        from stockagent.analysis import analyze_news_sentiment

        mock_headlines = [
            {"title": "Good news", "url": "http://test.com", "date": "2024-01-01"}
        ]

        with patch("stockagent.analysis.news_sentiment.fetch_news", return_value=mock_headlines):
            result = analyze_news_sentiment("TEST", "Test Company")

            assert "overall_score" in result
            assert "overall_label" in result
            assert "headlines" in result
            assert "headline_count" in result

    @pytest.mark.feature009
    def test_overall_score_bounds(self):
        """Test overall score is within bounds."""
        from unittest.mock import patch

        from stockagent.analysis import analyze_news_sentiment

        mock_headlines = [
            {"title": "Great earnings beat expectations", "url": "", "date": ""},
            {"title": "Stock price rises", "url": "", "date": ""},
        ]

        with patch("stockagent.analysis.news_sentiment.fetch_news", return_value=mock_headlines):
            result = analyze_news_sentiment("TEST", "Test Company")
            assert -1.0 <= result["overall_score"] <= 1.0

    @pytest.mark.feature009
    def test_no_headlines_returns_neutral(self):
        """Test no headlines returns neutral."""
        from unittest.mock import patch

        from stockagent.analysis import analyze_news_sentiment

        with patch("stockagent.analysis.news_sentiment.fetch_news", return_value=[]):
            result = analyze_news_sentiment("TEST", "Test Company")
            assert result["overall_label"] == "neutral"
            assert result["headline_count"] == 0


class TestSentimentKeywords:
    """Test sentiment keyword detection."""

    @pytest.mark.feature009
    def test_positive_keywords(self):
        """Test positive keywords are detected."""
        from stockagent.analysis import analyze_sentiment

        positive_words = ["surge", "growth", "profit", "beat", "upgrade"]
        for word in positive_words:
            result = analyze_sentiment(f"Company shows {word}")
            assert result["score"] > 0, f"'{word}' should give positive score"

    @pytest.mark.feature009
    def test_negative_keywords(self):
        """Test negative keywords are detected."""
        from stockagent.analysis import analyze_sentiment

        negative_words = ["crash", "loss", "decline", "miss", "downgrade"]
        for word in negative_words:
            result = analyze_sentiment(f"Company faces {word}")
            assert result["score"] < 0, f"'{word}' should give negative score"

    @pytest.mark.feature009
    def test_mixed_keywords(self):
        """Test mixed keywords produce balanced score."""
        from stockagent.analysis import analyze_sentiment

        result = analyze_sentiment("Company shows growth but faces decline")
        # Should be closer to neutral with mixed signals
        assert -0.5 <= result["score"] <= 0.5
