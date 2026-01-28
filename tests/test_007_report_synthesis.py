"""Tests for Feature 007: Report Synthesis."""

from unittest.mock import MagicMock, patch

import pytest


class TestSynthesisImports:
    """Test that synthesis functions can be imported."""

    @pytest.mark.feature007
    def test_generate_report_import_from_synthesis(self):
        """Test that generate_report can be imported from synthesis module."""
        from stockagent.analysis.synthesis import generate_report

        assert generate_report is not None

    @pytest.mark.feature007
    def test_generate_report_import_from_analysis(self):
        """Test that generate_report can be imported from analysis package."""
        from stockagent.analysis import generate_report

        assert generate_report is not None


class TestReportHeader:
    """Test report header generation."""

    @pytest.mark.feature007
    def test_header_contains_ticker(self):
        """Test that header contains ticker symbol."""
        from stockagent.analysis.synthesis import _generate_header

        header = _generate_header("AAPL", "Apple Inc.")
        assert "AAPL" in header

    @pytest.mark.feature007
    def test_header_contains_company_name(self):
        """Test that header contains company name."""
        from stockagent.analysis.synthesis import _generate_header

        header = _generate_header("AAPL", "Apple Inc.")
        assert "Apple Inc." in header

    @pytest.mark.feature007
    def test_header_contains_timestamp(self):
        """Test that header contains timestamp."""
        from stockagent.analysis.synthesis import _generate_header

        header = _generate_header("AAPL", "Apple Inc.")
        assert "UTC" in header
        assert "Generated" in header

    @pytest.mark.feature007
    def test_header_is_markdown(self):
        """Test that header is valid markdown."""
        from stockagent.analysis.synthesis import _generate_header

        header = _generate_header("AAPL", "Apple Inc.")
        assert header.startswith("# ")
        assert "**Company:**" in header


class TestPriceSummary:
    """Test price summary section generation."""

    @pytest.mark.feature007
    def test_price_summary_shows_current_price(self):
        """Test that price summary shows current price."""
        from stockagent.analysis.synthesis import _generate_price_summary

        state = {"current_price": 150.50, "previous_close": 148.25}
        summary = _generate_price_summary(state)
        assert "$150.50" in summary

    @pytest.mark.feature007
    def test_price_summary_shows_previous_close(self):
        """Test that price summary shows previous close."""
        from stockagent.analysis.synthesis import _generate_price_summary

        state = {"current_price": 150.50, "previous_close": 148.25}
        summary = _generate_price_summary(state)
        assert "$148.25" in summary

    @pytest.mark.feature007
    def test_price_summary_shows_change(self):
        """Test that price summary shows price change."""
        from stockagent.analysis.synthesis import _generate_price_summary

        state = {"current_price": 150.50, "previous_close": 148.25}
        summary = _generate_price_summary(state)
        # Should show change amount
        assert "Change" in summary

    @pytest.mark.feature007
    def test_price_summary_shows_trend_up(self):
        """Test that price summary shows upward trend."""
        from stockagent.analysis.synthesis import _generate_price_summary

        state = {"current_price": 150.50, "previous_close": 148.25}
        summary = _generate_price_summary(state)
        assert "Up" in summary

    @pytest.mark.feature007
    def test_price_summary_shows_trend_down(self):
        """Test that price summary shows downward trend."""
        from stockagent.analysis.synthesis import _generate_price_summary

        state = {"current_price": 145.00, "previous_close": 148.25}
        summary = _generate_price_summary(state)
        assert "Down" in summary

    @pytest.mark.feature007
    def test_price_summary_handles_missing_data(self):
        """Test that price summary handles missing data gracefully."""
        from stockagent.analysis.synthesis import _generate_price_summary

        state = {}
        summary = _generate_price_summary(state)
        # Should not crash
        assert "Price Summary" in summary


class TestTechnicalSection:
    """Test technical analysis section generation."""

    @pytest.mark.feature007
    def test_technical_section_shows_rsi(self):
        """Test that technical section shows RSI."""
        from stockagent.analysis.synthesis import _generate_technical_section

        signals = {
            "rsi": 45.5,
            "rsi_interpretation": "neutral",
        }
        section = _generate_technical_section(signals)
        assert "RSI" in section
        assert "45.50" in section

    @pytest.mark.feature007
    def test_technical_section_shows_macd(self):
        """Test that technical section shows MACD."""
        from stockagent.analysis.synthesis import _generate_technical_section

        signals = {
            "macd": {"macd_line": 1.25, "signal_line": 0.75, "histogram": 0.50},
            "macd_interpretation": "bullish",
        }
        section = _generate_technical_section(signals)
        assert "MACD" in section
        assert "1.25" in section

    @pytest.mark.feature007
    def test_technical_section_shows_bollinger(self):
        """Test that technical section shows Bollinger Bands."""
        from stockagent.analysis.synthesis import _generate_technical_section

        signals = {
            "bollinger": {"upper": 155.0, "middle": 150.0, "lower": 145.0},
        }
        section = _generate_technical_section(signals)
        assert "Bollinger" in section
        assert "$155.00" in section
        assert "$145.00" in section

    @pytest.mark.feature007
    def test_technical_section_shows_smas(self):
        """Test that technical section shows moving averages."""
        from stockagent.analysis.synthesis import _generate_technical_section

        signals = {
            "sma_20": 148.50,
            "sma_50": 145.25,
            "sma_200": 140.00,
        }
        section = _generate_technical_section(signals)
        assert "SMA (20)" in section
        assert "SMA (50)" in section
        assert "SMA (200)" in section

    @pytest.mark.feature007
    def test_technical_section_handles_none_values(self):
        """Test that technical section handles None values."""
        from stockagent.analysis.synthesis import _generate_technical_section

        signals = {
            "rsi": None,
            "macd": None,
            "bollinger": None,
        }
        section = _generate_technical_section(signals)
        assert "N/A" in section

    @pytest.mark.feature007
    def test_technical_section_is_markdown_table(self):
        """Test that technical section uses markdown tables."""
        from stockagent.analysis.synthesis import _generate_technical_section

        signals = {"rsi": 50.0}
        section = _generate_technical_section(signals)
        assert "|" in section  # Markdown table delimiter


class TestSentimentSection:
    """Test news sentiment section generation."""

    @pytest.mark.feature007
    def test_sentiment_section_shows_overall_score(self):
        """Test that sentiment section shows overall score."""
        from stockagent.analysis.synthesis import _generate_sentiment_section

        sentiment = {
            "overall_score": 0.35,
            "overall_label": "positive",
            "headlines": [],
            "headline_count": 0,
        }
        section = _generate_sentiment_section(sentiment)
        assert "0.35" in section or "+0.35" in section

    @pytest.mark.feature007
    def test_sentiment_section_shows_label(self):
        """Test that sentiment section shows sentiment label."""
        from stockagent.analysis.synthesis import _generate_sentiment_section

        sentiment = {
            "overall_score": 0.35,
            "overall_label": "positive",
            "headlines": [],
            "headline_count": 0,
        }
        section = _generate_sentiment_section(sentiment)
        assert "Positive" in section

    @pytest.mark.feature007
    def test_sentiment_section_shows_headlines(self):
        """Test that sentiment section shows headlines."""
        from stockagent.analysis.synthesis import _generate_sentiment_section

        sentiment = {
            "overall_score": 0.35,
            "overall_label": "positive",
            "headlines": [
                {"title": "Stock Surges on Earnings", "label": "positive", "score": 0.8},
                {"title": "New Product Launch", "label": "positive", "score": 0.5},
            ],
            "headline_count": 2,
        }
        section = _generate_sentiment_section(sentiment)
        assert "Stock Surges on Earnings" in section
        assert "New Product Launch" in section

    @pytest.mark.feature007
    def test_sentiment_section_shows_headline_tags(self):
        """Test that sentiment section shows headline sentiment tags."""
        from stockagent.analysis.synthesis import _generate_sentiment_section

        sentiment = {
            "overall_score": 0.35,
            "overall_label": "positive",
            "headlines": [
                {"title": "Test Headline", "label": "positive", "score": 0.5},
            ],
            "headline_count": 1,
        }
        section = _generate_sentiment_section(sentiment)
        assert "[positive]" in section

    @pytest.mark.feature007
    def test_sentiment_section_handles_no_headlines(self):
        """Test that sentiment section handles no headlines gracefully."""
        from stockagent.analysis.synthesis import _generate_sentiment_section

        sentiment = {
            "overall_score": 0.0,
            "overall_label": "neutral",
            "headlines": [],
            "headline_count": 0,
        }
        section = _generate_sentiment_section(sentiment)
        assert "No recent headlines" in section

    @pytest.mark.feature007
    def test_sentiment_section_limits_headlines(self):
        """Test that sentiment section limits number of headlines."""
        from stockagent.analysis.synthesis import _generate_sentiment_section

        # Create 10 headlines
        headlines = [
            {"title": f"Headline {i}", "label": "neutral", "score": 0.0}
            for i in range(10)
        ]
        sentiment = {
            "overall_score": 0.0,
            "overall_label": "neutral",
            "headlines": headlines,
            "headline_count": 10,
        }
        section = _generate_sentiment_section(sentiment)
        # Should only show 5 headlines
        assert "Headline 4" in section
        assert "Headline 5" not in section


class TestRecommendationSection:
    """Test recommendation section generation."""

    @pytest.mark.feature007
    def test_recommendation_section_shows_recommendation(self):
        """Test that recommendation section shows recommendation."""
        from stockagent.analysis.synthesis import _generate_recommendation_section

        section = _generate_recommendation_section("BUY", 75.0, ["Factor 1"])
        assert "BUY" in section

    @pytest.mark.feature007
    def test_recommendation_section_is_bold(self):
        """Test that recommendation is bold/prominent."""
        from stockagent.analysis.synthesis import _generate_recommendation_section

        section = _generate_recommendation_section("BUY", 75.0, ["Factor 1"])
        assert "**BUY**" in section or "### **BUY**" in section

    @pytest.mark.feature007
    def test_recommendation_section_shows_confidence(self):
        """Test that recommendation section shows confidence."""
        from stockagent.analysis.synthesis import _generate_recommendation_section

        section = _generate_recommendation_section("BUY", 75.0, ["Factor 1"])
        assert "75%" in section

    @pytest.mark.feature007
    def test_recommendation_section_shows_factors(self):
        """Test that recommendation section shows explanation factors."""
        from stockagent.analysis.synthesis import _generate_recommendation_section

        factors = [
            "RSI indicates oversold condition",
            "MACD shows bullish momentum",
        ]
        section = _generate_recommendation_section("BUY", 75.0, factors)
        assert "RSI indicates oversold condition" in section
        assert "MACD shows bullish momentum" in section

    @pytest.mark.feature007
    def test_recommendation_section_handles_no_factors(self):
        """Test that recommendation section handles no factors."""
        from stockagent.analysis.synthesis import _generate_recommendation_section

        section = _generate_recommendation_section("HOLD", 50.0, [])
        assert "No specific factors" in section


class TestDisclaimer:
    """Test disclaimer section generation."""

    @pytest.mark.feature007
    def test_disclaimer_contains_educational_warning(self):
        """Test that disclaimer contains educational purpose warning."""
        from stockagent.analysis.synthesis import _generate_disclaimer

        disclaimer = _generate_disclaimer()
        assert "educational" in disclaimer.lower()

    @pytest.mark.feature007
    def test_disclaimer_contains_not_financial_advice(self):
        """Test that disclaimer states not financial advice."""
        from stockagent.analysis.synthesis import _generate_disclaimer

        disclaimer = _generate_disclaimer()
        assert "financial advice" in disclaimer.lower() or "not" in disclaimer.lower()

    @pytest.mark.feature007
    def test_disclaimer_credits_polygon(self):
        """Test that disclaimer credits Polygon.io."""
        from stockagent.analysis.synthesis import _generate_disclaimer

        disclaimer = _generate_disclaimer()
        assert "Polygon" in disclaimer

    @pytest.mark.feature007
    def test_disclaimer_credits_duckduckgo(self):
        """Test that disclaimer credits DuckDuckGo."""
        from stockagent.analysis.synthesis import _generate_disclaimer

        disclaimer = _generate_disclaimer()
        assert "DuckDuckGo" in disclaimer


class TestGenerateReport:
    """Test complete report generation."""

    @pytest.mark.feature007
    def test_generate_report_returns_string(self):
        """Test that generate_report returns a string."""
        from stockagent.analysis.synthesis import generate_report

        state = {
            "ticker": "AAPL",
            "company_name": "Apple Inc.",
            "current_price": 150.0,
            "previous_close": 148.0,
            "technical_signals": {},
            "news_sentiment": {},
            "recommendation": "HOLD",
            "confidence": 50.0,
            "explanation_factors": [],
        }
        report = generate_report(state)
        assert isinstance(report, str)
        assert len(report) > 0

    @pytest.mark.feature007
    def test_generate_report_contains_all_sections(self):
        """Test that report contains all required sections."""
        from stockagent.analysis.synthesis import generate_report

        state = {
            "ticker": "AAPL",
            "company_name": "Apple Inc.",
            "current_price": 150.0,
            "previous_close": 148.0,
            "technical_signals": {"rsi": 50.0},
            "news_sentiment": {"overall_score": 0.0, "overall_label": "neutral", "headlines": []},
            "recommendation": "HOLD",
            "confidence": 50.0,
            "explanation_factors": ["Test factor"],
        }
        report = generate_report(state)

        # Check all sections present
        assert "# Stock Analysis Report" in report
        assert "## Price Summary" in report
        assert "## Technical Analysis" in report
        assert "## News Sentiment" in report
        assert "## Recommendation" in report
        assert "## Disclaimer" in report

    @pytest.mark.feature007
    def test_generate_report_contains_ticker(self):
        """Test that report contains ticker."""
        from stockagent.analysis.synthesis import generate_report

        state = {"ticker": "MSFT", "company_name": "Microsoft"}
        report = generate_report(state)
        assert "MSFT" in report

    @pytest.mark.feature007
    def test_generate_report_handles_empty_state(self):
        """Test that report handles empty state gracefully."""
        from stockagent.analysis.synthesis import generate_report

        state = {}
        report = generate_report(state)
        # Should not crash and return something
        assert isinstance(report, str)
        assert "UNKNOWN" in report  # Default ticker

    @pytest.mark.feature007
    def test_generate_report_includes_errors_section(self):
        """Test that report includes errors section when errors present."""
        from stockagent.analysis.synthesis import generate_report

        state = {
            "ticker": "TEST",
            "errors": ["Error 1", "Error 2"],
        }
        report = generate_report(state)
        assert "Analysis Warnings" in report
        assert "Error 1" in report
        assert "Error 2" in report

    @pytest.mark.feature007
    def test_generate_report_valid_markdown(self):
        """Test that generated report is valid markdown."""
        from stockagent.analysis.synthesis import generate_report

        state = {
            "ticker": "AAPL",
            "company_name": "Apple Inc.",
            "current_price": 150.0,
            "previous_close": 148.0,
            "technical_signals": {
                "rsi": 45.0,
                "macd": {"macd_line": 1.0, "signal_line": 0.5, "histogram": 0.5},
            },
            "news_sentiment": {
                "overall_score": 0.3,
                "overall_label": "positive",
                "headlines": [{"title": "Test", "label": "positive", "score": 0.3}],
            },
            "recommendation": "BUY",
            "confidence": 65.0,
            "explanation_factors": ["RSI bullish", "MACD bullish"],
        }
        report = generate_report(state)

        # Check markdown formatting
        assert report.count("#") >= 5  # Multiple headings
        assert "|" in report  # Tables
        assert "---" in report  # Horizontal rules


class TestWorkflowIntegration:
    """Test integration with workflow synthesize node."""

    @pytest.mark.feature007
    def test_synthesize_returns_report(self):
        """Test that workflow synthesize returns report."""
        from stockagent.graph.workflow import synthesize

        state = {
            "ticker": "AAPL",
            "company_name": "Apple Inc.",
            "current_price": 150.0,
            "previous_close": 148.0,
            "technical_signals": {},
            "news_sentiment": {},
            "recommendation": "HOLD",
            "confidence": 50.0,
            "explanation_factors": [],
            "errors": [],
        }
        result = synthesize(state)

        assert "synthesis" in result
        assert isinstance(result["synthesis"], str)
        assert len(result["synthesis"]) > 100  # Should be substantial

    @pytest.mark.feature007
    def test_synthesize_not_placeholder(self):
        """Test that synthesize is not returning placeholder."""
        from stockagent.graph.workflow import synthesize

        state = {
            "ticker": "AAPL",
            "company_name": "Apple Inc.",
            "technical_signals": {"rsi": 50.0},
            "news_sentiment": {"overall_score": 0.0},
            "errors": [],
        }
        result = synthesize(state)

        # Should not be the old placeholder
        assert "will be generated here" not in result["synthesis"]
        # Should be a real report
        assert "# Stock Analysis Report" in result["synthesis"]

    @pytest.mark.feature007
    def test_run_analysis_returns_populated_synthesis(self):
        """Test that run_analysis returns populated synthesis."""
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

                assert "synthesis" in result
                assert isinstance(result["synthesis"], str)
                assert "# Stock Analysis Report" in result["synthesis"]
                assert "TEST" in result["synthesis"]

    @pytest.mark.feature007
    def test_synthesize_handles_error(self):
        """Test that synthesize handles errors gracefully."""
        from stockagent.graph.workflow import synthesize

        # Pass data that might cause issues
        state = {
            "ticker": None,
            "errors": [],
        }
        result = synthesize(state)

        # Should not crash
        assert "synthesis" in result


class TestFormatHelpers:
    """Test format helper functions."""

    @pytest.mark.feature007
    def test_format_price(self):
        """Test price formatting."""
        from stockagent.analysis.synthesis import _format_price

        assert _format_price(150.5) == "$150.50"
        assert _format_price(1234567.89) == "$1,234,567.89"
        assert _format_price(None) == "N/A"
        assert _format_price(0) == "N/A"

    @pytest.mark.feature007
    def test_format_number(self):
        """Test number formatting."""
        from stockagent.analysis.synthesis import _format_number

        assert _format_number(45.5678) == "45.57"
        assert _format_number(45.5678, 1) == "45.6"
        assert _format_number(None) == "N/A"

    @pytest.mark.feature007
    def test_format_percentage(self):
        """Test percentage formatting."""
        from stockagent.analysis.synthesis import _format_percentage

        assert _format_percentage(75.5) == "75.5%"
        assert _format_percentage(None) == "N/A"
