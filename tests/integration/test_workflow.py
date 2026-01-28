"""Integration tests for workflow execution."""

from unittest.mock import MagicMock, patch

import pytest


class TestWorkflowExecution:
    """Test complete workflow execution."""

    @pytest.mark.feature009
    def test_run_analysis_returns_complete_state(self):
        """Test run_analysis returns complete state with all fields."""
        from stockagent.graph import run_analysis

        mock_client = MagicMock()
        mock_client.get_stock_aggregates.return_value = [
            {"close": 100 + i * 0.5} for i in range(100)
        ]
        mock_client.get_ticker_details.return_value = {
            "company_name": "Test Corporation",
            "sector": "Technology"
        }
        mock_client.get_previous_close.return_value = {
            "previous_close": 149.0,
            "current_price": 150.0
        }

        mock_sentiment = {
            "overall_score": 0.3,
            "overall_label": "positive",
            "headlines": [{"title": "Test", "label": "positive", "score": 0.3}],
            "headline_count": 1,
        }

        with patch("stockagent.graph.workflow.PolygonClient", return_value=mock_client):
            with patch("stockagent.graph.workflow.analyze_news_sentiment", return_value=mock_sentiment):
                result = run_analysis("TEST")

                # Verify all required fields present
                assert result["ticker"] == "TEST"
                assert "price_data" in result
                assert "company_name" in result
                assert "current_price" in result
                assert "previous_close" in result
                assert "technical_signals" in result
                assert "news_sentiment" in result
                assert "synthesis" in result
                assert "recommendation" in result
                assert "confidence" in result
                assert "explanation_factors" in result
                assert "errors" in result

    @pytest.mark.feature009
    def test_workflow_handles_api_errors(self):
        """Test workflow handles API errors gracefully."""
        from stockagent.data import PolygonAPIError
        from stockagent.graph import run_analysis

        mock_client = MagicMock()
        mock_client.get_stock_aggregates.side_effect = PolygonAPIError("API Error")
        mock_client.get_ticker_details.return_value = {"company_name": "Test"}
        mock_client.get_previous_close.return_value = {"previous_close": 100.0, "current_price": 100.0}

        mock_sentiment = {
            "overall_score": 0.0,
            "overall_label": "neutral",
            "headlines": [],
            "headline_count": 0,
        }

        with patch("stockagent.graph.workflow.PolygonClient", return_value=mock_client):
            with patch("stockagent.graph.workflow.analyze_news_sentiment", return_value=mock_sentiment):
                result = run_analysis("TEST")

                # Should not crash and should have errors
                assert "errors" in result
                assert len(result["errors"]) > 0
                # Should still have recommendation
                assert "recommendation" in result

    @pytest.mark.feature009
    def test_workflow_normalizes_ticker(self):
        """Test workflow normalizes ticker to uppercase."""
        from stockagent.graph import run_analysis

        mock_client = MagicMock()
        mock_client.get_stock_aggregates.return_value = []
        mock_client.get_ticker_details.return_value = {"company_name": "Test"}
        mock_client.get_previous_close.return_value = {"previous_close": 100.0, "current_price": 100.0}

        mock_sentiment = {
            "overall_score": 0.0,
            "overall_label": "neutral",
            "headlines": [],
            "headline_count": 0,
        }

        with patch("stockagent.graph.workflow.PolygonClient", return_value=mock_client):
            with patch("stockagent.graph.workflow.analyze_news_sentiment", return_value=mock_sentiment):
                result = run_analysis("aapl")
                assert result["ticker"] == "AAPL"


class TestWorkflowStateTransitions:
    """Test workflow state transitions."""

    @pytest.mark.feature009
    def test_fetch_data_populates_price_data(self):
        """Test fetch_data node populates price data."""
        from stockagent.graph.workflow import fetch_data

        mock_client = MagicMock()
        mock_client.get_stock_aggregates.return_value = [
            {"close": 100.0}, {"close": 101.0}
        ]
        mock_client.get_ticker_details.return_value = {"company_name": "Test"}
        mock_client.get_previous_close.return_value = {"previous_close": 99.0, "current_price": 100.0}

        with patch("stockagent.graph.workflow.PolygonClient", return_value=mock_client):
            state = {"ticker": "TEST", "errors": []}
            result = fetch_data(state)

            assert "price_data" in result
            assert len(result["price_data"]) == 2

    @pytest.mark.feature009
    def test_technical_analysis_populates_signals(self):
        """Test technical_analysis node populates signals."""
        from stockagent.graph.workflow import technical_analysis

        price_data = [{"close": 100 + i * 0.5} for i in range(100)]
        state = {"price_data": price_data, "current_price": 150.0, "errors": []}

        result = technical_analysis(state)

        assert "technical_signals" in result
        assert "rsi" in result["technical_signals"]
        assert "macd" in result["technical_signals"]

    @pytest.mark.feature009
    def test_synthesize_populates_report(self):
        """Test synthesize node populates report."""
        from stockagent.graph.workflow import synthesize

        state = {
            "ticker": "TEST",
            "company_name": "Test Corp",
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
        assert len(result["synthesis"]) > 0
        assert "# Stock Analysis Report" in result["synthesis"]

    @pytest.mark.feature009
    def test_recommend_populates_recommendation(self):
        """Test recommend node populates recommendation."""
        from stockagent.graph.workflow import recommend

        state = {
            "technical_signals": {"rsi": 25.0},
            "news_sentiment": {"overall_score": 0.5},
            "errors": [],
        }

        result = recommend(state)

        assert "recommendation" in result
        assert result["recommendation"] in ["STRONG BUY", "BUY", "HOLD", "SELL", "STRONG SELL"]
        assert "confidence" in result
        assert "explanation_factors" in result


class TestGoldenRun:
    """Golden run tests - verify output structure matches expected."""

    @pytest.mark.feature009
    def test_output_structure_matches_expected(self):
        """Test run_analysis output has correct structure."""
        from stockagent.graph import run_analysis

        mock_client = MagicMock()
        mock_client.get_stock_aggregates.return_value = [
            {"close": 100 + i * 0.5} for i in range(100)
        ]
        mock_client.get_ticker_details.return_value = {"company_name": "Golden Corp", "sector": "Tech"}
        mock_client.get_previous_close.return_value = {"previous_close": 149.0, "current_price": 150.0}

        mock_sentiment = {
            "overall_score": 0.25,
            "overall_label": "positive",
            "headlines": [
                {"title": "Test headline", "label": "positive", "score": 0.25, "url": "", "date": ""}
            ],
            "headline_count": 1,
        }

        with patch("stockagent.graph.workflow.PolygonClient", return_value=mock_client):
            with patch("stockagent.graph.workflow.analyze_news_sentiment", return_value=mock_sentiment):
                result = run_analysis("GOLD")

                # Verify structure matches expected StockAnalysisState
                expected_keys = [
                    "ticker",
                    "price_data",
                    "company_name",
                    "current_price",
                    "previous_close",
                    "technical_signals",
                    "news_sentiment",
                    "synthesis",
                    "recommendation",
                    "confidence",
                    "explanation_factors",
                    "errors",
                ]

                for key in expected_keys:
                    assert key in result, f"Missing key: {key}"

    @pytest.mark.feature009
    def test_output_types_match_expected(self):
        """Test run_analysis output has correct types."""
        from stockagent.graph import run_analysis

        mock_client = MagicMock()
        mock_client.get_stock_aggregates.return_value = [{"close": 100 + i} for i in range(50)]
        mock_client.get_ticker_details.return_value = {"company_name": "Type Corp"}
        mock_client.get_previous_close.return_value = {"previous_close": 149.0, "current_price": 150.0}

        mock_sentiment = {
            "overall_score": 0.0,
            "overall_label": "neutral",
            "headlines": [],
            "headline_count": 0,
        }

        with patch("stockagent.graph.workflow.PolygonClient", return_value=mock_client):
            with patch("stockagent.graph.workflow.analyze_news_sentiment", return_value=mock_sentiment):
                result = run_analysis("TYPE")

                # Verify types
                assert isinstance(result["ticker"], str)
                assert isinstance(result["price_data"], list)
                assert isinstance(result["company_name"], str)
                assert isinstance(result["current_price"], (int, float))
                assert isinstance(result["previous_close"], (int, float))
                assert isinstance(result["technical_signals"], dict)
                assert isinstance(result["news_sentiment"], dict)
                assert isinstance(result["synthesis"], str)
                assert isinstance(result["recommendation"], str)
                assert isinstance(result["confidence"], (int, float))
                assert isinstance(result["explanation_factors"], list)
                assert isinstance(result["errors"], list)

    @pytest.mark.feature009
    def test_technical_signals_structure(self):
        """Test technical_signals has expected structure."""
        from stockagent.graph import run_analysis

        mock_client = MagicMock()
        mock_client.get_stock_aggregates.return_value = [{"close": 100 + i * 0.5} for i in range(100)]
        mock_client.get_ticker_details.return_value = {"company_name": "Tech Corp"}
        mock_client.get_previous_close.return_value = {"previous_close": 149.0, "current_price": 150.0}

        mock_sentiment = {
            "overall_score": 0.0,
            "overall_label": "neutral",
            "headlines": [],
            "headline_count": 0,
        }

        with patch("stockagent.graph.workflow.PolygonClient", return_value=mock_client):
            with patch("stockagent.graph.workflow.analyze_news_sentiment", return_value=mock_sentiment):
                result = run_analysis("TECH")

                signals = result["technical_signals"]
                assert "rsi" in signals
                assert "macd" in signals
                assert "bollinger" in signals
                assert "sma_20" in signals
                assert "rsi_interpretation" in signals
                assert "macd_interpretation" in signals
