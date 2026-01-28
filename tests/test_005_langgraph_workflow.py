"""Tests for Feature 005: LangGraph Workflow."""

from unittest.mock import MagicMock, patch

import pytest


class TestWorkflowImports:
    """Test that workflow functions can be imported."""

    @pytest.mark.feature005
    def test_create_workflow_import(self):
        """Test that create_workflow can be imported."""
        from stockagent.graph import create_workflow

        assert create_workflow is not None

    @pytest.mark.feature005
    def test_run_analysis_import(self):
        """Test that run_analysis can be imported."""
        from stockagent.graph import run_analysis

        assert run_analysis is not None

    @pytest.mark.feature005
    def test_node_functions_import(self):
        """Test that node functions can be imported."""
        from stockagent.graph.workflow import (
            fetch_data,
            news_sentiment_node,
            recommend,
            synthesize,
            technical_analysis,
        )

        assert fetch_data is not None
        assert technical_analysis is not None
        assert news_sentiment_node is not None
        assert synthesize is not None
        assert recommend is not None


class TestCreateWorkflow:
    """Test workflow creation."""

    @pytest.mark.feature005
    def test_create_workflow_returns_compiled_graph(self):
        """Test that create_workflow returns a compiled graph."""
        from stockagent.graph import create_workflow

        graph = create_workflow()

        assert graph is not None
        # Check it's a compiled graph (has invoke method)
        assert hasattr(graph, "invoke")

    @pytest.mark.feature005
    def test_workflow_compiles_without_error(self):
        """Test that workflow compiles without errors."""
        from stockagent.graph import create_workflow

        # Should not raise any exceptions
        graph = create_workflow()
        assert graph is not None


class TestFetchDataNode:
    """Test fetch_data node function."""

    @pytest.mark.feature005
    def test_fetch_data_returns_dict(self):
        """Test that fetch_data returns a dict."""
        from stockagent.graph.workflow import fetch_data

        mock_client = MagicMock()
        mock_client.get_stock_aggregates.return_value = [
            {"open": 100, "high": 105, "low": 99, "close": 103, "volume": 1000000, "timestamp": "2024-01-01"}
        ]
        mock_client.get_ticker_details.return_value = {"company_name": "Apple Inc.", "sector": "Technology"}
        mock_client.get_previous_close.return_value = {"previous_close": 102.0, "current_price": 103.0}

        with patch("stockagent.graph.workflow.PolygonClient", return_value=mock_client):
            state = {"ticker": "AAPL", "errors": []}
            result = fetch_data(state)

            assert isinstance(result, dict)
            assert "price_data" in result
            assert "company_name" in result

    @pytest.mark.feature005
    def test_fetch_data_with_no_ticker(self):
        """Test fetch_data with no ticker returns error."""
        from stockagent.graph.workflow import fetch_data

        state = {"ticker": "", "errors": []}
        result = fetch_data(state)

        assert "errors" in result
        assert len(result["errors"]) > 0

    @pytest.mark.feature005
    def test_fetch_data_handles_api_error(self):
        """Test that fetch_data handles API errors gracefully."""
        from stockagent.data import PolygonAPIError
        from stockagent.graph.workflow import fetch_data

        mock_client = MagicMock()
        mock_client.get_stock_aggregates.side_effect = PolygonAPIError("API Error")
        mock_client.get_ticker_details.return_value = {"company_name": "Test", "sector": "Tech"}
        mock_client.get_previous_close.return_value = {"previous_close": 100.0, "current_price": 100.0}

        with patch("stockagent.graph.workflow.PolygonClient", return_value=mock_client):
            state = {"ticker": "AAPL", "errors": []}
            result = fetch_data(state)

            # Should have error but not crash
            assert "errors" in result
            assert len(result["errors"]) > 0


class TestTechnicalAnalysisNode:
    """Test technical_analysis node function."""

    @pytest.mark.feature005
    def test_technical_analysis_with_data(self):
        """Test technical_analysis with price data."""
        from stockagent.graph.workflow import technical_analysis

        # Create enough price data for indicators
        price_data = [{"close": 100 + i * 0.5} for i in range(100)]
        state = {"price_data": price_data, "current_price": 150.0, "errors": []}

        result = technical_analysis(state)

        assert "technical_signals" in result
        assert result["technical_signals"]["rsi"] is not None
        assert result["technical_signals"]["macd"] is not None

    @pytest.mark.feature005
    def test_technical_analysis_empty_data(self):
        """Test technical_analysis with empty price data."""
        from stockagent.graph.workflow import technical_analysis

        state = {"price_data": [], "current_price": 0.0, "errors": []}
        result = technical_analysis(state)

        assert "technical_signals" in result
        assert result["technical_signals"]["rsi"] is None

    @pytest.mark.feature005
    def test_technical_analysis_returns_interpretations(self):
        """Test that technical_analysis includes interpretations."""
        from stockagent.graph.workflow import technical_analysis

        price_data = [{"close": 100 + i * 0.5} for i in range(100)]
        state = {"price_data": price_data, "current_price": 150.0, "errors": []}

        result = technical_analysis(state)

        assert "rsi_interpretation" in result["technical_signals"]
        assert "macd_interpretation" in result["technical_signals"]


class TestNewsSentimentNode:
    """Test news_sentiment node function."""

    @pytest.mark.feature005
    def test_news_sentiment_returns_dict(self):
        """Test that news_sentiment returns a dict."""
        from stockagent.graph.workflow import news_sentiment_node

        mock_sentiment = {
            "overall_score": 0.5,
            "overall_label": "positive",
            "headlines": [],
            "headline_count": 0,
        }

        with patch("stockagent.graph.workflow.analyze_news_sentiment", return_value=mock_sentiment):
            state = {"ticker": "AAPL", "company_name": "Apple Inc.", "errors": []}
            result = news_sentiment_node(state)

            assert "news_sentiment" in result
            assert result["news_sentiment"]["overall_score"] == 0.5

    @pytest.mark.feature005
    def test_news_sentiment_handles_error(self):
        """Test that news_sentiment handles errors gracefully."""
        from stockagent.graph.workflow import news_sentiment_node

        with patch("stockagent.graph.workflow.analyze_news_sentiment", side_effect=Exception("API Error")):
            state = {"ticker": "AAPL", "company_name": "Apple Inc.", "errors": []}
            result = news_sentiment_node(state)

            # Should return neutral sentiment on error
            assert "news_sentiment" in result
            assert result["news_sentiment"]["overall_score"] == 0.0
            assert "errors" in result


class TestPlaceholderNodes:
    """Test placeholder nodes (synthesize, recommend)."""

    @pytest.mark.feature005
    def test_synthesize_returns_synthesis(self):
        """Test that synthesize returns synthesis field."""
        from stockagent.graph.workflow import synthesize

        state = {"ticker": "AAPL", "errors": []}
        result = synthesize(state)

        assert "synthesis" in result
        assert isinstance(result["synthesis"], str)

    @pytest.mark.feature005
    def test_recommend_returns_recommendation(self):
        """Test that recommend returns recommendation fields."""
        from stockagent.graph.workflow import recommend

        state = {"ticker": "AAPL", "errors": [], "technical_signals": {}, "news_sentiment": {}}
        result = recommend(state)

        assert "recommendation" in result
        assert "confidence" in result
        assert result["recommendation"] in ["STRONG BUY", "BUY", "HOLD", "SELL", "STRONG SELL"]
        assert isinstance(result["confidence"], (int, float))


class TestRunAnalysis:
    """Test run_analysis function."""

    @pytest.mark.feature005
    def test_run_analysis_returns_complete_state(self):
        """Test that run_analysis returns complete state."""
        from stockagent.graph import run_analysis

        # Mock all external dependencies
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

                # Check all required fields present
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

    @pytest.mark.feature005
    def test_run_analysis_normalizes_ticker(self):
        """Test that run_analysis normalizes ticker to uppercase."""
        from stockagent.graph import run_analysis

        mock_client = MagicMock()
        mock_client.get_stock_aggregates.return_value = []
        mock_client.get_ticker_details.return_value = {"company_name": "Test", "sector": "Tech"}
        mock_client.get_previous_close.return_value = {"previous_close": 100.0, "current_price": 100.0}

        mock_sentiment = {"overall_score": 0.0, "overall_label": "neutral", "headlines": [], "headline_count": 0}

        with patch("stockagent.graph.workflow.PolygonClient", return_value=mock_client):
            with patch("stockagent.graph.workflow.analyze_news_sentiment", return_value=mock_sentiment):
                result = run_analysis("aapl")

                assert result["ticker"] == "AAPL"

    @pytest.mark.feature005
    def test_run_analysis_accumulates_errors(self):
        """Test that run_analysis accumulates errors from nodes."""
        from stockagent.data import PolygonAPIError
        from stockagent.graph import run_analysis

        mock_client = MagicMock()
        mock_client.get_stock_aggregates.side_effect = PolygonAPIError("API Error")
        mock_client.get_ticker_details.return_value = {"company_name": "Test", "sector": "Tech"}
        mock_client.get_previous_close.return_value = {"previous_close": 100.0, "current_price": 100.0}

        mock_sentiment = {"overall_score": 0.0, "overall_label": "neutral", "headlines": [], "headline_count": 0}

        with patch("stockagent.graph.workflow.PolygonClient", return_value=mock_client):
            with patch("stockagent.graph.workflow.analyze_news_sentiment", return_value=mock_sentiment):
                result = run_analysis("TEST")

                assert "errors" in result
                # Should have at least one error from the API failure
                assert len(result["errors"]) > 0


class TestWorkflowIntegration:
    """Integration tests for the complete workflow."""

    @pytest.mark.feature005
    def test_workflow_state_flows_through_nodes(self):
        """Test that state flows correctly through all nodes."""
        from stockagent.graph import run_analysis

        mock_client = MagicMock()
        mock_client.get_stock_aggregates.return_value = [
            {"open": 100, "high": 105, "low": 99, "close": 103, "volume": 1000000, "timestamp": "2024-01-01"}
            for _ in range(50)
        ]
        mock_client.get_ticker_details.return_value = {"company_name": "Integration Test Corp", "sector": "Tech"}
        mock_client.get_previous_close.return_value = {"previous_close": 102.0, "current_price": 103.0}

        mock_sentiment = {
            "overall_score": 0.5,
            "overall_label": "positive",
            "headlines": [{"title": "Good news", "score": 0.5, "label": "positive"}],
            "headline_count": 1,
        }

        with patch("stockagent.graph.workflow.PolygonClient", return_value=mock_client):
            with patch("stockagent.graph.workflow.analyze_news_sentiment", return_value=mock_sentiment):
                result = run_analysis("INTG")

                # Verify data flowed from fetch_data
                assert result["company_name"] == "Integration Test Corp"
                assert result["current_price"] == 103.0

                # Verify technical analysis ran
                assert "technical_signals" in result

                # Verify sentiment analysis ran
                assert result["news_sentiment"]["overall_score"] == 0.5

                # Verify synthesize and recommend ran
                assert "synthesis" in result
                assert result["recommendation"] == "HOLD"

    @pytest.mark.feature005
    def test_workflow_handles_complete_failure(self):
        """Test that workflow handles complete API failure gracefully."""
        from stockagent.data import PolygonAPIError
        from stockagent.graph import run_analysis

        mock_client = MagicMock()
        mock_client.get_stock_aggregates.side_effect = PolygonAPIError("Total failure")
        mock_client.get_ticker_details.side_effect = PolygonAPIError("Total failure")
        mock_client.get_previous_close.side_effect = PolygonAPIError("Total failure")

        with patch("stockagent.graph.workflow.PolygonClient", return_value=mock_client):
            with patch("stockagent.graph.workflow.analyze_news_sentiment", side_effect=Exception("Also failed")):
                # Should not crash, should return state with errors
                result = run_analysis("FAIL")

                assert result["ticker"] == "FAIL"
                assert len(result["errors"]) > 0
                # Should still have recommendation (placeholder)
                assert result["recommendation"] == "HOLD"
