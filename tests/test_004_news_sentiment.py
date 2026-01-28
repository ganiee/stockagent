"""Tests for Feature 004: News Sentiment."""

from unittest.mock import MagicMock, patch

import pytest


class TestNewsSentimentImports:
    """Test that news sentiment functions can be imported."""

    @pytest.mark.feature004
    def test_analyze_news_sentiment_import(self):
        """Test that analyze_news_sentiment can be imported."""
        from stockagent.analysis import analyze_news_sentiment

        assert analyze_news_sentiment is not None

    @pytest.mark.feature004
    def test_analyze_sentiment_import(self):
        """Test that analyze_sentiment can be imported."""
        from stockagent.analysis import analyze_sentiment

        assert analyze_sentiment is not None

    @pytest.mark.feature004
    def test_fetch_news_import(self):
        """Test that fetch_news can be imported."""
        from stockagent.analysis import fetch_news

        assert fetch_news is not None


class TestAnalyzeSentiment:
    """Test headline sentiment analysis."""

    @pytest.mark.feature004
    def test_positive_headline(self):
        """Test sentiment for positive headline."""
        from stockagent.analysis import analyze_sentiment

        result = analyze_sentiment("Stock surges to record high after strong earnings beat")

        assert result["score"] > 0
        assert result["label"] == "positive"
        assert result["positive_count"] > 0

    @pytest.mark.feature004
    def test_negative_headline(self):
        """Test sentiment for negative headline."""
        from stockagent.analysis import analyze_sentiment

        result = analyze_sentiment("Company crashes amid massive losses and layoffs")

        assert result["score"] < 0
        assert result["label"] == "negative"
        assert result["negative_count"] > 0

    @pytest.mark.feature004
    def test_neutral_headline(self):
        """Test sentiment for neutral headline."""
        from stockagent.analysis import analyze_sentiment

        result = analyze_sentiment("Company announces quarterly results")

        assert -0.2 <= result["score"] <= 0.2
        assert result["label"] == "neutral"

    @pytest.mark.feature004
    def test_empty_headline(self):
        """Test sentiment for empty headline."""
        from stockagent.analysis import analyze_sentiment

        result = analyze_sentiment("")

        assert result["score"] == 0.0
        assert result["label"] == "neutral"
        assert result["positive_count"] == 0
        assert result["negative_count"] == 0

    @pytest.mark.feature004
    def test_score_range(self):
        """Test that score is always in [-1.0, +1.0]."""
        from stockagent.analysis import analyze_sentiment

        # Very positive
        result1 = analyze_sentiment("surge growth profit bullish upgrade beat record strong gain rally")
        assert -1.0 <= result1["score"] <= 1.0

        # Very negative
        result2 = analyze_sentiment("crash loss decline bearish downgrade miss weak fall drop plunge")
        assert -1.0 <= result2["score"] <= 1.0

    @pytest.mark.feature004
    def test_case_insensitive(self):
        """Test that keyword matching is case insensitive."""
        from stockagent.analysis import analyze_sentiment

        result1 = analyze_sentiment("STOCK SURGES")
        result2 = analyze_sentiment("stock surges")
        result3 = analyze_sentiment("Stock Surges")

        assert result1["score"] == result2["score"] == result3["score"]

    @pytest.mark.feature004
    def test_mixed_sentiment(self):
        """Test headline with mixed positive and negative keywords."""
        from stockagent.analysis import analyze_sentiment

        result = analyze_sentiment("Stock gains despite concerns about losses")

        # Should have both counts
        assert result["positive_count"] > 0
        assert result["negative_count"] > 0

    @pytest.mark.feature004
    def test_returns_correct_structure(self):
        """Test that result has all required fields."""
        from stockagent.analysis import analyze_sentiment

        result = analyze_sentiment("Test headline")

        assert "score" in result
        assert "label" in result
        assert "positive_count" in result
        assert "negative_count" in result
        assert isinstance(result["score"], float)
        assert result["label"] in ["positive", "negative", "neutral"]

    @pytest.mark.feature004
    def test_deterministic(self):
        """Test that sentiment analysis is deterministic."""
        from stockagent.analysis import analyze_sentiment

        headline = "Stock surges after earnings beat expectations"
        result1 = analyze_sentiment(headline)
        result2 = analyze_sentiment(headline)

        assert result1["score"] == result2["score"]
        assert result1["label"] == result2["label"]


class TestFetchNews:
    """Test news fetching with mocked DuckDuckGo."""

    @pytest.mark.feature004
    def test_fetch_news_returns_list(self):
        """Test that fetch_news returns a list."""
        from stockagent.analysis.news_sentiment import fetch_news

        mock_results = [
            {"title": "Test headline 1", "url": "http://example.com/1", "date": "2024-01-01", "source": "Test"},
            {"title": "Test headline 2", "url": "http://example.com/2", "date": "2024-01-02", "source": "Test"},
        ]

        with patch("stockagent.analysis.news_sentiment.DDGS") as mock_ddgs:
            mock_instance = MagicMock()
            mock_instance.news.return_value = mock_results
            mock_ddgs.return_value.__enter__.return_value = mock_instance

            result = fetch_news("AAPL", "Apple Inc.")

            assert isinstance(result, list)
            assert len(result) == 2

    @pytest.mark.feature004
    def test_fetch_news_transforms_results(self):
        """Test that fetch_news transforms results correctly."""
        from stockagent.analysis.news_sentiment import fetch_news

        mock_results = [
            {"title": "Test headline", "url": "http://example.com", "date": "2024-01-01", "source": "Test Source"},
        ]

        with patch("stockagent.analysis.news_sentiment.DDGS") as mock_ddgs:
            mock_instance = MagicMock()
            mock_instance.news.return_value = mock_results
            mock_ddgs.return_value.__enter__.return_value = mock_instance

            result = fetch_news("AAPL", "Apple Inc.")

            assert result[0]["title"] == "Test headline"
            assert result[0]["url"] == "http://example.com"
            assert result[0]["date"] == "2024-01-01"
            assert result[0]["source"] == "Test Source"

    @pytest.mark.feature004
    def test_fetch_news_uses_company_name(self):
        """Test that fetch_news uses company name in query."""
        from stockagent.analysis.news_sentiment import fetch_news

        with patch("stockagent.analysis.news_sentiment.DDGS") as mock_ddgs:
            mock_instance = MagicMock()
            mock_instance.news.return_value = []
            mock_ddgs.return_value.__enter__.return_value = mock_instance

            fetch_news("AAPL", "Apple Inc.")

            mock_instance.news.assert_called_once()
            call_args = mock_instance.news.call_args
            assert "Apple Inc." in call_args[0][0]

    @pytest.mark.feature004
    def test_fetch_news_uses_ticker_when_no_company(self):
        """Test that fetch_news uses ticker when no company name."""
        from stockagent.analysis.news_sentiment import fetch_news

        with patch("stockagent.analysis.news_sentiment.DDGS") as mock_ddgs:
            mock_instance = MagicMock()
            mock_instance.news.return_value = []
            mock_ddgs.return_value.__enter__.return_value = mock_instance

            fetch_news("AAPL", "")

            mock_instance.news.assert_called_once()
            call_args = mock_instance.news.call_args
            assert "AAPL" in call_args[0][0]

    @pytest.mark.feature004
    def test_fetch_news_handles_error(self):
        """Test that fetch_news handles errors gracefully."""
        from stockagent.analysis.news_sentiment import fetch_news

        with patch("stockagent.analysis.news_sentiment.DDGS") as mock_ddgs:
            mock_ddgs.return_value.__enter__.side_effect = Exception("API Error")

            result = fetch_news("AAPL", "Apple Inc.")

            assert result == []

    @pytest.mark.feature004
    def test_fetch_news_respects_max_results(self):
        """Test that fetch_news passes max_results to API."""
        from stockagent.analysis.news_sentiment import fetch_news

        with patch("stockagent.analysis.news_sentiment.DDGS") as mock_ddgs:
            mock_instance = MagicMock()
            mock_instance.news.return_value = []
            mock_ddgs.return_value.__enter__.return_value = mock_instance

            fetch_news("AAPL", "Apple", max_results=5)

            call_kwargs = mock_instance.news.call_args[1]
            assert call_kwargs["max_results"] == 5


class TestAnalyzeNewsSentiment:
    """Test aggregate news sentiment analysis."""

    @pytest.mark.feature004
    def test_returns_sentiment_result(self):
        """Test that analyze_news_sentiment returns correct structure."""
        from stockagent.analysis import analyze_news_sentiment

        mock_articles = [
            {"title": "Stock surges on earnings", "url": "http://example.com/1", "date": "2024-01-01"},
            {"title": "Analyst upgrades rating", "url": "http://example.com/2", "date": "2024-01-02"},
        ]

        with patch("stockagent.analysis.news_sentiment.fetch_news", return_value=mock_articles):
            result = analyze_news_sentiment("AAPL", "Apple Inc.")

            assert "overall_score" in result
            assert "overall_label" in result
            assert "headlines" in result
            assert "headline_count" in result

    @pytest.mark.feature004
    def test_positive_news_returns_positive(self):
        """Test that positive news returns positive sentiment."""
        from stockagent.analysis import analyze_news_sentiment

        mock_articles = [
            {"title": "Stock surges after strong earnings beat", "url": "http://example.com/1", "date": "2024-01-01"},
            {"title": "Company profits surge to record high", "url": "http://example.com/2", "date": "2024-01-02"},
            {"title": "Analyst upgrades stock with bullish outlook", "url": "http://example.com/3", "date": "2024-01-03"},
        ]

        with patch("stockagent.analysis.news_sentiment.fetch_news", return_value=mock_articles):
            result = analyze_news_sentiment("AAPL", "Apple Inc.")

            assert result["overall_score"] > 0
            assert result["overall_label"] == "positive"

    @pytest.mark.feature004
    def test_negative_news_returns_negative(self):
        """Test that negative news returns negative sentiment."""
        from stockagent.analysis import analyze_news_sentiment

        mock_articles = [
            {"title": "Stock crashes amid massive losses", "url": "http://example.com/1", "date": "2024-01-01"},
            {"title": "Company announces layoffs after weak earnings", "url": "http://example.com/2", "date": "2024-01-02"},
            {"title": "Analyst downgrades with bearish outlook", "url": "http://example.com/3", "date": "2024-01-03"},
        ]

        with patch("stockagent.analysis.news_sentiment.fetch_news", return_value=mock_articles):
            result = analyze_news_sentiment("AAPL", "Apple Inc.")

            assert result["overall_score"] < 0
            assert result["overall_label"] == "negative"

    @pytest.mark.feature004
    def test_no_news_returns_neutral(self):
        """Test that no news returns neutral sentiment."""
        from stockagent.analysis import analyze_news_sentiment

        with patch("stockagent.analysis.news_sentiment.fetch_news", return_value=[]):
            result = analyze_news_sentiment("AAPL", "Apple Inc.")

            assert result["overall_score"] == 0.0
            assert result["overall_label"] == "neutral"
            assert result["headlines"] == []
            assert result["headline_count"] == 0

    @pytest.mark.feature004
    def test_limits_headlines_to_5(self):
        """Test that result contains at most 5 headlines."""
        from stockagent.analysis import analyze_news_sentiment

        mock_articles = [
            {"title": f"Headline {i} about stock", "url": f"http://example.com/{i}", "date": "2024-01-01"}
            for i in range(10)
        ]

        with patch("stockagent.analysis.news_sentiment.fetch_news", return_value=mock_articles):
            result = analyze_news_sentiment("AAPL", "Apple Inc.")

            assert len(result["headlines"]) <= 5

    @pytest.mark.feature004
    def test_headline_count_reflects_all_analyzed(self):
        """Test that headline_count reflects total analyzed, not just returned."""
        from stockagent.analysis import analyze_news_sentiment

        mock_articles = [
            {"title": f"Headline {i}", "url": f"http://example.com/{i}", "date": "2024-01-01"}
            for i in range(8)
        ]

        with patch("stockagent.analysis.news_sentiment.fetch_news", return_value=mock_articles):
            result = analyze_news_sentiment("AAPL", "Apple Inc.")

            assert result["headline_count"] == 8
            assert len(result["headlines"]) <= 5

    @pytest.mark.feature004
    def test_headlines_have_sentiment_info(self):
        """Test that returned headlines include sentiment info."""
        from stockagent.analysis import analyze_news_sentiment

        mock_articles = [
            {"title": "Stock surges on news", "url": "http://example.com/1", "date": "2024-01-01"},
        ]

        with patch("stockagent.analysis.news_sentiment.fetch_news", return_value=mock_articles):
            result = analyze_news_sentiment("AAPL", "Apple Inc.")

            assert len(result["headlines"]) > 0
            headline = result["headlines"][0]
            assert "title" in headline
            assert "score" in headline
            assert "label" in headline

    @pytest.mark.feature004
    def test_overall_score_is_average(self):
        """Test that overall score is average of headline scores."""
        from stockagent.analysis import analyze_news_sentiment
        from stockagent.analysis.news_sentiment import analyze_sentiment

        mock_articles = [
            {"title": "Stock surges", "url": "http://example.com/1", "date": "2024-01-01"},
            {"title": "Stock crashes", "url": "http://example.com/2", "date": "2024-01-02"},
        ]

        # Get individual scores
        score1 = analyze_sentiment("Stock surges")["score"]
        score2 = analyze_sentiment("Stock crashes")["score"]
        expected_avg = (score1 + score2) / 2

        with patch("stockagent.analysis.news_sentiment.fetch_news", return_value=mock_articles):
            result = analyze_news_sentiment("AAPL", "Apple Inc.")

            assert abs(result["overall_score"] - expected_avg) < 0.001

    @pytest.mark.feature004
    def test_handles_empty_titles(self):
        """Test that empty titles are handled gracefully."""
        from stockagent.analysis import analyze_news_sentiment

        mock_articles = [
            {"title": "", "url": "http://example.com/1", "date": "2024-01-01"},
            {"title": "Valid headline", "url": "http://example.com/2", "date": "2024-01-02"},
        ]

        with patch("stockagent.analysis.news_sentiment.fetch_news", return_value=mock_articles):
            result = analyze_news_sentiment("AAPL", "Apple Inc.")

            # Should still work, just skip empty titles
            assert result["headline_count"] == 1


class TestKeywordLists:
    """Test keyword list properties."""

    @pytest.mark.feature004
    def test_positive_keywords_lowercase(self):
        """Test that positive keywords are lowercase."""
        from stockagent.analysis.news_sentiment import POSITIVE_KEYWORDS

        for kw in POSITIVE_KEYWORDS:
            assert kw == kw.lower(), f"Keyword '{kw}' is not lowercase"

    @pytest.mark.feature004
    def test_negative_keywords_lowercase(self):
        """Test that negative keywords are lowercase."""
        from stockagent.analysis.news_sentiment import NEGATIVE_KEYWORDS

        for kw in NEGATIVE_KEYWORDS:
            assert kw == kw.lower(), f"Keyword '{kw}' is not lowercase"

    @pytest.mark.feature004
    def test_keywords_are_non_empty(self):
        """Test that keyword lists are not empty."""
        from stockagent.analysis.news_sentiment import NEGATIVE_KEYWORDS, POSITIVE_KEYWORDS

        assert len(POSITIVE_KEYWORDS) > 0
        assert len(NEGATIVE_KEYWORDS) > 0

    @pytest.mark.feature004
    def test_no_overlap_between_keyword_lists(self):
        """Test that there's no overlap between positive and negative keywords."""
        from stockagent.analysis.news_sentiment import NEGATIVE_KEYWORDS, POSITIVE_KEYWORDS

        overlap = set(POSITIVE_KEYWORDS) & set(NEGATIVE_KEYWORDS)
        assert len(overlap) == 0, f"Keywords appear in both lists: {overlap}"
